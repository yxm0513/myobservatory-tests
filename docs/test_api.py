import requests
import json
from datetime import datetime, timedelta

def test_weather_api():
    # API endpoint
    url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    params = {
        "dataType": "fnd",
        "lang": "en"
    }
    
    try:
        # Send GET request
        response = requests.get(url, params=params)
        
        # Test response status
        assert response.status_code == 200, f"API request failed with status {response.status_code}"
        print("API request successful")
        
        # Parse JSON response
        data = response.json()
        
        # Get day after tomorrow's date
        today = datetime.now()
        day_after_tomorrow = today + timedelta(days=2)
        target_date = day_after_tomorrow.strftime("%Y%m%d")
        
        # Extract relative humidity for day after tomorrow
        for forecast in data["weatherForecast"]:
            if forecast["forecastDate"] == target_date:
                humidity_range = f"{forecast['forecastMinrh']['value']} - {forecast['forecastMaxrh']['value']}%"
                print(f"Relative humidity for {day_after_tomorrow.strftime('%A')}: {humidity_range}")
                return humidity_range
        
        raise ValueError("Forecast for day after tomorrow not found")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    test_weather_api()
