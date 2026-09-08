"""
Krishi Setu — Farmer Registration Agent (run this first)

Asks a farmer a handful of basic questions and saves the answers to
data/farmers.xlsx. This CLI conversation is a stand-in for how this
would eventually run: over a phone call, an IVR menu, or a WhatsApp
chat — the questions, validation, and storage stay the same, only the
input/output channel changes.

Usage (in a VS Code terminal, inside the project's virtual environment):
    python agent.py
"""
from dotenv import load_dotenv
load_dotenv()

import os
import storage
from advisory_engine import CROPS
from location_service import resolve_location

STAGES = ["Sowing", "Vegetative", "Flowering", "Pre-harvest"]


def ask(prompt: str, options: list[str] | None = None) -> str:
    while True:
        answer = input(prompt).strip()
        if not options:
            if answer:
                return answer
            print("  Please enter a value.")
            continue
        for opt in options:
            if answer.lower() == opt.lower():
                return opt
        print(f"  Please choose one of: {', '.join(options)}")


def run():
    print("=" * 52)
    print(" Krishi Setu - Farmer Registration Agent")
    print("=" * 52)
    print("Answer a few basic questions to register. (Ctrl+C to cancel)\n")

    name = ask("Farmer's name: ")
    village = ask("Location (village, town, or district): ")
    latitude = None
    longitude = None
    location_source = "manual"
    if os.getenv("MOCK_MODE", "true").lower() == "true":
        print("  Location saved; GPS lookup will be used when live mode is enabled.")
    else:
        location = resolve_location(village)
        latitude, longitude = location["latitude"], location["longitude"]
        location_source = location["source"]

    crop_keys = list(CROPS.keys())
    crop_labels = [CROPS[c]["en"] for c in crop_keys]
    crop_label = ask(f"Crop ({'/'.join(crop_labels)}): ", crop_labels)
    crop = crop_keys[crop_labels.index(crop_label)]

    stage = ask(f"Growth stage ({'/'.join(STAGES)}): ", STAGES)
    language = ask("Preferred language (Hindi/English/Telugu): ", ["Hindi", "English", "Telugu"])
    phone = ask("Phone number (with country code, e.g. +9198xxxxxxx): ")
    channel = ask("Preferred channel (SMS/WhatsApp): ", ["SMS", "WhatsApp"])

    farmer_id = storage.add_farmer({
        "name": name,
        "village": village,
        "crop": crop,
        "stage": stage,
        "language": {"Hindi": "hi", "Telugu": "te"}.get(language, "en"),
        "phone": phone,
        "channel": channel.lower(),
        "latitude": latitude,
        "longitude": longitude,
        "location_source": location_source,
    })
    print(f"\nSaved. {name} registered as farmer #{farmer_id} in data/farmers.xlsx")
    print("Run agent.py again to register another farmer, or main.py to send advisories.")


if __name__ == "__main__":
    run()
