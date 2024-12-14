from fastapi import APIRouter
from loguru import logger

from fabioard.api.dto.weather_dto import WeatherByDayDto, WeatherDto
from fabioard.domain.service_handler import ServiceHandler

router = APIRouter()


@router.get("/weather", response_model=WeatherDto)
async def get_weather() -> WeatherDto:
    logger.info("Weather requested")

    return WeatherDto.from_business(ServiceHandler.weather_service().get_weather("Rennes"))


@router.get("/forecast", response_model=list[WeatherDto])
async def get_forecast() -> list[WeatherDto]:
    logger.info("Weather forecast requested")

    return [WeatherDto.from_business(weather) for weather in ServiceHandler.weather_service().get_forecast("Rennes")]

@router.get("/forecast/by_day", response_model=list[WeatherByDayDto])
async def get_forecast_by_day() -> list[WeatherByDayDto]:
    logger.info("Weather forecast requested")

    return [WeatherByDayDto.from_business(weather) for weather in ServiceHandler.weather_service().get_forecast_by_day("Rennes")]
