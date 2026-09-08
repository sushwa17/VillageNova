"""Resolve a farmer's place into GPS coordinates."""
import os
import requests


def resolve_location(place: str) -> dict:
    """Use OpenWeather geocoding when configured, otherwise OpenStreetMap."""
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    try:
        if api_key:
            response = requests.get(
                "https://api.openweathermap.org/geo/1.0/direct",
                params={"q": f"{place},IN", "limit": 1, "appid": api_key}, timeout=8,
            )
            response.raise_for_status()
            result = response.json()[0]
            return {"latitude": result["lat"], "longitude": result["lon"], "source": "openweather"}
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": f"{place}, India", "format": "jsonv2", "limit": 1},
            headers={"User-Agent": "KrishiSetu/1.0"}, timeout=8,
        )
        response.raise_for_status()
        result = response.json()[0]
        return {"latitude": float(result["lat"]), "longitude": float(result["lon"]), "source": "openstreetmap"}
    except (IndexError, KeyError, ValueError, requests.RequestException) as error:
        print(f"[location_service] Could not resolve location ({error}); continuing without GPS.")
        return {"latitude": None, "longitude": None, "source": "manual"}