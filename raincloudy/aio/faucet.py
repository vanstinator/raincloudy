"""RainCloud Faucet."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .core import RainCloudy
    from .controller import RainCloudyController

from ..const import (
    HEADERS,
    HOME_ENDPOINT,
    MANUAL_OP_DATA,
    MANUAL_WATERING_ALLOWED,
    MAX_RAIN_DELAY_DAYS,
    MAX_WATERING_MINUTES,
    STATUS_ENDPOINT,
)
from ..helpers import (
    find_controller_or_faucet_name,
    find_selected_controller_or_faucet_index,
)


class RainCloudyFaucetCore:
    """RainCloudyFaucetCore object."""

    def __init__(
        self,
        parent: RainCloudy,
        controller: RainCloudyController,
        faucet_id: int,
        index: int,
        zone_names: list = [],
    ):
        """
        Initialize RainCloudy Controller object.

        :param parent: RainCloudy object
        :param controller: RainCloudy Controller parent object
        :param faucet_id: faucet ID assigned controller
        :type parent: RainCloudy object
        :type controller: RainCloudyControler object
        :type faucet_id: string
        :return: RainCloudyFaucet object
        :rtype: RainCloudyFaucet object
        """
        self.index = index
        self._parent = parent
        self._controller = controller
        self._id = faucet_id
        self._zone_names = zone_names
        self._attributes: dict[str, Any] = {}

        # zones associated with faucet
        self.zones = self._create_zones()

    def _create_zones(self) -> list[RainCloudyFaucetZone]:
        """Assign all RainCloudyFaucetZone managed by faucet."""
        return [
            RainCloudyFaucetZone(
                parent=self._parent,
                controller=self._controller,
                faucet=self,
                zone_id=zone_id,
                zone_name=self._zone_names[zone_id - 1],
            )
            for zone_id in range(1, 5)
        ]

    def __repr__(self) -> str:
        """Object representation."""
        try:
            return f"<{self.__class__.__name__}: {self.name}>"
        except AttributeError:
            return f"<{self.__class__.__name__}: {self.id}>"

    @property
    def attributes(self) -> dict[str, Any]:
        """Return faucet id."""
        return self._attributes

    @property
    def serial(self) -> int | str:
        """Return faucet id."""
        return self._id

    # pylint: disable=invalid-name
    @property
    def id(self) -> int | str:
        """Return faucet id."""
        return self._id

    @property
    def current_time(self) -> str:
        """Return controller current time."""
        return self._controller.current_time

    @property
    def name(self) -> str | None:
        """Return faucet name."""
        return find_controller_or_faucet_name(
            self._controller.home, "faucet", self.index
        )

    async def update_name(self, value: str) -> None:
        """Set a new name to faucet."""
        data = {
            "_set_faucet_name": "Set Name",
            "select_faucet": self.index,
            "faucet_name": value,
        }
        await self._parent.post(data)

    @property
    def status(self) -> str:
        """Return status."""
        return self._attributes["faucet_status"]

    @property
    def battery(self) -> str | None:
        """Return faucet battery."""
        battery = self._attributes["battery_percent"]
        if battery == "" or battery is None:
            return None
        return battery.strip("%")

    async def update(self) -> None:
        """Submit GET request to update information."""
        # adjust headers
        headers = HEADERS.copy()
        headers["Accept"] = "*/*"
        headers["X-Requested-With"] = "XMLHttpRequest"
        headers["X-CSRFToken"] = self._parent.csrftoken

        url = f"{STATUS_ENDPOINT}?controller_serial\
={self._controller.serial}&faucet_serial={self.id}"

        async with self._parent.client.get(
            url, headers=headers, **self._parent._args
        ) as req:
            # token probably expired, then try again
            if req.status == 403:
                await self._parent.login()
                await self.update()
            elif req.status == 200:
                self._controller.attributes = self._attributes = await req.json()
            else:
                req.raise_for_status()

    def _find_zone_by_id(self, zone_id) -> RainCloudyFaucetZone | None:
        """Return zone by id."""
        if not self.zones:
            return None

        zone = list(filter(lambda zone: zone.id == zone_id, self.zones))

        return zone[0] if zone else None


class RainCloudyFaucet(RainCloudyFaucetCore):
    """RainCloudyFaucet object."""

    @property
    def zone1(self) -> RainCloudyFaucetZone | None:
        """Return zone managed by faucet."""
        return self._find_zone_by_id(1)

    @property
    def zone2(self) -> RainCloudyFaucetZone | None:
        """Return zone managed by faucet."""
        return self._find_zone_by_id(2)

    @property
    def zone3(self) -> RainCloudyFaucetZone | None:
        """Return zone managed by faucet."""
        return self._find_zone_by_id(3)

    @property
    def zone4(self) -> RainCloudyFaucetZone | None:
        """Return zone managed by faucet."""
        return self._find_zone_by_id(4)


class RainCloudyFaucetZone:  # (RainCloudyFaucetCore):
    """RainCloudyFaucetZone object."""

    # pylint: disable=super-init-not-called
    # needs review later
    def __init__(
        self,
        parent: RainCloudy,
        controller: RainCloudyController,
        faucet: RainCloudyFaucetCore,
        zone_id: int,
        zone_name: str,
    ):
        """
        Initialize RainCloudy Controller object.

        :param parent: RainCloudy object
        :param controller: RainCloudy Controller parent object
        :param faucet: faucet assigned controller
        :param zone_id: zone ID assigned controller
        :type parent: RainCloudy object
        :type controller: RainCloudyControler object
        :type faucet: RainCloudyFaucet object
        :type zone_id: integer
        :return: RainCloudyFaucet object
        :rtype: RainCloudyFaucet object
        """
        self._parent = parent
        self._controller = controller
        self._faucet = faucet
        self._id = zone_id
        self._name = zone_name

    def __repr__(self) -> str:
        """Object representation."""
        try:
            return "<{0}: {1}>".format(self.__class__.__name__, self.name)
        except AttributeError:
            return "<{0}: {1}>".format(self.__class__.__name__, self.id)

    # pylint: disable=invalid-name
    @property
    def id(self) -> int:
        """Return zone id."""
        return self._id

    async def set_zone_name(self, zoneid, name) -> None:
        """Set zone name."""
        # zone starts with index 0
        zoneid -= 1
        data = {
            "select_controller": self._controller.index,
            "select_faucet": self._faucet.index,
            "_set_zone_name": "Set Name",
            "select_zone": str(zoneid),
            "zone_name": name,
        }
        await self._parent.post(data)

    @property
    def name(self) -> str:
        """Return zone name."""
        return self._name

    async def update_name(self, value: str) -> None:
        """Set a new zone name to faucet."""
        await self.set_zone_name(self.id, value)

    async def set_manual_watering_time(self, value: str | int) -> None:
        """Set watering_time per zone."""
        if value not in MANUAL_WATERING_ALLOWED:
            raise ValueError(
                "Valid options are: {}".format(
                    ", ".join(map(str, MANUAL_WATERING_ALLOWED))
                )
            )

        ddata = await self.preupdate()
        attr = "zone{}_select_manual_mode".format(self.id)

        if (isinstance(value, int) and value == 0) or (
            isinstance(value, str) and value.lower() == "off"
        ):
            value = "OFF"

            # If zone is turned on at the valve we need to toggle ON first
            ddata[attr] = "ON"
            await self.submit_action(ddata)
            await asyncio.sleep(1)
        elif isinstance(value, str):
            value = value.upper()
            if value == "ON":
                value = MAX_WATERING_MINUTES

        ddata[attr] = value
        await self.submit_action(ddata)

    @property
    def watering_time(self) -> int:
        """Return watering_time from zone."""
        auto_watering_time = self.lookup_attr("auto_watering_time")

        manual_watering_time = self.lookup_attr("manual_watering_time")

        if auto_watering_time > manual_watering_time:
            watering_time = auto_watering_time
        else:
            watering_time = manual_watering_time

        return watering_time

    @property
    def manual_watering(self) -> bool:
        """Return zone manual_mode_on"""
        return self.lookup_attr("manual_mode_on")

    async def set_rain_delay(self, value: int | str | None) -> None:
        """Set rain delay."""
        if isinstance(value, int):
            if value > MAX_RAIN_DELAY_DAYS or value < 0:
                value = None
            elif value == 0:
                value = "off"
            elif value == 1:
                value = "1day"
            elif value >= 2:
                value = str(value) + "days"
        elif isinstance(value, str):
            if value.lower() != "off":
                value = None

        if value is None:
            return None

        ddata = await self.preupdate()
        ddata[f"zone{self.id}_rain_delay_select"] = value
        await self.submit_action(ddata)

    @property
    def rain_delay(self) -> int:
        """Return the rain delay day from zone."""
        return self.lookup_attr("rain_delay_mode")

    @property
    def next_cycle(self) -> str:
        """Return the time scheduled for next watering from zone."""
        return self.lookup_attr("next_water_cycle")

    async def set_auto_watering(self, value: bool):
        """Set auto_watering program."""
        if not isinstance(value, bool):
            return None

        ddata = await self.preupdate()
        attr = f"zone{self.id}_program_toggle"
        try:
            if not value:
                ddata.pop(attr)
            else:
                ddata[attr] = "on"
        except KeyError:
            pass

        await self.submit_action(ddata)
        return True

    @property
    def auto_watering(self) -> bool:
        """Return if zone is configured to automatic watering."""
        return self.lookup_attr("program_mode_on")

    @property
    def is_watering(self) -> bool:
        """Return boolean if zone is watering."""
        return bool(self.watering_time > 0)

    def lookup_attr(self, attr: str) -> Any:
        """Returns rain_delay_mode attributes by zone index"""
        return self._faucet.attributes["rain_delay_mode"][int(self.id) - 1][attr]

    def _to_dict(self) -> dict:
        """Method to build zone dict."""
        return {
            "auto_watering": self.auto_watering,
            "manual_watering": self.manual_watering,
            "is_watering": self.is_watering,
            "name": self.name,
            "next_cycle": self.next_cycle,
            "rain_delay": self.rain_delay,
            "watering_time": self.watering_time,
        }

    def report(self) -> dict:
        """Return status from zone."""
        return self._to_dict()

    async def update(self) -> None:
        """Request faucet to update"""
        await self._faucet.update()

    async def preupdate(self, force_refresh: bool = True) -> dict:
        """Return a dict with all current options prior submitting request."""
        ddata = MANUAL_OP_DATA.copy()

        # force update to make sure status is accurate
        if force_refresh:
            await self._faucet.update()

        # select current controller and faucet
        ddata["select_controller"] = self._parent.controllers.index(self._controller)
        ddata["select_faucet"] = self._controller.faucets.index(self._faucet)

        # check if zone is scheduled automatically (zone1_program_toggle)
        # only add zoneX_program_toogle to ddata when needed,
        # otherwise the field will be always on
        for zone in self._faucet.zones:
            attr = f"zone{zone.id}_program_toggle"
            if zone.auto_watering:
                ddata[attr] = "on"

        # check if zone current watering manually (zone1_select_manual_mode)
        for zone in self._faucet.zones:
            attr = f"zone{zone.id}_select_manual_mode"
            if zone.watering_time and attr in ddata.keys():
                ddata[attr] = zone.watering_time

        # check if rain delay is selected (zone0_rain_delay_select)
        for zone in self._faucet.zones:
            attr = "zone{}_rain_delay_select".format(zone.id - 1)
            value: str | int = zone.rain_delay
            if value and attr in ddata.keys():
                if int(value) >= 2 and int(value) <= 7:
                    value = str(value) + "days"
                else:
                    value = str(value) + "day"
                ddata[attr] = value

        return ddata

    async def submit_action(self, ddata: dict) -> None:
        """Post data."""

        controller_index = self._parent.controllers.index(self._controller)
        faucet_index = self._controller.faucets.index(self._faucet)

        current_controller_index = find_selected_controller_or_faucet_index(
            self._parent.html["home"], "controller"
        )

        current_faucet_index = find_selected_controller_or_faucet_index(
            self._parent.html["home"], "faucet"
        )

        # This is an artifact of how the web-page we're impersonating works.
        # The form submit will only apply actions to _selected_ controllers
        # and faucets. So if the active controller and/or faucet on the page
        # isn't the faucet we're trying to submit an action for we need to
        # send the response twice. The first time we send it will switch us
        # to the action
        if (
            current_controller_index != controller_index
            or current_faucet_index != faucet_index
        ):
            await self._parent.post(ddata, url=HOME_ENDPOINT, referer=HOME_ENDPOINT)

        response = await self._parent.post(
            ddata, url=HOME_ENDPOINT, referer=HOME_ENDPOINT
        )
        if response:
            self._parent.update_home(await response.text())
