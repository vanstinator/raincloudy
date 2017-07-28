# -*- coding: utf-8 -*-
"""Constants used by RainCloudy."""

API_URL = 'https://wifiaquatimer.com'
DAJAXICE_ENDPOINT = API_URL + '/dajaxice/webserver.get_cu_and_fu_status/'
HOME_ENDPOINT = API_URL + '/home'
LOGIN_ENDPOINT = API_URL + '/login/'

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

# vim:sw=4:ts=4:et:
