import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float

@dataclass
class ForecastData:
    date: str
    time: str
    temperature: float
    humidity: int
    wind_speed: float
    description: str
    icon: str

def get_lat_lon(city_name, API_KEY):
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_KEY}'
    ).json()
    if resp:
        data = resp[0]
        return data.get('lat'), data.get('lon')
    return None, None

def get_current_weather(lat, lon, API_KEY):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric').json()
    return WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp'))
    )

def get_weather_forecast(lat, lon, API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    forecast_times = ["12:00:00"]  # Afternoon

    daily_forecast = [
        ForecastData(
            date=datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%A, %d %B"),
            time=datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p"),
            temperature=forecast["main"]["temp"],
            humidity=forecast["main"]["humidity"],
            wind_speed=forecast["wind"]["speed"],
            description=forecast["weather"][0]["description"].title(),
            icon=forecast["weather"][0]["icon"]
        )
        for forecast in data["list"] if any(t in forecast["dt_txt"] for t in forecast_times)
    ]

    return daily_forecast

def main(city_name):
    lat, lon = get_lat_lon(city_name, api_key)
    if lat is None or lon is None:
        return None, None
    return get_current_weather(lat, lon, api_key), get_weather_forecast(lat, lon, api_key)

if __name__ == "__main__":
    lat, lon = get_lat_lon('Toronto', 'Canada', api_key)
    print(get_current_weather(lat, lon, api_key))
    print(get_weather_forecast(lat, lon, api_key))