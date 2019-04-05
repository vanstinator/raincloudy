# -*- coding: utf-8 -*-
"""Constants used by RainCloudy."""

API_URL = 'https://wifiaquatimer.com'
STATUS_ENDPOINT = API_URL + '/get_cu_and_fu_status'
HOME_ENDPOINT = API_URL + '/home'
LOGIN_ENDPOINT = API_URL + '/login/'
SETUP_ENDPOINT = API_URL + '/setup/'
PROGRAM_ENDPOINT = API_URL + '/program/'
MANAGE_ENDPOINT = API_URL + '/manage/'
LOGOUT_ENDPOINT = API_URL + '/logout'

MAX_RAIN_DELAY_DAYS = 7
MAX_WATERING_MINUTES = 60
MANUAL_WATERING_ALLOWED = \
    ['on', 'ON', 'off', 'OFF', 0, 5, 10, 15, 30, 45, 60]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) \
                  Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml, \
               application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': HOME_ENDPOINT,
}

# initial structured used to acquire token
INITIAL_DATA = {
    'csrfmiddlewaretoken': None,
    'email': None,
    'password': None,
    '_login': 'Login',
}

# structure used to manual operation like
# enable faucet X with zone1 for 5 minutes
MANUAL_OP_DATA = {
    'select_controller': None,
    'select_faucet': None,

    # manual operation
    'zone1_select_manual_mode': 'OFF',
    'zone2_select_manual_mode': 'OFF',
    'zone3_select_manual_mode': 'OFF',
    'zone4_select_manual_mode': 'OFF',

    # rain delay - zone0 is not a typo.
    'zone0_rain_delay_select': 'off',
    'zone1_rain_delay_select': 'off',
    'zone2_rain_delay_select': 'off',
    'zone3_rain_delay_select': 'off',
}

# vim:sw=4:ts=4:et:
