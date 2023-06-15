# -*- coding: utf-8 -*-
"""Test raincloudy.core."""
from tests.extras import CONTROLLER_SERIAL
from tests.test_base import UnitTestBase


class TestRainCloudyCore(UnitTestBase):
    """Unit tests for core attributes."""

    def test_client_attrs(self):
        """Test client (requests.Session) attributes."""
        import requests

        self.assertIsInstance(self.rdy.client, requests.Session)
        self.assertListEqual(list(self.rdy.client.proxies.values()), [None, None])
        self.assertTrue(self.rdy.client.verify)
        self.assertTrue(self.rdy.client.stream)
        self.assertEqual(self.rdy.is_connected, True)

    # def test_errors_or_exceptions(self):
    #     """Tests for errors or exceptions."""

    def test_attributes(self):
        """Test core attributes."""
        from bs4 import BeautifulSoup

        from raincloudy.controller import RainCloudyController

        self.assertTrue(hasattr(self.rdy, "client"))
        self.assertTrue(hasattr(self.rdy, "controllers"))
        self.assertTrue(hasattr(self.rdy, "controllers"))
        self.assertTrue(hasattr(self.rdy, "csrftoken"))
        self.assertTrue(hasattr(self.rdy, "html"))
        self.assertTrue(hasattr(self.rdy, "login"))
        self.assertTrue(hasattr(self.rdy, "logout"))
        self.assertTrue(hasattr(self.rdy, "update"))

        objname = "<RainCloudy: {}>".format(CONTROLLER_SERIAL)
        self.assertEquals(self.rdy.__repr__(), objname)

        self.assertEqual(2, len(self.rdy.controllers))
        self.assertIsInstance(self.rdy.controllers[0], RainCloudyController)

        self.assertIsInstance(self.rdy.html["home"], BeautifulSoup)
        self.assertIsInstance(self.rdy.html["setup"], BeautifulSoup)
        self.assertIsNone(self.rdy.html["program"])
        self.assertIsNone(self.rdy.html["manage"])

        self.assertIsNone(self.rdy.logout())


# vim:sw=4:ts=4:et:
