import wx

from pubsub import pub

from kurier.constants import DEFAULT_GAP, DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP, \
    SAVE_STATE_TOPIC, LOAD_STATE_TOPIC, CLOSE_APPLICATION_TOPIC
from kurier.utils.history_manager import HistoryManager
from kurier.widgets.list_ctrl import ResizableListCtrl


class HistoryPanel(wx.Panel):
    STATE_STRING_REPR = "{index} Exchange={exchange}; routing_key={routing_key}"
    MINIMAL_COLUMN_WIDTH = 50

    def __init__(self, parent, app_directory=None, *args, **kwargs):
        super(HistoryPanel, self).__init__(parent, *args, **kwargs)
        self.app_directory = app_directory

        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.search_input = None
        self.history_entries = None
        self.history_manager = HistoryManager(self.app_directory)

        self.InitUI()
        self.BindUI()
        self.ShowFullHistory()

    def InitUI(self):
        self.search_input = wx.SearchCtrl(self)
        self.search_input.ShowCancelButton(True)
        self.grid.Add(
            self.search_input,
            pos=(0, 0),
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=DEFAULT_GAP
        )

        self.history_entries = ResizableListCtrl(
            self,
            columns=["Old requests", ],
            style=ResizableListCtrl.DEFAULT_LIST_CTRL_STYLE | wx.LC_NO_HEADER
        )
        size = self.history_entries.GetSize()
        size.width = self.MINIMAL_COLUMN_WIDTH
        self.history_entries.SetMinSize(size)
        self.grid.Add(
            self.history_entries,
            pos=(1, 0),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )

        self.grid.AddGrowableCol(0)
        self.grid.AddGrowableRow(1)
        self.SetSizer(self.grid)

    def BindUI(self):
        self.search_input.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearchByKeyword)
        self.search_input.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancelSearchByKeyword)
        self.history_entries.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnLoadState)
        pub.subscribe(self.OnSaveState, SAVE_STATE_TOPIC)
        pub.subscribe(self.OnCloseApplication, CLOSE_APPLICATION_TOPIC)

    def RefreshListCtrl(self, indices):
        self.history_entries.DeleteAllItems()

        saved_states_count = self.history_manager.SavedStates
        for index in indices:
            state = self.history_manager.GetState(index)
            formatted_state = self.STATE_STRING_REPR.format(
                index=saved_states_count - index,
                exchange=state["request_exchange"],
                routing_key=state["request_routing_key"]
            )
            self.history_entries.InsertItem(index, formatted_state)

    def ShowFullHistory(self):
        matched_indices = range(self.history_manager.SavedStates)
        self.RefreshListCtrl(matched_indices)

    def GetStateIndicesByKeyword(self, keyword):
        matched_state_indices = []

        for index in range(self.history_manager.SavedStates):
            state = self.history_manager.GetState(index)
            match_in_exchange = keyword in state["request_exchange"]
            match_in_routing_key = keyword in state["request_routing_key"]
            if match_in_exchange or match_in_routing_key:
                matched_state_indices.append(index)

        return matched_state_indices

    def OnSaveState(self, message):
        self.history_manager.AddState(message)
        self.ShowFullHistory()

    def OnLoadState(self, event):
        index = self.history_entries.GetFirstSelected()
        state = self.history_manager.GetState(index)
        pub.sendMessage(LOAD_STATE_TOPIC, message=state)
        event.Skip()

    def OnSearchByKeyword(self, event):
        keyword = event.GetString().strip()

        if keyword in [wx.EmptyString, ""]:
            self.ShowFullHistory()
            event.Skip()
            return

        matched_state_indices = self.GetStateIndicesByKeyword(keyword)
        self.RefreshListCtrl(matched_state_indices)
        event.Skip()

    def OnCancelSearchByKeyword(self, event):
        self.search_input.Clear()
        self.ShowFullHistory()
        event.Skip()

    def OnCloseApplication(self, message):
        self.history_manager.ExportHistoryToDefaultFile()
