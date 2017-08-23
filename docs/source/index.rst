.. RainCloudy documentation master file, created by
   sphinx-quickstart on Wed Aug 23 01:21:34 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to RainCloudy's documentation!
======================================
RainCloudy is a library written in Python 2.7/3.x that manages the Melnor RainCloud Smart Garden Watering Irrigation Timer.

Currently Melnor WifiAquaTimer not provide an official API. The results of this project are merely from reverse engineering. This project does not have any official relationship or support by Melnor.com. Use it at your own risk.

.. note::
    Melnor RainCloud official page: http://www.melnor.com/16043-raincloud-smart-water-timer

    Melnor RainCloud Youtube video: https://goo.gl/Y5kx1X

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Developing
==========

.. autoclass:: raincloudy.core.RainCloudy
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: raincloudy.controller.RainCloudyController
    :members:
    :undoc-members:
    :show-inheritance:

Faucet.py
--------
.. autoclass:: raincloudy.faucet.RainCloudyFaucetCore
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: raincloudy.faucet.RainCloudyFaucet
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: raincloudy.faucet.RainCloudyFacuetZone
    :members:
    :undoc-members:
    :show-inheritance:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
