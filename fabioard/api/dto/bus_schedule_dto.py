from pydantic import BaseModel

from fabioard.domain.business.bus_schedule import BusSchedule


class BusScheduleDto(BaseModel):
    bus_number: str
    destination: str
    departure_time: str
    bus_stop: str

    @staticmethod
    def from_business(bus_schedule: BusSchedule) -> "BusScheduleDto":
        return BusScheduleDto(bus_number=bus_schedule.bus_number,
                              destination=bus_schedule.destination,
                              departure_time=bus_schedule.departure_time.to_datetime_string(),
                              bus_stop=bus_schedule.bus_stop)
