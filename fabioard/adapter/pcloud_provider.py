import random

import requests
from pydantic import BaseModel

from fabioard.config import settings
from fabioard.domain.protocol.CloudProviderProtocol import CloudProviderProtocol


class FileDto(BaseModel):
    name: str
    is_folder: bool
    file_id: int


class FolderContentDto(BaseModel):
    name: str
    folders: list[FileDto]
    files: list[FileDto]


class PCloudProvider(CloudProviderProtocol):
    BASE_URL = "https://eapi.pcloud.com"

    def __init__(self):
        self.auth = self._get_access_token()

    def get_random_picture(self) -> str:
        random_image = self._choose_random_image(settings.pcloud_image_folderid)
        return self._download_file(random_image.file_id)

    @staticmethod
    def _get_access_token():
        url = f"{PCloudProvider.BASE_URL}/userinfo"
        params = {
            "getauth": 1,
            "username": settings.pcloud_user,
            "password": settings.pcloud_password
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data["result"] == 0:
            return data["auth"]
        else:
            raise Exception(f"Authentication error: {data['error']}")

    def _list_content(self, folder_id: int = 0) -> FolderContentDto:
        url = f"{PCloudProvider.BASE_URL}/listfolder"
        params = {
            "auth": self.auth,
            "folderid": folder_id
        }
        response = requests.get(url, params=params)

        if 400 <= response.status_code < 500:
            self.auth = self._get_access_token()
            response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Error while requesting: {response.text}")

        content = FolderContentDto(
            name=response.json()["metadata"]["name"],
            folders=[FileDto(name=folder["name"], is_folder=True, file_id=folder["folderid"]) for folder in
                     response.json()["metadata"]["contents"] if folder["isfolder"]],
            files=[FileDto(name=folder["name"], is_folder=False, file_id=folder["fileid"]) for folder in
                   response.json()["metadata"]["contents"] if not folder["isfolder"]]
        )

        return content

    def _choose_random_image(self, folder_id: int) -> FileDto:
        while True:
            files = self._list_content(folder_id)

            if not files.folders:
                return random.choice(files.files)
            else:
                next_folder = random.choice(files.folders)
                print(f"Chosen folder: {next_folder.name} from {files.folders}")
                return self._choose_random_image(next_folder.file_id)

    def _download_file(self, file_id) -> str:
        url = f"{PCloudProvider.BASE_URL}/getfilelink"
        params = {
            "auth": self.auth,
            "fileid": file_id
        }
        response = requests.get(url, params=params)

        if 400 <= response.status_code < 500:
            self.auth = self._get_access_token()
            response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Error while requesting: {response.text}")

        data = response.json()
        download_url = f"https://{data['hosts'][0]}{data['path']}"

        return download_url
        # if data["result"] == 0:
        #     file_response = requests.get(download_url)
        #     return file_response.content
        # else:
        #     raise Exception(f"Error while downloading {file_id} from {download_url}: {data['error']}")
