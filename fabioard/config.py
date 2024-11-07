from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_base_path: str = "/fabioard-api/v1"
    api_path_version: str = "v1"
    api_port: int = 8090

    pcloud_user: str
    pcloud_password: str
    pcloud_image_folderid: int = 13212918957


settings = Settings()
