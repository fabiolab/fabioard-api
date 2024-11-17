from fastapi import APIRouter
from loguru import logger

from fabioard.adapter.harddrive_provider import HardDriveProvider
from fabioard.api.dto.picture_dto import PictureDto
from fabioard.domain.services.picture_service import PictureService

router = APIRouter()

picture_service = PictureService(HardDriveProvider(path="/media/kvjw3322/2078B0CD25633F53/Backup/Photos"))


@router.get("/pictures/random", response_model=PictureDto)
async def get_random_picture():
    picture = picture_service.get_random_picture()
    logger.info(f"Random picture requested: {picture}")
    return PictureDto.from_business(picture)
