import os
import sys

import wx

sys.path.insert(0, os.path.dirname(os.getcwd()))  # NOQA

from kurier.widgets.history import HistoryPanel
from kurier.widgets.work_area import WorkAreaPanel


class Application(wx.Frame):
    WINDOW_TITLE = "Kurier"
    DEFAULT_SIZE = (800, 600)
    MINIMUM_PANE_SIZE = 0.25

    def __init__(self):
        super(Application, self).__init__(None, title=self.WINDOW_TITLE, size=self.DEFAULT_SIZE)
        self.SetMinSize(self.DEFAULT_SIZE)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        window_splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        history = HistoryPanel(window_splitter)
        work_area = WorkAreaPanel(window_splitter)

        window_splitter.SplitVertically(history, work_area)
        window_splitter.SetSashGravity(self.MINIMUM_PANE_SIZE)
        window_splitter.SetMinimumPaneSize(self.DEFAULT_SIZE[0] * self.MINIMUM_PANE_SIZE)

        self.sizer.Add(window_splitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(self.sizer)


if __name__ == '__main__':
    app = wx.App(redirect=True)
    kurier = Application()
    app.MainLoop()
