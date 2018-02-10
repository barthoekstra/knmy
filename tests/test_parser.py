from knmy.knmy import get_hourly_data, get_daily_rain_data
from knmy.parser import parse_raw_weather_data, parse_raw_rain_data

raw_data = get_hourly_data([209, 257], start=2017010101, end=2017010524)

disclaimer, stations, variables, data = parse_raw_weather_data(raw_data)


def test_disclaimer():
    with open('tests/test_data/disclaimer.txt') as f:
        disclaimer_reference = f.read()

    assert disclaimer == disclaimer_reference


def test_stations():
    stations_string = stations.to_csv()
    with open('tests/test_data/stations.csv') as f:
        stations_reference = f.read()

    assert stations_string == stations_reference


def test_variables():
    with open('tests/test_data/variables.txt') as f:
        variables_reference = f.read()

    assert str(variables) == variables_reference.strip('\n')


def test_data():
    data_string = data.to_csv()
    with open('tests/test_data/data.csv') as f:
        data_reference = f.read()

    assert data_string == data_reference


raw_data_rain = get_daily_rain_data(stations=[21, 22], start=20170101, end=20170105)

disclaimer_rain, variables_rain, data_rain = parse_raw_rain_data(raw_data_rain)


def test_rain_disclaimer():
    with open('tests/test_data/disclaimer_rain.txt') as f:
        disclaimer_rain_reference = f.read()

    assert disclaimer_rain == disclaimer_rain_reference

def test_rain_variables():
    with open('tests/test_data/variables_rain.txt') as f:
        variables_rain_reference = f.read()

    assert variables_rain == variables_rain_reference

def test_rain_data():
    data_string = data_rain.to_csv()
    with open('tests/test_data/data_rain.csv') as f:
        data_rain_reference = f.read()

    assert data_string == data_rain_reference
