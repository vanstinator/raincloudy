# -*- coding: utf-8 -*-
"""Test raincloudy.controller post."""
import requests_mock

from raincloudy.const import HOME_ENDPOINT, SETUP_ENDPOINT, STATUS_ENDPOINT
from tests.extras import load_fixture
from tests.test_base import UnitTestBase


class TestRainCloudyController(UnitTestBase):
    """Unit tests for controller attributes."""

    @requests_mock.Mocker()
    def test_request_actions(self, mock):
        """Test post actions."""
        mock.get(STATUS_ENDPOINT, text=load_fixture("get_cu_and_fu_status.json"))
        mock.get(HOME_ENDPOINT, text=load_fixture("home.html"))
        mock.post(SETUP_ENDPOINT)
        mock.get(SETUP_ENDPOINT)

        controller = self.rdy.controllers[0]
        controller.update()
        self.assertIsNone(setattr(controller, "name", "test"))


# vim:sw=4:ts=4:et:
