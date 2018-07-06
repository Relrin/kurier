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
        self.BindUI()

    def InitUI(self):
        for index, column_name in enumerate(self.columns):
            self.InsertColumn(index, column_name, width=wx.LIST_AUTOSIZE_USEHEADER)

    def BindUI(self):
        pass

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

        self.BindUI()

    def BindUI(self):
        super(EditableListCtrl, self).BindUI()

        deleteRowId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnDeleteRow, id=deleteRowId)

        accelerator_table = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_BACK, deleteRowId),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, deleteRowId),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DELETE, deleteRowId)
        ])
        self.SetAcceleratorTable(accelerator_table)

    def OnDeleteRow(self, event):
        is_editor_mode = self.editor and self.editor.IsShown()
        is_utility_row = self.curRow == self.GetItemCount() - 1 if self.has_utility_row else False
        if not is_editor_mode and not is_utility_row:
            self.DeleteItem(self.curRow)
            return

        event.Skip()

    def OnLeftDown(self, event=None):
        x, y = event.GetPosition()
        row, _flags = self.HitTest((x, y))

        if self.has_utility_row and row == self.GetItemCount() - 1:
            event.Skip()
            return

        super(EditableListCtrl, self).OnLeftDown(event)
