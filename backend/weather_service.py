import requests
from datetime import datetime
import json

class WeatherService:
    def __init__(self, api_key):
        """
        Initialize weather service with API key
        
        Args:
            api_key (str): API key for weather service
        """
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"
        
    def get_weather_data(self, latitude, longitude, date_time):
        """
        Get weather data for specific location and time
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            date_time (datetime): Date and time for weather data
            
        Returns:
            dict: Weather data including temperature and cloud cover
        """
        try:
            # Format date for API
            date_str = date_time.strftime("%Y-%m-%d")
            
            # Make API request
            response = requests.get(
                f"{self.base_url}/history.json",
                params={
                    "key": self.api_key,
                    "q": f"{latitude},{longitude}",
                    "dt": date_str
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                hour = date_time.hour
                
                # Extract relevant weather data
                weather_data = {
                    'temperature': data['forecast']['forecastday'][0]['hour'][hour]['temp_c'],
                    'cloud_cover': data['forecast']['forecastday'][0]['hour'][hour]['cloud'],
                    'humidity': data['forecast']['forecastday'][0]['hour'][hour]['humidity']
                }
                
                return weather_data
            else:
                print(f"Error fetching weather data: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
            
    def get_forecast(self, latitude, longitude, days=1):
        """
        Get weather forecast for future optimization
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            days (int): Number of days to forecast
            
        Returns:
            dict: Forecast data
        """
        try:
            response = requests.get(
                f"{self.base_url}/forecast.json",
                params={
                    "key": self.api_key,
                    "q": f"{latitude},{longitude}",
                    "days": days
                }
            )
            
            if response.status_code == 200:
                return response.json()['forecast']['forecastday']
            else:
                print(f"Error fetching forecast: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None