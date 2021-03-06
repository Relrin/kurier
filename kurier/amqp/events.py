import wx

from kurier.constants import AMQP_RESPONSE_RECEIVED_TOPIC
from kurier.amqp.response import Response


CUSTOM_EVT_AMQP_RESPONSE = wx.NewEventType()
EVT_AMQP_RESPONSE = wx.PyEventBinder(CUSTOM_EVT_AMQP_RESPONSE, 1)

CUSTOM_EVT_AMQP_ERROR = wx.NewEventType()
EVT_AMQP_ERROR = wx.PyEventBinder(CUSTOM_EVT_AMQP_ERROR, 1)

CUSTOM_EVT_UPDATE_AMQP_TAB_NAME = wx.NewEventType()
EVT_UPDATE_AMQP_TAB_NAME = wx.PyEventBinder(CUSTOM_EVT_UPDATE_AMQP_TAB_NAME, 1)


def get_topic_name(suffix):
    return "{}_{}".format(AMQP_RESPONSE_RECEIVED_TOPIC, suffix)


class AmqpResponseEvent(wx.PyCommandEvent):

    def __init__(self, etype, eid, properties=None, headers=None, body=None, error=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._response = Response(properties=properties, headers=headers, body=body)
        self._error = error

    def GetResponse(self):
        return self._response

    def GetError(self):
        return self._error


class UpdateAmqpTabNameEvent(wx.PyCommandEvent):

    def __init__(self, etype, eid, exchange=None, routing_key=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._exchange = exchange
        self._routing_key = routing_key

    def GetExchangeName(self):
        return self._exchange

    def GetRoutingKey(self):
        return self._routing_key
