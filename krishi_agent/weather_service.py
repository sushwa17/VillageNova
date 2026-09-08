"""
Weather lookups, by village.

MOCK_MODE=true (the default in .env.example) never calls the internet —
it generates realistic, deterministic values from a hash of the village
name and today's date, so the whole pipeline runs and demos offline, and
the same village gives the same numbers all day (repeatable demos).

Set MOCK_MODE=false and add OPENWEATHER_API_KEY to go live.

Known simplification: OpenWeatherMap's free /weather endpoint doesn't
return a true "chance of rain" — that needs the One Call API (or IMD's
own feed). Cloud-cover % is used here as a rough stand-in; swap it for
a real precipitation-probability field once you're on a paid/IMD source.
"""
import os
import random
import hashlib
import datetime
import requests


def get_weather(village: str, latitude: float | None = None, longitude: float | None = None) -> dict:
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
    api_key = os.getenv("OPENWEATHER_API_KEY", "")

    if not mock_mode and api_key:
        try:
            resp = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"lat": latitude, "lon": longitude, "appid": api_key, "units": "metric"}
                if latitude is not None and longitude is not None
                else {"q": f"{village},IN", "appid": api_key, "units": "metric"},
                timeout=8,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "rain": int(data.get("clouds", {}).get("all", 0)),
                "temp": round(data["main"]["temp"]),
                "wind": round(data["wind"]["speed"] * 3.6),  # m/s -> km/h
                "description": data.get("weather", [{}])[0].get("description", ""),
            }
        except Exception as e:
            print(f"[weather_service] Live API call failed ({e}); falling back to mock data.")

    seed = f"{village}-{datetime.date.today()}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    rng = random.Random(h)
    return {
        "rain": rng.randint(10, 90),
        "temp": rng.randint(24, 44),
        "wind": rng.randint(5, 45),
        "description": "mock daily conditions",
    }
