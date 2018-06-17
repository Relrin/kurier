import wx

from kurier.constants import DEFAULT_MESSAGE_PROPERTIES
from kurier.widgets.resizable_list_ctrl import ResizableListCtrl


class RequestPropertiesTab(wx.Panel):
    AVAILABLE_PROPERTIES = DEFAULT_MESSAGE_PROPERTIES
    USED_COLUMNS = ["Property name", "Value"]
    UTILITY_ROW_TEXT = "Click here for adding a new property..."

    def __init__(self, *args, **kwargs):
        super(RequestPropertiesTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.properties_ctrl = ResizableListCtrl(
            self,
            columns=self.USED_COLUMNS,
            utility_row_text=self.UTILITY_ROW_TEXT
        )
        self.available_choices = wx.Choice(self.properties_ctrl, choices=self.AVAILABLE_PROPERTIES)

        self.InitUI()

    def InitUI(self):
        self.AddUtilityRow()

        self.sizer.Add(self.properties_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def AddUtilityRow(self):
        self.properties_ctrl.AddUtilityRow()
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)

    def DeleteUtilityRow(self):
        self.properties_ctrl.DeleteUtilityRow()
        self.Unbind(wx.EVT_LIST_ITEM_SELECTED, handler=self.OnListItemSelected)

    def AddNewHeader(self, header_name, value=wx.EmptyString):
        self.properties_ctrl.AddNewHeader(header_name, value)

        if self.properties_ctrl.GetItemCount() > len(self.AVAILABLE_PROPERTIES):
            self.DeleteUtilityRow()

    def OnListItemSelected(self, event):
        event.Skip()
        row_info = event.GetItem()

        # TODO: Add new row and focus on selection a property from ComboBox (dynamic)
        if row_info.GetId() == self.properties_ctrl.GetItemCount() - 1:
            self.AddNewHeader('new')
