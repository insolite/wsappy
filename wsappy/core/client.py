import asyncio
import json


class Client():

    def __init__(self, connection):
        self.connection = connection

    @asyncio.coroutine
    def send_message(self, request_id, module, event, **data):
        raw_message = json.dumps({'request_id': request_id,
                                  'module': module,
                                  'event': event,
                                  'data': data})
        yield from self.connection.send(raw_message)

    def on_connected(self):
        pass

    def on_disconnected(self):
        pass