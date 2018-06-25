import unittest
from time import sleep

from tests.amqp.fake import FakeWxApp, EchoServer
from tests.amqp.constants import TEST_AMQP_URL, TEST_ECHO_QUEUE, TEST_ECHO_EXCHANGE


class RpcClientTestCase(unittest.TestCase):
    RESPONSE_ROUTING_KEY = "test"

    @classmethod
    def setUpClass(cls):
        super(RpcClientTestCase, cls).setUpClass()
        cls.echo_server = EchoServer(
            url=TEST_AMQP_URL,
            listened_queue=TEST_ECHO_QUEUE,
            request_exchange=TEST_ECHO_EXCHANGE,
            response_exchange=TEST_ECHO_EXCHANGE,
            response_routing_key=cls.RESPONSE_ROUTING_KEY
        )
        cls.echo_server.start()

    def wait_for_response(self, app):
        while not app.response_returned.is_set() and not app.IsEndedTimeout:
            sleep(0.05)

        sleep(1)
        if app.response is None:
            self.echo_server.stop()
            raise ValueError("Response wasn't returned in time.")

    @classmethod
    def tearDownClass(cls):
        super(RpcClientTestCase, cls).tearDownClass()
        cls.echo_server.stop()

    def test_rpc_client_returns_response(self):
        app = FakeWxApp(timeout=10)
        app.SendRequest(
            url=TEST_AMQP_URL,
            request_exchange=TEST_ECHO_EXCHANGE,
            request_routing_key=TEST_ECHO_QUEUE,
            response_exchange=TEST_ECHO_EXCHANGE,
            response_routing_key=self.RESPONSE_ROUTING_KEY,
            body="test message"
        )
        self.wait_for_response(app)

        assert app.response.body == b"test message"
