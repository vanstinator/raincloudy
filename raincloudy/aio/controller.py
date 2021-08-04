"""RainCloud Controller."""
from __future__ import annotations

import asyncio

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .core import RainCloudy
from .faucet import RainCloudyFaucet, RainCloudyFaucetCore
from ..const import SETUP_ENDPOINT
from ..helpers import find_controller_or_faucet_name


class RainCloudyController:
    """RainCloudy Controller object."""

    def __init__(
        self,
        parent: "RainCloudy",
        controller_id: str,
        index: int,
        faucets: list[dict[str, Any]] | None = None,
    ):
        """
        Initialize RainCloudy Controller object.

        :param parent: RainCloudy parent object
        :param controller_id: Control Unit ID
        :param valve_id: Value Unit ID assigned controller
        :type parent: RainCloudy object
        :type controller_id: string
        :type valve_id: string
        :return: RainCloudyController object
        :rtype: RainCloudyController object
        """
        self._parent = parent
        self.home = parent.html["home"]
        self._controller_id = controller_id
        self.index = index
        self.attributes: dict[str, Any] = {}
        # faucets associated with controller
        self._faucets = self._create_faucets(faucets)

    def _create_faucets(self, faucets: list[dict] | None) -> list[RainCloudyFaucetCore]:
        """Assign RainCloudyFaucet objects to self._faucets."""
        if not faucets:
            raise TypeError("Controller does not have a faucet assigned.")

        return [
            RainCloudyFaucet(
                self._parent, self, faucet["serial"], index, faucet["zones"]
            )
            for index, faucet in enumerate(faucets)
        ]

    def __repr__(self) -> str:
        """Object representation."""
        try:
            return f"<{self.__class__.__name__}: {self.name}>"
        except AttributeError:
            return f"<{self.__class__.__name__}: {self.id}>"

    async def update(self) -> None:
        """Call 1 method to update zone attributes."""
        # update zone attributes
        await asyncio.gather(*[faucet.update() for faucet in self._faucets])

    @property
    def serial(self) -> str:
        """Return controller id."""
        return self._controller_id

    # pylint: disable=invalid-name
    @property
    def id(self) -> str:
        """Return controller id."""
        return self._controller_id

    @property
    def name(self) -> str | None:
        """Return controller name."""
        return find_controller_or_faucet_name(
            self._parent.html["home"], "controller", self.index
        )

    async def update_name(self, value) -> None:
        """Set a new name to controller."""
        data = {
            "select_controller": self.index,
            "_set_controller_name": "Set Name",
            "controller_name": value,
        }
        await self._parent.post(data, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT)

    @property
    def status(self) -> str:
        """Return controller status."""
        return self.attributes["controller_status"]

    @property
    def current_time(self) -> str:
        """Return controller current time."""
        return self.attributes["current_time"]

    @property
    def faucets(self) -> list[RainCloudyFaucetCore]:
        """Show current linked faucet."""
        if hasattr(self, "_faucets"):
            return self._faucets
        raise AttributeError("There are no faucets assigned.")


# vim:sw=4:ts=4:et:
