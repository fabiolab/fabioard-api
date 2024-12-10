import random
import shutil
from pathlib import Path

import pendulum
from loguru import logger

from fabioard.commons.file_utils import get_images, keep_latest_images
from fabioard.domain.business.picture import Picture
from fabioard.domain.protocol.cloud_provider_protocol import CloudProviderProtocol


class HardDriveProvider(CloudProviderProtocol):

    def __init__(self, path: str):
        self.path = Path(path)
        # For big folders, this could use a lot of memory
        self.images = get_images(self.path)
        logger.info(f"Found {len(self.images)} images in {str(self.path)}")

    def get_random_picture(self) -> Picture:
        pic: Path = random.choice(self.images)
        logger.info(f"Picked picture: {str(pic)}")

        try:
            date = pendulum.parse(pic.parent.name[:10])
            location = " ".join(pic.parent.name.split("-")[3:])
        except ValueError:
            date = pendulum.now()
            location = "Unknown"

        # os.symlink(pic.absolute(), f"static/images/{pic.name}")
        shutil.copy(pic, f"static/images/{pic.name}")
        keep_latest_images(Path("static/images"), num_to_keep=10)

        return Picture(url=f"images/{pic.name}", date=date, location=location)
