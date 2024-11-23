import asyncio

from loguru import logger

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from fabioard.api.websocket.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("Websocket connection requested")
    await manager.connect(websocket)
    try:
        # @TODO: understand why this loop is required
        while True:
            # Handle received message
            # data = await websocket.receive_text()

            # Send message to all connected clients
            # await manager.broadcast(f"Message reçu : {data}")

            logger.info("Waiting for message")
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        logger.error("A client has disconnected")
