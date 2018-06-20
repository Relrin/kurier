import wx

from kurier.widgets.list_ctrl import ResizableListCtrl


class ResponsePropertiesTab(wx.Panel):
    USED_COLUMNS = ["Property name", "Value"]

    def __init__(self, *args, **kwargs):
        super(ResponsePropertiesTab, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.properties_ctrl = ResizableListCtrl(self, columns=self.USED_COLUMNS)

        self.InitUI()

    def InitUI(self):
        self.sizer.Add(self.properties_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def AddRows(self, iterable):
        for key, value in iterable:
            self.properties_ctrl.AddNewRow(key, value)

    def DeleteAllRows(self):
        self.properties_ctrl.DeleteAllItems()
