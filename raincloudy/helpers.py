# -*- coding: utf-8 -*-
"""Raincloudy helpers."""
import re
from bs4 import BeautifulSoup


def generate_soup_html(data):
    """Return an BeautifulSoup HTML parser document."""
    try:
        return BeautifulSoup(data, 'html.parser')
    except:
        raise


def serial_finder(data):
    """
    Find controller serial and faucet_serial from the initial page.

    :param data: text to be parsed
    :type data: BeautilSoup object
    :return: a dict with controller_serial and faucet_serial
    :rtype: dict
    :raises IndexError: if controller_serial was not found on the data

    Many thanks to Pablo Hess <pablo@hess.net.br> for the regex filter
    """
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautilSoup HTML element.")

    try:
        child = data.find_all('script',
                              text=re.compile('controller_serial'))[0]

        # pylint: disable=line-too-long
        regex = re.compile(r"controller_serial':\s*'(?P<controller_serial>\w*)',\s*'faucet_serial':\s*'(?P<faucet_serial>\w*)'") # noqa
        return regex.search(child.string).groupdict()

    except IndexError:
        raise "Could not find expression."


def find_attr(data, key):
    """
    Find attribute based on a given key.
    self._attributes has a dict list with objects
    To acquire the current data, the dict must have ['cmd'] = 'as'

    :param data: list of BeautifulSoup objects
    :param key: html object identifier
    :return: html object value
    :rtype: str
    :raises TypeError: if data is not a list
    """
    if not isinstance(data, list):
        raise TypeError("Data must be a list.")

    if not key.startswith('#'):
        key = '#' + key

    for member in data:
        if member.get('cmd') == 'as' and member.get('id') == key:
            return member.get('val')
    return None


def find_program_status(data, zone):
    """
    Find on the HTML document if zoneX has the configuration
    of the auto-schedule/program (auto_watering) enabled.

    # expected result if enabled
    #<input checked="checked" class="switch" id="id_zone2_program_toggle" \
        name="zone2_program_toggle" onchange="submit()" type="checkbox"/>

    # expected result if disabled
    #<input class="switch" id="id_zone1_program_toggle" \
        name="zone1_program_toggle" onchange="submit()" type="checkbox"/>

    :param data: BeautifulSoup object
    :param zone: zone name from class='switch'
    :return: boolean if zone has program enabled
    :rtype: boolean
    :raises TypeError: if data is not a BeautifulSoup object
    :raises IndexError: if object not found
    """
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautilSoup HTML element.")

    try:
        child = data.find_all('input', {'class': 'switch'})
        zone_id = 'id_{0}_program_toggle'.format(zone)
        for member in child:
            if member.get('type') == 'checkbox' and \
               member.get('id') == zone_id:
                return bool(member.has_attr('checked'))
        raise IndexError
    except IndexError:
        raise "Could not find expression."


def find_controller_or_faucet_name(data, p_type):
    """
    Find on the HTML document the controller name.

    # expected result
    <label for="select_controller">
     <span class="more_info" id="#styling-type-light" data-hasqtip="26" \
     title="Select Control Unit to display." >Control Unit:</span></label><br/>
     <select class="simpleselect" id="id_select_controller" \
       name="select_controller" onchange="submit()" >
          <option value="0" selected="selected">HERE_IS_CONTROLLER_NAME

    :param data: BeautifulSoup object
    :param p_type: parameter type. (controller or faucet)
    :return: controller or valve name
    :rtype: string.
    :raises TypeError: if data is not a BeautifulSoup object
    :raises IndexError: return None because controller name was not found
    """
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautilSoup HTML element.")

    if not (p_type == 'controller' or p_type == 'faucet'):
        raise TypeError("Function p_type must be controller or faucet")

    try:
        search_field = 'id_select_{0}'.format(p_type)
        child = data.find_all('select', {'id': search_field})[0]
        return child.get_text().strip()
    except IndexError:
        return None


def find_zone_name(data, zone_id):
    """
    Find on the HTML document the zone name.

    # expected result
    <span class="more_info" \
        title="Zone can be renamed on Setup tab">1 - zone1</span>,

    :param data: BeautifulSoup object
    :param zone: zone id
    :return: zone name
    :rtype: string
    :raises TypeError: if data is not a BeautifulSoup object
    :raises IndexError: return None because controller name was not found
    """
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautilSoup HTML element.")

    try:
        table = data.find('table', {'class': 'zone_table'})
        table_body = table.find('tbody')
        rows = table_body.find_all('span', {'class': 'more_info'})
        for row in rows:
            if row.get_text().startswith(str(zone_id)):
                return row.get_text()[4:].strip()
        return None
    except IndexError:
        return None


# vim:sw=4:ts=4:et:
