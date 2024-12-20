import requests
from abc import ABC, abstractmethod
from typing import List
from models.event import Event
from utils.geocoding import GeocodingAPI

class BaseCrawler(ABC):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.geocoding_api = GeocodingAPI()

    @abstractmethod
    def crawl(self) -> List[Event]:
        pass

    def _make_request(self, url: str) -> requests.Response:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error making request to {url}: {str(e)}")
            return None

    def _enrich_location_data(self, event: Event):
        if event.address:
            coordinates = self.geocoding_api.get_coordinates(event.address)
            if coordinates:
                event.latitude, event.longitude = coordinates
