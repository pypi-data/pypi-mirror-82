Welcome to Open Energy Monitor's Thermostat documentation!
==========================================================

This module provides a Python API to the Open Energy Monitor `Thermostat
<https://shop.openenergymonitor.com/wifi-mqtt-relay-thermostat/>`_. Currently it
only provides enough functionality for external control of the thermostat rather
than providing access to all the configuration options.

This package implements one class `oemthermostat.Thermostat` which provides properties and methods to control the device. Some simple examples are below::

     >>> from oemthermostat import Thermostat
     >>> t = thermostat('192.168.0.1')
     >>> t.setpoint
     21.5
     >>> t.setpoint = 18.6
     >>> t.state
     False
     >>> t.switch()
     >>> t.state
     True


Contents:

.. toctree::
   :maxdepth: 2

   api


.. automodapi:: oemthermostat

