import wx

from kurier.constants import DEFAULT_GAP, DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP
from kurier.widgets.notebook import CustomAuiNotebook


class WorkAreaPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(WorkAreaPanel, self).__init__(parent, *args, **kwargs)
        self.notebook = CustomAuiNotebook(self)
        self.sizer = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.InitUI()

    def InitUI(self):
        self.sizer.Add(self.notebook, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.SetSizer(self.sizer)
