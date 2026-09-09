

"""Run the daily personalized farmer advisory pipeline."""
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
import storage
import os
from advisory_engine import build_personalized_message, evaluate_rules, generate_fresh_message
from weather_service import get_weather
from mandi_service import get_mandi_price
from messaging_service import send_message


def run():
    farmers = storage.get_all_farmers()
    if not farmers:
        print("No farmers registered yet. Run agent.py first.")
        return

    print(f"Running advisory pipeline for {len(farmers)} farmer(s)...\n")
    send_every_run = os.getenv("SEND_EVERY_RUN", "false").lower() == "true"
    for farmer in farmers:
        last_sent = storage.last_delivery_at(farmer["id"], farmer["name"])
        if not send_every_run and last_sent and datetime.now() - last_sent < timedelta(hours=24):
            print(f"{farmer['name']}: skipped (next message due after 24 hours).\n")
            continue

        weather = get_weather(farmer["village"], farmer.get("latitude"), farmer.get("longitude"))
        price = get_mandi_price(farmer["crop"], farmer["village"])
        conditions = {**weather, "price": price["change"]}

        fired = evaluate_rules(farmer, conditions)
        message = generate_fresh_message(farmer, weather, price, fired[0]) or build_personalized_message(
            farmer, weather, price, fired[0]
        )

        status = send_message(farmer["phone"], farmer["channel"], message)
        storage.log_delivery(farmer["name"], farmer["village"], farmer["channel"], message, status, farmer["id"])

        print(f"{farmer['name']} ({farmer['village']}, {farmer['crop']}/{farmer['stage']}):")
        print(f"  conditions: rain={weather['rain']}% temp={weather['temp']}C wind={weather['wind']}km/h price={price['change']:+d}%")
        print(f"  -> {message}  [{status}]\n")

    print("Done. See data/farmers.xlsx (DeliveryLog sheet) for the full record.")


if __name__ == "__main__":
    run()
