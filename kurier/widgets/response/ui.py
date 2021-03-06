import wx

from pubsub import pub

from kurier.constants import DEFAULT_GAP,  DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP
from kurier.amqp.events import get_topic_name
from kurier.widgets.response.notebook import ResponseNotebook


class ResponseUIBlock(wx.Panel):
    SEND_BUTTON_FONT_SIZE = 10

    def __init__(self, tab_id, parent, *args, **kwargs):
        super(ResponseUIBlock, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.static_box_sizer = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Response")
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.queue_name_input = None
        self.exchange_name_input = None
        self.routing_key_input = None
        self.send_button = None
        self.request_data_notebook = None

        self.tab_id = tab_id
        self.topic_name = get_topic_name(self.tab_id)
        pub.subscribe(self.OnAmqpResponse, self.topic_name)

        self.InitUI()

    def InitUI(self):
        self.request_data_notebook = ResponseNotebook(self)
        self.grid.Add(
            self.request_data_notebook,
            pos=(0, 0),
            span=(0, 4),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )
        self.grid.AddGrowableCol(0, proportion=10)
        self.grid.AddGrowableRow(0, proportion=1)

        self.static_box_sizer.Add(self.grid, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.static_box_sizer)

    def OnAmqpResponse(self, message):
        self.request_data_notebook.RenderResponse(message)
