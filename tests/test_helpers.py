# -*- coding: utf-8 -*-
"""Test raincloudy.helpers."""
from tests.test_base import UnitTestBase
from tests.extras import load_fixture
from raincloudy.helpers import generate_soup_html
from raincloudy.exceptions import RainCloudyException


class TestRainCloudyHelpers(UnitTestBase):
    """Unit tests for helpers functions."""

    def test_generate_soup_html(self):
        """Test generate_soup_html method."""
        from bs4 import BeautifulSoup

        self.assertIsInstance(self.rdy.html['home'], BeautifulSoup)
        self.assertRaises(TypeError, generate_soup_html, None)

    def test_serial_finder(self):
        """Test serial finder method."""
        from raincloudy.helpers import serial_finder

        self.assertRaises(TypeError, serial_finder, None)

        broken_html = generate_soup_html(load_fixture('home_broken.html'))
        self.assertRaises(RainCloudyException, serial_finder, broken_html)

    def test_find_controller_or_faucet_name(self):
        """Test find_controller_or_faucet_name method."""
        from raincloudy.helpers import find_controller_or_faucet_name as fcfn

        self.assertRaises(TypeError, fcfn, None, None)
        self.assertRaises(TypeError, fcfn, self.rdy.html['home'], None)

        # test when controller is not found
        broken_html = generate_soup_html(load_fixture('home_broken.html'))
        self.assertIsNone(fcfn(broken_html, 'controller'))

    def test_find_zone_name(self):
        """test find_zone_name method."""
        from raincloudy.helpers import find_zone_name

        self.assertRaises(TypeError, find_zone_name, None, 1)

        # test when zone name is not found
        broken_html = generate_soup_html(load_fixture('home_broken.html'))
        self.assertIsNone(find_zone_name(broken_html, 1))
