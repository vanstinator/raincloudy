# -*- coding: utf-8 -*-
"""Test raincloudyfaucet.zone post."""
import requests_mock
from tests.test_base import UnitTestBase
from raincloudy.const import (
    STATUS_ENDPOINT, HOME_ENDPOINT, SETUP_ENDPOINT)
from tests.extras import load_fixture


class TestRainCloudyFaucetZone(UnitTestBase):
    """Unit tests for faucet attributes."""

    @requests_mock.Mocker()
    def test_post_actions(self, mock):
        """Test post actions."""
        mock.get(STATUS_ENDPOINT,
                 text=load_fixture('get_cu_and_fu_status.json'))
        mock.get(HOME_ENDPOINT,
                 text=load_fixture('home.html'))
        mock.post(SETUP_ENDPOINT)
        mock.post(HOME_ENDPOINT,
                  text=load_fixture('home.html'))

        zone = self.rdy.controller.faucet.zone1
        zone.update()

        self.assertIsNone(setattr(zone, 'name', 'test'))

        self.assertIsNone(setattr(zone, 'manual_watering', 0))
        self.assertIsNone(setattr(zone, 'manual_watering', 'on'))

        self.assertIsNone(setattr(zone, 'rain_delay', 0))
        self.assertIsNone(setattr(zone, 'rain_delay', 1))
        self.assertIsNone(setattr(zone, 'rain_delay', 2))

        self.assertIsNone(setattr(zone, 'auto_watering', False))

# vim:sw=4:ts=4:et:
