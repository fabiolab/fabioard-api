from pydantic import BaseModel


class Message(BaseModel):
    label: str
    data: dict
