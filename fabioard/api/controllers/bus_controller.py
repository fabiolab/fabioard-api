from fastapi import APIRouter
from loguru import logger

router = APIRouter()

@router.get("/bus/next")
async def get_next_bus():
    logger.info("Next bus requested")
    return {
        "time": "12:00",
    }
