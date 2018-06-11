import wx

from kurier.constants import DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP


class WorkAreaPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(WorkAreaPanel, self).__init__(parent, *args, **kwargs)
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.InitUI()

    def InitUI(self):
        self.SetSizer(self.grid)
