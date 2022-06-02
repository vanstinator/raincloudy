# -*- coding: utf-8 -*-
"""RainCloudy core object."""
import os
from pathlib import Path

import requests
import urllib3

from raincloudy.const import (
    HEADERS,
    HOME_ENDPOINT,
    INITIAL_DATA,
    LOGIN_ENDPOINT,
    LOGOUT_ENDPOINT,
    SETUP_ENDPOINT,
)
from raincloudy.controller import RainCloudyController
from raincloudy.helpers import (
    controller_serial_finder,
    faucet_serial_finder,
    find_zone_names,
    generate_soup_html,
)


class RainCloudy:
    """RainCloudy object."""

    def __init__(
        self,
        username,
        password,
        http_proxy=None,
        https_proxy=None,
        ssl_warnings=True,
        ssl_verify=True,
    ):
        """
        Initialize RainCloud object.

        :param username: username to authenticate user
        :param passwrod: password to authenticate user
        :param http_proxy: HTTP proxy information (127.0.0.1:8080)
        :param https_proxy: HTTPs proxy information (127.0.0.1:8080)
        :param ssl_warnings: Show SSL warnings
        :param ssl_verify: Verify SSL server certificate
        :type username: string
        :type password: string
        :type http_proxy: string
        :type https_proxy: string
        :type ssl_warnings: boolean
        :type ssl_verify: boolean
        :rtype: RainCloudy object
        """
        self._ssl_verify = ssl_verify
        if not ssl_warnings:
            urllib3.disable_warnings()

        # define credentials
        self._username = username
        self._password = password

        # initialize future attributes
        self._controllers = []
        self.client = None
        self.is_connected = False
        self.html = {
            "home": None,
            "setup": None,
            "program": None,
            "manage": None,
        }

        # set proxy environment
        self._proxies = {
            "http": http_proxy,
            "https": https_proxy,
        }

        # login
        self.login()

    def __repr__(self):
        """Object representation."""
        for controller in self.controllers:
            return "<{0}: {1}>".format(self.__class__.__name__, controller.serial)

    def login(self):
        """Call login."""
        return self._authenticate

    @property
    def _authenticate(self):
        """Authenticate."""

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )

        # cert_file = Path(__location__ + "/wifiaquatimer_com_chain.cer")

        # to obtain csrftoken, remove Referer from headers
        headers = HEADERS.copy()
        headers.pop("Referer")

        # initial GET request
        self.client = requests.Session()
        self.client.proxies = self._proxies
        # self.client.verify = cert_file.resolve()
        self.client.stream = True
        self.client.get(LOGIN_ENDPOINT, headers=headers)

        # set headers to submit POST request
        token = INITIAL_DATA.copy()
        token["csrfmiddlewaretoken"] = self.csrftoken
        token["email"] = self._username
        token["password"] = self._password

        req = self.client.post(LOGIN_ENDPOINT, data=token, headers=HEADERS)

        if req.status_code != 302:
            req.raise_for_status()

        home = self.client.get(url=HOME_ENDPOINT)

        self.html["home"] = generate_soup_html(home.text)

        setup = self.client.get(SETUP_ENDPOINT, headers=HEADERS)
        # populate device list
        self.html["setup"] = generate_soup_html(setup.text)

        controller_serials = controller_serial_finder(self.html["setup"])

        for index, controller_serial in enumerate(controller_serials):

            # We need to do a form submit for other controllers to get
            # faucet serials
            if index > 0:
                data = {"select_controller": index}
                self.html["setup"] = generate_soup_html(
                    self.post(data, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT).text
                )

            faucet_serials = faucet_serial_finder(self.html["setup"])

            faucets = []
            for faucet_index, faucet_serial in enumerate(faucet_serials):

                # We need to do a form submit for other faucets to get
                # zone names
                if faucet_index > 0:
                    data = {"select_faucet": faucet_index}
                    self.html["setup"] = generate_soup_html(
                        self.post(data, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT).text
                    )

                zone_names = find_zone_names(self.html["setup"])
                faucets.append({"serial": faucet_serial, "zones": zone_names})

            self._controllers.append(
                RainCloudyController(self, controller_serial, index, faucets)
            )
        self.is_connected = True
        return True

    @property
    def csrftoken(self):
        """Return current csrftoken from request session."""
        if self.client:
            return self.client.cookies.get("csrftoken")
        return None

    def update(self):
        """Update controller._attributes."""
        for controller in self._controllers:
            controller.update()

    @property
    def controllers(self):
        """Show current linked controllers."""
        if hasattr(self, "_controllers"):
            return self._controllers
        raise AttributeError("There is no controller assigned.")

    def update_home(self, data):
        """Update home html"""
        if not isinstance(data, str):
            raise TypeError("Function requires string response")
        self.html["home"] = generate_soup_html(data)

    def post(self, ddata, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT):
        """Method to update some attributes on namespace."""
        headers = HEADERS.copy()
        if referer is None:
            headers.pop("Referer")
        else:
            headers["Referer"] = referer

        # append csrftoken
        if "csrfmiddlewaretoken" not in ddata.keys():
            ddata["csrfmiddlewaretoken"] = self.csrftoken

        req = self.client.post(url, headers=headers, data=ddata)
        if not req.status_code == 200:
            return None

        return req

    def logout(self):
        """Logout."""
        self.client.get(LOGOUT_ENDPOINT)
        self._cleanup()

    def _cleanup(self):
        """Cleanup object when logging out."""
        self.client = None
        self._controllers = []
        self.is_connected = False


# vim:sw=4:ts=4:et:
