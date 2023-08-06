HTTP API
========

The following documents the HTTP API of the thermostat / relay device. This was
discovered by reading the original source code for the ESP8266 and using the dev
tools in Firefox to inspect the calls in the web interface.

.. note::
    This is incomplete, I will add more as I research it.

.. http:get:: /control/thermostat.cgi?param=state

   Get the status of the thermostat.

   :parameter param=state: Request state of the thermostat.

   **Example request**:

   .. sourcecode:: http

      GET /control/thermostat.cgi?param=state HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
       "temperature": "22.81",
       "humidity": "N/A",
       "humidistat": 0,
       "relay1state": 0,
       "relay1name":"Heating",
       "state":2,
       "manualsetpoint": 1900,
       "heat_cool":0
      }


   :statuscode 200: no error


.. http:post:: /control/thermostat.cgi?param=thermostat_state

    Set operation mode of the thermostat.

    :parameter param=thermostat_state: Set thermostat operation mode.
    :form: 0 - off, 1 - schedule, 2 - manual


.. http:post:: /control/thermostat.cgi?param=thermostat_manualsetpoint

   Set target temperature of thermostat.

   :form int: Temperature in 1/100 C.


.. http:post:: /control/thermostat.cgi?param=thermostat_heat_cool

   :form: 0 - heating, 1 - cooling


.. http:post:: /control/thermostat.cgi?param=thermostat_schedule

   Set scheduled setpoint.

   **Example request**:

   .. sourcecode:: http

      POST /control/thermostat.cgi?param=thermostat_schedule HTTP/1.1
      Accept: application/json

      {"mon":
       [
        {"s": 0,
        "e": 2400,
        "sp": 2100
       ]
      }

.. http:get:: /control/relay.cgi?relay1=(int:state)

   Change the current state of the relay.

   :parameter relay1: 0 - off, 1 - on
