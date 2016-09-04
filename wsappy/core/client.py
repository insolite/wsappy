"""
Client wrapper

"""

import asyncio
import json


class Client:
    """Connection wrapper"""

    def __init__(self, connection):
        """
        Init client

        :param connection: `websockets` connection descriptor
        """
        self.connection = connection

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
        raw_message = json.dumps({'request_id': request_id,
                                  'module': module,
                                  'method': method,
                                  'event': event,
                                  'data': data})
        yield from self.connection.send(raw_message)

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
