"""
Basic Server

"""

import asyncio
import json

import websockets


class Server:
    """Server"""

    def __init__(self, request_factory, client_factories,
                 json_encoder=json.JSONEncoder,
                 json_decoder=json.JSONDecoder):
        """
        Init server

        :param request_factory: Request class
        :param client_factories: Router configuration
        :param json_encoder: JSONEncoder
        :param json_decoder: JSONDecoder
        """
        self.request_factory = request_factory
        self.client_factories = client_factories
        self.json_encoder = json_encoder
        self.json_decoder = json_decoder

    @asyncio.coroutine
    def process_message(self, raw_message, client):
        """
        Process incoming raw text message

        Load JSON object, create Request, find Handler and pass request to it.

        :param raw_message: Valid JSON string
        :param client: Client
        """
        message_obj = json.loads(raw_message, cls=self.json_decoder)
        module_name = message_obj['module']
        method_name = message_obj['method']
        data = message_obj.get('data', {})
        request_id = message_obj.get('request_id')
        request = self.request_factory(module_name, method_name, data,
                                       client, request_id)
        yield from client.process_message(request)

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
        client_name = path.split('?', 1)[0].strip('/')
        client_factory, handlers = self.client_factories[client_name]
        client = client_factory(self, connection, handlers)
        yield from client.on_connected()
        while True:
            try:
                raw_message = yield from connection.recv()
            except websockets.exceptions.ConnectionClosed:
                break
            asyncio.async(self.process_message(raw_message, client))
        yield from client.on_disconnected()

    @asyncio.coroutine
    def send_message(self, data, client):
        """
        Send message to client's connection

        :param data: Data
        :param client: Client
        """
        message = json.dumps(data, cls=self.json_encoder)
        yield from client.connection.send(message)

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
