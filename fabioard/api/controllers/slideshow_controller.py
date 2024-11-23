from fastapi import APIRouter

from fabioard.adapter.harddrive_provider import HardDriveProvider
from fabioard.api.websocket.websocket_manager import manager
from fabioard.config import settings
from fabioard.domain.services.picture_service import PictureService

router = APIRouter()

picture_service = PictureService(HardDriveProvider(path=settings.hardrive_path))


@router.post("/slideshow/next")
async def post_next_slideshow():
    await manager.broadcast("next")
