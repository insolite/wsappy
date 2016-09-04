"""
Helper functions

"""

import asyncio


HANDLER_FLAG = '_is_handler_method'


def handler_method(func):
    """
    Wrap Handler method so that can be called by :meth:`Server.process_message`

    :param func: Source method
    :return: Wrapped method
    """
    @asyncio.coroutine
    def wrapped(*args, **kwargs):
        return (yield from func(*args, **kwargs))
    setattr(wrapped, HANDLER_FLAG, True)
    return wrapped
