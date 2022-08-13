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
    raw = raw.splitlines()

    # Disclaimer
    disclaimer_clean = [line.strip('# ').strip('"# ') for line in raw[0:5] if line != '']
    disclaimer = '\n'.join(disclaimer_clean).strip('# ')

    # Metadata
    data_line = None  # Line number at which data starts
    station_lines = []
    Variable = namedtuple('Variable', ['Index', 'Abbreviation', 'Description'])
    variables = {}
    variable_index = 0
    header = ''

    for i, line in enumerate(raw[5:]):
        if not line.startswith('# '):
            # Apparently data has started, store line number
            data_line = i + 5
            break

        line_start = line.split(' ')[1]
        if line_start == 'STN':
            continue
        elif line_start.isnumeric():
            # Stations start with a number
            station_attributes = [attribute.strip() for attribute in line.strip('#').split('  ')]
            station_attributes = [attribute for attribute in station_attributes if attribute != '']
            number, longitude, latitude, altitude, name = station_attributes
            station_line = ','.join([number, name, latitude, longitude, altitude])
            station_lines.append(station_line)
        else:
            # Variables start with an abbreviation that is not STN
            variable = [variable.lstrip().rstrip() for variable in line.strip('# ').split(' : ')]
            if len(variable) == 2:
                variables.update({variable_index: Variable(variable_index, variable[0], variable[1])})
                variable_index = variable_index + 1
            else:
                # We've reached the header of the CSV section with data
                header = line.strip('# ').replace(' ', '')

    # Save stations to dataframe
    station_lines = '\n'.join(station_lines)
    stations = pd.read_csv(StringIO(station_lines), index_col=0, names=['number', 'name', 'latitude', 'longitude',
                                                                        'altitude'])

    # Data parsing
    records = []
    for record in raw[data_line:]:
        values = [value.lstrip().rstrip() for value in record.strip(' ').split(',')]
        records.append(','.join(values))

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

    disclaimer_clean = [line.strip('# ').strip('"# ') for line in raw[0:5]]
    disclaimer = '\n'.join(disclaimer_clean).strip('# ')

    data_line = None
    station_lines = []
    Variable = namedtuple('Variable', ['Index', 'Abbreviation', 'Description'])
    variables = {}
    variable_index = 0
    header = ''

    for i, line in enumerate(raw[5:]):
        if not line.startswith('# '):
            # Apparently data has started, store line number
            data_line = i + 5
            break

        line_start = line.split(' ')[1]

        if line_start == 'STN':
            continue
        elif line_start.isnumeric():
            # Stations start with a number
            station_attributes = [attribute.strip() for attribute in line.strip('#').split('  ')]
            station_attributes = [attribute for attribute in station_attributes if attribute != '']
            number, name = station_attributes
            station_line = ','.join([number, name])
            station_lines.append(station_line)
        else:
            # Variables start with an abbreviation that is not STN
            variable = [variable.lstrip().rstrip() for variable in line.strip('# ').split(' : ')]
            if len(variable) == 2:
                variables.update({variable_index: Variable(variable_index, variable[0], variable[1])})
                variable_index = variable_index + 1
            else:
                # We've reached the header of the CSV section with data
                header = line.strip('# ').replace(' ', '')

    # Save stations to dataframe
    station_lines = '\n'.join(station_lines)
    stations = pd.read_csv(StringIO(station_lines), index_col=0, names=['number', 'name'])

    # Data parsing
    records = []
    for record in raw[data_line:]:
        values = [value.lstrip().rstrip() for value in record.strip(' ').split(',')]
        records.append(','.join(values))

    data = pd.read_csv(StringIO('\n'.join(records)), names=header.split(','))

    return disclaimer, variables, data
