from fastapi import FastAPI
from fabioard.config import settings
from fabioard.controller import status_controller, picture_controller
from loguru import logger

BASE_PATH = f"{settings.api_base_path}"

app = FastAPI(
    title="Fabioard api",
    description="Access to data and external apis",
    version=settings.api_path_version,
    docs_url=f"{BASE_PATH}/docs",
    openapi_url=f"/openapi.json",
    redoc_url=None,
)

app.include_router(
    status_controller.router, prefix=settings.api_base_path, tags=["status"]
)

app.include_router(
    picture_controller.router, prefix=settings.api_base_path, tags=["status"]
)

if __name__ == "__main__":
    import uvicorn

    logger.info(
        f"Starting Fabioard API on port {settings.api_port}"
    )
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.api_port
    )
