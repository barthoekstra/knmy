# -*- coding: utf-8 -*-

import requests
import datetime
from knmy.parser import parse_raw_rain_data, parse_raw_weather_data

__title__ = 'knmy'
__version__ = '1.5.1'
__author__ = 'Bart Hoekstra'
__license__ = 'MIT'


def get_knmi_data(type, stations=None, start=None, end=None, variables=None, inseason=None, parse=None):
    """ Downloads and returns KNMI weather data

    Downloads daily, hourly or daily rain weather data from KNMI's automated weather stations, using the API
    documented here: https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script (Dutch).

    Args:
        type: (string) data type, either 'daily', 'hourly', or 'rain_daily', corresponding with respectively all
            daily accumulated weather data, hourly weather data and accumulated rain data.
        stations: (list) weather station IDs
        start: (datetime, int) starting datetime. When providing an integer, make sure format is:
            yyyymmdd when type is 'daily' and 'rain_daily'
            yyyymmddhh when type is 'hourly'
        end: (datetime, int) ending datetime. When providing an integer, make sure format is:
            yyyymmdd when type is 'daily' and 'rain_daily'
            yyyymmddhh when type is 'hourly'
        variables: (list) variables. See API documentation for available variable sets for each data type
        inseason: (boolean) setting to True makes function return only seasonal data. The season from which to
            fetch the data is now defined by the starting and ending month-day combinations, resulting in a dataset
            that only contains weather data in between starting and ending month-day combinations for each of the
            years in between starting and ending years. So if inseason is True the following result will fetch all
            data from January 1st to March 15th for each year in the range 2005-2012: start: 20050101, end: 20120315
        parse (boolean) function returns parsed data if set to true

    Returns:
        If parse is not set the function returns the raw output of the API request.

        If parse is set to True, the function parses the API request and returns the following:
            disclaimer: (string) KNMI data disclaimer
            stations: (DataFrame) pandas dataframe containing for all stations: name, number, latitude, longitude and
                altitude
            variables: (dict): dictionary of namedtuples containing the variables and corresponding columns and
                descriptions
            data: (DataFrame) pandas dataframe containing the weather measurements for all selected variables (see the
                returned variables dictionary), but always a station number and date in YYYYMMDD format.

        Unpack output as follows:
            disclaimer, stations, variables, data = get_knmi_data(...)
    """
    urls = {'daily': 'https://www.daggegevens.knmi.nl/klimatologie/daggegevens',
            'hourly': 'https://www.daggegevens.knmi.nl/klimatologie/uurgegevens',
            'daily_rain': 'https://www.daggegevens.knmi.nl/klimatologie/monv/reeksen'}

    if stations is not None:
        params = dict(stns=':'.join(str(station) for station in stations))
    else:
        params = dict(stns='ALL')

    if start is not None:

        if not isinstance(start, str):

            if type == 'hourly':
                if isinstance(start, datetime.datetime):
                    hour = str(start.hour + 1)  # 0h00m is in the 1st hour, so increase by 1 for API
                    if len(hour) < 2:
                        hour = '0' + hour
                    date = start.strftime('%Y%m%d')
                    start = date + hour
                elif isinstance(start, int):
                    if len(str(start)) != 10:
                        raise ValueError('start should have the following format: yyyymmddhh')
                    start = str(start)
                else:
                    raise ValueError('start should be an int (format: yyyymmddhh) or datetime object')

            else:
                if isinstance(start, datetime.datetime) or isinstance(end, datetime.date):
                    start = start.strftime('%Y%m%d')
                elif isinstance(start, int):
                    if len(str(start)) != 8:
                        raise ValueError('start should have the following format: yyyymmdd')
                    start = str(start)
                else:
                    raise ValueError('start should be an int (format: yyyymmdd) or datetime object')

        params.update(start=start)

    if end is not None:

        if not isinstance(end, str):

            if type == 'hourly':
                if isinstance(end, datetime.datetime):
                    hour = str(end.hour + 1)  # 0h00m is in the 1st hour, so increase by 1 for API
                    if len(hour) < 2:
                        hour = '0' + hour
                    date = end.strftime('%Y%m%d')
                    end = date + hour
                elif isinstance(end, int):
                    if len(str(end)) != 10:
                        raise ValueError('end should have the following format: yyyymmddhh')
                    end = str(end)
                else:
                    raise ValueError('end should be an int (format: yyyymmddhh) or datetime object')

            else:
                if isinstance(end, datetime.datetime) or isinstance(end, datetime.date):
                    end = end.strftime('%Y%m%d')
                elif isinstance(end, int):
                    if len(str(end)) != 8:
                        raise ValueError('end should have the following format: yyyymmdd')
                    end = str(end)
                else:
                    raise ValueError('end should be an int (format: yyyymmdd) or datetime object')

        params.update(end=end)

    if inseason is True:
        params.update(inseason='Y')

    if variables is not None:
        params.update(vars=':'.join(variables))
    else:
        params.update(vars='ALL')

    r = requests.post(url=urls[type], data=params)

    if r.status_code != 200:
        raise requests.HTTPError(r.status_code, urls[type], params)

    if parse:
        if type != 'daily_rain':
            return parse_raw_weather_data(r.text)
        else:
            return parse_raw_rain_data(r.text)
    else:
        return r.text


