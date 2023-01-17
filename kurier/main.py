import os
import sys

from pathlib import Path

import wx
from pubsub import pub

sys.path.insert(0, os.path.dirname(os.getcwd()))  # NOQA

from kurier.constants import CLOSE_APPLICATION_TOPIC
from kurier.widgets.history import HistoryPanel
from kurier.widgets.work_area import WorkAreaPanel


class Application(wx.Frame):
    WINDOW_TITLE = "Kurier"
    APP_DIRECTORY_NAME = WINDOW_TITLE.lower()
    DEFAULT_SIZE = (800, 600)
    MINIMUM_PANE_SIZE = 0.25

    def __init__(self):
        super(Application, self).__init__(None, title=self.WINDOW_TITLE, size=self.DEFAULT_SIZE)
        self.app_directory_path = str(Path.home().joinpath(self.APP_DIRECTORY_NAME))
        self.window_splitter = None
        self.history = None
        self.work_are = None

        self.SetMinSize(self.DEFAULT_SIZE)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.InitUI()
        self.BindUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        self.window_splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.history = HistoryPanel(self.window_splitter, self.app_directory_path)
        self.work_area = WorkAreaPanel(self.window_splitter)

        self.window_splitter.SplitVertically(self.history, self.work_area)
        self.window_splitter.SetSashGravity(self.MINIMUM_PANE_SIZE)
        self.window_splitter.SetMinimumPaneSize(int(self.DEFAULT_SIZE[0] * self.MINIMUM_PANE_SIZE))

        self.sizer.Add(self.window_splitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(self.sizer)

    def BindUI(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        pub.sendMessage(CLOSE_APPLICATION_TOPIC, message=None)
        event.Skip()


if __name__ == '__main__':
    app = wx.App(redirect=True)
    kurier = Application()
    app.MainLoop()
