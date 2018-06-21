import wx

from wx.lib.scrolledpanel import ScrolledPanel

from kurier.constants import DEFAULT_GAP,  DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP
from kurier.widgets.request.notebook import RequestNotebook


class RequestUIBlock(ScrolledPanel):
    SEND_BUTTON_FONT_SIZE = 10
    HORIZONTAL_SCROLL_INC = DEFAULT_GAP // 2 - 1

    def __init__(self, *args, **kwargs):
        super(RequestUIBlock, self).__init__(*args, **kwargs)
        self.static_box_sizer = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Request")
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.connection_string = None
        self.request_queue_name_input = None
        self.request_exchange_name_input = None
        self.request_routing_key_input = None
        self.response_queue_name_input = None
        self.response_exchange_name_input = None
        self.send_button = None
        self.request_data_notebook = None

        self.InitUI()

    def InitUI(self):
        self.connection_string = wx.TextCtrl(self)
        self.connection_string.SetHint("Connection string in `schema://username:password@host:port/vhost/?query` format")
        self.grid.Add(
            self.connection_string,
            pos=(0, 0),
            span=(0, 4),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )

        self.request_queue_name_input = wx.TextCtrl(self)
        self.request_queue_name_input.SetHint("Request queue name")
        self.grid.Add(self.request_queue_name_input, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.request_exchange_name_input = wx.TextCtrl(self)
        self.request_exchange_name_input.SetHint("Request exchange name")
        self.grid.Add(self.request_exchange_name_input, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.request_routing_key_input = wx.TextCtrl(self)
        self.request_routing_key_input.SetHint("Request routing key")
        self.grid.Add(self.request_routing_key_input, pos=(1, 2), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.response_queue_name_input = wx.TextCtrl(self)
        self.response_queue_name_input.SetHint("Response queue name")
        self.grid.Add(self.response_queue_name_input, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.response_exchange_name_input = wx.TextCtrl(self)
        self.response_exchange_name_input.SetHint("Response exchange name")
        self.grid.Add(self.response_exchange_name_input, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.send_button = wx.Button(self, label="Send", style=wx.BORDER_NONE)
        self.send_button.SetBackgroundColour("#20A5FF")
        self.send_button.SetForegroundColour('#FFFFFF')
        self.send_button.SetFont(wx.Font(wx.FontInfo(self.SEND_BUTTON_FONT_SIZE).Bold().AntiAliased()))
        self.grid.Add(self.send_button, pos=(1, 3), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.request_data_notebook = RequestNotebook(self)
        self.grid.Add(
            self.request_data_notebook,
            pos=(3, 0),
            span=(0, 4),
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            border=DEFAULT_GAP
        )

        self.grid.AddGrowableCol(0, proportion=10)
        self.grid.AddGrowableCol(1, proportion=10)
        self.grid.AddGrowableCol(2, proportion=10)
        self.grid.AddGrowableCol(3, proportion=1)
        self.grid.AddGrowableRow(3, proportion=1)

        self.static_box_sizer.Add(self.grid, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.static_box_sizer)
        self.SetupScrolling(scroll_y=False, rate_x=self.HORIZONTAL_SCROLL_INC)
