from pydantic import BaseModel

from fabioard.domain.business.weather import Weather, WeatherByDay


class WeatherDto(BaseModel):
    description: str
    icon: str
    temperature: float
    feels_like: float
    wind_speed: float
    sunrise: int
    sunset: int
    date: str
    day_of_week: str

    @staticmethod
    def from_business(weather: Weather) -> "WeatherDto":
        return WeatherDto(
            description=weather.description,
            icon=weather.icon,
            temperature=weather.temperature,
            feels_like=weather.feels_like,
            wind_speed=weather.wind_speed,
            sunrise=weather.sunrise,
            sunset=weather.sunset,
            date=weather.date.to_datetime_string(),
            day_of_week=weather.date.format("ddd")
        )


class WeatherByDayDto(BaseModel):
    min: WeatherDto
    max: WeatherDto
    date: str
    day_of_week: str

    @staticmethod
    def from_business(weather: WeatherByDay) -> "WeatherByDayDto":
        return WeatherByDayDto(
            min=WeatherDto.from_business(weather.min),
            max=WeatherDto.from_business(weather.max),            
            date=weather.date.to_datetime_string(),
            day_of_week=weather.date.format("ddd")
        )
