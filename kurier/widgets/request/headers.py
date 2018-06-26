import wx

from kurier.widgets.list_ctrl import EditableListCtrl


class RequestHeadersTab(wx.Panel):
    USED_COLUMNS = ["Header name", "Value"]
    UTILITY_ROW_TEXT = "Click here for adding a new user header..."

    def __init__(self, *args, **kwargs):
        super(RequestHeadersTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headers_ctrl = EditableListCtrl(
            self,
            columns=self.USED_COLUMNS,
            utility_row_text=self.UTILITY_ROW_TEXT
        )

        self.InitUI()

    def InitUI(self):
        self.AddUtilityRow()

        self.sizer.Add(self.headers_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def AddUtilityRow(self):
        self.headers_ctrl.AddUtilityRow()
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)

    def AddNewHeader(self, header_name, value=wx.EmptyString):
        insert_index = self.headers_ctrl.GetItemCount() - 1
        self.headers_ctrl.AddNewRow(header_name, value, insert_index)

    def OnListItemSelected(self, event):
        event.Skip()
        row_info = event.GetItem()

        # TODO: Add new row and focus on the first column (header name)
        if row_info.GetId() == self.headers_ctrl.GetItemCount() - 1:
            self.AddNewHeader('Key')
