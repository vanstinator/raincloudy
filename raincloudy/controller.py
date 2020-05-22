# -*- coding: utf-8 -*-
"""RainCloud Controller."""

import raincloudy
from raincloudy.faucet import RainCloudyFaucet
from raincloudy.const import SETUP_ENDPOINT
from raincloudy.helpers import find_controller_or_faucet_name


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
        self.attributes = {}
        self._parent = parent
        self.home = parent.html['home']
        self._controller_id = controller_id
        self.index = index

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

    def update(self):
        """
        Call 1 method to update zone attributes
        """
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
            find_controller_or_faucet_name(self._parent.html['home'],
                                           'controller',
                                           self.index)

    @name.setter
    def name(self, value):
        """Set a new name to controller."""
        data = {
            'select_controller': self.index,
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
