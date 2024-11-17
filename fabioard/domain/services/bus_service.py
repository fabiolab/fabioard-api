from fabioard.domain.protocol.bus_schedule_provider_protocol import BusProviderProtocol


class BusService:
    def __init__(self, bus_provider: BusProviderProtocol):
        self.bus_provider = bus_provider

    def get_next_bus_schedule(self, bus_station: str, bus_line: str, bus_destination: str):
        return sorted(self.bus_provider.get_next_bus(bus_station=bus_station, bus_line=bus_line,
                                              bus_destination=bus_destination), key=lambda x: x.departure_time)
