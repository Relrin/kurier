import wx

from kurier.constants import DEFAULT_GAP, DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP
from kurier.widgets.request.ui import RequestUIBlock


class AmqpTab(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(AmqpTab, self).__init__(parent, *args, **kwargs)
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.request_ui_block = None

        self.InitUI()

    def InitUI(self):
        self.request_ui_block = RequestUIBlock(self)
        self.grid.Add(self.request_ui_block, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.grid.AddGrowableCol(0)
        self.grid.AddGrowableRow(0)
        self.SetSizer(self.grid)
