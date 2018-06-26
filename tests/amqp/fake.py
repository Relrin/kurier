from time import time, sleep
from threading import Thread, Event

from pika import BlockingConnection, URLParameters

from kurier.amqp.rpc import RpcAmqpClient, RequestSendThread


class Running(object):
    def __init__(self, seconds=10):
        self.run_time = seconds
        self.start_time = time.time()


class PatchedRequestSendThread(RequestSendThread):

    def __init__(self, *args, **kwargs):
        self.ReturnResponse = kwargs.pop('mock', RequestSendThread)
        super(PatchedRequestSendThread, self).__init__(*args, **kwargs)


class FakeWxApp(object):

    def __init__(self, timeout=10):
        self.client = RpcAmqpClient(self, thread_cls=PatchedRequestSendThread)
        self.response_returned = Event()
        self.timeout = timeout
        self.response = None
        self.start_time = None

    def SendRequest(self, url, request_exchange, request_routing_key,
                    response_exchange="", response_routing_key="", body="",
                    properties={}, headers={}):
        self.start_time = time()

        self.client.SendRequest(**{
            "mock": self.OnResponse,
            "connection_url": url,
            "request_exchange": request_exchange,
            "request_routing_key": request_routing_key,
            "response_exchange": response_exchange,
            "response_routing_key": response_routing_key,
            "body": body,
            "properties": properties,
            "headers": headers
        })

    @property
    def IsEndedTimeout(self):
        return time() - self.start_time < self.timeout

    def CancelRequest(self):
        self.client.CancelRequest()

    def OnResponse(self, response):
        self.response = response
        self.response_returned.set()


class EchoServer(Thread):

    def __init__(self, url, listened_queue, request_exchange,
                 response_exchange, response_routing_key):
        super(EchoServer, self).__init__()
        self.connection_parameters = URLParameters(url)
        self.listened_queue = listened_queue
        self.request_exchange = request_exchange
        self.response_exchange = response_exchange
        self.response_routing_key = response_routing_key

        self.channel = None
        self.connection = None
        self.event = Event()

    def run(self):
        self.connection = BlockingConnection(self.connection_parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=self.listened_queue,
            exclusive=True,
            durable=True,
            passive=False,
            auto_delete=True
        )
        self.channel.queue_bind(
            queue=self.listened_queue,
            exchange=self.request_exchange,
            routing_key=self.listened_queue
        )

        method_frame = None
        while method_frame is None:
            if self.event.is_set():
                break

            method_frame, header_frame, body = self.channel.basic_get(self.listened_queue)
            if method_frame:
                self.channel.publish(
                    exchange=self.response_exchange,
                    routing_key=self.response_routing_key,
                    body=body,
                    properties=header_frame
                )
                self.channel.basic_ack(method_frame.delivery_tag)

            method_frame = None
            sleep(0.1)

    def stop(self):
        self.event.set()

        if self.channel:
            self.channel.stop_consuming()
            self.channel.close()

        if self.connection:
            self.connection.close()
