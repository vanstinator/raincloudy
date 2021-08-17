"""Define basic data for unittests."""
import imp
import sys

import pytest

# python 2.7 unicode compatibility
try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except NameError:
    pass

import asyncio
import unittest
from mock import patch
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web, ClientSession
from aioresponses import aioresponses

from tests.extras import load_fixture, USERNAME, PASSWORD

from raincloudy.aio.core import RainCloudy
from raincloudy.const import (
    LOGIN_ENDPOINT,
    LOGOUT_ENDPOINT,
    STATUS_ENDPOINT,
    HOME_ENDPOINT,
    SETUP_ENDPOINT,
)

from tests.extras import CONTROLLER_SERIAL


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
        )
        mocked.get(
            LOGIN_ENDPOINT,
            status=200,
            body=load_fixture("home.html"),
            content_type="text/html; charset=UTF-8",
        )
        mocked.get(
            f"{STATUS_ENDPOINT}?controller_serial={CONTROLLER_SERIAL}&faucet_serial=1234",
            status=200,
            body=load_fixture("get_cu_and_fu_status.json"),
        )
        mocked.post(
            LOGIN_ENDPOINT,
            status=200,
            body=load_fixture("home.html"),
            content_type="text/html; charset=UTF-8",
        )
        mocked.get(
            HOME_ENDPOINT,
            status=200,
            body=load_fixture("home.html"),
            content_type="text/html; charset=UTF-8",
        )
        mocked.get(LOGOUT_ENDPOINT, status=200)
        mocked.post(SETUP_ENDPOINT)
