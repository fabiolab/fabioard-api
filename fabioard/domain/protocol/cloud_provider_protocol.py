from typing import Protocol

from fabioard.domain.business.picture import Picture


class CloudProviderProtocol(Protocol):
    def get_random_picture(self) -> Picture:
        ...
