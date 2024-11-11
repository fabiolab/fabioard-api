from pydantic import BaseModel

from fabioard.domain.business.weather import Weather


class WeatherDto(BaseModel):
    description: str
    icon: str
    temperature: float
    feels_like: float
    wind_speed: float
    sunrise: int
    sunset: int

    @staticmethod
    def from_business(weather: Weather) -> "WeatherDto":
        return WeatherDto(
            description=weather.description,
            icon=weather.icon,
            temperature=weather.temperature,
            feels_like=weather.feels_like,
            wind_speed=weather.wind_speed,
            sunrise=weather.sunrise,
            sunset=weather.sunset
        )
