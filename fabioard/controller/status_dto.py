from pydantic import BaseModel


class StatusDto(BaseModel):
    name: str
    status: str
    version: str
