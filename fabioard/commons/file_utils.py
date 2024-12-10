import socket
import os
from pathlib import Path
from loguru import logger
from qrcode.constants import ERROR_CORRECT_L
from qrcode.main import QRCode
from PIL import Image

IMAGES_EXTENSIONS = ['.jpg', '.jpeg', '.png']


def get_images(path: Path) -> list[Path]:
    return sum([get_files(path, extension=ext) for ext in IMAGES_EXTENSIONS], [])  # Flat the list


def get_files(path: Path, extension: str = "*") -> list[Path]:
    # return list(path.rglob(f'*{extension}', case_sensitive=False))  # From python 3.12 only
    return list(path.rglob(f'*{extension}'))


def keep_latest_images(directory: Path, num_to_keep: int = 10):
    images = [item for item in directory.iterdir() if
              item.suffix.lower() in IMAGES_EXTENSIONS]
    images.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_images = images[:num_to_keep]
    logger.info(f"Keeping {len(latest_images)} latest images: {latest_images}")

    for image in images[num_to_keep:]:
        logger.info(f"Removing {image}")
        image.unlink()


def generate_qrcode(url: str, out_file: str):
    qr = QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white", )
    desired_size = (100, 100)
    img = img.resize(desired_size, Image.LANCZOS)
    img.save(out_file)


def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address
