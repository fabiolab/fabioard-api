from typing import Protocol


class CloudProviderProtocol(Protocol):
    def get_random_picture(self) -> str:
        ...
