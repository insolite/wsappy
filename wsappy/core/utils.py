import asyncio


HANDLER_FLAG = '_is_handler_method'


def handler_method(func):
    @asyncio.coroutine
    def wrapped(*args, **kwargs):
        return (yield from func(*args, **kwargs))
    setattr(wrapped, HANDLER_FLAG, True)
    return wrapped
