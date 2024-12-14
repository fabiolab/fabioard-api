from fastapi import FastAPI
import pendulum
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fabioard.api.controllers.websocket_controller import websocket_endpoint
from fabioard.commons.file_utils import generate_qrcode, get_ip_address
from fabioard.config import settings
from fabioard.api.controllers import (
    status_controller,
    picture_controller,
    weather_controller,
    bus_controller,
    calendar_controller, websocket_controller, slideshow_controller,
)
from loguru import logger

BASE_PATH = f"{settings.api_base_path}"

pendulum.set_locale('fr')

app = FastAPI(
    title="Fabioard api",
    description="Access to data and external apis",
    version=settings.api_path_version,
    docs_url=f"{BASE_PATH}/docs",
    openapi_url=f"/openapi.json",
    redoc_url=None,
)
app.include_router(
    websocket_controller.router, prefix=settings.api_base_path, tags=["ws"]
)

app.include_router(
    status_controller.router, prefix=settings.api_base_path, tags=["status"]
)

app.include_router(
    picture_controller.router, prefix=settings.api_base_path, tags=["picture"]
)

app.include_router(
    slideshow_controller.router, prefix=settings.api_base_path, tags=["slideshow"]
)

app.include_router(
    weather_controller.router, prefix=settings.api_base_path, tags=["weather"]
)

app.include_router(bus_controller.router, prefix=settings.api_base_path, tags=["bus"])

app.include_router(
    calendar_controller.router, prefix=settings.api_base_path, tags=["calendar"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["http://localhost:*", "http://localhost:8090", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    # Generate the remote control qrcode at startup (use the IP of the machine running the API)
    generate_qrcode(f"http://{get_ip_address()}:{settings.api_port}/static/remote.html", "static/remote_qrcode.png")

    logger.info(f"Starting Fabioard API on port {settings.api_port}")
    uvicorn.run("main:app", host="0.0.0.0", port=settings.api_port)
