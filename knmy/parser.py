import pandas as pd
from io import StringIO
from collections import namedtuple


def parse_raw_weather_data(raw):
    """ Parses raw weather data

    Parses raw weather data from KNMI's automated weather stations and returns the disclaimer, a dict of variables
    and pandas dataframes of the stations and the weather measurements.

    Args:
        raw: (string) raw output of the get_knmi_data function and the corresponding API call (see get_knmi_data for
            reference

    Returns:
        disclaimer: (string) KNMI data disclaimer
        stations: (DataFrame) pandas dataframe containing for all stations: name, number, latitude, longitude and
            altitude
        variables: (dict): dictionary of namedtuples containing the variables and corresponding columns and descriptions
        data: (DataFrame) pandas dataframe containing the weather measurements for all selected variables (see the
            returned variables dictionary), but always a station number and date in YYYYMMDD format.
    """
    chunk = _generate_chunks(raw, '# ')

    # Disclaimer
    disclaimer_raw = next(chunk)
    disclaimer = '\n'.join(line.strip('# ') for line in disclaimer_raw)

    # Stations list
    stations_raw = next(chunk)
    stations_raw = [line.strip('# ') for line in stations_raw]
    station_lines = []

    for station in stations_raw[1:]:
        station_attribute = [attribute.strip(":").strip() for attribute in station.split('  ') if attribute != '']

        try:
            number, longitude, latitude, altitude, name = station_attribute
        except ValueError:
            print('Metadata for station {} is invalid'.format(station_attribute[0]))
        else:
            station_line = ','.join([number, name, latitude, longitude, altitude])
            station_lines.append(station_line)

    station_lines = '\n'.join(station_lines)

    stations = pd.read_csv(StringIO(station_lines), index_col=0, names=['number', 'name', 'latitude', 'longitude',
                                                                        'altitude'])

    # Variables
    variables_raw = next(chunk)
    variables_raw = [line.strip('# ').strip(';') for line in variables_raw]

    Variable = namedtuple('Variable', ['Index', 'Abbreviation', 'Description'])
    variables = {}

    for index, variable in enumerate(variables_raw):
        variable_split = variable.split('=')
        key = variable_split[0].strip()
        value = '='.join(variable_split[1:]).lstrip()
        new_variable = {index: Variable(index, key, value)}
        variables.update(new_variable)

    # Header
    header_raw = next(chunk)
    header = header_raw[0].strip('# ').replace(' ', '')

    # Data
    data_raw = next(chunk)
    records = []

    for record in data_raw:
        records.append(record.strip('# ').replace(' ', ''))

    records.insert(0, header)

    data = pd.read_csv(StringIO('\n'.join(records)), names=header.split(','))

    return disclaimer, stations, variables, data

def parse_raw_rain_data(raw):
    """ Parses raw daily rain data

    Parses raw daily rain data from KNMI's automated rain measurement stations and returns the disclaimer, variables and
    a dataframe of the rain data.

    Args:
        raw: (string) raw output of the get_knmi_data/get_daily_rain_data function and the corresponding API call (see
            get_knmi_data and get_daily_rain-data for reference)

    Returns:
        disclaimer: (string) KNMI data disclaimer
        variables: (string) description of measured variables and interpretation of the data.
        data: (DataFrame) pandas dataframe containing the daily rain data, which is a static set of measurements (see
            variables for details and interpretation of the measurements)
    """
    raw = raw.splitlines()

    disclaimer = '\n'.join(raw[0:5])
    variables = '\n'.join(raw[6:22])

    header = raw[23].replace(' ', '') + 'NAME'
    records = []
    for record in raw[24:]:
        records.append(record.replace('  ', ''))
    records.insert(0, header)

    data = pd.read_csv(StringIO('\n'.join(records)))

    return disclaimer, variables, data


def _generate_chunks(raw, chunk_separator):
    """ Splits raw data in chunks separated by a separator

    Args:
        raw: (string) raw output of get_knmi_data function
        chunk_separator: (string) split raw data in chunks where a line in the raw data equals this separator

    Returns:
        chunk: (string) chunk of raw data
    """
    chunk = []

    for line in raw.splitlines():
        if line != chunk_separator:
            chunk.append(line)
        else:
            if len(chunk) == 0:
                continue
            else:
                yield chunk
                chunk = []
    else:
        yield chunk
