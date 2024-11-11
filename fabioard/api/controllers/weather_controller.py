from fastapi import APIRouter
from loguru import logger

from fabioard.adapter.owm_provider import OpenWeatherMapProvider
from fabioard.api.dto.weather_dto import WeatherDto
from fabioard.domain.services.weather_service import WeatherService

router = APIRouter()

weather_service = WeatherService(OpenWeatherMapProvider())


@router.get("/weather", response_model=WeatherDto)
async def get_weather() -> WeatherDto:
    logger.info("Weather requested")

    return WeatherDto.from_business(weather_service.get_weather("Rennes"))
