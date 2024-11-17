import random
import shutil
from pathlib import Path

import pendulum

from fabioard.commons.file_utils import get_files
from fabioard.domain.business.picture import Picture
from fabioard.domain.protocol.CloudProviderProtocol import CloudProviderProtocol

IMAGES_EXTENSIONS = ['.jpg', '.jpeg', '.png']


class HardDriveProvider(CloudProviderProtocol):

    def __init__(self, path: str):
        self.path = Path(path)
        # For big folders, this could use a lot of memory
        self.images = sum([get_files(self.path, extension=ext) for ext in IMAGES_EXTENSIONS], [])  # Flat the list

    def get_random_picture(self) -> Picture:
        pic: Path = random.choice(self.images)

        try:
            date = pendulum.parse(pic.name[:10])
            location = " ".join(pic.name.split("-")[3:-1])
        except ValueError:
            date = pendulum.now()
            location = "Unknown"

        shutil.copy(pic, "static/background.jpg")

        return Picture(url="background.jpg", date=date, location=location)
