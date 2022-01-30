# -*- coding: utf-8 -*-
"""Test raincloudy.faucet.zone."""
from aioresponses import aioresponses
from aiohttp import ClientSession
from tests.test_base_aio import UnitTestBaseAsync
from tests.extras import CONTROLLER_TIMESTAMP


class TestRainCloudyFaucetZoneAsync(UnitTestBaseAsync):
    """Unit tests for faucet zone attributes."""

    @aioresponses()
    async def test_attributes(self, mocked):
        """Test zone.attributes."""
        self.add_methods(mocked)
        await self.rdy.login()

        faucet = self.rdy.controllers[0].faucets[0]
        # zones = faucet.zones

        # check zone attributes
        # ZONE_ATTRS = [
        #     'auto_watering',
        #     'manual_watering',
        #     'battery',
        #     'id',
        #     'is_watering',
        #     'name',
        #     'next_cycle',
        #     'rain_delay',
        #     'serial',
        #     'status',
        #     'update',
        #     'watering_time',
        # ]

        # for zone in zones:
        #     for zone_attr in ZONE_ATTRS:
        #         zone_attr = zone_attr.format(zone.id)
        #         self.assertTrue(hasattr(zone, zone_attr))

        # objname = "<RainCloudyFaucetZone: {}>".format('Front Yard')
        # self.assertEquals(faucet.zone1.__repr__(), objname)

        self.assertEquals(faucet.zone1.watering_time, 0)
        self.assertEquals(faucet.zone4.rain_delay, 4)
        self.assertEquals(faucet.zone3.current_time, CONTROLLER_TIMESTAMP)

        self.assertTrue(faucet.zone2.manual_watering)
        self.assertTrue(faucet.zone2.auto_watering)
        self.assertFalse(faucet.zone1.manual_watering)
        self.assertFalse(faucet.zone1.auto_watering)

        self.assertIsInstance(faucet.zone2.report(), dict)

    @aioresponses()
    async def test_set_rain_delay(self, mocked):
        """Test faucet._set_rain_delay method."""
        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        # test if a non-valid parameter is passed
        for zone in faucet.zones:
            self.assertIsNone(await zone.set_rain_delay("foorbar"))
            self.assertIsNone(await zone.set_rain_delay(100))

    @aioresponses()
    async def test_set_auto_watering(self, mocked):
        """Test faucet._set_auto_watering method."""
        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        # test if a non-valid parameter is passed
        for zone in faucet.zones:
            self.assertIsNone(await zone.set_auto_watering("foobar"))

    @aioresponses()
    async def test_set_watering_time(self, mocked):
        """Test faucet._set_watering_time method."""
        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        # verify allowed values
        with self.assertRaises(ValueError):
            await faucet.zone1.set_manual_watering_time(1000)

    @aioresponses()
    async def test_watering_time(self, mocked):
        """Test faucet.watering_time property"""
        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        # manual time
        self.assertEqual(faucet.zone2.watering_time, 15)

        # auto time
        self.assertEqual(faucet.zone3.watering_time, 60)

    @aioresponses()
    async def test_errors_or_exceptions(self, mocked):
        """Tests for errors or exceptions."""
        self.add_methods(mocked)
        await self.rdy.login()
        faucet = self.rdy.controllers[0].faucets[0]

        faucet._parent = None
        # objname = "<RainCloudyFaucetZone: {}>".format('Front Yard')
        # self.assertEquals(faucet.zone1.__repr__(), objname)

        faucet.zones = None
        self.assertIsNone(faucet.zone1)
