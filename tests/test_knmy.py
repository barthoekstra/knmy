import pytest
import datetime
from knmy.knmy import get_knmi_data, get_daily_data, get_hourly_data, get_daily_rain_data

test_data = {
    'daily_single_station': 'daily_single_station.txt',
    'daily_multiple_stations': 'daily_multiple_stations.txt',
    'daily_single_var': 'daily_single_var.txt',
    'daily_multiple_vars': 'daily_multiple_vars.txt',
    'hourly': 'hourly.txt',
    'inseason': 'inseason.txt',
    'daily_rain': 'daily_rain.txt',
}

def test_gkd_empty():
    with pytest.raises(TypeError):
        get_knmi_data()

# Stations
def test_gkd_single_station():
    output = get_knmi_data('daily', stations=[209], start=20170101, end=20170105)
    output_comparison(output, test_data['daily_single_station'])

def test_gkd_multiple_stations():
    output = get_knmi_data('daily', stations=[209, 235], start=20170101, end=20170105)
    output_comparison(output, test_data['daily_multiple_stations'])

# Start and End date(time)s
## Daily
def test_datetime_integer_validation_daily():
    with pytest.raises(ValueError):
        get_knmi_data('daily', stations=[209], start=201701, end=20170105)
    with pytest.raises(ValueError):
        get_knmi_data('daily', stations=[209], start=20170101, end=201701052)

def test_datetime_date_daily():
    date_start = datetime.date(2017, 1, 1)
    date_end = datetime.date(2017, 1, 5)
    output = get_knmi_data('daily', stations=[209], start=date_start, end=date_end)
    output_comparison(output, test_data['daily_single_station'])

def test_datetime_datetime_daily():
    datetime_start = datetime.datetime(2017, 1, 1, 0, 0)
    datetime_end = datetime.datetime(2017, 1, 5, 23, 59, 59)
    output = get_knmi_data('daily', stations=[209], start=datetime_start, end=datetime_end)
    output_comparison(output, test_data['daily_single_station'])

## Hourly
def test_integer_validation_hourly():
    with pytest.raises(ValueError):
        get_knmi_data('hourly', stations=[209], start=20170101, end=2017010524)
    with pytest.raises(ValueError):
        get_knmi_data('hourly', stations=[209], start=2017010101, end=20170105241)

def test_datetime_validation_hourly_():
    date_start = datetime.date(2017, 1, 1)
    date_end = datetime.date(2017, 1, 5)
    with pytest.raises(ValueError):
        get_knmi_data('hourly', stations=[209], start=date_start, end=date_end)

def test_hourly_integer():
    output = get_knmi_data('hourly', stations=[209], start=2017010101, end=2017010524)
    output_comparison(output, test_data['hourly'])

def test_hourly_datetime():
    datetime_start = datetime.datetime(2017, 1, 1, 0, 0)
    datetime_end = datetime.datetime(2017, 1, 5, 23, 59, 59)
    output = get_knmi_data('hourly', stations=[209], start=datetime_start, end=datetime_end)
    output_comparison(output, test_data['hourly'])

# Inseason
def test_inseason():
    output = get_knmi_data('daily', stations=[209], start=20150101, end=20170105, inseason=True)
    output_comparison(output, test_data['inseason'])

# Variables
def test_gkd_single_var():
    output = get_knmi_data('daily', stations=[209], start=20170101, end=20170105, variables=['WIND'])
    output_comparison(output, test_data['daily_single_var'])

def test_gkd_multiple_vars():
    output = get_knmi_data('daily', stations=[209], start=20170101, end=20170105, variables=['WIND', 'VICL'])
    output_comparison(output, test_data['daily_multiple_vars'])

# Wrapper functions
def test_get_daily_data():
    output = get_daily_data(stations=[209], start=20170101, end=20170105)
    output_comparison(output, test_data['daily_single_station'])

def test_get_hourly_data():
    output = get_hourly_data(stations=[209], start=2017010101, end=2017010524)
    output_comparison(output, test_data['hourly'])

def test_get_daily_rain_data():
    output = get_daily_rain_data(stations=[10], start=20170101, end=20170105)
    output_comparison(output, test_data['daily_rain'])

def output_comparison(output, reference):
    with open('tests/test_data/' + reference) as f:
        reference_output = f.read()
        reference_output = reference_output.replace(' ', '')
        output = output.replace(' ', '')
        assert reference_output == output