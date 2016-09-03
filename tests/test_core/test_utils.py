import asyncio
from unittest.mock import MagicMock

from asynctest.mock import CoroutineMock

from wsappy.core.utils import handler_method, HANDLER_FLAG
from tests.common import WsAppyTest


class UtilsTest(WsAppyTest):

    def test_handler_method(self):
        result = MagicMock()
        method = CoroutineMock(return_value=result)
        args = ('foo', 'bar')
        kwargs = {'some': 'args'}

        wrapped_method = handler_method(asyncio.coroutine(method))
        self.loop.run_until_complete(wrapped_method(*args, **kwargs))

        self.assertTrue(getattr(wrapped_method, HANDLER_FLAG))
        method.assert_called_once_with(*args, **kwargs)
