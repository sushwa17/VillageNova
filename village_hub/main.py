"""Send one personalized daily digest to every opted-in resident."""
from datetime import datetime, timedelta

from messaging import send_digest
from resident_registry import get_residents, mark_sent
from domain_runtime import message_for


DOMAIN_ALIASES = {"student": "education", "general": "village_updates"}


def build_message(resident: dict) -> str:
    greeting = {"hi": "Namaste", "te": "Namaskaram"}.get(resident["language"], "Hello")
    domains = [DOMAIN_ALIASES.get(category, category) for category in resident["categories"]]
    updates = [message_for(domain, resident) for domain in domains if domain != "farmer"]
    if "farmer" in resident["categories"]:
        updates.insert(0, message_for("farmer", resident))
    return "\n\n".join([f"{greeting} {resident['name']} ({resident['location']}), VillageNova update:", *updates])


def run(force: bool = False) -> list[dict]:
    residents = get_residents()
    if not residents:
        print("No residents registered. Run register_resident.py first.")
        return []
    results = []
    for resident in residents:
        if resident.get("last_sent"):
            last_sent = datetime.fromisoformat(resident["last_sent"])
            if not force and datetime.now() - last_sent < timedelta(hours=24):
                print(f"{resident['name']}: skipped (message sent within 24 hours).")
                results.append({"resident": resident["name"], "status": "skipped"})
                continue
        message = build_message(resident)
        status = send_digest(resident, message)
        mark_sent(resident, message, status)
        print(f"{resident['name']}: {status}")
        results.append({"resident": resident["name"], "status": status, "message": message})
    return results


if __name__ == "__main__":
    run()
