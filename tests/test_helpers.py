# -*- coding: utf-8 -*-
"""Test raincloudy.helpers."""
from tests.test_base import UnitTestBase
from tests.extras import load_fixture


class TestRainCloudyHelpers(UnitTestBase):
    """Unit tests for helpers functions."""

    def test_generate_soup_html(self):
        """Test generate_soup_html method."""
        from bs4 import BeautifulSoup
        from raincloudy.helpers import generate_soup_html

        self.assertIsInstance(self.rdy.html['home'], BeautifulSoup)
        self.assertRaises(TypeError, generate_soup_html, None)

    def test_serial_finder(self):
        """Test serial finder method."""
        from raincloudy.helpers import generate_soup_html, serial_finder
        from raincloudy.exceptions import RaincloudyException

        self.assertRaises(TypeError, serial_finder, None)

        doc = generate_soup_html(load_fixture('home_no_serial.html'))
        self.assertRaises(RaincloudyException, serial_finder, doc)

    def test_find_attr(self):
        """Test find_attr method."""
        from raincloudy.helpers import find_attr

        self.assertRaises(TypeError, find_attr, None, None)

    def test_find_program_status(self):
        """Test find_program_status method."""
        from raincloudy.helpers import find_program_status

        self.assertRaises(TypeError, find_program_status, None, None)

    def test_find_controller_or_faucet_name(self):
        """Test find_controller_or_faucet_name method."""
        from raincloudy.helpers import find_controller_or_faucet_name as fcfn

        self.assertRaises(TypeError, fcfn, None, None)
        self.assertRaises(TypeError, fcfn, self.rdy.html['home'], None)

    def test_find_zone_name(self):
        """test find_zone_name method."""
        from raincloudy.helpers import find_zone_name

        self.assertRaises(TypeError, find_zone_name, None, 1)
