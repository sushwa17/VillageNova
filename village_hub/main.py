"""Send one personalized daily digest to every opted-in resident."""
from datetime import datetime, timedelta

from messaging import send_digest
from resident_registry import get_residents, mark_sent
from update_catalog import daily_updates


def build_message(resident: dict) -> str:
    greeting = {"hi": "Namaste", "te": "Namaskaram"}.get(resident["language"], "Hello")
    updates = daily_updates(resident["categories"])
    return "\n".join([f"{greeting} {resident['name']} ({resident['location']}), VillageNova update:", *updates])


def run() -> None:
    residents = get_residents()
    if not residents:
        print("No residents registered. Run register_resident.py first.")
        return
    for resident in residents:
        if resident.get("last_sent"):
            last_sent = datetime.fromisoformat(resident["last_sent"])
            if datetime.now() - last_sent < timedelta(hours=24):
                print(f"{resident['name']}: skipped (message sent within 24 hours).")
                continue
        message = build_message(resident)
        status = send_digest(resident, message)
        mark_sent(resident, message, status)
        print(f"{resident['name']}: {status}")


if __name__ == "__main__":
    run()
