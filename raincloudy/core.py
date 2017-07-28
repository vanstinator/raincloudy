# -*- coding: utf-8 -*-
"""RainCloud."""
import requests
import urllib3
from .const import (
    INITIAL_DATA, DAJAXICE_ENDPOINT, HEADERS, LOGIN_ENDPOINT)
from .helpers import serial_finder


class RainCloudy(object):
    """RainCloudy object."""

    def __init__(self, username, password, http_proxy=None, https_proxy=None,
                 ssl_warnings=False):
        """
        Initialize RainCloud object.

        :param str username: username to authenticate user
        :param str passwrod: password to authenticate user
        :param str http_proxy: HTTP proxy information (127.0.0.1:8080)
        :param str https_proxy: HTTPs proxy information (127.0.0.1:8080)
        :param bol ssl_warnings: Show SSL warnings. Defaults to False
        """
        if not ssl_warnings:
            urllib3.disable_warnings()

        # define credentials
        self._username = username
        self._password = password

        # initialize future attributes
        self._attributes = None
        self._devices = []
        self.client = None

        # set proxy environment
        self._proxies = {
            "http": http_proxy,
            "https": https_proxy,
        }

        # login
        self.login()

    def __repr__(self):
        """Object representation."""
        return "<{0}: {1}>".format(self.__class__.__name__,
                                   self.devices.get('controller_serial'))

    def login(self):
        """Call login."""
        self._authenticate()

    def _authenticate(self):
        """Authenticate."""
        # to obtain csrftoken, remove Referer from headers
        headers = HEADERS.copy()
        headers.pop('Referer')

        # initial GET request
        self.client = requests.Session()
        self.client.proxies = self._proxies
        self.client.get(LOGIN_ENDPOINT, headers=headers, verify=False)

        # set headers to submit POST request
        token = INITIAL_DATA.copy()
        token['csrfmiddlewaretoken'] = self._csrftoken
        token['email'] = self._username
        token['password'] = self._password

        req = self.client.post(LOGIN_ENDPOINT, stream=True, data=token,
                               headers=HEADERS, verify=False)

        if req.status_code != 302:
            req.raise_for_status()

        # populate device list
        self._devices.append(serial_finder(req.text))
        self.update()

        return True

    @property
    def _csrftoken(self):
        '''Return current csrftoken from request session.'''
        if self.client:
            return self.client.cookies.get('csrftoken')
        return None

    def _get_cu_and_fu_status(self):
        """Submit POST request to update self.device information."""

        # adjust headers
        headers = HEADERS.copy()
        headers['Accept'] = '*/*'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['X-CSRFToken'] = self._csrftoken

        # example {"controller_serial":"12345","faucet_serial":"abcd"}
        argv = '{"controller_serial":"' + \
               self.devices['controller_serial'] + \
               '","faucet_serial":"' + \
               self.devices['faucet_serial'] + \
               '"}'

        post_data = {'argv': argv}

        req = self.client.post(DAJAXICE_ENDPOINT, stream=True, data=post_data,
                               headers=headers, verify=False)

        # token probably expired, then try again
        if req.status_code == 403:
            self.login()
            self.update()
        elif req.status_code == 200:
            self._attributes = req.json()
        else:
            req.raise_for_status()

    def update(self):
        """Update self._attributes object."""
        self._get_cu_and_fu_status()

    @property
    def devices(self):
        """Show current linked devices."""
        if len(self._devices) > 1:
            return self._devices
        return self._devices[0]


# vim:sw=4:ts=4:et:
