from threading import Event

import wx

from kurier.amqp.events import CUSTOM_EVT_AMQP_RESPONSE, AmqpResponseEvent
from kurier.amqp.exceptions import AmqpRequestCancelled
from kurier.utils.multithreading import Thread


class RequestSendThread(Thread):

    def __init__(self, parent, event, *args, **kwargs):
        Thread.__init__(event, *args, **kwargs)
        self.parent = parent
        self.waiter = Event()

        self.connection_url = kwargs.get('connection_url', None)
        assert self.connection_url is not None, "Connection URL must be specified"

        self.routing_key = kwargs.get('routing_key', None)
        assert self.routing_key is not None, "Routing key must be specified"

        self.request_exchange = kwargs.get('request_exchange', '')
        self.response_queue = kwargs.get('response_queue', None)
        self.response_exchange = kwargs.get('response_exchange', '')
        self.properties = kwargs.get('properties', None)
        self.headers = kwargs.get('headers', None)

    def IsResponseReturned(self):
        return self.waiter.is_set()

    def CancellOrContinueTask(self):
        if self.IsEventSet():
            raise AmqpRequestCancelled()

    def GetConnection(self):
        self.CancellOrContinueTask()

    def CreateChannel(self):
        self.CancellOrContinueTask()

    def DeclareQueue(self):
        self.CancellOrContinueTask()

    def BindQueue(self):
        self.CancellOrContinueTask()

    def SetQueueQos(self):
        self.CancellOrContinueTask()

    def PublishMessage(self):
        self.CancellOrContinueTask()

    def ConsumeResponse(self):
        self.CancellOrContinueTask()

    def CleanResources(self):
        pass

    def run(self):
        try:
            self.waiter.clear()

            self.GetConnection()
            self.CreateChannel()
            self.DeclareQueue()
            self.BindQueue()
            self.SetQueueQos()
            self.PublishMessage()

            wx_event = AmqpResponseEvent(
                CUSTOM_EVT_AMQP_RESPONSE,
                wx.ID_ANY,
                properties=None,
                headers=None,
                body=None,
            )
            wx.PostEvent(self.parent, wx_event)
        except AmqpRequestCancelled:
            pass
        finally:
            self.CleanResources()


class RpcAmqpClient(object):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.event = Event()
        self.thread = None

    def SendRequest(self, *args, **kwargs):
        self.event.clear()
        self.thread = RequestSendThread(self.parent, self.event, *args, **kwargs)
        self.thread.start()

    def CancelRequest(self):
        self.event.set()
