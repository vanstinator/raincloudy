# -*- coding: utf-8 -*-
"""Raincloudy helpers."""
from bs4 import BeautifulSoup
from raincloudy.exceptions import RainCloudyException


def generate_soup_html(data):
    """Return an BeautifulSoup HTML parser document."""
    try:
        return BeautifulSoup(data, 'html.parser')
    except:
        raise


def serial_finder(data):
    """
    Find controller serial and faucet_serial from the setup page.

    <select id="id_select_controller2" name="select_controller" >
        <option value='0' selected='selected'>1 - Controller001</option>
    </select>

    :param data: text to be parsed
    :type data: BeautilSoup object
    :return: a dict with controller_serial and faucet_serial
    :rtype: dict
    :raises IndexError: if controller_serial was not found on the data
    """
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautifulSoup HTML element.")

    try:

        # The setup page contains a select box for each controller and each
        # faucet
        controllersElement = data.find_all('select',
                                           {'id': 'id_select_controller2'})

        faucetsElement = data.find_all('select',
                                       {'id': 'id_select_faucet2'})

        controllerSerial = controllersElement[0].text.split('-')[1].strip()
        faucetSerial = faucetsElement[0].text.split('-')[1].strip()

        # currently only one faucet is supported on the code
        # we have plans to support it in the future
        parsed_dict = {}
        parsed_dict['controller_serial'] = controllerSerial
        parsed_dict['faucet_serial'] = [faucetSerial]
        return parsed_dict

    except (AttributeError, IndexError, ValueError):
        raise RainCloudyException(
            'Could not find any valid controller or faucet')


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
    except (AttributeError, IndexError, ValueError):
        raise RainCloudyException(
            'Could not find any valid controller or faucet')


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
        child = data.find('select', {'id': search_field})
        return child.get_text().strip()
    except AttributeError:
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

    table = data.find('table', {'class': 'zone_table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('span', {'class': 'more_info'})
    for row in rows:
        if row.get_text().startswith(str(zone_id)):
            return row.get_text()[4:].strip()
    return None


# vim:sw=4:ts=4:et:
