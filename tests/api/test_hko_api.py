import requests
from datetime import datetime, timedelta
import pytest

HKO_API_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"

def get_9day_forecast():
    params = {
        "dataType": "fnd",
        "lang": "en"
    }
    response = requests.get(HKO_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def test_api_status():
    response = requests.get(HKO_API_URL, params={"dataType": "fnd"})
    assert response.status_code == 200

def test_day_after_tomorrow_humidity():
    data = get_9day_forecast()
    day_after_tomorrow = (datetime.now() + timedelta(days=2)).strftime("%Y%m%d")
    
    for forecast in data['weatherForecast']:
        if forecast['forecastDate'] == day_after_tomorrow:
            humidity = f"{forecast['forecastMinrh']['value']}-{forecast['forecastMaxrh']['value']}%"
            assert humidity, "Humidity value should not be empty"
            assert "-" in humidity, "Humidity range should contain a dash"
            assert "%" in humidity, "Humidity should end with %"
            return 
    
    pytest.fail("Day after tomorrow forecast not found in API response")
