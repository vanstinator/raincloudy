# -*- coding: utf-8 -*-
"""Test raincloudyfaucet.zone post."""
import requests_mock

from raincloudy.const import HOME_ENDPOINT, SETUP_ENDPOINT, STATUS_ENDPOINT
from tests.extras import load_fixture
from tests.test_base import UnitTestBase


class TestRainCloudyFaucetZone(UnitTestBase):
    """Unit tests for faucet attributes."""

    @requests_mock.Mocker()
    def test_post_actions(self, mock):
        """Test post actions."""
        mock.get(STATUS_ENDPOINT, text=load_fixture("get_cu_and_fu_status.json"))
        mock.get(HOME_ENDPOINT, text=load_fixture("home.html"))
        mock.post(SETUP_ENDPOINT)
        mock.post(HOME_ENDPOINT, text=load_fixture("home.html"))

        zone = self.rdy.controllers[0].faucets[0].zone1
        zone.update()

        self.assertIsNone(setattr(zone, "name", "test"))

        self.assertIsNone(setattr(zone, "manual_watering", 0))
        self.assertIsNone(setattr(zone, "manual_watering", "on"))

        self.assertIsNone(setattr(zone, "rain_delay", 0))
        self.assertIsNone(setattr(zone, "rain_delay", 1))
        self.assertIsNone(setattr(zone, "rain_delay", 2))

        self.assertIsNone(setattr(zone, "auto_watering", False))


# vim:sw=4:ts=4:et:
