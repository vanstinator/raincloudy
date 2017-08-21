# -*- coding: utf-8 -*-
"""Test raincloudyfaucet.zone post."""
import requests_mock
from tests.test_base import UnitTestBase
from raincloudy.const import (
    DAJAXICE_ENDPOINT, HOME_ENDPOINT, SETUP_ENDPOINT)
from tests.extras import load_fixture


class TestRainCloudyFaucetZone(UnitTestBase):
    """Unit tests for faucet attributes."""

    @requests_mock.Mocker()
    def test_post_actions(self, mock):
        """Test post actions."""
        mock.post(DAJAXICE_ENDPOINT,
                  text=load_fixture('get_cu_and_fu_status.json'))
        mock.get(HOME_ENDPOINT,
                 text=load_fixture('home.html'))
        mock.post(SETUP_ENDPOINT)
        mock.post(HOME_ENDPOINT,
                  text=load_fixture('home.html'))

        zone = self.rdy.controller.faucet.zone1
        zone.update()

        self.assertIsNone(setattr(zone, 'name', 'test'))

        self.assertIsNone(setattr(zone, 'watering_time', 0))
        self.assertIsNone(setattr(zone, 'watering_time', 'on'))

        self.assertIsNone(setattr(zone, 'rain_delay', 0))
        self.assertIsNone(setattr(zone, 'rain_delay', 1))
        self.assertIsNone(setattr(zone, 'rain_delay', 2))

        self.assertIsNone(setattr(zone, 'auto_watering', False))

# vim:sw=4:ts=4:et:
