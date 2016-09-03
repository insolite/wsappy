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
