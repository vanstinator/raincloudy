# -*- coding: utf-8 -*-
"""RainCloud Faucet."""
from raincloudy.const import (
    HOME_ENDPOINT, MANUAL_OP_DATA, MANUAL_WATERING_ALLOWED,
    MAX_RAIN_DELAY_DAYS, MAX_WATERING_MINUTES)
from raincloudy.helpers import (
    find_controller_or_faucet_name,
    find_program_status, find_zone_name)


class RainCloudyFaucetCore(object):
    """RainCloudyFaucetCore object."""

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

        # zones associated with faucet
        self.zones = []

        # load assigned zones
        self._assign_zones()

    def _assign_zones(self):
        """Assign all RainCloudyFaucetZone managed by faucet."""
        for zone_id in range(1, 5):
            zone = \
                RainCloudyFaucetZone(
                    parent=self._parent,
                    controller=self._controller,
                    faucet=self,
                    zone_id=zone_id)

            if zone not in self.zones:
                self.zones.append(zone)

    def __repr__(self):
        """Object representation."""
        try:
            return "<{0}: {1}>".format(self.__class__.__name__, self.name)
        except AttributeError:
            return "<{0}: {1}>".format(self.__class__.__name__, self.id)

    @property
    def _attributes(self):
        """Callback to self._controller attributes."""
        return self._controller.attributes

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
    def current_time(self):
        """Return controller current time."""
        return self._controller.current_time

    @property
    def name(self):
        """Return faucet name."""
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
        self._controller.post(data)

    @property
    def status(self):
        """Return status."""
        return self._attributes['faucet_status']

    @property
    def battery(self):
        """Return faucet battery."""
        battery = self._attributes['battery_percent']
        if battery == '' or battery is None:
            return None
        return battery.strip('%')

    def update(self):
        """Callback self._controller.update()."""
        self._controller.update()

    def _find_zone_by_id(self, zone_id):
        """Return zone by id."""
        if not self.zones:
            return None

        zone = list(filter(
            lambda zone: zone.id == zone_id, self.zones))

        return zone[0] if zone else None


class RainCloudyFaucet(RainCloudyFaucetCore):
    """RainCloudyFaucet object."""

    @property
    def zone1(self):
        """Return zone managed by faucet."""
        return self._find_zone_by_id(1)

    @property
    def zone2(self):
        """Return zone managed by faucet."""
        return self._find_zone_by_id(2)

    @property
    def zone3(self):
        """Return zone managed by faucet."""
        return self._find_zone_by_id(3)

    @property
    def zone4(self):
        """Return zone managed by faucet."""
        return self._find_zone_by_id(4)


