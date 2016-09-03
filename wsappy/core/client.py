import asyncio
import json


class Client:

    def __init__(self, connection):
        self.connection = connection

    @asyncio.coroutine
    def send_message(self, request_id, module, method, event, **data):
        raw_message = json.dumps({'request_id': request_id,
                                  'module': module,
                                  'method': method,
                                  'event': event,
                                  'data': data})
        yield from self.connection.send(raw_message)

    @asyncio.coroutine
    def on_connected(self):
        pass

    @asyncio.coroutine
    def on_disconnected(self):
        pass
