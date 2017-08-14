# -*- coding: utf-8 -*-
"""Test raincloudy.core."""
from tests.test_base import UnitTestBase
from tests.helpers import CSRFTOKEN


class TestRainCloudyCore(UnitTestBase):
    """Unit tests for core attributes."""

    def test_client_attrs(self):
        """Test client (requests.Session) attributes."""
        import requests
        self.assertIsInstance(self.rdy.client, requests.Session)
        self.assertListEqual(list(self.rdy.client.proxies.values()),
                             [None, None])
        self.assertTrue(self.rdy.client.verify)
        self.assertTrue(self.rdy.client.stream)

    def test_attributes(self):
        """Test core attributes."""
        from raincloudy.controller import RainCloudyController
        from bs4 import BeautifulSoup

        self.assertTrue(hasattr(self.rdy, 'client'))
        self.assertTrue(hasattr(self.rdy, 'controller'))
        self.assertTrue(hasattr(self.rdy, 'controllers'))
        self.assertTrue(hasattr(self.rdy, 'csrftoken'))
        self.assertTrue(hasattr(self.rdy, 'html'))
        self.assertTrue(hasattr(self.rdy, 'login'))
        self.assertTrue(hasattr(self.rdy, 'logout'))
        self.assertTrue(hasattr(self.rdy, 'update'))

        self.assertEqual(self.rdy.csrftoken, CSRFTOKEN)

        self.assertEqual(1, len(self.rdy.controllers))
        self.assertIsInstance(self.rdy.controller, RainCloudyController)

        self.assertIsInstance(self.rdy.html['home'], BeautifulSoup)
        self.assertIsNone(self.rdy.html['setup'])
        self.assertIsNone(self.rdy.html['program'])
        self.assertIsNone(self.rdy.html['manage'])
