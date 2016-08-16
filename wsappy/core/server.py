import traceback
import asyncio
import json

import websockets


class Server():

    def __init__(self, client_factories, handlers={}):
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
                handler = self.handlers[message_obj['module']]
                method = getattr(handler, message_obj['method'])
                request_id = message_obj.get('request_id')
                if getattr(method, '_is_handler_method', False):
                    asyncio.async(method(client, request_id, **message_obj.get('data', {})))
                else:
                    raise PermissionError
            except:
                print(traceback.format_exc()) # TODO: logger
        client.on_disconnected()

    @asyncio.coroutine
    def run(self, host, port):
        server = websockets.serve(self.on_connect, host, port)
        yield from server
