"""Daily domain updates for the village hub.

Replace these mock entries with verified department feeds as each module is
connected. The hub keeps category selection and message composition stable.
"""
from datetime import date

UPDATES = {
    "farmer": "Farmer update: check today's weather and crop advisory in krishi_agent.",
    "cattle": "Cattle update: keep clean drinking water available and check animals for heat stress. Contact the local veterinary worker for vaccination dates.",
    "irrigation": "Water update: inspect pump wiring before use and follow the local canal or borewell schedule. Avoid wasting water during hot hours.",
    "livelihoods": "Livelihood update: check the panchayat, market, and skill-centre notice boards for local work and training opportunities.",
    "women": "Women support update: ask the local health worker about upcoming health, nutrition, self-help group, and training services.",
    "student": "Education update: check the school notice board for attendance, scholarship, exam, and digital-learning information.",
    "health": "Health update: use the nearest government health centre for urgent care and confirm camp dates with the ASHA or ANM worker.",
    "public_services": "Public services update: check verified panchayat notices for ration, pensions, water, power, roads, and document services.",
    "general": "Village update: check verified panchayat notices for water, power, roads, public services, and government announcements.",
}


def daily_updates(categories: list[str]) -> list[str]:
    day = date.today().isoformat()
    return [f"{day} - {UPDATES[category]}" for category in categories if category in UPDATES]
