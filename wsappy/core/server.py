"""
Basic Server

"""

import asyncio
import json

import websockets

from .utils import HANDLER_FLAG


class Server:
    """Server"""

    def __init__(self, request_factory, client_factories, handlers):
        """Init server"""
        self.request_factory = request_factory
        self.client_factories = client_factories
        self.handlers = handlers

    @asyncio.coroutine
    def process_message(self, raw_message, client):
        """
        Process incoming raw text message

        Load JSON object, create Request, find Handler and pass request to it.

        :param raw_message: Valid JSON string
        :param client: Client
        """
        message_obj = json.loads(raw_message)
        module_name = message_obj['module']
        handler = self.handlers[module_name]
        method_name = message_obj['method']
        method = getattr(handler, method_name)
        if getattr(method, HANDLER_FLAG, False):
            request_id = message_obj.get('request_id')
            data = message_obj.get('data', {})
            request = self.request_factory(module_name, method_name, data,
                                           client, request_id)
            yield from method(request, **data)
        else:
            raise PermissionError

    @asyncio.coroutine
    def on_connect(self, connection, path):
        """
        Handle connection open/close and websocket messages

        Called by :mod:`websockets` module
        Create Client and call connect/disconnect hooks. On each message call
        :meth:`process_message`.

        :param connection: Instance of :class:`websockets.WebSocketServerProtocol`
        :param path: URI
        """
        client = self.client_factories[path.strip('/')](connection)
        yield from client.on_connected()
        while True:
            try:
                raw_message = yield from connection.recv()
            except websockets.exceptions.ConnectionClosed:
                break
            asyncio.async(self.process_message(raw_message, client))
        yield from client.on_disconnected()

    @asyncio.coroutine
    def run(self, host, port, *args, **kwargs):
        """
        Create server and exit

        :param host: Listen host
        :param port: Listen port
        :param args: args to :func:`websockets.serve`
        :param kwargs: kwargs to :func:`websockets.serve`
        """
        server = websockets.serve(self.on_connect, host, port, *args, **kwargs)
        yield from server
