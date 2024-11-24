from fastapi import WebSocket
from loguru import logger

from fabioard.api.dto.message import Message


class ConnectionManager:
    def __init__(self):
        # accept one single connection
        self.active_connection = None

    async def connect(self, websocket: WebSocket):
        logger.info("Websocket connected")
        await websocket.accept()
        self.active_connection = websocket

    async def broadcast(self, message: Message):
        logger.info(f"Broadcasting message to connection {self.active_connection}")
        try:
            await self.active_connection.send_json(message.model_dump())
        except Exception as e:
            logger.error(f"An error occurred while broadcasting message: {e}")


manager = ConnectionManager()
