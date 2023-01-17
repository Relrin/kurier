from uuid import uuid4

import wx

from kurier.constants import DEFAULT_GAP
from kurier.interfaces import IStateRestorable
from kurier.amqp.events import EVT_UPDATE_AMQP_TAB_NAME
from kurier.widgets.request.ui import RequestUIBlock
from kurier.widgets.response.ui import ResponseUIBlock


class AmqpTab(IStateRestorable, wx.Panel):
    MINIMUM_PANE_SIZE = 0.45
    MINIMAL_PANEL_HEIGHT = 600

    def __init__(self, parent, *args, **kwargs):
        super(AmqpTab, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.window_splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.request_ui_block = None
        self.response_ui_block = None
        self.tab_id = str(uuid4())

        self.InitUI()
        self.BindUI()

    def InitUI(self):
        self.request_ui_block = RequestUIBlock(self.tab_id, self.window_splitter)
        self.response_ui_block = ResponseUIBlock(self.tab_id, self.window_splitter)

        self.window_splitter.SplitHorizontally(self.request_ui_block, self.response_ui_block)
        self.window_splitter.SetSashGravity(self.MINIMUM_PANE_SIZE)
        self.window_splitter.SetMinimumPaneSize(int(self.MINIMAL_PANEL_HEIGHT * self.MINIMUM_PANE_SIZE))

        self.sizer.Add(self.window_splitter, 1, wx.EXPAND | wx.ALL, border=DEFAULT_GAP)
        self.SetSizer(self.sizer)

    def InitFromState(self, **state):
        self.request_ui_block.InitFromState(**state)

    def BindUI(self):
        self.Bind(EVT_UPDATE_AMQP_TAB_NAME, self.OnUpdateAmqpTabName)

    def OnUpdateAmqpTabName(self, event):
        wx.PostEvent(self.parent, event)
