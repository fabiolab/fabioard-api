from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fabioard.config import settings
from fabioard.api.controllers import status_controller, picture_controller, weather_controller, bus_controller
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
    picture_controller.router, prefix=settings.api_base_path, tags=["picture"]
)

app.include_router(
    weather_controller.router, prefix=settings.api_base_path, tags=["weather"]
)

app.include_router(
    bus_controller.router, prefix=settings.api_base_path, tags=["bus"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:*",
    "http://localhost:8090",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
