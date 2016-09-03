import traceback
import asyncio
import json

import websockets


class Server():

    def __init__(self, request_factory, client_factories, handlers={}):
        self.request_factory = request_factory
        self.client_factories = client_factories
        self.handlers = handlers
        self.clients = []

    @asyncio.coroutine
    def on_connect(self, connection, path):
        client = self.client_factories[path.strip('/')](connection)
        client.on_connected()
        self.clients.append(client)
        while True:
            try:
                raw_message = yield from connection.recv()
            except websockets.exceptions.ConnectionClosed:
                break
            try:
                message_obj = json.loads(raw_message)
                module_name = message_obj['module']
                handler = self.handlers[module_name]
                method_name = message_obj['method']
                method = getattr(handler, method_name)
                if getattr(method, '_is_handler_method', False):
                    request_id = message_obj.get('request_id')
                    data = message_obj.get('data', {})
                    request = self.request_factory(module_name, method_name,
                                                   message_obj, client,
                                                   request_id)
                    asyncio.async(method(request, **data))
                else:
                    raise PermissionError
            except:
                print(traceback.format_exc()) # TODO: logger
        client.on_disconnected()

    @asyncio.coroutine
    def run(self, host, port, *args, **kwargs):
        server = websockets.serve(self.on_connect, host, port, *args, **kwargs)
        yield from server
