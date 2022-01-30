# -*- coding: utf-8 -*-
"""Test raincloudy.core."""
from aioresponses import aioresponses
from aiohttp import ClientSession
from tests.test_base_aio import UnitTestBaseAsync
from tests.extras import CONTROLLER_SERIAL


class TestRainCloudyCoreAsync(UnitTestBaseAsync):
    """Unit tests for core attributes."""

    @aioresponses()
    async def test_client_attrs(self, mocked):
        """Test client (requests.Session) attributes."""

        self.add_methods(mocked)
        await self.rdy.login()

        self.assertIsInstance(self.rdy.client, ClientSession)
        self.assertEqual(self.rdy.is_connected, True)

    @aioresponses()
    async def test_login(self, mocked):
        """Test login."""
        from raincloudy.aio.controller import RainCloudyController
        from bs4 import BeautifulSoup

        self.add_methods(mocked)
        await self.rdy.login()
        self.assertTrue(hasattr(self.rdy, "client"))
        self.assertTrue(hasattr(self.rdy, "controllers"))
        self.assertTrue(hasattr(self.rdy, "controllers"))
        self.assertTrue(hasattr(self.rdy, "csrftoken"))
        self.assertTrue(hasattr(self.rdy, "html"))
        self.assertTrue(hasattr(self.rdy, "login"))
        self.assertTrue(hasattr(self.rdy, "logout"))
        self.assertTrue(hasattr(self.rdy, "update"))

        objname = "<RainCloudy: {}>".format(CONTROLLER_SERIAL)
        self.assertEquals(self.rdy.__repr__(), objname)

        self.assertEqual(1, len(self.rdy.controllers))
        self.assertIsInstance(self.rdy.controllers[0], RainCloudyController)

        self.assertIsInstance(self.rdy.html["home"], BeautifulSoup)
        self.assertIsInstance(self.rdy.html["setup"], BeautifulSoup)
        self.assertIsNone(self.rdy.html["program"])
        self.assertIsNone(self.rdy.html["manage"])

        self.assertIsNone(await self.rdy.logout())
