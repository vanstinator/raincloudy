# -*- coding: utf-8 -*-
"""RainCloud Controller."""

import raincloudy
from raincloudy.faucet import RainCloudyFaucet
from raincloudy.const import (
    STATUS_ENDPOINT, HEADERS, SETUP_ENDPOINT, HOME_ENDPOINT)
from raincloudy.helpers import (
    find_controller_or_faucet_name, generate_soup_html)


class RainCloudyController():
    """RainCloudy Controller object."""

    def __init__(self, parent, controller_id, index, faucets=None):
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
        self.attributes = None
        self.home = None
        self._parent = parent
        self._controller_id = controller_id
        self._index = index

        self._verify_parent()

        # faucets associated with controller
        self._faucets = []

        # load assigned faucets
        self._assign_faucets(faucets)

        # populate controller attributes
        self.update()

    def _verify_parent(self):
        """Verify parent type."""
        if not isinstance(self._parent, raincloudy.core.RainCloudy):
            raise TypeError("Invalid parent object.")

    def _assign_faucets(self, faucets):
        """Assign RainCloudyFaucet objects to self._faucets."""
        if not faucets:
            raise TypeError("Controller does not have a faucet assigned.")

        for index, faucet_id in enumerate(faucets):
            self._faucets.append(
                RainCloudyFaucet(self._parent, self, faucet_id, index))

    def __repr__(self):
        """Object representation."""
        try:
            return "<{0}: {1}>".format(self.__class__.__name__, self.name)
        except AttributeError:
            return "<{0}: {1}>".format(self.__class__.__name__, self.id)

    def _refresh_html_home(self):
        """
        Function to refresh the self._parent.html['home'] object
        which provides the status if zones are scheduled to
        start automatically (program_toggle).
        """
        data = {
            'select_controller': self._index,
            'select_faucet': 0,
            'zone1_select_manual_mode': 'OFF',
            'zone2_select_manual_mode': 'OFF',
            'zone3_select_manual_mode': 'OFF',
            'zone4_select_manual_mode': 'OFF',
            'zone0_rain_delay_select': 'off',
            'zone1_rain_delay_select': 'off',
            'zone2_rain_delay_select': 'off',
            'zone3_rain_delay_select': 'off',
        }
        req = self._parent.post(data, url=HOME_ENDPOINT, referer=HOME_ENDPOINT)
        if req.status_code == 403:
            self._parent.login()
            self.update()
        elif req.status_code == 200:
            self.home = generate_soup_html(req.text)
        else:
            req.raise_for_status()

    def update(self):
        """
        Call 1 method to update zone attributes
        """
        self._refresh_html_home()
        # update zone attributes
        for faucet in self._faucets:
            faucet.update()

    @property
    def serial(self):
        """Return controller id."""
        return self._controller_id

    # pylint: disable=invalid-name
    @property
    def id(self):
        """Return controller id."""
        return self.serial

    @property
    def name(self):
        """Return controller name."""
        return \
            find_controller_or_faucet_name(self.home,
                                           'controller',
                                           self._index)

    @name.setter
    def name(self, value):
        """Set a new name to controller."""
        data = {
            '_set_controller_name': 'Set Name',
            'controller_name': value,
        }
        self._parent.post(data, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT)

    @property
    def status(self):
        """Return controller status."""
        return self.attributes['controller_status']

    @property
    def current_time(self):
        """Return controller current time."""
        return self.attributes['current_time']

    @property
    def faucets(self):
        """Show current linked faucet."""
        if hasattr(self, '_faucets'):
            return self._faucets
        raise AttributeError("There are no faucets assigned.")

# vim:sw=4:ts=4:et:
