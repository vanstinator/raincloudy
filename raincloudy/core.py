# -*- coding: utf-8 -*-
"""RainCloud."""
import requests
import urllib3
from .const import INITIAL_DATA, HEADERS, LOGIN_ENDPOINT
from .helpers import serial_finder
from .controller import RainCloudyController


class RainCloudy(object):
    """RainCloudy object."""

    def __init__(self, username, password, http_proxy=None, https_proxy=None,
                 ssl_warnings=False):
        """
        Initialize RainCloud object.

        :param username: username to authenticate user
        :param passwrod: password to authenticate user
        :param http_proxy: HTTP proxy information (127.0.0.1:8080)
        :param https_proxy: HTTPs proxy information (127.0.0.1:8080)
        :param ssl_warnings: Show SSL warnings. Defaults to False
        :type username: string
        :type password: string
        :type http_proxy: string
        :type https_proxy: string
        :type ssl_warnings: boolean
        :rtype: RainCloudy object
        """
        if not ssl_warnings:
            urllib3.disable_warnings()

        # define credentials
        self._username = username
        self._password = password

        # initialize future attributes
        self.controllers = []
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
                                   self.controller.serial)

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
        token['csrfmiddlewaretoken'] = self.csrftoken
        token['email'] = self._username
        token['password'] = self._password

        req = self.client.post(LOGIN_ENDPOINT, stream=True, data=token,
                               headers=HEADERS, verify=False)

        if req.status_code != 302:
            req.raise_for_status()

        # populate device list
        parsed_controller = serial_finder(req.text)
        self.controllers.append(
            RainCloudyController(
                self,
                parsed_controller['controller_serial'],
                parsed_controller['faucet_serial']
            )
        )
        return True

    @property
    def csrftoken(self):
        '''Return current csrftoken from request session.'''
        if self.client:
            return self.client.cookies.get('csrftoken')
        return None

    def update(self):
        """Update controller._attributes."""
        self.controller.update()

    @property
    def controller(self):
        """Show current linked controllers."""
        if len(self.controllers) > 1:
            # in the future, we should support more controllers
            raise TypeError("Only one controller per account.")
        return self.controllers[0]

# vim:sw=4:ts=4:et:
