# -*- coding: utf-8 -*-
"""RainCloud Controller."""

import raincloudy
from raincloudy.faucet import RainCloudyFaucet
from raincloudy.const import (
    STATUS_ENDPOINT, HEADERS, HOME_ENDPOINT, SETUP_ENDPOINT)
from raincloudy.helpers import (
    generate_soup_html, find_controller_or_faucet_name)


class RainCloudyController(object):
    """RainCloudy Controller object."""

    def __init__(self, parent, controller_id, faucets=None):
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
        self._parent = parent
        self._controller_id = controller_id

        self._verify_parent()

        # faucets associated with controller
        self.faucets = []

        # load assigned faucets
        self._assign_faucets(faucets)

        # populate controller attributes
        self.update()

    def _verify_parent(self):
        """Verify parent type."""
        if not isinstance(self._parent, raincloudy.core.RainCloudy):
            raise TypeError("Invalid parent object.")

    def _assign_faucets(self, faucets):
        """Assign RainCloudyFaucet objects to self.faucets."""
        if not faucets:
            raise TypeError("Controller does not have a faucet assigned.")

        for faucet_id in faucets:
            self.faucets.append(
                RainCloudyFaucet(self._parent, self, faucet_id))

    def __repr__(self):
        """Object representation."""
        try:
            return "<{0}: {1}>".format(self.__class__.__name__, self.name)
        except AttributeError:
            return "<{0}: {1}>".format(self.__class__.__name__, self.id)

    def post(self, ddata, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT):
        """Method to update some attributes on namespace."""
        headers = HEADERS.copy()
        if referer is None:
            headers.pop('Referer')
        else:
            headers['Referer'] = referer

        # append csrftoken
        if 'csrfmiddlewaretoken' not in ddata.keys():
            ddata['csrfmiddlewaretoken'] = self._parent.csrftoken

        req = self._parent.client.post(url, headers=headers, data=ddata)
        if req.status_code == 200:
            self.update()

    def _get_cu_and_fu_status(self):
        """Submit GET request to update information."""
        # adjust headers
        headers = HEADERS.copy()
        headers['Accept'] = '*/*'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['X-CSRFToken'] = self._parent.csrftoken

        args = '?controller_serial=' + self.serial \
               + '&faucet_serial=' + self.faucet.serial

        req = self._parent.client.get(STATUS_ENDPOINT + args,
                                      headers=headers)

        # token probably expired, then try again
        if req.status_code == 403:
            self._parent.login()
            self.update()
        elif req.status_code == 200:
            self.attributes = req.json()
        else:
            req.raise_for_status()

    def _refresh_html_home(self):
        """
        Function to refresh the self._parent.html['home'] object
        which provides the status if zones are scheduled to
        start automatically (program_toggle).
        """
        req = self._parent.client.get(HOME_ENDPOINT)
        if req.status_code == 403:
            self._parent.login()
            self.update()
        elif req.status_code == 200:
            self._parent.html['home'] = generate_soup_html(req.text)
        else:
            req.raise_for_status()

    def update(self):
        """
        Call 2 methods to update zone attributes and html['home'] object
        """
        # update zone attributes
        self._get_cu_and_fu_status()

        # update self._parent.html['home'] for gathering
        # auto_watering status (program_toggle tag)
        self._refresh_html_home()

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
                                           'controller')

    @name.setter
    def name(self, value):
        """Set a new name to controller."""
        data = {
            '_set_controller_name': 'Set Name',
            'controller_name': value,
        }
        self.post(data, url=SETUP_ENDPOINT, referer=SETUP_ENDPOINT)

    @property
    def status(self):
        """Return controller status."""
        return self.attributes['controller_status']

    @property
    def current_time(self):
        """Return controller current time."""
        return self.attributes['current_time']

    @property
    def faucet(self):
        """Show current linked faucet."""
        if hasattr(self, 'faucets'):
            if len(self.faucets) > 1:
                # in the future, we should support more faucets
                raise TypeError("Only one faucet per account.")
            return self.faucets[0]
        raise AttributeError("There is no faucet assigned.")

# vim:sw=4:ts=4:et:
