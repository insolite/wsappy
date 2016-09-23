"""
Client wrapper

"""

import asyncio

from .utils import HANDLER_FLAG


class Client:
    """Connection wrapper"""

    def __init__(self, server, connection, handlers):
        """
        Init client

        :param connection: `websockets` connection descriptor
        :param handlers: Handler configuration
        """
        self.server = server
        self.connection = connection
        self.handlers = handlers

    @asyncio.coroutine
    def send_message(self, request_id, module, method, event, **data):
        """
        Send message to client

        :param request_id: Request ID
        :param module: Module
        :param method: Method
        :param event: Event
        :param data: Data
        """
        yield from self.server.send_message({'request_id': request_id,
                                             'module': module,
                                             'method': method,
                                             'event': event,
                                             'data': data}, self)

    @asyncio.coroutine
    def process_message(self, request):
        """
        Process request

        :param request: Request
        :raises: PermissionError
        """
        handler = self.handlers[request.module]
        method = getattr(handler, request.method)
        if getattr(method, HANDLER_FLAG, False):
            yield from method(request, **request.data)
        else:
            raise PermissionError

    @asyncio.coroutine
    def on_connected(self):
        """
        Connection open hook

        """
        pass

    @asyncio.coroutine
    def on_disconnected(self):
        """
        Connection close hook

        """
        pass
