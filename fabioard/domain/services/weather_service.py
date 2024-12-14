from fabioard.domain.business.weather import Weather, WeatherByDay
from fabioard.domain.protocol.weather_provider_protocol import WeatherProviderProtocol


class WeatherService:
    def __init__(self, weather_provider: WeatherProviderProtocol):
        self.weather_provider = weather_provider

    def get_weather(self, city: str) -> Weather:
        return self.weather_provider.get_weather(city)

    def get_forecast(self, city: str) -> list[Weather]:
        return self.weather_provider.get_weather_forecast(city)

    def get_forecast_by_day(self, city: str) -> list[WeatherByDay]:
        forecast = self.weather_provider.get_weather_forecast(city)

        # Aggregate the forecast by day
        forecast_by_day = {}
        for weather in forecast:
            date = weather.date.format("YYYY-MM-DD")
            if date not in forecast_by_day:
                forecast_by_day[date] = {"min": weather, "max": weather}
            else:
                if weather.temperature < forecast_by_day[date]["min"].temperature:
                    forecast_by_day[date]["min"] = weather
                if weather.temperature > forecast_by_day[date]["max"].temperature:
                    forecast_by_day[date]["max"] = weather
        
        return [
            WeatherByDay(
                min=day["min"],
                max=day["max"],
                date=day["min"].date
            )
            for day in forecast_by_day.values()
        ]
 