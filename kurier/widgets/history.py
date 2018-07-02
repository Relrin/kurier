import wx

from wx.lib.pubsub import pub

from kurier.constants import DEFAULT_GAP, DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP, \
    SAVE_STATE_TOPIC
from kurier.utils.history_manager import HistoryManager
from kurier.widgets.list_ctrl import ResizableListCtrl


class HistoryPanel(wx.Panel):
    STATE_STRING_REPR = "{index} Exchange={exchange}; routing_key={routing_key}"

    def __init__(self, parent, *args, **kwargs):
        super(HistoryPanel, self).__init__(parent, *args, **kwargs)
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.search_input = None
        self.history_entries = None
        self.history_manager = HistoryManager()

        self.InitUI()
        self.BindUI()

    def InitUI(self):
        search_input = wx.SearchCtrl(self)
        self.grid.Add(
            search_input,
            pos=(0, 0),
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=DEFAULT_GAP
        )

        self.history_entries = ResizableListCtrl(
            self,
            columns=["Old requests", ],
            style=ResizableListCtrl.DEFAULT_LIST_CTRL_STYLE | wx.LC_NO_HEADER
        )
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
        pub.subscribe(self.OnSaveState, SAVE_STATE_TOPIC)

    def RefreshListCtrl(self):
        self.history_entries.DeleteAllItems()

        for index in range(self.history_manager.SavedStates):
            state = self.history_manager.GetState(index)
            formatted_state = self.STATE_STRING_REPR.format(
                index=index + 1,
                exchange=state["request_exchange"],
                routing_key=state["request_routing_key"]
            )
            self.history_entries.InsertItem(index, formatted_state)

    def OnSaveState(self, message):
        self.history_manager.AddState(message)
        self.RefreshListCtrl()
