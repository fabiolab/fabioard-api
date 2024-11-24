from fastapi import APIRouter
from loguru import logger

from fabioard.api.dto.picture_dto import PictureDto
from fabioard.domain.service_handler import ServiceHandler

router = APIRouter()


@router.get("/pictures/random", response_model=PictureDto)
async def get_random_picture():
    picture = ServiceHandler.picture_service().get_random_picture()
    logger.info(f"Random picture requested: {picture}")
    return PictureDto.from_business(picture)
