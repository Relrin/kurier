import wx

from kurier.amqp.response import Response

CUSTOM_EVT_AMQP_RESPONSE = wx.NewEventType()
EVT_AMQP_RESPONSE = wx.PyEventBinder(CUSTOM_EVT_AMQP_RESPONSE, 1)

CUSTOM_EVT_AMQP_ERROR = wx.NewEventType()
EVT_AMQP_ERROR = wx.PyEventBinder(CUSTOM_EVT_AMQP_ERROR, 1)


class AmqpResponseEvent(wx.PyCommandEvent):

    def __init__(self, etype, eid, properties=None, headers=None, body=None, error=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._response = Response(properties=properties, headers=headers, body=body)
        self._error = error

    def GetResponse(self):
        return self._response

    def GetError(self):
        return self._error
