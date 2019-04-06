# -*- coding: utf-8 -*-
"""Test raincloudy.core."""
from tests.test_base import UnitTestBase
from tests.extras import CONTROLLER_SERIAL


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
        self.assertEqual(self.rdy.is_connected, True)

    def test_errors_or_exceptions(self):
        """Tests for errors or exceptions."""

        # check if has more than 1 controller
        self.rdy.controllers.append(1)
        self.assertRaises(TypeError, getattr, self.rdy, 'controller')

        # check if controllers does not exist
        delattr(self.rdy, 'controllers')
        self.assertRaises(AttributeError, getattr, self.rdy, 'controller')

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

        objname = "<RainCloudy: {}>".format(CONTROLLER_SERIAL)
        self.assertEquals(self.rdy.__repr__(), objname)

        self.assertEqual(1, len(self.rdy.controllers))
        self.assertIsInstance(self.rdy.controller, RainCloudyController)

        self.assertIsInstance(self.rdy.html['home'], BeautifulSoup)
        self.assertIsInstance(self.rdy.html['setup'], BeautifulSoup)
        self.assertIsNone(self.rdy.html['program'])
        self.assertIsNone(self.rdy.html['manage'])

        self.assertIsNone(self.rdy.logout())

# vim:sw=4:ts=4:et:
