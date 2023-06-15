"""Define basic data for unittests."""
import re
import unittest

from aiohttp import ClientSession
from aioresponses import aioresponses

from raincloudy.aio.core import RainCloudy
from raincloudy.const import (
    HOME_ENDPOINT,
    LOGIN_ENDPOINT,
    LOGOUT_ENDPOINT,
    SETUP_ENDPOINT,
    STATUS_ENDPOINT,
)
from tests.extras import PASSWORD, USERNAME, load_fixture


class UnitTestBaseAsync(unittest.IsolatedAsyncioTestCase):
    """Top level test class for RainCloudy Core."""

    async def asyncSetUp(self):
        """Set up the test."""
        self.session = ClientSession()
        self.rdy = RainCloudy(USERNAME, PASSWORD, self.session)

    async def asyncTearDown(self):
        await self.session.close()
        self.rdy = None

    def add_methods(self, mocked: aioresponses):
        mocked.get(
            SETUP_ENDPOINT,
            status=200,
            body=load_fixture("setup.html"),
            content_type="text/html; charset=UTF-8",
            repeat=True,
        )
        mocked.get(
            LOGIN_ENDPOINT,
            status=200,
            body=load_fixture("home.html"),
            content_type="text/html; charset=UTF-8",
            repeat=True,
        )
        mocked.get(
            re.compile(rf"^{STATUS_ENDPOINT}*"),
            status=200,
            repeat=True,
            body=load_fixture("get_cu_and_fu_status.json"),
        )
        mocked.post(
            LOGIN_ENDPOINT,
            status=200,
            repeat=True,
            body=load_fixture("home.html"),
            content_type="text/html; charset=UTF-8",
        )
        mocked.get(
            HOME_ENDPOINT,
            status=200,
            repeat=True,
            body=load_fixture("home.html"),
            content_type="text/html; charset=UTF-8",
        )
        mocked.get(LOGOUT_ENDPOINT, repeat=True, status=200)
        mocked.post(
            SETUP_ENDPOINT,
            status=200,
            repeat=True,
            headers={"Referer": SETUP_ENDPOINT},
            body=load_fixture("setup.html"),
            content_type="text/html; charset=UTF-8",
        )
