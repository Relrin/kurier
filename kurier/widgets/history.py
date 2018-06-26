import wx

from kurier.constants import DEFAULT_GAP, DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP


class HistoryPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(HistoryPanel, self).__init__(parent, *args, **kwargs)
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)

        self.InitUI()

    def InitUI(self):
        history_input = wx.SearchCtrl(self)
        self.grid.Add(
            history_input,
            pos=(0, 0),
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=DEFAULT_GAP
        )

        history_entries = wx.ListCtrl(self)
        self.grid.Add(history_entries, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.grid.AddGrowableCol(0)
        self.grid.AddGrowableRow(1)
        self.SetSizer(self.grid)
