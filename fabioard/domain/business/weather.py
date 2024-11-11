from pydantic import BaseModel
from pendulum import DateTime

class Weather(BaseModel):
    description: str
    icon: str
    temperature: float
    feels_like: float
    wind_speed: float
    sunrise: int
    sunset: int
