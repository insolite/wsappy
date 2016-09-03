import json

from asynctest.mock import CoroutineMock

from wsappy.core.client import Client
from tests.common import WsAppyTest


class ClientTest(WsAppyTest):

    def setUp(self):
        super().setUp()
        self.connection = CoroutineMock()
        self.client = Client(self.connection)

    def test_send_message(self):
        request_id = 42
        module = 'foo'
        method = 'bar'
        event = 'test'
        data = {'some': 'args'}

        self.loop.run_until_complete(
            self.client.send_message(request_id, module, method, event, **data)
        )

        self.connection.send.assert_called_once_with(
            json.dumps({'request_id': request_id,
                        'module': module,
                        'method': method,
                        'event': event,
                        'data': data})
        )

    def test_on_connected(self):
        self.loop.run_until_complete(self.client.on_connected())

    def test_on_disconnected(self):
        self.loop.run_until_complete(self.client.on_disconnected())
