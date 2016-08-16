import asyncio


def handler_method(func):
    @asyncio.coroutine
    def wrapped(*args, **kwargs):
        return (yield from func(*args, **kwargs))
    wrapped._is_handler_method = True
    return wrapped