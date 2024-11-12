from fastapi import APIRouter
from loguru import logger

from fabioard.adapter.star_provider import StarProvider
from fabioard.api.dto.bus_schedule_dto import BusScheduleDto
from fabioard.domain.services.bus_service import BusService

router = APIRouter()

bus_service = BusService(StarProvider())


@router.get("/bus/next", response_model=list[BusScheduleDto]    )
async def get_next_bus():
    logger.info("Next bus requested")
    res=[BusScheduleDto.from_business(schedule) for schedule in bus_service.get_next_bus_schedule("Monsieur Vincent", "C2", "Cesson-Viasilva")]
    return res
