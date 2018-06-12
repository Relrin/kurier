import wx
from wx.aui import AuiNotebook

from kurier.constants import DEFAULT_GAP, DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP
from kurier.widgets.amqp_tab import AmqpTab


class WorkAreaPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(WorkAreaPanel, self).__init__(parent, *args, **kwargs)
        self.notebook = AuiNotebook(self)
        self.sizer = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.InitUI()

    def InitUI(self):
        self.AddNewTab()
        self.sizer.Add(self.notebook, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.SetSizer(self.sizer)

    def AddNewTab(self, tab_name="New tab"):
        new_tab = AmqpTab(self.notebook)
        self.notebook.AddPage(new_tab, tab_name, select=True)