class RainCloudyFaucetZone(RainCloudyFaucetCore):
    """RainCloudyFaucetZone object."""

    # pylint: disable=super-init-not-called
    # needs review later
    def __init__(self, parent, controller, faucet, zone_id):
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

    def __repr__(self):
        """Object representation."""
        try:
            return "<{0}: {1}>".format(self.__class__.__name__, self.name)
        except AttributeError:
            return "<{0}: {1}>".format(self.__class__.__name__, self.id)

    def _set_zone_name(self, zoneid, name):
        """Private method to override zone name."""
        # zone starts with index 0
        zoneid -= 1
        data = {
            '_set_zone_name': 'Set Name',
            'select_zone': str(zoneid),
            'zone_name': name,
        }
        self._controller.post(data)

    @property
    def name(self):
        """Return zone name."""
        return find_zone_name(self._parent.html['home'], self.id)

    @name.setter
    def name(self, value):
        """Set a new zone name to faucet."""
        self._set_zone_name(self.id, value)

    def _set_watering_time(self, zoneid, value):
        """Private method to set watering_time per zone."""
        if value not in MANUAL_WATERING_ALLOWED:
            raise ValueError(
                'Valid options are: {}'.format(
                    ', '.join(map(str, MANUAL_WATERING_ALLOWED)))
            )

        if isinstance(value, int) and value == 0:
            value = 'OFF'
        elif isinstance(value, str):
            value = value.upper()
            if value == 'ON':
                value = MAX_WATERING_MINUTES

        ddata = self.preupdate()
        attr = 'zone{}_select_manual_mode'.format(zoneid)
        ddata[attr] = value
        self.submit_action(ddata)

    @property
    def watering_time(self):
        """Return watering_time from zone."""
        # zone starts with index 0
        index = self.id - 1
        return self._attributes['rain_delay_mode'][index]['auto_watering_time']

    @watering_time.setter
    def watering_time(self, value):
        """Manually turn on water for X minutes."""
        return self._set_watering_time(self.id, value)

    @property
    def droplet(self):
        return None

    def _set_rain_delay(self, zoneid, value):
        """Generic method to set auto_watering program."""
        # current index for rain_delay starts in 0
        zoneid -= 1

        if isinstance(value, int):
            if value > MAX_RAIN_DELAY_DAYS or value < 0:
                return None
            elif value == 0:
                value = 'off'
            elif value == 1:
                value = '1day'
            elif value >= 2:
                value = str(value) + 'days'
        elif isinstance(value, str):
            if value.lower() != 'off':
                return None

        ddata = self.preupdate()
        attr = 'zone{}_rain_delay_select'.format(zoneid)
        ddata[attr] = value
        self.submit_action(ddata)
        return True

    @property
    def rain_delay(self):
        """Return the rain delay day from zone."""
        index = self.id - 1
        return self._attributes['rain_delay_mode'][index]['rain_delay_mode']

    @rain_delay.setter
    def rain_delay(self, value):
        """Set number of rain delay days for zone."""
        return self._set_rain_delay(self.id, value)

    @property
    def next_cycle(self):
        """Return the time scheduled for next watering from zone."""
        index = self.id - 1
        return self._attributes['rain_delay_mode'][index]['next_water_cycle']

    def _set_auto_watering(self, zoneid, value):
        """Private method to set auto_watering program."""
        if not isinstance(value, bool):
            return None

        ddata = self.preupdate()
        attr = 'zone{}_program_toggle'.format(zoneid)
        try:
            if not value:
                ddata.pop(attr)
            else:
                ddata[attr] = 'on'
        except KeyError:
            pass
        self.submit_action(ddata)
        return True

    @property
    def auto_watering(self):
        """Return if zone is configured to automatic watering."""
        value = "zone{}".format(self.id)
        return find_program_status(self._parent.html['home'], value)

    @auto_watering.setter
    def auto_watering(self, value):
        """Enable/disable zone auto_watering program."""
        return self._set_auto_watering(self.id, bool(value))

    @property
    def is_watering(self):
        """Return boolean if zone is watering."""
        return bool(self.watering_time > 0)

    def _to_dict(self):
        """Method to build zone dict."""
        return {
            'auto_watering':
                getattr(self, "auto_watering"),
            'droplet':
                getattr(self, "droplet"),
            'is_watering':
                getattr(self, "is_watering"),
            'name':
                getattr(self, "name"),
            'next_cycle':
                getattr(self, "next_cycle"),
            'rain_delay':
                getattr(self, "rain_delay"),
            'watering_time':
                getattr(self, "watering_time"),
        }

    def report(self):
        """Return status from zone."""
        return self._to_dict()

    def preupdate(self, force_refresh=True):
        """Return a dict with all current options prior submitting request."""
        ddata = MANUAL_OP_DATA.copy()

        # force update to make sure status is accurate
        if force_refresh:
            self.update()

        # select current controller and faucet
        ddata['select_controller'] = \
            self._parent.controllers.index(self._controller)
        ddata['select_faucet'] = \
            self._controller.faucets.index(self._faucet)

        # check if zone is scheduled automatically (zone1_program_toggle)
        # only add zoneX_program_toogle to ddata when needed,
        # otherwise the field will be always on
        for zone in self._faucet.zones:
            attr = 'zone{}_program_toggle'.format(zone.id)
            if zone.auto_watering:
                ddata[attr] = 'on'

        # check if zone current watering manually (zone1_select_manual_mode)
        for zone in self._faucet.zones:
            attr = 'zone{}_select_manual_mode'.format(zone.id)
            if zone.watering_time and attr in ddata.keys():
                ddata[attr] = zone.watering_time

        # check if rain delay is selected (zone0_rain_delay_select)
        for zone in self._faucet.zones:
            attr = 'zone{}_rain_delay_select'.format(zone.id - 1)
            value = zone.rain_delay
            if value and attr in ddata.keys():
                if int(value) >= 2 and int(value) <= 7:
                    value = str(value) + 'days'
                else:
                    value = str(value) + 'day'
                ddata[attr] = value

        return ddata

    def submit_action(self, ddata):
        """Post data."""
        self._controller.post(ddata,
                              url=HOME_ENDPOINT,
                              referer=HOME_ENDPOINT)
