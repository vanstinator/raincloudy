# -*- coding: utf-8 -*-
"""RainCloud Faucet."""
from raincloudy.const import API_URL, HOME_ENDPOINT, MANUAL_OP_DATA
from raincloudy.helpers import (
    find_controller_or_faucet_name,
    find_program_status, find_zone_name)


class RainCloudyFaucet(object):
    """RainCloudy Faucet object."""

    def __init__(self, parent, controller, faucet_id):
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

        self._parent = parent
        self._controller = controller
        self._id = faucet_id

    def __repr__(self):
        """Object representation."""
        try:
            return "<{0}: {1}>".format(self.__class__.__name__, self.name)
        except AttributeError:
            return "<{0}: {1}>".format(self.__class__.__name__, self.name)

    @property
    def _attributes(self):
        """Callback to self._controller attributes."""
        return self._controller.attributes

    def _lookup_attr(self, key):
        """Callback for find_attr method."""
        return getattr(self._controller, 'lookup_attr', None)(key)

    @property
    def serial(self):
        """Return faucet id."""
        return self.id

    # pylint: disable=invalid-name
    @property
    def id(self):
        """Return controller id."""
        return self._id

    @property
    def name(self):
        """Return controller name."""
        return \
            find_controller_or_faucet_name(
                self._parent.html['home'],
                'faucet')

    @name.setter
    def name(self, value):
        """Set a new name to faucet."""
        data = {
            '_set_faucet_name': 'Set Name',
            'select_faucet': 0,
            'faucet_name': value,
        }
        self._controller.setup_post(data)

    @property
    def status(self):
        """Return status."""
        return self._lookup_attr('faucet_online')

    @property
    def battery(self):
        """Return faucet battery."""
        return self._lookup_attr('active_faucet_battery_level')

    def update(self):
        """Callback self._controller.update()."""
        self._controller.update()

    # some fields on the backend refers to zone0 as zone1 as well
    # to keep it cohenret and since the frontend refers to zone1
    # we will call it publicly as zone1
    @property
    def zone1_watering_time(self):
        """Return watering_time from zone."""
        return self._lookup_attr('zone_0_watering_time')

    @property
    def zone2_watering_time(self):
        """Return watering_time from zone."""
        return self._lookup_attr('zone_1_watering_time')

    @property
    def zone3_watering_time(self):
        """Return watering_time from zone."""
        return self._lookup_attr('zone_2_watering_time')

    @property
    def zone4_watering_time(self):
        """Return watering_time from zone."""
        return self._lookup_attr('zone_3_watering_time')

    @property
    def zone1_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._lookup_attr('droplet_zone_0'))

    @property
    def zone2_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._lookup_attr('droplet_zone_1'))

    @property
    def zone3_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._lookup_attr('droplet_zone_2'))

    @property
    def zone4_droplet(self):
        """Return droplet URL from zone"""
        return "{0}{1}".format(API_URL, self._lookup_attr('droplet_zone_3'))

    @property
    def zone1_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._lookup_attr('id_zone1_rain_delay_select')

    @property
    def zone2_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._lookup_attr('id_zone2_rain_delay_select')

    @property
    def zone3_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._lookup_attr('id_zone3_rain_delay_select')

    @property
    def zone4_rain_delay(self):
        """Return the rain delay day from zone."""
        return self._lookup_attr('id_zone4_rain_delay_select')

    @property
    def zone1_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._lookup_attr('zone_0_countdown_time')

    @property
    def zone2_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._lookup_attr('zone_1_countdown_time')

    @property
    def zone3_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._lookup_attr('zone_2_countdown_time')

    @property
    def zone4_next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        return self._lookup_attr('zone_3_countdown_time')

    @property
    def zone1_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        return find_program_status(self._parent.html['home'], 'zone1')

    @property
    def zone2_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        return find_program_status(self._parent.html['home'], 'zone2')

    @property
    def zone3_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        return find_program_status(self._parent.html['home'], 'zone3')

    @property
    def zone4_auto_watering(self):
        """Return if zone is configured to automatic watering."""
        return find_program_status(self._parent.html['home'], 'zone4')

    @property
    def zone1_is_watering(self):
        """Return boolean if zone is watering."""
        return bool(self.zone1_watering_time > 0)

    @property
    def zone2_is_watering(self):
        """Return boolean if zone is watering."""
        return bool(self.zone2_watering_time > 0)

    @property
    def zone3_is_watering(self):
        """Return boolean if zone is watering."""
        return bool(self.zone3_watering_time > 0)

    @property
    def zone4_is_watering(self):
        """Return boolean if zone is watering."""
        return bool(self.zone4_watering_time > 0)

    def _set_zone_name(self, zone, name):
        """Private method to override zone name."""
        data = {
            '_set_zone_name': 'Set Name',
            'select_zone': str(zone),
            'zone_name': name,
        }
        self._controller.setup_post(data)

    @property
    def zone1_name(self):
        """Return zone name."""
        return find_zone_name(self._parent.html['home'], 1)

    @zone1_name.setter
    def zone1_name(self, value):
        """Set a new zone name to faucet."""
        self._set_zone_name(0, value)

    @property
    def zone2_name(self):
        """Return zone name."""
        return find_zone_name(self._parent.html['home'], 2)

    @zone2_name.setter
    def zone2_name(self, value):
        """Set a new zone name to faucet."""
        self._set_zone_name(1, value)

    @property
    def zone3_name(self):
        """Return zone name."""
        return find_zone_name(self._parent.html['home'], 3)

    @zone3_name.setter
    def zone3_name(self, value):
        """Set a new zone name to faucet."""
        self._set_zone_name(2, value)

    @property
    def zone4_name(self):
        """Return zone name."""
        return find_zone_name(self._parent.html['home'], 4)

    @zone4_name.setter
    def zone4_name(self, value):
        """Set a new zone name to faucet."""
        self._set_zone_name(3, value)

    @property
    def zone1(self):
        """Return status from zone."""
        return {
            'auto_watering': self.zone1_auto_watering,
            'droplet': self.zone1_droplet,
            'is_watering': self.zone1_is_watering,
            'name': self.zone1_name,
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
            'is_watering': self.zone2_is_watering,
            'name': self.zone2_name,
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
            'is_watering': self.zone3_is_watering,
            'name': self.zone3_name,
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
            'is_watering': self.zone4_is_watering,
            'name': self.zone4_name,
            'next_cycle': self.zone4_next_cycle,
            'rain_delay': self.zone4_rain_delay,
            'watering_time': self.zone4_watering_time,
        }

    @property
    def zones(self):
        """Return a dict from all zones status."""
        zones = {}
        for zone in range(1, 5):
            attr = 'zone{0}'.format(zone)
            zones[attr] = getattr(self, attr)
        return zones

    def prepare_update(self, force_refresh=True):
        """Return a dict with all current options prior submitting request."""
        ddata = MANUAL_OP_DATA.copy()

        # force update to make sure status is accurate
        if force_refresh:
            self.update()

        # select current controller and faucet
        ddata['select_controller'] = \
            self._parent.controllers.index(self._controller)
        ddata['select_faucet'] = self._controller.faucets.index(self)

        # check if zone is scheduled automatically (zone1_program_toggle)
        for zone in range(1, 5):
            attr = 'zone{}_program_toggle'.format(zone)
            attr_opt = 'zone{}_auto_watering'.format(zone)
            if getattr(self, attr_opt) and attr in ddata.keys():
                ddata[attr] = 'on'

        # check if zone current watering manually (zone1_select_manual_mode)
        for zone in range(1, 5):
            attr = 'zone{}_select_manual_mode'.format(zone)
            attr_opt = 'zone{}_watering_time'.format(zone)
            if bool(getattr(self, attr_opt)) and attr in ddata.keys():
                ddata[attr] = getattr(self, attr_opt)

        # check if rain delay is selected (zone0_rain_delay_select)
        for zone in range(0, 4):
            attr = 'zone{}_rain_delay_select'.format(zone)
            attr_opt = 'zone{}_rain_delay'.format(zone + 1)
            value = getattr(self, attr_opt)
            if value and attr in ddata.keys():
                if int(value) >= 2 and int(value) <= 7:
                    value = str(value) + 'days'
                else:
                    value = str(value) + 'day'
                ddata[attr] = value

        return ddata

    def submit(self, ddata):
        """Post data."""
        self._controller.setup_post(ddata, referer=HOME_ENDPOINT)
