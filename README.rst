RainCloudy
==========

.. image:: https://badge.fury.io/py/raincloudy.svg
    :target: https://badge.fury.io/py/raincloudy

.. image:: https://travis-ci.org/tchellomello/raincloudy.svg?branch=master
    :target: https://travis-ci.org/tchellomello/raincloudy

.. image:: https://coveralls.io/repos/github/tchellomello/raincloudy/badge.svg?branch=master
    :target: https://coveralls.io/github/tchellomello/raincloudy?branch=master


RainCloudy is a library written in Python 2.7/3.x that manages the Melnor RainCloud Smart Garden Watering Irrigation Timer.

*Currently Melnor WifiAquaTimer not provide an official API. The results of this project are merely from reverse engineering. This project does not have any official relationship or support by Melnor.com. Use it at your own risk.*

Melnor RainCloud official page: `http://www.melnor.com/16043-raincloud-smart-water-timer`

Melnor RainCloud Youtube video: `https://goo.gl/Y5kx1X`

Source code documentation: `http://raincloudy.readthedocs.io/ <http://raincloudy.readthedocs.io/>`_

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

    raincloudy.controller.name
    'MelnorC001'

    raincloudy.controller.faucet.name
    'Backyard'

    raincloudy.controller.faucet.status
    'Online'

    # 4 zones controlled per faucet
    len(raincloudy.controller.faucet.zones)
    4

    # show details from zone1
    raincloudy.controller.faucet.zone1
    {'auto_watering': True,
     'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
     'next_cycle': 'Delayed',
     'rain_delay': 1,
     'watering_time': 0}

     # update attributes and show all zones
     raincloudy.controller.update()
     raincloudy.controller.faucet.zones
     {
        'zone1': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'is_watering': False,
            'next_cycle': 'Delayed',
            'name': 'Backyard Flowers',
            'rain_delay': 1,
            'watering_time': 0
        },
        'zone2': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'is_watering': False,
            'next_cycle': 'Delayed',
            'name': 'Tree Patio',
            'rain_delay': 2,
            'watering_time': 0
        },
        'zone3': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'is_watering': False,
            'next_cycle': '3:17 AM',
            'name': 'Grass Backyard',
            'rain_delay': 0,
            'watering_time': 0
        },
        'zone4': {
            'auto_watering': True,
            'droplet': 'https://wifiaquatimer.com/static/images/blank.gif',
            'is_watering': False,
            'next_cycle': '4:00 AM',
            'name': 'Grass Front yard',
            'rain_delay': 0,
            'watering_time': 0
        }
    }


    # set faucet name
    raincloudy.controller.faucet.name = 'Outside Left'
    raincloudy.controller.faucet.name
    'Outside Left'

    # enable automatic program for zone1
    raincloudy.controller.faucet.zone1.auto_watering = True

    # run water for 15 minutes on zone3
    raincloudy.controller.faucet.zone3.watering_time = 15

    # set rain delay for 2 days on zone2
    raincloudy.controller.faucet.zone2.rain_delay = 2


Current Limitations
------------
- Only 1 (one) controller is supported.
- Only 1 (one) valve unit is supported.
