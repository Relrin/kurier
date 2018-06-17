import wx

from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class ResizableListCtrl(ListCtrlAutoWidthMixin, wx.ListCtrl):
    DEFAULT_LIST_CTRL_STYLE = wx.LC_REPORT \
        | wx.LC_VRULES \
        | wx.LC_HRULES \
        | wx.LC_SINGLE_SEL
    DEFAULT_UTILITY_ROW_TEXT = "Click here for adding a new row..."
    DEFAULT_COLUMNS = ["Key", "Value"]

    def __init__(self, *args, **kwargs):
        self.columns = kwargs.pop("columns", self.DEFAULT_COLUMNS)
        self.default_utility_row_text = kwargs.pop("utility_row_text", self.DEFAULT_UTILITY_ROW_TEXT)

        kwargs['style'] = kwargs.get("style", self.DEFAULT_LIST_CTRL_STYLE)
        wx.ListCtrl.__init__(self, *args, **kwargs)
        ListCtrlAutoWidthMixin.__init__(self)

        self.InitUI()

    def InitUI(self):
        for index, column_name in enumerate(self.columns):
            self.InsertColumn(index, column_name, width=wx.LIST_AUTOSIZE_USEHEADER)

    def AddUtilityRow(self):
        total_rows = self.GetItemCount()
        insert_index = total_rows if total_rows > 0 else 0
        self.InsertItem(insert_index, label=self.default_utility_row_text)

    def DeleteUtilityRow(self):
        last_item_index = self.GetItemCount() - 1
        self.DeleteItem(last_item_index)

    def AddNewHeader(self, header_name, value=wx.EmptyString):
        insert_index = self.GetItemCount() - 1
        self.InsertItem(insert_index, header_name)
        self.SetItem(insert_index, 1, value)
