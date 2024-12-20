import requests
from typing import Optional, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class GeocodingAPI:
    def __init__(self):
        self.client_id = os.getenv('NAVER_CLIENT_ID')
        self.client_secret = os.getenv('NAVER_CLIENT_SECRET')
        self.geocode_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
        }
        
        params = {
            "query": address
        }

        try:
            response = requests.get(
                self.geocode_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            result = response.json()

            if result.get("addresses"):
                first_result = result["addresses"][0]
                return (
                    float(first_result["y"]),  # latitude
                    float(first_result["x"])   # longitude
                )
            return None

        except Exception as e:
            print(f"Geocoding error for address {address}: {str(e)}")
            return None