from fabioard.domain.business.picture import Picture
from fabioard.domain.protocol.CloudProviderProtocol import CloudProviderProtocol


class PictureService:

    def __init__(self, cloud_provider: CloudProviderProtocol):
        self.cloud_provider = cloud_provider

    def get_random_picture(self) -> Picture:
        pic = self.cloud_provider.get_random_picture()
        return pic
