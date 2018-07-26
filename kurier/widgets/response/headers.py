import wx

from kurier.widgets.list_ctrl import ResizableListCtrl


class ResponseHeadersTab(wx.Panel):
    USED_COLUMNS = ["Header name", "Value"]

    def __init__(self, *args, **kwargs):
        super(ResponseHeadersTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headers_ctrl = ResizableListCtrl(self, columns=self.USED_COLUMNS)

        self.InitUI()

    def InitUI(self):
        self.sizer.Add(self.headers_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def AddRows(self, iterable):
        for key, value in iterable:
            self.headers_ctrl.AddNewRow(key, value)

    def DeleteAllRows(self):
        self.headers_ctrl.DeleteAllItems()

    def RenderHeader(self, headers):
        headers = headers or {}
        self.DeleteAllRows()
        self.AddRows(list(headers.items()))
