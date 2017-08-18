# -*- coding: utf-8 -*-
"""Test raincloudy.faucet."""
from tests.test_base import UnitTestBase
from tests.extras import FAUCET_NAME, FAUCET_SERIAL


class TestRainCloudyFaucet(UnitTestBase):
    """Unit tests for faucet attributes."""

    def test_attributes(self):
        """Test faucet.attributes."""
        faucet = self.rdy.controller.faucet

        self.assertTrue(hasattr(faucet, 'battery'))
        self.assertTrue(hasattr(faucet, 'id'))
        self.assertTrue(hasattr(faucet, 'name'))
        self.assertTrue(hasattr(faucet, 'serial'))
        self.assertTrue(hasattr(faucet, 'status'))
        self.assertTrue(hasattr(faucet, 'update'))

        # check zone attributes
        ZONE_ATTRS = [
            'zone{}',
            'zone{}_auto_watering',
            'zone{}_droplet',
            'zone{}_is_watering',
            'zone{}_name',
            'zone{}_next_cycle',
            'zone{}_rain_delay',
            'zone{}_watering_time',
        ]

        for zone_id in range(1, 5):
            for zone_attr in ZONE_ATTRS:
                zone_attr = zone_attr.format(zone_id)
                self.assertTrue(hasattr(faucet, zone_attr))

        objname = "<RainCloudyFaucet: {}>".format(FAUCET_NAME)
        self.assertEquals(faucet.__repr__(), objname)

        self.assertEquals(faucet.id, FAUCET_SERIAL)
        self.assertEquals(faucet.name, FAUCET_NAME)
        self.assertEquals(faucet.status, 'Online')

        self.assertEquals(faucet.zone1_auto_watering, False)
        self.assertEquals(faucet.zone1_watering_time, 0)
        self.assertEquals(faucet.zone4_rain_delay, 4)

    def test_set_rain_delay(self):
        """Test faucet._set_rain_delay method."""
        faucet = self.rdy.controller.faucet

        # test if a non-valid parameter is passed
        for zone_id in range(1, 5):
            self.assertIsNone(faucet._set_rain_delay(zone_id, 'foorbar'))
            self.assertIsNone(faucet._set_rain_delay(zone_id, 100))

    def test_set_auto_watering(self):
        """Test faucet._set_auto_watering method."""
        faucet = self.rdy.controller.faucet

        # test if a non-valid parameter is passed
        for zone_id in range(1, 5):
            self.assertIsNone(faucet._set_auto_watering(zone_id, 'foobar'))

    def test_zones(self):
        """test faucet.zones attribute."""
        faucet = self.rdy.controller.faucet

        zones = faucet.zones
        self.assertIsInstance(zones, dict)
        self.assertIsInstance(zones['zone1'], dict)

    def test_errors_or_exceptions(self):
        """Tests for errors or exceptions."""
        faucet = self.rdy.controller.faucet

        # if name attribute fails, displays id
        faucet._parent = None
        objname = "<RainCloudyFaucet: {}>".format(FAUCET_SERIAL)
        self.assertEquals(faucet.__repr__(), objname)


# vim:sw=4:ts=4:et:
