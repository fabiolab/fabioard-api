from fastapi import APIRouter, Depends

from fabioard.adapter.pcloud_provider import PCloudProvider
from fabioard.domain.picture_service import PictureService

router = APIRouter()

picture_service = PictureService(PCloudProvider())

@router.get("/pictures/random", response_model=str)
async def get_random_picture():
    return picture_service.get_random_picture()
