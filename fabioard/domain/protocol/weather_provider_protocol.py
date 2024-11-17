from typing import Protocol

from fabioard.domain.business.weather import Weather


class WeatherProviderProtocol(Protocol):
    def get_weather(self, city: str) -> Weather:
        ...

    def get_weather_forecast(self, city: str) -> list[Weather]:
        ...
