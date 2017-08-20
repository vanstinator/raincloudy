# -*- coding: utf-8 -*-
"""Test raincloudy.faucet.zone."""
from tests.test_base import UnitTestBase


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

        self.assertEquals(faucet.zone1.auto_watering, False)
        self.assertEquals(faucet.zone1.watering_time, 0)
        self.assertEquals(faucet.zone4.rain_delay, 4)

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


# vim:sw=4:ts=4:et:
