from fabioard.domain.business.weather import Weather
from fabioard.domain.protocol.weather_provider_protocol import WeatherProviderProtocol


class WeatherService:
    def __init__(self, weather_provider: WeatherProviderProtocol):
        self.weather_provider = weather_provider

    def get_weather(self, city: str) -> Weather:
        return self.weather_provider.get_weather(city)

    def get_forecast(self, city: str) -> list[Weather]:
        return self.weather_provider.get_weather_forecast(city)
