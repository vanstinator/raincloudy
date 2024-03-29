# -*- coding: utf-8 -*-
"""Test raincloudy.helpers."""
from raincloudy.exceptions import RainCloudyException
from raincloudy.helpers import generate_soup_html
from tests.extras import load_fixture
from tests.test_base import UnitTestBase


class TestRainCloudyHelpers(UnitTestBase):
    """Unit tests for helpers functions."""

    def test_generate_soup_html(self):
        """Test generate_soup_html method."""
        from bs4 import BeautifulSoup

        self.assertIsInstance(self.rdy.html["home"], BeautifulSoup)
        self.assertRaises(TypeError, generate_soup_html, None)

    def test_serial_finder(self):
        """Test serial finder method."""
        from raincloudy.helpers import faucet_serial_finder

        self.assertRaises(TypeError, faucet_serial_finder, None)

        broken_html = generate_soup_html(load_fixture("home_broken.html"))
        self.assertRaises(RainCloudyException, faucet_serial_finder, broken_html)

    def test_find_controller_or_faucet_name(self):
        """Test find_controller_or_faucet_name method."""
        from raincloudy.helpers import find_controller_or_faucet_name as fcfn

        self.assertRaises(TypeError, fcfn, None, None)
        self.assertRaises(TypeError, fcfn, self.rdy.html["home"], None)

        # test when controller is not found
        broken_html = generate_soup_html(load_fixture("home_broken.html"))
        self.assertIsNone(fcfn(broken_html, "controller"))

    def test_find_zone_name(self):
        """test find_zone_name method."""
        from raincloudy.helpers import find_zone_names

        self.assertRaises(TypeError, find_zone_names, None, 1)

        # test when zone name is not found
        broken_html = generate_soup_html(load_fixture("home_broken.html"))
        self.assertEquals(find_zone_names(broken_html), ["1", "2", "3", "4"])
