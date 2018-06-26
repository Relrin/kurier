from bisect import bisect

import wx

from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, TextEditMixin


class ResizableListCtrl(ListCtrlAutoWidthMixin, wx.ListCtrl):
    DEFAULT_LIST_CTRL_STYLE = wx.LC_REPORT \
        | wx.LC_VRULES \
        | wx.LC_HRULES \
        | wx.LC_SINGLE_SEL
    DEFAULT_UTILITY_ROW_TEXT = "Click here for adding a new row..."
    DEFAULT_COLUMNS = ["Key", "Value"]
    has_utility_row = False

    def __init__(self, *args, **kwargs):
        self.columns = kwargs.pop("columns", self.DEFAULT_COLUMNS)
        self.default_utility_row_text = kwargs.pop("utility_row_text", self.DEFAULT_UTILITY_ROW_TEXT)  # NOQA

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
        self.has_utility_row = True

    def DeleteUtilityRow(self):
        last_item_index = self.GetItemCount() - 1
        self.DeleteItem(last_item_index)
        self.has_utility_row = False

    def AddNewRow(self, key, value=wx.EmptyString, index=None):
        if value is None:
            return

        insert_index = index if index is not None else self.GetItemCount()
        value = self.ValueToString(value)
        self.InsertItem(insert_index, key)
        self.SetItem(insert_index, 1, value)

    def ValueToString(self, value):
        if value in [wx.EmptyString, ""]:
            return wx.EmptyString
        return str(value)


class EditableListCtrl(TextEditMixin, ResizableListCtrl):

    def __init__(self, *args, **kwargs):
        ResizableListCtrl.__init__(self, *args, **kwargs)
        TextEditMixin.__init__(self)

    def OnLeftDown(self, event=None):
        x, y = event.GetPosition()

        loc = 0
        self.col_locs = [0]
        for n in range(self.GetColumnCount()):
            loc = loc + self.GetColumnWidth(n)
            self.col_locs.append(loc)

        col = bisect(self.col_locs, x + self.GetScrollPos(wx.HORIZONTAL)) - 1
        if self.has_utility_row and col == self.GetItemCount() - 1:
            event.Skip()
            return

        super(EditableListCtrl, self).OnLeftDown(event)
