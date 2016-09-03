from unittest.mock import MagicMock

from wsappy.core.request import Request
from tests.common import WsAppyTest


class RequestTest(WsAppyTest):

    def setUp(self):
        super().setUp()
        self.module = 'foo'
        self.method = 'var'
        self.data = {'some': 'args'}
        self.client = MagicMock()
        self.request_id = 42
        self.request = Request(self.module, self.method, self.data,
                               self.client, self.request_id)

    def test_response(self):
        event = 'foo'
        data = {'another': 'params'}

        self.loop.run_until_complete(
            self.request.response(event, **data)
        )

        self.client.send_message.assert_called_once_with(
            self.request_id, self.module, self.method, event, **data
        )
