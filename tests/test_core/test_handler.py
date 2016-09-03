from unittest.mock import MagicMock

from wsappy.core.handler import Handler
from tests.common import WsAppyTest


class HandlerTest(WsAppyTest):

    def setUp(self):
        super().setUp()
        self.handler = Handler()

    def test_get_module_name(self):
        class FooBarHandler(Handler):
            pass
        foo_handler = FooBarHandler()

        module_name = foo_handler.get_module_name()

        self.assertEqual(module_name, 'foobar')

    def test_send_message(self):
        client = MagicMock()
        request_id = 42
        event = 'foo'
        data = {'some': 'args'}
        module_name = 'bar'
        self.handler.get_module_name = MagicMock(return_value=module_name)

        self.loop.run_until_complete(
            self.handler.send_message(client, request_id, event, **data)
        )

        client.send_message.assert_called_once_with(
            request_id, module_name, event, **data
        )
        self.handler.get_module_name.assert_called_once_with()
