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


@router.get("/forecast", response_model=list[WeatherDto])
async def get_forecast() -> list[WeatherDto]:
    logger.info("Weather forecast requested")

    return [WeatherDto.from_business(weather) for weather in weather_service.get_forecast("Rennes")]
