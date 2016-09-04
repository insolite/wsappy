"""
Request handler

"""


import asyncio


class Handler:
    """Request handler"""

    def get_module_name(self):
        """
        Get module name

        :return: Module name
        :rtype: str
        """
        return self.__class__.__name__.rsplit(Handler.__name__, 1)[0].lower()

    @asyncio.coroutine
    def send_message(self, client, request_id, event, **data):
        """
        Send message to client

        :param client: Client
        :param request_id: Request ID
        :param event: Event
        :param data: Data
        """
        yield from client.send_message(request_id, self.get_module_name(),
                                       event, **data)
