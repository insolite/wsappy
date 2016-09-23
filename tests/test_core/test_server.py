import json
from unittest.mock import MagicMock, patch

from asynctest.mock import CoroutineMock, call
import websockets

from wsappy.core.server import Server
import wsappy.core.server
from tests.common import WsAppyTest


class ServerTest(WsAppyTest):

    def setUp(self):
        super().setUp()
        self.request_factory = MagicMock()
        self.client_name = 'client'
        self.client_factory = MagicMock()
        self.handler_name = 'foo'
        self.handler = MagicMock()
        self.handlers = {self.handler_name: self.handler}
        self.client_factories = {
            self.client_name: (self.client_factory, self.handlers),
        }
        self.server = Server(self.request_factory,
                             self.client_factories)

    def test_process_message(self):
        request_id = 42
        module_name = self.handler_name
        method_name = 'bar'
        data = {'some': 'args'}
        client = MagicMock()
        raw_message = json.dumps({'request_id': request_id,
                                  'module': module_name,
                                  'method': method_name,
                                  'data': data})

        self.loop.run_until_complete(
            self.server.process_message(raw_message, client)
        )

        self.request_factory.assert_called_once_with(module_name, method_name,
                                                     data, client, request_id)
        client.process_message.assert_called_once_with(self.request_factory())

    def test_on_connect(self):
        connection = MagicMock()
        path = '/{}/'.format(self.client_name)
        self.server.process_message = CoroutineMock()
        messages = [MagicMock(), MagicMock()]
        exc = websockets.exceptions.ConnectionClosed(MagicMock(), MagicMock())
        connection.recv = CoroutineMock(
            side_effect=messages + [exc]
        )

        self.loop.run_until_complete(self.server.on_connect(connection, path))

        self.client_factory.assert_called_once_with(self.server,
                                                    connection,
                                                    self.handlers)
        client = self.client_factory()
        client.on_connected.assert_called_once_with()
        client.on_disconnected.assert_called_once_with()
        self.server.process_message.assert_has_calls(
            [call(message, client) for message in messages],
            any_order=False
        )

    def test_send_message(self):
        data = {'some': 'args'}
        data_text = json.dumps(data)
        client = CoroutineMock()
        # self.server.json_encoder = MagicMock()
        # self.server.json_encoder().encode = MagicMock(return_value=data_text)

        self.loop.run_until_complete(
            self.server.send_message(data, client)
        )

        client.connection.send.assert_called_once_with(data_text)

    def test_run(self):
        host = 'foo'
        port = 42
        args = ('bar', 'test')
        kwargs = {'some': 'args'}

        with patch.object(wsappy.core.server, 'websockets',
                          CoroutineMock()) as websockets_mock:
            self.loop.run_until_complete(
                self.server.run(host, port, *args, **kwargs)
            )

        websockets_mock.serve.assert_called_once_with(
            self.server.on_connect, host, port, *args, **kwargs
        )
