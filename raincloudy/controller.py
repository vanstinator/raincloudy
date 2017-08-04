# -*- coding: utf-8 -*-
"""RainCloud Controller."""
import raincloudy

from bs4 import BeautifulSoup
from .const import API_URL, DAJAXICE_ENDPOINT, HEADERS, HOME_ENDPOINT
from .helpers import find_attr, find_program_status


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
        :return: RainCloudyController object
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
            headers=headers)

        # token probably expired, then try again
        if req.status_code == 403:
            self._parent.login()
            self.update()
        elif req.status_code == 200:
            self._attributes = req.json()
        else:
            req.raise_for_status()

    def _refresh_htmlsoup(self):
        """
        Function to refresh the self._parent.htmlsoup object
        which provides the status if zones are scheduled to
        start automatically (program_toggle).
        """
        req = self._parent.client.get(HOME_ENDPOINT)
        if req.status_code == 403:
            self._parent.login()
            self.update()
        elif req.status_code == 200:
            self._parent.htmlsoup = BeautifulSoup(req.text, 'html.parser')
        else:
            req.raise_for_status()

    def update(self):
        """
        Call 2 methods to update zone attributes and htmlsoup object
        """
        # update zone attributes
        self._get_cu_and_fu_status()

        # update self._parent.htmlsoup for gathering
        # auto_watering status (program_toggle tag)
        self._refresh_htmlsoup()

    def _find_attr(self, key):
        """Callback for find_attr method."""
        return find_attr(self._attributes, key)

    @property
    def status(self):
        """Return controller status."""
        return self._find_attr('controller_online')

    @property
    def faucet_status(self):
        """Return valve status."""
        return self._find_attr('faucet_online')

    @property
    def current_time(self):
        """Return controller current time."""
        return self._find_attr('current_time')

    @property
    def faucet_battery(self):
        """Return faucet battery."""
        return self._find_attr('active_faucet_battery_level')

    # some fields on the backend refers to zone0 as zone1 as well
    # to keep it cohenret and since the frontend refers to zone1
    # we will call it publicly as zone1
    @property
    def zone1_watering_time(self):
        """Return watering_time from zone."""
        return self._find_attr('zone_0_watering_time')

    @property
    def zone2_watering_time(self):
        """Return watering_time from zone."""
        return self._find_attr('zone_1_watering_time')

    @property
    def zone3_watering_time(self):
        """Return watering_time from zone."""
        return self._find_attr('zone_2_watering_time')

    @property
    def zone4_watering_time(self):
        """Return watering_time from zone."""
        return self._find_attr('zone_3_watering_time')

    @property
    def zone1_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._find_attr('droplet_zone_0'))

    @property
    def zone2_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._find_attr('droplet_zone_1'))

    @property
    def zone3_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._find_attr('droplet_zone_2'))

    @property
    def zone4_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._find_attr('droplet_zone_3'))

    @property
    def zone1_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._find_attr('id_zone1_rain_delay_select')

    @property
    def zone2_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._find_attr('id_zone2_rain_delay_select')

    @property
    def zone3_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._find_attr('id_zone3_rain_delay_select')

    @property
    def zone4_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._find_attr('id_zone4_rain_delay_select')

    @property
    def zone1_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._find_attr('zone_0_countdown_time')

    @property
    def zone2_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._find_attr('zone_1_countdown_time')

    @property
    def zone3_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._find_attr('zone_2_countdown_time')

    @property
    def zone4_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._find_attr('zone_3_countdown_time')

    @property
    def zone1_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        # NOTE to myself: when sending a POST, we need to update htmlsoup obj
        return find_program_status(self._parent.htmlsoup, 'zone1')

    @property
    def zone2_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        return find_program_status(self._parent.htmlsoup, 'zone2')

    @property
    def zone3_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        return find_program_status(self._parent.htmlsoup, 'zone3')

    @property
    def zone4_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        return find_program_status(self._parent.htmlsoup, 'zone4')

    @property
    def zone1(self):
        """Return status from zone."""
        return {
            'auto_watering': self.zone1_auto_watering,
            'droplet': self.zone1_droplet,
            'next_cycle': self.zone1_next_cycle,
            'rain_delay': self.zone1_rain_delay,
            'watering_time': self.zone1_watering_time,
        }

    @property
    def zone2(self):
        """Return status from zone."""
        return {
            'auto_watering': self.zone2_auto_watering,
            'droplet': self.zone2_droplet,
            'next_cycle': self.zone2_next_cycle,
            'rain_delay': self.zone2_rain_delay,
            'watering_time': self.zone2_watering_time,
        }

    @property
    def zone3(self):
        """Return status from zone."""
        return {
            'auto_watering': self.zone3_auto_watering,
            'droplet': self.zone3_droplet,
            'next_cycle': self.zone3_next_cycle,
            'rain_delay': self.zone3_rain_delay,
            'watering_time': self.zone3_watering_time,
        }

    @property
    def zone4(self):
        """Return status from zone."""
        return {
            'auto_watering': self.zone4_auto_watering,
            'droplet': self.zone4_droplet,
            'next_cycle': self.zone4_next_cycle,
            'rain_delay': self.zone4_rain_delay,
            'watering_time': self.zone4_watering_time,
        }

    @property
    def zones(self):
        """Return a dict from all zones status."""
        zones = {}
        zones['zone1'] = self.zone1
        zones['zone2'] = self.zone2
        zones['zone3'] = self.zone3
        zones['zone4'] = self.zone4
        return zones
