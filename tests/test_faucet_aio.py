# -*- coding: utf-8 -*-
"""Test raincloudy.faucet."""
from aiohttp import ClientSession
from aioresponses import aioresponses

from tests.extras import FAUCET_NAME, FAUCET_SERIAL
from tests.test_base_aio import UnitTestBaseAsync


class TestRainCloudyFaucetAsync(UnitTestBaseAsync):
    """Unit tests for faucet attributes."""

    @aioresponses()
    async def test_attributes(self, mocked):
        """Test faucet.attributes."""
        from raincloudy.aio.faucet import RainCloudyFaucetZone

        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        self.assertTrue(hasattr(faucet, "battery"))
        self.assertTrue(hasattr(faucet, "id"))
        self.assertTrue(hasattr(faucet, "name"))
        self.assertTrue(hasattr(faucet, "serial"))
        self.assertTrue(hasattr(faucet, "status"))
        self.assertTrue(hasattr(faucet, "update"))

        # check zone attributes
        for zone_id in range(1, 5):
            zone_attr = "zone{}".format(zone_id)
            self.assertTrue(hasattr(faucet, zone_attr))

            # make sure zoneX return a RainCloudyFaucetZone obj
            zone_obj = getattr(faucet, zone_attr)
            self.assertIsInstance(zone_obj, RainCloudyFaucetZone)

        objname = "<RainCloudyFaucet: {}>".format(FAUCET_NAME)
        self.assertEquals(faucet.__repr__(), objname)

        self.assertEquals(faucet.id, FAUCET_SERIAL)
        self.assertEquals(faucet.name, FAUCET_NAME)
        self.assertEquals(faucet.status, "Online")

    @aioresponses()
    async def test_zones(self, mocked):
        """test faucet.zones attribute."""
        from raincloudy.aio.faucet import RainCloudyFaucetZone

        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        zones = faucet.zones
        self.assertIsInstance(zones, list)
        self.assertIsInstance(zones[0], RainCloudyFaucetZone)

    @aioresponses()
    async def test_errors_or_exceptions(self, mocked):
        """Tests for errors or exceptions."""
        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        # if name attribute fails, displays id
        faucet._controller = None
        objname = "<RainCloudyFaucet: {}>".format(FAUCET_SERIAL)
        self.assertEquals(faucet.__repr__(), objname)
