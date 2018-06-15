import wx

from kurier.constants import DEFAULT_GAP,  DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP
from kurier.widgets.request.notebook import RequestNotebook


class RequestUIBlock(wx.Panel):
    SEND_BUTTON_FONT_SIZE = 10

    def __init__(self, *args, **kwargs):
        super(RequestUIBlock, self).__init__(*args, **kwargs)
        self.static_box_sizer = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Request")
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.queue_name_input = None
        self.exchange_name_input = None
        self.routing_key_input = None
        self.send_button = None
        self.request_data_notebook = None

        self.InitUI()

    def InitUI(self):
        self.queue_name_input = wx.TextCtrl(self)
        self.queue_name_input.SetHint("Queue name")
        self.grid.Add(self.queue_name_input, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.exchange_name_input = wx.TextCtrl(self)
        self.exchange_name_input.SetHint("Exchange name")
        self.grid.Add(self.exchange_name_input, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.routing_key_input = wx.TextCtrl(self)
        self.routing_key_input.SetHint("Routing key")
        self.grid.Add(self.routing_key_input, pos=(0, 2), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.send_button = wx.Button(self, label="Send", style=wx.BORDER_NONE)
        self.send_button.SetBackgroundColour("#20A5FF")
        self.send_button.SetForegroundColour('#FFFFFF')
        self.send_button.SetFont(wx.Font(wx.FontInfo(self.SEND_BUTTON_FONT_SIZE).Bold().AntiAliased()))
        self.grid.Add(self.send_button, pos=(0, 3), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.request_data_notebook = RequestNotebook(self)
        self.grid.Add(
            self.request_data_notebook,
            pos=(1, 0),
            span=(0, 4),
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            border=DEFAULT_GAP
        )

        self.grid.AddGrowableCol(0, proportion=10)
        self.grid.AddGrowableCol(1, proportion=10)
        self.grid.AddGrowableCol(2, proportion=10)
        self.grid.AddGrowableCol(3, proportion=1)
        self.grid.AddGrowableRow(1, proportion=1)

        self.static_box_sizer.Add(self.grid, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.static_box_sizer)