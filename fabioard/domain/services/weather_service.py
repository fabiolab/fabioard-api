from fabioard.domain.business.weather import Weather
from fabioard.domain.protocol.WeatherProviderProtocol import WeatherProviderProtocol


class WeatherService:
    def __init__(self, weather_provider: WeatherProviderProtocol):
        self.weather_provider = weather_provider

    def get_weather(self, city: str) -> Weather:
        return self.weather_provider.get_weather(city)
