"""Live weather lookups for a farmer's village."""
import os
import requests


def get_weather(village: str, latitude: float | None = None, longitude: float | None = None) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is required for live weather data.")

    params = {"appid": api_key, "units": "metric"}
    if latitude is not None and longitude is not None:
        params.update({"lat": latitude, "lon": longitude})
    else:
        params["q"] = f"{village},IN"

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params,
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "rain": int(data.get("clouds", {}).get("all", 0)),
            "temp": round(data["main"]["temp"]),
            "wind": round(data["wind"]["speed"] * 3.6),
            "description": data.get("weather", [{}])[0].get("description", ""),
        }
    except (requests.RequestException, KeyError, TypeError, ValueError) as error:
        raise RuntimeError(f"Live weather lookup failed for {village}: {error}") from error
