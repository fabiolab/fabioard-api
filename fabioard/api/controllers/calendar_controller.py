from fastapi import APIRouter

from fabioard.adapter.google_calendar_provider import GoogleCalendarProvider
from fabioard.api.dto.event_dto import EventDto
from fabioard.domain.services.calendar_service import CalendarService

router = APIRouter()

calendar_service = CalendarService(GoogleCalendarProvider())


@router.get("/events", response_model=list[EventDto])
async def get_events():
    return [EventDto.from_business(event) for event in
            calendar_service.get_events('51d6dnavf5k4gnqrgn5trqo70c@group.calendar.google.com', )]
