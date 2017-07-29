# -*- coding: utf-8 -*-
"""RainCloud Controller."""
import raincloudy
from .const import DAJAXICE_ENDPOINT, HEADERS


class RainCloudyController(object):
    """RainCloudy Controller object."""

    def __init__(self, parent, controller_id, valve_id):
        """
        Initialize RainCloudy Controller object.

        :param parent: RainCloudy parent object
        :param controller_id: Control Unit ID
        :param valve_id: Value Unit ID assigned controller
        :type parent: RainCloudy object
        :type controller_id: string
        :type valve_id: string
        :rtype: RainCloudyController object
        """

        if not isinstance(parent, raincloudy.core.RainCloudy):
            raise TypeError("Invalid parent object.")

        self._attributes = None
        self._parent = parent
        self._controller_id = controller_id
        self._valve_id = valve_id

        # populate controller attributes
        self.update()

    def __repr__(self):
        """Object representation."""
        return "<{0}: control_unit:{1} valve_unit:{2}>".format(
            self.__class__.__name__,
            self.id,
            self.valve_id)

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
    def faucet_serial(self):
        """Return valve ID."""
        return self._valve_id

    @property
    def valve_id(self):
        """Return valve ID."""
        return self.faucet_serial

    def _get_cu_and_fu_status(self):
        """Submit POST request to update information."""

        # adjust headers
        headers = HEADERS.copy()
        headers['Accept'] = '*/*'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['X-CSRFToken'] = self._parent.csrftoken

        # example {"controller_serial":"12345","faucet_serial":"abcd"}
        argv = '{"controller_serial":"' + self.serial + \
               '","faucet_serial":"' + self.faucet_serial + '"}'
        post_data = {'argv': argv}

        req = self._parent.client.post(
            DAJAXICE_ENDPOINT, stream=True, data=post_data,
            headers=headers, verify=False)

        # token probably expired, then try again
        if req.status_code == 403:
            self._parent.login()
            self.update()
        elif req.status_code == 200:
            self._attributes = req.json()
        else:
            req.raise_for_status()

    def update(self):
        """Update object."""
        self._get_cu_and_fu_status()
