import asyncio
from unittest import TestCase


class WsAppyTest(TestCase):

    def setUp(self):
        super().setUp()
        self.loop = asyncio.get_event_loop()
