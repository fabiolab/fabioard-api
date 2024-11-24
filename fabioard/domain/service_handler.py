from fabioard.adapter.google_calendar_provider import GoogleCalendarProvider
from fabioard.adapter.harddrive_provider import HardDriveProvider
from fabioard.adapter.owm_provider import OpenWeatherMapProvider
from fabioard.adapter.star_provider import StarProvider
from fabioard.config import settings
from fabioard.domain.services.bus_service import BusService
from fabioard.domain.services.calendar_service import CalendarService
from fabioard.domain.services.picture_service import PictureService
from fabioard.domain.services.weather_service import WeatherService


class ServiceHandler:
    _bus_service = None
    _calendar_service = None
    _picture_service = None
    _weather_service = None

    @classmethod
    def bus_service(cls):
        if not cls._bus_service:
            cls._bus_service = BusService(StarProvider())
        return cls._bus_service

    @classmethod
    def calendar_service(cls):
        if not cls._calendar_service:
            cls._calendar_service = CalendarService(GoogleCalendarProvider())
        return cls._calendar_service

    @classmethod
    def picture_service(cls):
        if not cls._picture_service:
            cls._picture_service = PictureService(HardDriveProvider(path=settings.hardrive_path))
        return cls._picture_service

    @classmethod
    def weather_service(cls):
        if not cls._weather_service:
            cls._weather_service = WeatherService(OpenWeatherMapProvider())
        return cls._weather_service
