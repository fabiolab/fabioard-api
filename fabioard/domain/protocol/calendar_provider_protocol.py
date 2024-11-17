from typing import Protocol

from fabioard.domain.business.event import Event


class CalendarProviderProtocol(Protocol):

    def get_events(self, calendar_id: str) -> list[Event]:
        ...
