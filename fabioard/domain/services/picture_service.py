from fabioard.domain.business.picture import Picture
from fabioard.domain.protocol.cloud_provider_protocol import CloudProviderProtocol


class PictureService:
    def __init__(self, cloud_provider: CloudProviderProtocol):
        self.cloud_provider = cloud_provider
        self.history = []

    def get_random_picture(self) -> Picture:
        pic = self.cloud_provider.get_random_picture()
        self.history.append(pic)
        return pic

    def get_previous_picture(self) -> Picture:
        del self.history[-1]
        return self.history[-1]
