import wx


CUSTOM_EVT_AMQP_RESPONSE = wx.NewEventType()
EVT_AMQP_RESPONSE = wx.PyEventBinder(CUSTOM_EVT_AMQP_RESPONSE, 1)


class AmqpResponseEvent(wx.PyCommandEvent):

    def __init__(self, etype, eid, properties=None, headers=None, body=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.properties = properties
        self.headers = headers
        self.body = body

    def GetProperties(self):
        return self.properties

    def GetHeaders(self):
        return self.headers

    def GetBody(self):
        return self.body
