from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from fabioard.domain.business.event import Event


class EventDto(BaseModel):
    start: DateTime
    end: DateTime
    summary: str

    @staticmethod
    def from_business(event: Event) -> "EventDto":
        return EventDto(
            summary=event.summary,
            start=event.start,
            end=event.end,
        )
