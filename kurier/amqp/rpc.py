from threading import Event

import wx

from pika import BlockingConnection
from pika.connection import URLParameters
from pika.exceptions import ProbableAuthenticationError, ProbableAccessDeniedError, \
    IncompatibleProtocolError, ConnectionClosed, ChannelClosed, UnroutableError, NackError
from pika.spec import BasicProperties

from kurier.constants import DEFAULT_MESSAGE_PROPERTIES
from kurier.amqp.events import CUSTOM_EVT_AMQP_RESPONSE, CUSTOM_EVT_AMQP_ERROR, AmqpResponseEvent
from kurier.amqp.exceptions import BaseAmqpException, AmqpInvalidUrl, AmqpInvalidExchange, \
    AmqpUnroutableError, AmqpRequestCancelled
from kurier.amqp.response import Response
from kurier.utils.multithreading import Thread


class RequestSendThread(Thread):

    def __init__(self, parent, event, *args, **kwargs):
        self.connection_url = kwargs.pop('connection_url', None)
        assert self.connection_url is not None, "Connection URL must be specified."

        self.request_exchange = kwargs.pop('request_exchange', None)
        assert self.request_exchange is not None, "The request exchange must be specified."

        self.request_routing_key = kwargs.pop('request_routing_key', None)
        assert self.request_routing_key is not None, "The request routing key must be specified."

        self.response_queue = kwargs.pop("response_queue", "")
        self.response_exchange = kwargs.pop("response_exchange", "")
        self.response_routing_key = kwargs.pop("response_routing_key", "")
        self.body = kwargs.pop("body", "")
        self.properties = kwargs.pop("properties", {})
        self.headers = kwargs.pop("headers", {})

        super(RequestSendThread, self).__init__(event, *args, **kwargs)
        self.parent = parent

        self._connection = None
        self._connection_parameters = None
        self._channel = None
        self._response_queue_name = None

    def CancelOrContinueTask(self):
        if self.IsEventSet():
            raise AmqpRequestCancelled()

    def GetConnection(self):
        self.CancelOrContinueTask()
        try:
            self._connection_parameters = URLParameters(self.connection_url)
            self._connection = BlockingConnection(self._connection_parameters)
        except (ProbableAccessDeniedError, ProbableAuthenticationError):
            raise AmqpInvalidUrl("Invalid credentials to the AMQP node and vhost.")
        except (IncompatibleProtocolError, ConnectionClosed, IndexError):
            raise AmqpInvalidUrl("Invalid URL to the AMQP node.")
        return self._connection

    def CreateChannel(self, connection):
        self.CancelOrContinueTask()
        self._channel = connection.channel()
        return self._channel

    def DeclareQueue(self, channel, queue_name):
        self.CancelOrContinueTask()
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
        self.CancelOrContinueTask()
        try:
            channel.queue_bind(
                queue=queue_name,
                exchange=exchange,
                routing_key=routing_key
            )
        except ChannelClosed:
            message = "No exchange \"{}\" in vhost \"{}\".".format(
                exchange, self._connection_parameters.virtual_host
            )
            raise AmqpInvalidExchange(message)

    def SetChannelQos(self, channel):
        self.CancelOrContinueTask()
        channel.basic_qos(
            prefetch_count=1,
            prefetch_size=0,
            all_channels=False
        )

    def PublishMessage(self, channel):
        self.CancelOrContinueTask()

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
                properties=BasicProperties(**properties),
                immediate=True
            )
        except (UnroutableError, NackError) as exc:
            raise AmqpUnroutableError(repr(exc))

    def ConsumeResponse(self, channel, queue_name):
        self.CancelOrContinueTask()

        try:
            method_frame = None
            response = Response()
            while method_frame is None:
                self.CancelOrContinueTask()

                method_frame, header_frame, body = channel.basic_get(queue_name)
                if method_frame:
                    channel.basic_ack(method_frame.delivery_tag)
                    properties = {
                        key: getattr(header_frame, key, None)
                        for key in DEFAULT_MESSAGE_PROPERTIES
                    }
                    headers = header_frame.headers
                    response = Response(properties=properties, headers=headers, body=body)
                    break
        except ChannelClosed:
            message = "No exchange \"{}\" in vhost \"{}\".".format(
                self.request_exchange, self._connection_parameters.virtual_host
            )
            raise AmqpInvalidExchange(message)
        except ConnectionClosed:
            raise AmqpInvalidExchange("The queue with the \"{}\" routing key was not found.".format(self.request_routing_key))

        return response

    def ReturnResponse(self, response):
        self.CancelOrContinueTask()

        wx_event = AmqpResponseEvent(
            CUSTOM_EVT_AMQP_RESPONSE,
            wx.ID_ANY,
            properties=response.properties,
            headers=response.headers,
            body=response.body,
        )
        wx.PostEvent(self.parent, wx_event)

    def ReturnError(self, error):
        wx_event = AmqpResponseEvent(CUSTOM_EVT_AMQP_ERROR, wx.ID_ANY, error=error)
        wx.PostEvent(self.parent, wx_event)

    def CleanResources(self):
        self._response_queue_name = None

        if self._channel and not (self._channel.is_closed or self._channel.is_closing):
            self._channel.close()
            self._channel = None

        if self._connection and not (self._connection.is_closed or self._connection.is_closing):
            self._connection.close()
            self._connection = None

    def run(self):
        try:
            connection = self.GetConnection()
            channel = self.CreateChannel(connection)
            queue_name = self.DeclareQueue(channel, self.response_queue)
            self.BindQueue(channel, queue_name, self.response_exchange, self.response_routing_key)
            self.SetChannelQos(channel)
            self.PublishMessage(channel)
            response = self.ConsumeResponse(channel, queue_name)
            self.ReturnResponse(response)
        except AmqpRequestCancelled:
            pass
        except BaseAmqpException as amqp_error:
            self.ReturnError(amqp_error)
        finally:
            self.CleanResources()


class RpcAmqpClient(object):

    def __init__(self, parent, thread_cls=RequestSendThread, *args, **kwargs):
        self.parent = parent
        self.event = Event()
        self.thread = None
        self.thread_cls = thread_cls

    def SendRequest(self, *args, **kwargs):
        self.event.clear()
        self.thread = self.thread_cls(self.parent, self.event, *args, **kwargs)
        self.thread.start()

    def CancelRequest(self):
        self.event.set()
