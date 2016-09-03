import asyncio


class Handler:

    def get_module_name(self):
        return self.__class__.__name__.rsplit(Handler.__name__, 1)[0].lower()

    @asyncio.coroutine
    def send_message(self, client, request_id, event, **data):
        yield from client.send_message(request_id, self.get_module_name(),
                                       event, **data)
