from threading import Event

import wx

from pika import BlockingConnection
from pika.connection import URLParameters
from pika.exceptions import IncompatibleProtocolError, ChannelClosed, UnroutableError, \
    NackError
from pika.spec import BasicProperties

from kurier.constants import DEFAULT_MESSAGE_PROPERTIES
from kurier.amqp.events import CUSTOM_EVT_AMQP_RESPONSE, AmqpResponseEvent
from kurier.amqp.exceptions import AmqpInvalidUrl, AmqpInvalidExchange, \
    AmqpUnroutableError, AmqpRequestCancelled
from kurier.utils.multithreading import Thread


class RequestSendThread(Thread):

    def __init__(self, parent, event, *args, **kwargs):
        self.connection_url = kwargs.pop('connection_url', None)
        assert self.connection_url is not None, "Connection URL must be specified."

        self.request_exchange = kwargs.pop('request_exchange', None)
        assert self.request_exchange is not None, "The request exchange must be specified."

        self.request_routing_key = kwargs.pop('request_routing_key', None)
        assert self.request_routing_key is not None, "The request routing key must be specified."

        self.connection_parameters = URLParameters(self.connection_url)
        self.response_queue = kwargs.pop("response_queue", "")
        self.response_exchange = kwargs.pop("response_exchange", "")
        self.response_routing_key = kwargs.pop("response_routing_key", "")
        self.body = kwargs.pop("body", "")
        self.properties = kwargs.pop("properties", {})
        self.headers = kwargs.pop("headers", {})

        super(RequestSendThread, self).__init__(event, *args, **kwargs)
        self.parent = parent
        self.waiter = Event()

        self._connection = None
        self._channel = None
        self._response_queue_name = None

    def IsResponseReturned(self):
        return self.waiter.is_set()

    def CancellOrContinueTask(self):
        if self.IsEventSet():
            raise AmqpRequestCancelled()

    def GetConnection(self):
        self.CancellOrContinueTask()
        try:
            self._connection = BlockingConnection(self.connection_parameters)
        except IncompatibleProtocolError:
            raise AmqpInvalidUrl("Invalid URL to the AMQP node.")
        return self._connection

    def CreateChannel(self, connection):
        self.CancellOrContinueTask()
        self._channel = connection.channel()
        return self._channel

    def DeclareQueue(self, channel, queue_name):
        self.CancellOrContinueTask()
        declare_result = channel.queue_declare(
            queue=queue_name,
            exclusive=True,
            durable=True,
            passive=False,
            auto_delete=True
        )
        self._response_queue_name = declare_result.method.queue
        return self._response_queue_name

    def BindQueue(self, channel, queue_name, exchange, routing_key):
        self.CancellOrContinueTask()
        try:
            channel.queue_bind(
                queue=queue_name,
                exchange=exchange,
                routing_key=routing_key
            )
        except ChannelClosed:
            message = "No exchange '{}' in vhost '{}'.".format(
                exchange, self.connection_parameters.virtual_host
            )
            raise AmqpInvalidExchange(message)

    def SetChannelQos(self, channel):
        self.CancellOrContinueTask()
        channel.basic_qos(
            prefetch_count=1,
            prefetch_size=0,
            all_channels=False
        )

    def PublishMessage(self, channel):
        self.CancellOrContinueTask()

        properties = {'headers': self.headers}
        properties.update({
            key: self.properties.get(key, None)
            for key in DEFAULT_MESSAGE_PROPERTIES
        })

        try:
            channel.publish(
                exchange=self.request_exchange,
                routing_key=self.request_routing_key,
                body=self.body,
                properties=BasicProperties(**properties)
            )
        except (UnroutableError, NackError) as exc:
            raise AmqpUnroutableError(repr(exc))

    # TODO: Implement consuming only one incoming message
    def ConsumeResponse(self, channel):
        self.CancellOrContinueTask()
        return None

    def CleanResources(self):
        self._response_queue_name = None

        if self._channel:
            self._channel.close()
            self._channel = None

        if self._connection:
            self._connection.close()
            self._connection = None

    def run(self):
        try:
            self.waiter.clear()

            connection = self.GetConnection()
            channel = self.CreateChannel(connection)
            queue_name = self.DeclareQueue(channel, self.response_queue)
            self.BindQueue(channel, queue_name, self.response_exchange, queue_name)
            self.SetChannelQos(channel)
            self.PublishMessage(channel)
            response = self.ConsumeResponse(channel)

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
