# -*- coding:utf-8 -*-
"""Define basic data for unittests."""
import sys

# python 2.7 unicode compatibility
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass

import unittest
import requests_mock

from tests.helpers import load_fixture, CSRFTOKEN, USERNAME, PASSWORD

from raincloudy.const import LOGIN_ENDPOINT, DAJAXICE_ENDPOINT, HOME_ENDPOINT


class UnitTestBase(unittest.TestCase):
    """Top level test class for RainCloudy Core."""

    @requests_mock.Mocker()
    def setUp(self, mock):
        """Initialize rdy object for unittests."""
        from raincloudy.core import RainCloudy

        mock.get(LOGIN_ENDPOINT,
                 text=load_fixture('home.html'))
        mock.post(LOGIN_ENDPOINT,
                  text=load_fixture('home.html'))
        mock.post(DAJAXICE_ENDPOINT,
                  text=load_fixture('get_cu_and_fu_status.json'))
        mock.get(HOME_ENDPOINT,
                 text=load_fixture('home.html'))

        # initialize self.rdy object
        self.rdy = RainCloudy(USERNAME, PASSWORD)

        # mock CSRF token
        self.rdy.client.cookies['csrftoken'] = CSRFTOKEN

    def cleanUp(self):
        """Cleanup any data created from the tests."""
        self.rdy = None

    def tearDown(self):
        """Stop everything initialized."""
        self.cleanUp()
