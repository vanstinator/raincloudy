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

# vim:sw=4:ts=4:et:
