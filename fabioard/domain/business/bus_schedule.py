from pydantic_extra_types.pendulum_dt import DateTime
from pydantic import BaseModel


class BusSchedule(BaseModel):
    bus_number: str
    destination: str
    departure_time: DateTime
    bus_stop: str

