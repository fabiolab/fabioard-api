from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime


class Event(BaseModel):
    start: DateTime
    end: DateTime
    summary: str
