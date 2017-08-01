RainCloudy
==========

.. image:: https://badge.fury.io/py/raincloudy.svg
    :target: https://badge.fury.io/py/raincloudy

.. image:: https://travis-ci.org/tchellomello/raincloudy.svg?branch=master
    :target: https://travis-ci.org/tchellomello/raincloudy

.. image:: https://coveralls.io/repos/github/tchellomello/raincloudy/badge.svg?branch=master
    :target: https://coveralls.io/github/tchellomello/raincloudy?branch=master

.. image:: https://img.shields.io/pypi/pyversions/raincloudy.svg
   :target: https://pypi.python.org/pypi/raincloudy


RainCloudy is a library written in Python 2.7/3.x that manages the Melnor RainCloud Smart Garden Watering Irrigation Timer.

*Currently Melnor WifiAquaTimer not provide an official API. The results of this project are merely from reverse engineering.*

Melnor RainCloud Youtube video: `https://goo.gl/Y5kx1X`

Usage
-----

.. code-block:: python

    from raincloudy.core import RainCloudy
    raincloudy = RainCloudy('username@domain', 'secret')

    # list controllers linked with account
    raincloudy.controllers
    [<RainCloudyController: control_unit:abdcd1234 valve_unit:a123>]

    # show valve unit battery status
    raincloudy.controller.faucet_battery
    99%

    # show status
    raincloudy.controller.status
    'Online'

    raincloudy.controller.faucet_status
    'Online'

    # controlled total zones
    len(raincloudy.controller.zones)
    4

    # show details from zone1
    raincloudy.controller.zone1
    {'auto_watering': True,
     'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
     'next_cycle': 'Delayed',
     'rain_delay': 1,
     'watering_time': 0}

     # update attributes and show all zones
     raincloudy.update()
     raincloudy.controller.zones
     {
        'zone1': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'next_cycle': 'Delayed',
            'rain_delay': 1,
            'watering_time': 0
        },
        'zone2': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'next_cycle': 'Delayed',
            'rain_delay': 2,
            'watering_time': 0
        },
        'zone3': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'next_cycle': '3:17 AM',
            'rain_delay': 0,
            'watering_time': 0
        },
        'zone4': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'next_cycle': '4:00 AM',
            'rain_delay': 0,
        'watering_time': 0
        }
    }
