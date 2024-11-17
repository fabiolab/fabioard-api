import pendulum
import requests

from fabioard.domain.business.bus_schedule import BusSchedule
from fabioard.domain.protocol.bus_schedule_provider_protocol import BusProviderProtocol


class StarProvider(BusProviderProtocol):

    def __init__(self):
        self.base_url = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-circulation-passages-tr/records"

    def get_next_bus(self, bus_station: str, bus_line: str, bus_destination: str) -> list[BusSchedule]:
        params = {
            "limit": 20,
            "timezone": "Europe/Paris",
            "refine": [f'nomcourtligne:"{bus_line}"', f'nomarret:"{bus_station}"',
                       f'destination:"{bus_destination}"']
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code >= 400:
            raise Exception(f"Error while requesting: {response.text}")

        data = response.json()
        return [BusSchedule(bus_number=schedule['idligne'],
                            destination=schedule['destination'],
                            departure_time=pendulum.parse(schedule['arrivee']),
                            bus_stop=schedule['nomarret']) for schedule in data.get('results', [])]
