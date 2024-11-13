from pydantic_extra_types.pendulum_dt import DateTime
from pydantic import BaseModel


class Picture(BaseModel):
    url: str
    date: DateTime
    location: str
