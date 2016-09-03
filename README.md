# WsAppy

## A bit more higher level of asyncio websocket server

## Overview

**wsappy** provides base classes for creating websocket API server using request handlers and client routes.

## Usage example

Server:
```python
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
```

Client:
```python
import asyncio
import json

import websockets


@asyncio.coroutine
def main():
    connection = yield from websockets.connect('ws://localhost:8008/api')
    request_id = 1
    item_ids = (42, 15, 30)
    items = {}
    for item_id in item_ids:
        request_text = json.dumps({'module': 'entity',
                                   'method': 'get',
                                   'data': {
                                       'item_id': item_id,
                                   },
                                   'request_id': request_id})
        print('-->', request_text)
        yield from connection.send(request_text)
        response_text = yield from connection.recv()
        print('<--', response_text)
        response = json.loads(response_text)
        response_items = response['data']['items']
        if response_items:
            items[item_id] = response_items[0]
        request_id += 1
    yield from connection.close()
    print('items', items)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

```bash
python3 server.py
```

```bash
python3 client.py
```

...on client will result in:

```
--> {"method": "get", "module": "entity", "data": {"item_id": 42}, "request_id": 1}
<-- {"request_id": 1, "event": "result", "module": "entity", "data": {"items": [{"id": 42, "name": "a"}]}}
--> {"method": "get", "module": "entity", "data": {"item_id": 15}, "request_id": 1}
<-- {"request_id": 1, "event": "result", "module": "entity", "data": {"items": [{"id": 15, "name": "b"}]}}
--> {"method": "get", "module": "entity", "data": {"item_id": 30}, "request_id": 1}
<-- {"request_id": 1, "event": "result", "module": "entity", "data": {"items": [{"id": 30, "name": "c"}]}}
items {42: {'name': 'a', 'id': 42}, 30: {'name': 'c', 'id': 30}, 15: {'name': 'b', 'id': 15}}
```

See examples/simple for details

## Features

 * **Clients** - creating custom clients for URL routing
 * **Handlers** - creating custom handlers for handling separate modules/methods

## Run tests

```bash
python3 -m unittest discover tests
```

## TODO

* More complex URL routing
