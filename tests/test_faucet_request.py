# -*- coding: utf-8 -*-
"""Test raincloudy.faucet post."""
import requests_mock

from raincloudy.const import HOME_ENDPOINT, SETUP_ENDPOINT, STATUS_ENDPOINT
from tests.extras import load_fixture
from tests.test_base import UnitTestBase


class TestRainCloudyFaucet(UnitTestBase):
    """Unit tests for faucet attributes."""

    @requests_mock.Mocker()
    def test_post_actions(self, mock):
        """Test request actions."""
        mock.get(STATUS_ENDPOINT, text=load_fixture("get_cu_and_fu_status.json"))
        mock.get(HOME_ENDPOINT, text=load_fixture("home.html"))
        mock.post(SETUP_ENDPOINT)
        mock.get(SETUP_ENDPOINT)

        faucet = self.rdy.controllers[0].faucets[0]
        self.assertIsNone(setattr(faucet, "name", "test"))
        faucet.update()


# vim:sw=4:ts=4:et:
