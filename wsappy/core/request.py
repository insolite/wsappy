import asyncio


class Request:

    def __init__(self, module, method, data, client, id):
        self.module = module
        self.method = method
        self.data = data
        self.client = client
        self.id = id

    @asyncio.coroutine
    def response(self, event, **data):
        yield from self.client.send_message(self.id, self.module, self.method,
                                            event, **data)
