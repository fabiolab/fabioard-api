import requests

from fabioard.config import settings
from fabioard.domain.business.weather import Weather


class OpenWeatherMapProvider:
    def __init__(self):
        self.api_key = settings.openweathermap_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_weather(self, city: str):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "fr"
        }
        response = requests.get(f"{self.base_url}/weather", params=params)

        if response.status_code >= 400:
            raise Exception(f"Error while requesting: {response.text}")

        return Weather(
            description=response.json()["weather"][0]["description"],
            icon=response.json()["weather"][0]["icon"],
            temperature=response.json()["main"]["temp"],
            feels_like=response.json()["main"]["feels_like"],
            wind_speed=response.json()["wind"]["speed"],
            sunrise=response.json()["sys"]["sunrise"],
            sunset=response.json()["sys"]["sunset"],
        )

    def get_weather_forecast(self, city: str) -> list[Weather]:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "fr"
        }
        response = requests.get(f"{self.base_url}/forecast", params=params)
        return response.json()
