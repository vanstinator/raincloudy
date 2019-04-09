# -*- coding: utf-8 -*-
"""Test raincloudy.faucet.zone."""
from tests.test_base import UnitTestBase
from tests.extras import CONTROLLER_TIMESTAMP


class TestRainCloudyFaucetZone(UnitTestBase):
    """Unit tests for faucet zone attributes."""

    def test_attributes(self):
        """Test zone.attributes."""
        faucet = self.rdy.controller.faucet
        zones = faucet.zones

        # check zone attributes
        ZONE_ATTRS = [
            'auto_watering',
            'battery',
            'droplet',
            'id',
            'is_watering',
            'name',
            'next_cycle',
            'rain_delay',
            'serial',
            'status',
            'update',
            'watering_time',
        ]

        for zone in zones:
            for zone_attr in ZONE_ATTRS:
                zone_attr = zone_attr.format(zone.id)
                self.assertTrue(hasattr(zone, zone_attr))

        objname = "<RainCloudyFaucetZone: {}>".format('Front Yard')
        self.assertEquals(faucet.zone1.__repr__(), objname)

        self.assertEquals(faucet.zone1.auto_watering, False)
        self.assertEquals(faucet.zone1.watering_time, 0)
        self.assertEquals(faucet.zone4.rain_delay, 4)
        self.assertEquals(faucet.zone3.current_time, CONTROLLER_TIMESTAMP)

        self.assertIsInstance(faucet.zone2.report(), dict)

    def test_private_methods(self):
        """Test private methods from faucet.py."""
        faucet = self.rdy.controller.faucet

        self.assertIsInstance(faucet.zone2._attributes, dict)

    def test_set_rain_delay(self):
        """Test faucet._set_rain_delay method."""
        faucet = self.rdy.controller.faucet

        # test if a non-valid parameter is passed
        for zone in faucet.zones:
            self.assertIsNone(zone._set_rain_delay(zone.id, 'foorbar'))
            self.assertIsNone(zone._set_rain_delay(zone.id, 100))

    def test_set_auto_watering(self):
        """Test faucet._set_auto_watering method."""
        faucet = self.rdy.controller.faucet

        # test if a non-valid parameter is passed
        for zone in faucet.zones:
            self.assertIsNone(zone._set_auto_watering(zone.id, 'foobar'))

    def test_set_watering_time(self):
        """Test faucet._set_watering_time method."""
        faucet = self.rdy.controller.faucet

        # verify allowed values
        self.assertRaises(ValueError,
                          faucet.zone1._set_watering_time,
                          faucet.zone1.id,
                          1000)

    def test_watering_time(self):
        """Test faucet.watering_time property"""
        faucet = self.rdy.controller.faucet

        # manual time
        self.assertEqual(faucet.zone2.watering_time, 15)

        # auto time
        self.assertEqual(faucet.zone3.watering_time, 60)


    def test_errors_or_exceptions(self):
        """Tests for errors or exceptions."""
        faucet = self.rdy.controller.faucet

        faucet._parent = None
        objname = "<RainCloudyFaucetZone: {}>".format('Front Yard')
        self.assertEquals(faucet.zone1.__repr__(), objname)

        faucet.zones = None
        self.assertIsNone(faucet.zone1)

# vim:sw=4:ts=4:et:
