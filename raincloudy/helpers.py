# -*- coding: utf-8 -*-
"""Raincloudy helpers."""
from bs4 import BeautifulSoup
from raincloudy.exceptions import RainCloudyException


def generate_soup_html(data):
    """Return an BeautifulSoup HTML parser document."""
    try:
        return BeautifulSoup(data, 'html5lib')
    except:
        raise TypeError(
            'Invalid data passed to BeautifulSoup')


def faucet_serial_finder(data):
    """
    Find faucet_serial from the setup page.

    <select id="id_select_controller2" name="select_controller" >
        <option value='0' selected='selected'>1 - Controller001</option>
        <option value='1>2 - Controller002</option>
    </select>

    :param data: text to be parsed :type data: BeautilSoup object :return: a
    dict with array of controller_serials and array of faucet_serials
    :raises IndexError: if controller_serial was not found on the data
    """
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautifulSoup HTML element.")

    try:

        faucets_element = data.find(id="id_select_faucet2").find_all('option')

        faucet_serials = []
        for faucet_element in faucets_element:
            faucet_serials.append(faucet_element.text.split('-')[1].strip())

        return faucet_serials

    except (AttributeError, IndexError, ValueError):
        raise RainCloudyException(
            'Could not find any valid controller or faucet')


def controller_serial_finder(data):
    """
    Find all controller serials from the setup page.

    <select id="id_select_controller2" name="select_controller" >
        <option value='0' selected='selected'>1 - Controller001</option>
    </select>

    :param data: text to be parsed
    :type data: BeautilSoup object
    :return: an array of controller serials
    :raises IndexError: if controller_serial was not found on the data
    """

    try:

        controllers_element = data.find(id="id_select_controller2").find_all(
            'option')

        controller_serials = []

        for controller_element in controllers_element:
            controller_serials.append(
                controller_element.text.split('-')[1].strip())

        return controller_serials

    except (AttributeError, IndexError, ValueError):
        raise RainCloudyException(
            'Could not find any valid controller serials')


def find_controller_or_faucet_name(data, p_type, index=0):
    """
    Find on the HTML document the controller name.

    # expected result
    <label for="select_controller">
     <span class="more_info" id="#styling-type-light" data-hasqtip="26" \
     title="Select Control Unit to display." >Control Unit:</span></label><br/>
     <select class="simpleselect" id="id_select_controller" \
       name="select_controller" onchange="submit()" >
          <option value="0" selected="selected">HERE_IS_CONTROLLER_NAME

    :param index: The index of the element we're parsing
    :param data: BeautifulSoup object
    :param p_type: parameter type. (controller or faucet)
    :return: controller or valve name
    :rtype: string.
    :raises TypeError: if data is not a BeautifulSoup object
    :raises IndexError: return None because controller name was not found
    """
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautilSoup HTML element.")

    if p_type not in ('controller', 'faucet'):
        raise TypeError("Function p_type must be controller or faucet")

    try:
        search_field = 'id_select_{0}'.format(p_type)
        child = data.find(id=search_field).findAll('option')

        parsed_text = child[index].text.strip()

        return parsed_text
    except AttributeError:
        return None


def find_zone_name(data, zone_id):
    """
    Find on the HTML document the zone name.

    # expected result
    <span class="more_info" \
        title="Zone can be renamed on Setup tab">1 - zone1</span>,

    :param zone_id:
    :param data: BeautifulSoup object
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
            zone_name = row.get_text()[4:].strip()
            if zone_name != '':
                return row.get_text()[4:].strip()

            return 'Zone {0}'.format(zone_id)
    return None


def find_selected_controller_or_faucet_index(data, p_type):
    """
    Find the currently selected controller index from the home html
    :param p_type: parameter type. (controller or faucet)
    :param data: BeautifulSoup object
    :return: controller index
    """

    entity_index = None
    if not isinstance(data, BeautifulSoup):
        raise TypeError("Function requires BeautilSoup HTML element.")

    if p_type not in ('controller', 'faucet'):
        raise TypeError("Function p_type must be controller or faucet")

    try:
        search_field = 'id_select_{0}'.format(p_type)
        child = data.find(id=search_field).findAll('option')

        for index, option in enumerate(child):
            if "selected" in str(option):
                entity_index = index

    except AttributeError:
        pass

    return entity_index
# vim:sw=4:ts=4:et:
