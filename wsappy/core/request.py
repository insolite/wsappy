"""
Request descriptor

"""


import asyncio


class Request:
    """Request descriptor"""

    def __init__(self, module, method, data, client, id):
        """Init request"""
        self.module = module
        self.method = method
        self.data = data
        self.client = client
        self.id = id

    @asyncio.coroutine
    def response(self, event, **data):
        """
        Send response for request to client

        :param event: Event
        :param data: Data
        """
        yield from self.client.send_message(self.id, self.module, self.method,
                                            event, **data)
