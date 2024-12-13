from fastapi import APIRouter

from fabioard.api.dto.message import Message
from fabioard.api.websocket.websocket_manager import manager
from fabioard.domain.service_handler import ServiceHandler

router = APIRouter()


@router.post("/slideshow/next")
async def post_next_slideshow():
    message = Message(label="next", data={})
    await manager.broadcast(message)


@router.post("/slideshow/previous")
async def post_previous_slideshow():
    picture = ServiceHandler.picture_service().get_previous_picture()
    message = Message(label="previous", data=picture.model_dump(mode="json"))
    await manager.broadcast(message)


# @router.post("/slideshow/like")
# async def post_like():
#     picture = ServiceHandler.picture_service().like()
#     message = Message(label="previous", data=picture.model_dump(mode="json"))
#     await manager.broadcast(message)
