from fastapi import APIRouter

from fabioard.api.dto.event_dto import EventDto
from fabioard.domain.service_handler import ServiceHandler

router = APIRouter()



@router.get("/events", response_model=list[EventDto])
async def get_events():
    return [EventDto.from_business(event) for event in
            ServiceHandler.calendar_service().get_events('51d6dnavf5k4gnqrgn5trqo70c@group.calendar.google.com', )]
