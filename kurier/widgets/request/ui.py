import wx

from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel

from kurier.constants import DEFAULT_GAP,  DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP, \
    SAVE_STATE_TOPIC
from kurier.interfaces import IStateRestorable
from kurier.amqp.events import EVT_AMQP_RESPONSE, EVT_AMQP_ERROR, get_topic_name, \
    UpdateAmqpTabNameEvent, CUSTOM_EVT_UPDATE_AMQP_TAB_NAME
from kurier.amqp.rpc import RpcAmqpClient
from kurier.widgets.error_dlg import ErrorDialog
from kurier.widgets.request.notebook import RequestNotebook


class RequestUIBlock(IStateRestorable, ScrolledPanel):
    SEND_BUTTON_FONT_SIZE = 10
    HORIZONTAL_SCROLL_INC = DEFAULT_GAP // 2 - 1

    SEND_REQUEST_BUTTON_LABEL = "Send"
    CANCEL_REQUEST_BUTTON_LABEL = "Cancel"

    def __init__(self, tab_id, parent, *args, **kwargs):
        super(RequestUIBlock, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.static_box_sizer = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Request")
        self.grid = wx.GridBagSizer(DEFAULT_VERTICAL_GAP, DEFAULT_HORIZONTAL_GAP)
        self.connection_string = None
        self.request_exchange_name_input = None
        self.request_routing_key_input = None
        self.response_queue_name_input = None
        self.response_exchange_name_input = None
        self.send_button = None
        self.request_data_notebook = None

        self.tab_id = tab_id
        self.topic_name = get_topic_name(self.tab_id)
        self.amqp_client = RpcAmqpClient(self)

        self.InitUI()
        self.BindUI()

    def InitUI(self):
        self.connection_string = wx.TextCtrl(self)
        self.connection_string.SetHint("schema://username:password@host:port/vhost/?query")
        self.grid.Add(
            self.connection_string,
            pos=(0, 0),
            span=(0, 3),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )

        button_font = wx.Font(wx.FontInfo(self.SEND_BUTTON_FONT_SIZE).Bold().AntiAliased())
        self.send_button = wx.Button(self, label=self.SEND_REQUEST_BUTTON_LABEL, style=wx.BORDER_NONE)  # NOQA
        self.send_button.SetBackgroundColour("#20A5FF")
        self.send_button.SetForegroundColour("#FFFFFF")
        self.send_button.SetFont(button_font)
        self.grid.Add(self.send_button, pos=(0, 3), flag=wx.EXPAND | wx.ALL, border=DEFAULT_GAP)

        self.request_exchange_name_input = wx.TextCtrl(self)
        self.request_exchange_name_input.SetHint("Request exchange name")
        self.grid.Add(
            self.request_exchange_name_input,
            pos=(1, 0),
            span=(0, 2),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP,
        )

        self.request_routing_key_input = wx.TextCtrl(self)
        self.request_routing_key_input.SetHint("Request routing key")
        self.grid.Add(
            self.request_routing_key_input,
            pos=(1, 2),
            span=(0, 2),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )

        self.response_queue_name_input = wx.TextCtrl(self)
        self.response_queue_name_input.SetHint("Response queue name")
        self.grid.Add(
            self.response_queue_name_input,
            pos=(2, 0),
            span=(0, 1),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )

        self.response_exchange_name_input = wx.TextCtrl(self)
        self.response_exchange_name_input.SetHint("Response exchange name")
        self.grid.Add(
            self.response_exchange_name_input,
            pos=(2, 1),
            span=(0, 1),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )

        self.response_routing_key_input = wx.TextCtrl(self)
        self.response_routing_key_input.SetHint("Response routing key")
        self.grid.Add(
            self.response_routing_key_input,
            pos=(2, 2),
            span=(0, 2),
            flag=wx.EXPAND | wx.ALL,
            border=DEFAULT_GAP
        )

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

    def InitFromState(self, **state):
        self.connection_string.SetValue(state.get("connection_url", ""))
        self.request_exchange_name_input.SetValue(state.get("request_exchange", ""))
        self.request_routing_key_input.SetValue(state.get("request_routing_key", ""))
        self.response_queue_name_input.SetValue(state.get("response_queue", ""))
        self.response_exchange_name_input.SetValue(state.get("response_exchange", ""))
        self.response_routing_key_input.SetValue(state.get("response_routing_key", ""))
        self.request_data_notebook.InitFromState(**state)

    def BindUI(self):
        self.Bind(wx.EVT_BUTTON, self.OnSendButtonClick)
        self.Bind(EVT_AMQP_RESPONSE, self.OnAmqpResponse)
        self.Bind(EVT_AMQP_ERROR, self.OnAmqpError)

    def GetRequestParameters(self):
        return {
            "connection_url": self.connection_string.GetValue(),
            "request_exchange": self.request_exchange_name_input.GetValue(),
            "request_routing_key": self.request_routing_key_input.GetValue(),
            "response_queue": self.response_queue_name_input.GetValue(),
            "response_exchange": self.response_exchange_name_input.GetValue(),
            "response_routing_key": self.response_routing_key_input.GetValue(),
            "properties": self.request_data_notebook.GetRequestProperties(),
            "headers": self.request_data_notebook.GetRequestHeaders(),
            "body": self.request_data_notebook.GetRequestData(),
        }

    def OnSendButtonClick(self, _event):
        if self.send_button.GetLabel() == self.SEND_REQUEST_BUTTON_LABEL:
            self.send_button.SetLabel(self.CANCEL_REQUEST_BUTTON_LABEL)
            request_parameters = self.GetRequestParameters()

            wx_event = UpdateAmqpTabNameEvent(
                CUSTOM_EVT_UPDATE_AMQP_TAB_NAME,
                wx.ID_ANY,
                exchange=request_parameters["request_exchange"],
                routing_key=request_parameters["request_routing_key"],
            )
            wx.PostEvent(self.parent, wx_event)

            self.amqp_client.SendRequest(**request_parameters)
        else:
            self.amqp_client.CancelRequest()
            self.send_button.SetLabel(self.SEND_REQUEST_BUTTON_LABEL)

    def OnAmqpResponse(self, event):
        response = event.GetResponse()
        pub.sendMessage(self.topic_name, message=response)
        pub.sendMessage(SAVE_STATE_TOPIC, message=self.GetRequestParameters())
        self.send_button.SetLabel(self.SEND_REQUEST_BUTTON_LABEL)

    def OnAmqpError(self, event):
        error = event.GetError()
        error_dialog = ErrorDialog(self, error, "AMQP error")
        error_dialog.ShowDialog()
        self.send_button.SetLabel(self.SEND_REQUEST_BUTTON_LABEL)
