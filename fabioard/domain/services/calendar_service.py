from fabioard.domain.protocol.calendar_provider_protocol import CalendarProviderProtocol


class CalendarService:
    def __init__(self, calendar_provider: CalendarProviderProtocol):
        self.calendar_provider = calendar_provider

    def get_events(self, calendar_id: str):
        return self.calendar_provider.get_events(calendar_id)
