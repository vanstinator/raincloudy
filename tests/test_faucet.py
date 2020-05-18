# -*- coding: utf-8 -*-
"""Test raincloudy.faucet."""
from tests.test_base import UnitTestBase
from tests.extras import FAUCET_NAME, FAUCET_SERIAL


class TestRainCloudyFaucet(UnitTestBase):
    """Unit tests for faucet attributes."""

    def test_attributes(self):
        """Test faucet.attributes."""
        from raincloudy.faucet import RainCloudyFaucetZone
        faucet = self.rdy.controllers[0].faucets[0]

        self.assertTrue(hasattr(faucet, 'battery'))
        self.assertTrue(hasattr(faucet, 'id'))
        self.assertTrue(hasattr(faucet, 'name'))
        self.assertTrue(hasattr(faucet, 'serial'))
        self.assertTrue(hasattr(faucet, 'status'))
        self.assertTrue(hasattr(faucet, 'update'))

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
        self.assertEquals(faucet.status, 'Online')

    def test_zones(self):
        """test faucet.zones attribute."""
        from raincloudy.faucet import RainCloudyFaucetZone
        faucet = self.rdy.controllers[0].faucets[0]

        zones = faucet.zones
        self.assertIsInstance(zones, list)
        self.assertIsInstance(zones[0], RainCloudyFaucetZone)

    def test_errors_or_exceptions(self):
        """Tests for errors or exceptions."""
        faucet = self.rdy.controllers[0].faucets[0]

        # if name attribute fails, displays id
        faucet._parent = None
        objname = "<RainCloudyFaucet: {}>".format(FAUCET_SERIAL)
        self.assertEquals(faucet.__repr__(), objname)

# vim:sw=4:ts=4:et:
