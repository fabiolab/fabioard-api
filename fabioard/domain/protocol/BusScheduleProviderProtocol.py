from typing import Protocol

from fabioard.domain.business.bus_schedule import BusSchedule


class BusProviderProtocol(Protocol):
    def get_next_bus(self, bus_station: str, bus_line: str, bus_destination: str) -> list[BusSchedule]:
        ...
