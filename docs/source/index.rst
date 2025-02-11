knmy - A simple Python wrapper for Dutch weather data from KNMI
===============================================================
.. image:: https://github.com/barthoekstra/knmy/actions/workflows/python-app.yml/badge.svg?branch=master
    :target: https://github.com/barthoekstra/knmy/actions/workflows/python-app.yml
.. image:: https://coveralls.io/repos/github/barthoekstra/knmy/badge.svg?branch=master
    :target: https://coveralls.io/github/barthoekstra/knmy?branch=master
.. image:: https://readthedocs.org/projects/knmy/badge/?version=latest
    :target: http://knmy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://badge.fury.io/py/knmy.svg
    :target: https://badge.fury.io/py/knmy

knmy is a Python package for downloading and processing weather data from the automated weather stations of the Dutch
Meteorological Institute (KNMI). Documentation of the used API can be
`found here <https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script>`_ (only in Dutch).

Contents
--------

.. toctree::
   :maxdepth: 2

   License <license>
   Authors <authors>
   Changelog <changelog>

Usage
-----

The main function is ``get_knmi_data()``, which requires at minimum a ``type`` (first argument) to function. You can choose
from:

1. ``type = 'daily'``, which returns the daily aggregate weather data of all selected weather variables.
2. ``type = 'hourly'``, which returns the hourly aggregate weather data of all selected weather variables.
3. ``type = 'daily_rain'``, which always returns only the daily rain and snow cover data.

For convenience you have access to three wrapper functions that correspond to each of the aforementioned types:
``get_daily_data()``, ``get_hourly_data()`` and ``get_daily_rain_data()``

Example usage
-------------
.. code-block:: python

   from knmy import knmy

   # Return daily aggregated wind, temperature and sunshine duration data for station 209 (IJmond) for the 1st til
   # 6th of January, 2017
   knmy.get_daily_data(stations=[209], start=20170101, end=20170106, variables=['WIND','TEMP', 'SQ'])

   # Return dataframe with hourly wind and temperature data for station 209 (IJmond) and 235 (De Kooy) for the 1st
   # til 6th of January of the years 2015 til 2017 for the 8th til 20th hour of the day
   disclaimer, stations, variables, data = knmy.get_hourly_data(stations=[209, 235], start=2015010108, end=2017010620,
                                                                inseason=True, variables=['WIND', 'TEMP'], parse=True)

   # Return dataframe with daily rain data for all stations for January 1st, 2017
   disclaimer, variables, data = knmy.get_daily_rain_data(start=20170101, end=20170101, parse=True)


Function parameters
-------------------
``stations`` should contain a list of weather station numbers. To find out which weather stations are available for use,
use the function without setting any `stations` (but with a ``start`` and ``end`` set), the function will then return a
variable ``stations`` which contains a list of stations for which data is available for that period.

``start`` and ``end`` are either an integer or ``datetime`` object (``datetime.date`` for ``get_daily_data`` and
``datetime.datetime`` for ``get_hourly_data``. If hourly data is requested, data is always returned starting from the
hour set in ``start`` until the hour set in ``end``. In case an integer is provided, make sure the first hour of the day
(00:00-01:00) is hour 1 and the last hour of the day (23:00-24:00) is hour 24. To request overnight data — such as from
22:00 til 06:00 the next morning — use for example ``start=2017010123`` and ``end=2017010507``.

``variables`` should contain a list of variables, and if none are specified returns all recorded variables. Variables
can be selected individually, but also in the groups below. If you are unsure of the available variables, use one of the
functions without providing variables and read the unpacked list of variables (see `Example usage`_).

Variable groups:
-----------------
^^^^^^^^^^^
Daily Data
^^^^^^^^^^^
* ``ALL`` =  All  variables (**Default**)
* ``WIND`` = DDVEC:FG:FHX:FHX:FX Wind
* ``TEMP`` = TG:TN:TX:T10N Temperature
* ``SUNR`` = SQ:SP:Q Sunshine
* ``PRCP`` = DR:RH:EV24 Precipitation and potential evaporation
* ``PRES`` = PG:PGX:PGN Pressure at sea level
* ``VICL`` = VVN:VVX:NG Visibility and cloud cover
* ``MSTR`` = UG:UX:UN Humidity

^^^^^^^^^^^
Hourly Data
^^^^^^^^^^^

* ``WIND`` = DD:FH:FF:FX Wind
* ``TEMP`` = T:T10N:TD Temperature
* ``SUNR`` = SQ:Q Sunshine duration and global radiation
* ``PRCP`` = DR:RH Precipitation and potential evaporation
* ``VICL`` = VV:N:U Visibility, cloud cover and relative humidity
* ``WEATHER`` = M:R:S:O:Y:WW Weather phenomena, weather types
* ``ALL`` = all variables

``inseason`` is a boolean. If set to `True`, the function will only return data within the month-date combination for
all given years (see `Example usage`_).

``parse`` is a boolean. If set to `True`, the function will parse the KNMI output data and return a `disclaimer`,
measured `variables`, `data` and a list of `stations`.

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