def get_daily_data(stations=None, start=None, end=None, variables=None, inseason=None, parse=None):
    """ Downloads and returns KNMI daily weather data

    Downloads daily weather data from KNMI's automated weather stations, using the API documented here:
    https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script (Dutch).

    Args:
        stations: (list) weather station IDs
        start: (datetime, int) starting datetime. When providing an integer, make sure format is: yyyymmdd
        end: (datetime, int) ending datetime. When providing an integer, make sure format is: yyyymmdd
        variables: (list) variables. See API documentation for available variable sets for each data type
        inseason: (boolean) setting to True makes function return only seasonal data. The season from which to
            fetch the data is now defined by the starting and ending month-day combinations, resulting in a dataset
            that only contains weather data in between starting and ending month-day combinations for each of the
            years in between starting and ending years. So if inseason is True the following result will fetch all
            data from January 1st to March 15th for each year in the range 2005-2012: start: 20050101, end: 20120315
        dataframe (boolean) function returns a pandas dataframe if set to true

    Returns:
        If parse is not set the function returns the raw output of the API request.

        If parse is set to True, the function parses the API request and returns the following:
            disclaimer: (string) KNMI data disclaimer
            stations: (DataFrame) pandas dataframe containing for all stations: name, number, latitude, longitude and
                altitude
            variables: (dict): dictionary of namedtuples containing the variables and corresponding columns and
                descriptions
            data: (DataFrame) pandas dataframe containing the weather measurements for all selected variables (see the
                returned variables dictionary), but always a station number and date in YYYYMMDD format.

        Unpack output as follows:
            disclaimer, stations, variables, data = get_daily_data(...)

    """
    return get_knmi_data('daily', stations=stations, start=start, end=end, variables=variables, inseason=inseason,
                         parse=parse)


def get_hourly_data(stations=None, start=None, end=None, variables=None, inseason=None, parse=None):
    """ Downloads and returns KNMI daily weather data

    Downloads hourly weather data from KNMI's automated weather stations, using the API documented here:
    https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script (Dutch).

    Args:
        stations: (list) weather station IDs
        start: (datetime, int) starting datetime. When providing an integer, make sure format is: yyyymmddhh
        end: (datetime, int) ending datetime. When providing an integer, make sure format is: yyyymmddhh
        variables: (list) variables. See API documentation for available variable sets for each data type
        inseason: (boolean) setting to True makes function return only seasonal data. The season from which to
            fetch the data is now defined by the starting and ending month-day combinations, resulting in a dataset
            that only contains weather data in between starting and ending month-day combinations for each of the
            years in between starting and ending years. So if inseason is True the following result will fetch all
            data from January 1st to March 15th for each year in the range 2005-2012: start: 20050101, end: 20120315
        dataframe (boolean) function returns a pandas dataframe if set to true

    Returns:
        If parse is not set the function returns the raw output of the API request.

        If parse is set to True, the function parses the API request and returns the following:
            disclaimer: (string) KNMI data disclaimer
            stations: (DataFrame) pandas dataframe containing for all stations: name, number, latitude, longitude and
                altitude
            variables: (dict): dictionary of namedtuples containing the variables and corresponding columns and
                descriptions
            data: (DataFrame) pandas dataframe containing the weather measurements for all selected variables (see the
                returned variables dictionary), but always a station number and date in YYYYMMDD format.

        Unpack output as follows:
            disclaimer, stations, variables, data = get_hourly_data(...)
    """
    return get_knmi_data('hourly', stations=stations, start=start, end=end, variables=variables, inseason=inseason,
                         parse=parse)


def get_daily_rain_data(stations=None, start=None, end=None, parse=None):
    """ Downloads and returns KNMI daily weather data

    Downloads daily rain weather data from KNMI's automated weather stations, using the API documented here:
    https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script (Dutch).

    Args:
        stations: (list) weather station IDs
        start: (datetime, int) starting datetime. When providing an integer, make sure format is: yyyymmdd
        end: (datetime, int) ending datetime. When providing an integer, make sure format is: yyyymmdd
            data from January 1st to March 15th for each year in the range 2005-2012: start: 20050101, end: 20120315
        dataframe (boolean) function returns a pandas dataframe if set to true

    Returns:
        If parse is not set the function returns the raw output of the API request.

        If parse is set to True, the function parses the API request and returns the following:
            disclaimer: (string) KNMI data disclaimer
            variables: (string) description of measured variables and interpretation of the data.
            data: (DataFrame) pandas dataframe containing the daily rain data, which is a static set of measurements
                (see variables for details and interpretation of the measurements)
    """
    return get_knmi_data('daily_rain', stations=stations, start=start, end=end, parse=parse)
