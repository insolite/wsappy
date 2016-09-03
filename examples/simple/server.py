import asyncio

from wsappy import Server, Client, Handler, handler_method, Request


class EntityHandler(Handler):

    def __init__(self):
        super().__init__()
        self.data = [{'id': 42, 'name': 'a'},
                     {'id': 15, 'name': 'b'},
                     {'id': 30, 'name': 'c'}]

    @handler_method
    def get(self, request, item_id):
        items = list(filter(lambda x: x['id'] == item_id, self.data))
        yield from request.response('result', items=items)


def main():
    client_factories = {'api': Client}
    handlers = {'entity': EntityHandler()}
    server = Server(Request, client_factories, handlers)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.run('localhost', 8008))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
