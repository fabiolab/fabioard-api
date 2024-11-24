import os
from pathlib import Path
from loguru import logger

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
