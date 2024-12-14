from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

class Weather(BaseModel):
    description: str
    icon: str
    temperature: float
    feels_like: float
    wind_speed: float
    sunrise: int
    sunset: int
    date: DateTime


class WeatherByDay(BaseModel):
    min: Weather
    max: Weather
    date: DateTime
