"""RainCloudy core object."""
from __future__ import annotations

import asyncio
import os
import ssl
from pathlib import Path
from typing import Any

from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse
from bs4 import BeautifulSoup

from ..const import (HEADERS, HOME_ENDPOINT, INITIAL_DATA, LOGIN_ENDPOINT,
                     LOGOUT_ENDPOINT, SETUP_ENDPOINT)
from ..helpers import (controller_serial_finder, faucet_serial_finder,
                       find_zone_names, generate_soup_html)
from .controller import RainCloudyController


class RainCloudy:
    """RainCloudy object."""

    def __init__(
        self,
        username: str,
        password: str,
        client_session: ClientSession = None,
        http_proxy: str = None,
        ssl_verify: bool = True,
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
        if client_session:
            self.client = client_session
            self._client_provided = True
        else:
            self.client = ClientSession()
            self._client_provided = False
        self._ssl_verify = ssl_verify

        # define credentials
        self._username = username
        self._password = password

        # initialize future attributes
        self._controllers: list[RainCloudyController] = []
        self.is_connected = False
        self.html: dict[str, BeautifulSoup | None] = {
            "home": None,
            "setup": None,
            "program": None,
            "manage": None,
        }

        # set proxy environment
        self._args: dict[str, Any] = {"proxy": http_proxy, "ssl": None}

    def __repr__(self) -> str:
        """Object representation."""
        return f"<{self.__class__.__name__}: {self.controllers[0].serial}>"

    async def login(self) -> None:
        """Login to the raincloud cloud service."""
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )

        cert_file = Path(__location__, "../wifiaquatimer_com_chain.cer").resolve()

        # to obtain csrftoken, remove Referer from headers
        headers = HEADERS.copy()
        headers.pop("Referer")

        # initial GET request
        # self.client = requests.Session()
        # self._client_session.proxies = self._proxies
        self._args["ssl"] = ssl.create_default_context(cafile=str(cert_file))
        # self.client.verify = cert_file.resolve()
        await self.client.get(LOGIN_ENDPOINT, headers=headers, **self._args)

        # set headers to submit POST request
        token = INITIAL_DATA.copy()
        token["csrfmiddlewaretoken"] = self.csrftoken
        token["email"] = self._username
        token["password"] = self._password

        async with self.client.post(
            LOGIN_ENDPOINT,
            data=token,
            headers=HEADERS,
            **self._args,
        ) as req:
            if req.status != 302:
                req.raise_for_status()

        async with self.client.get(url=HOME_ENDPOINT, **self._args) as home:
            self.html["home"] = generate_soup_html(await home.text())

        async with self.client.get(
            SETUP_ENDPOINT, headers=HEADERS, **self._args
        ) as setup:
            # populate device list
            self.html["setup"] = generate_soup_html(await setup.text())

        controller_serials = controller_serial_finder(self.html["setup"])

        for index, controller_serial in enumerate(controller_serials):

            # We need to do a form submit for other controllers to get
            # faucet serials
            if index > 0:
                data = {"select_controller": index}
                resp = await self.post(data, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT)
                if resp:
                    self.html["setup"] = generate_soup_html(await resp.text())

            faucet_serials = faucet_serial_finder(self.html["setup"])

            faucets = []
            for faucet_index, faucet_serial in enumerate(faucet_serials):

                # We need to do a form submit for other faucets to get
                # zone names
                if faucet_index > 0:
                    data = {"select_faucet": faucet_index}
                    resp = await self.post(
                        data, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT
                    )
                    if resp:
                        self.html["setup"] = generate_soup_html(await resp.text())

                zone_names = find_zone_names(self.html["setup"])
                faucets.append({"serial": faucet_serial, "zones": zone_names})

            self._controllers.append(
                RainCloudyController(self, controller_serial, index, faucets)
            )
        await asyncio.gather(*[controller.update() for controller in self._controllers])
        self.is_connected = True

    @property
    def csrftoken(self) -> str:
        """Return current csrftoken from request session."""
        if self.client:
            for cookie in self.client.cookie_jar:
                if cookie.key == "csrftoken":
                    return cookie.value
        return ""

    async def update(self) -> None:
        """Update controller._attributes."""
        await asyncio.gather(*[controller.update() for controller in self._controllers])

    @property
    def controllers(self) -> list[RainCloudyController]:
        """Show current linked controllers."""
        if hasattr(self, "_controllers"):
            return self._controllers
        raise AttributeError("There is no controller assigned.")

    def update_home(self, data: str) -> None:
        """Update home html"""
        if not isinstance(data, str):
            raise TypeError("Function requires string response")
        self.html["home"] = generate_soup_html(data)

    async def post(
        self, ddata: dict, url: str = SETUP_ENDPOINT, referer: str = SETUP_ENDPOINT
    ) -> ClientResponse | None:
        """Update some attributes on namespace."""
        headers = HEADERS.copy()
        if referer is None:
            headers.pop("Referer")
        else:
            headers["Referer"] = referer

        # append csrftoken
        if "csrfmiddlewaretoken" not in ddata.keys():
            ddata["csrfmiddlewaretoken"] = self.csrftoken

        async with self.client.post(
            url, headers=headers, data=ddata, **self._args
        ) as req:
            if not req.status == 200:
                return None

            return req

    async def logout(self) -> None:
        """Logout."""
        await self.client.get(LOGOUT_ENDPOINT, **self._args)
        if not self._client_provided:
            await self.client.close()
        self._cleanup()

    def _cleanup(self) -> None:
        """Cleanup object when logging out."""
        self._controllers = []
        self.is_connected = False


# vim:sw=4:ts=4:et:
