from fastapi import APIRouter

from fabioard.config import settings
from fabioard.controller.status_dto import StatusDto

router = APIRouter()


@router.get("/status", response_model=StatusDto)
async def get_api_health_status():
    return StatusDto(name="fabioard api", status="ok",
                     version=settings.api_path_version)
