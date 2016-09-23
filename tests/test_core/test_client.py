from unittest.mock import MagicMock
import json

from asynctest.mock import CoroutineMock

from wsappy.core.client import Client
from wsappy.core.utils import HANDLER_FLAG
from tests.common import WsAppyTest


class ClientTest(WsAppyTest):

    def setUp(self):
        super().setUp()
        self.server = CoroutineMock()
        self.connection = CoroutineMock()
        self.handler_name = 'foo'
        self.handler = MagicMock()
        self.handlers = {self.handler_name: self.handler}
        self.client = Client(self.server, self.connection, self.handlers)

    def test_send_message(self):
        request_id = 42
        module = 'foo'
        method = 'bar'
        event = 'test'
        data = {'some': 'args'}

        self.loop.run_until_complete(
            self.client.send_message(request_id, module, method, event, **data)
        )

        self.server.send_message.assert_called_once_with(
            {'request_id': request_id,
             'module': module,
             'method': method,
             'event': event,
             'data': data},
            self.client
        )

    def test_on_connected(self):
        self.loop.run_until_complete(self.client.on_connected())

    def test_on_disconnected(self):
        self.loop.run_until_complete(self.client.on_disconnected())

    def test_process_message__called(self):
        # request_id = 42
        module_name = self.handler_name
        method_name = 'bar'
        data = {'some': 'args'}
        # client = MagicMock()
        method = MagicMock()
        setattr(method, HANDLER_FLAG, True)
        setattr(self.handler, method_name, method)
        request = MagicMock()
        request.module = module_name
        request.method = method_name
        request.data = data

        self.loop.run_until_complete(
            self.client.process_message(request)
        )

        method.assert_called_once_with(request, **request.data)

    def test_process_message__not_handler(self):
        # request_id = 42
        module_name = self.handler_name
        method_name = 'bar'
        data = {'some': 'args'}
        # client = MagicMock()
        method = MagicMock()
        setattr(method, HANDLER_FLAG, False)
        setattr(self.handler, method_name, method)
        request = MagicMock()
        request.module = module_name
        request.method = method_name
        request.data = data

        self.assertRaises(PermissionError,
                          self.loop.run_until_complete,
                          self.client.process_message(request))

        method.assert_not_called()
