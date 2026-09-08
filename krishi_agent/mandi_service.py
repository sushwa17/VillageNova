"""Daily mandi price lookup with data.gov.in and an offline fallback."""
import os
import random
import hashlib
import datetime
import requests

from advisory_engine import CROPS


def get_mandi_price(crop: str, village: str) -> dict:
    crop_info = CROPS.get(crop, CROPS["wheat"])
    api_key = os.getenv("DATA_GOV_API_KEY", "")
    resource_id = os.getenv("AGMARKNET_RESOURCE_ID", "")
    if os.getenv("MOCK_MODE", "true").lower() != "true" and api_key and resource_id:
        try:
            response = requests.get(
                f"https://api.data.gov.in/resource/{resource_id}",
                params={"api-key": api_key, "format": "json", "limit": 50,
                        "filters[commodity]": crop_info["en"]}, timeout=10,
            )
            response.raise_for_status()
            records = response.json().get("records", [])
            if records:
                location_text = village.lower()
                record = next(
                    (item for item in records if location_text in " ".join(
                        str(item.get(field, "")) for field in ("market", "district", "state")
                    ).lower()),
                    records[0],
                )
                price = float(record.get("modal_price") or record.get("modal price") or 0)
                return {"market": record.get("market", crop_info["mandi"]), "price": round(price), "change": 0}
        except (requests.RequestException, TypeError, ValueError) as error:
            print(f"[mandi_service] Live API call failed ({error}); falling back to mock data.")

    seed = f"{crop}-{village}-{datetime.date.today()}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    rng = random.Random(h)
    return {"market": crop_info["mandi"], "price": rng.randint(1800, 6500), "change": rng.randint(-15, 15)}


def get_mandi_price_change(crop: str, village: str) -> int:
    return get_mandi_price(crop, village)["change"]
