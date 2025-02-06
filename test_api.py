import requests
import os

api_key = os.getenv('WEATHER_API_KEY')

# Test URL
url = f"http://api.weatherapi.com/v1/current.json?key={"3ab2eda07aaf460086064219250502"}&q=London"

response = requests.get(url)
if response.status_code == 200:
    print("API connection successful!")
    data = response.json()
    print(f"Current temperature in London: {data['current']['temp_c']}°C")
else:
    print(f"Error: {response.status_code}")
    print(response.text)