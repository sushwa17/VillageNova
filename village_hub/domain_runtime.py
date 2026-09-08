"""Runtime shared by the independently runnable village domain agents."""
import json
from datetime import datetime, timedelta
from pathlib import Path

DOMAIN_DEFINITIONS = {
    "cattle": {
        "title": "Cattle Agent",
        "fields": [("animals", "Animals (cow/buffalo/goat/sheep): "), ("count", "Approximate number of animals: "), ("concern", "Main concern (fodder/health/milk/vaccination): ")],
        "messages": [
            "Keep clean water and shade available for {animals}; monitor {concern} closely.",
            "Record the next vaccination or deworming date with your local veterinary worker.",
            "If an animal stops eating, has high fever, or cannot stand, contact a veterinarian promptly.",
        ],
    },
    "irrigation": {
        "title": "Irrigation Agent",
        "fields": [("source", "Water source (borewell/canal/tank/river): "), ("crop", "Main crop or area served: "), ("equipment", "Equipment (pump/drip/sprinkler/none): ")],
        "messages": [
            "For {source} irrigation of {crop}, check the local water turn before starting the pump.",
            "Inspect cables, earthing, pipes, and leaks before operating {equipment}.",
            "Water early morning or evening when possible to reduce evaporation and protect the supply.",
        ],
    },
    "livelihoods": {
        "title": "Livelihoods Agent",
        "fields": [("work", "Work or skill (driver/tailor/shop/artisan/labour/other): "), ("need", "Information needed (jobs/training/loans/market): ")],
        "messages": [
            "Livelihood update for {work}: check the panchayat and skill-centre notice boards for verified opportunities.",
            "For {need}, use official bank, government, or registered training-centre contacts before sharing documents or paying fees.",
            "Keep a simple record of work, payments, and customer orders to protect your income.",
        ],
    },
    "women": {
        "title": "Women Support Agent",
        "fields": [("interest", "Main interest (health/SHG/training/safety/childcare): "), ("group", "Self-help group or community group (optional): ")],
        "messages": [
            "Women support update for {interest}: ask the ASHA, ANM, Anganwadi, or panchayat worker about the next local service date.",
            "For self-help groups such as {group}, keep meeting notes, savings, and loan records safely.",
            "For immediate danger or violence, contact a trusted person and the official local emergency or support service.",
        ],
    },
    "health": {
        "title": "Health Agent",
        "fields": [("topic", "Health topic (nutrition/maternal/child/elderly/sanitation): "), ("age_group", "Person or age group needing information: ")],
        "messages": [
            "Health update for {topic}, especially for {age_group}: confirm dates with the government health centre or ASHA worker.",
            "Do not delay urgent care for severe breathing trouble, chest pain, heavy bleeding, unconsciousness, or serious injury.",
            "Keep prescriptions and vaccination records together and do not share private medical details publicly.",
        ],
    },
    "education": {
        "title": "Education Agent",
        "fields": [("learner", "Learner (child/adult/student): "), ("need", "Need (school/scholarship/exam/skills/digital): ")],
        "messages": [
            "Education update for {learner}: check the school or official portal for {need} notices.",
            "Ask the teacher or education office about scholarships and deadlines; never pay an unverified agent.",
            "Set aside a regular study time and keep school documents and application numbers safely.",
        ],
    },
    "public_services": {
        "title": "Public Services Agent",
        "fields": [("service", "Service needed (ration/pension/water/power/documents/roads): "), ("ward", "Ward, hamlet, or local area: ")],
        "messages": [
            "Public-service update for {service} in {ward}: verify the latest notice with the panchayat office.",
            "Keep application receipts and acknowledgement numbers; do not pay unofficial fees for government services.",
            "Report unsafe roads, outages, or water problems through the official local complaint channel.",
        ],
    },
    "village_updates": {
        "title": "Village Updates Agent",
        "fields": [("interests", "Interests (news/health/weather/school/schemes): ")],
        "messages": [
            "Village update for {interests}: use verified panchayat, school, health-centre, and department notices.",
            "Check the date and source before forwarding a message; do not forward rumours or unverified emergency claims.",
            "Keep important local helpline numbers saved and share urgent verified notices responsibly.",
        ],
    },
}


def _paths(folder: Path) -> tuple[Path, Path]:
    data_dir = folder / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir / "profiles.json", data_dir / "outbox.log"


def _load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def register(domain: str, folder: Path) -> None:
    definition = DOMAIN_DEFINITIONS[domain]
    profiles_file, _ = _paths(folder)
    profiles = _load(profiles_file)
    profile = {
        "id": max((item["id"] for item in profiles), default=0) + 1,
        "name": input("Name: ").strip(),
        "location": input("Village or location: ").strip(),
        "phone": input("Phone number: ").strip(),
        "channel": input("Channel (sms/whatsapp): ").strip().lower() or "sms",
        "language": input("Language (english/hindi/telugu): ").strip().lower() or "english",
        "last_sent": None,
    }
    for key, prompt in definition["fields"]:
        profile[key] = input(prompt).strip()
    profiles.append(profile)
    profiles_file.write_text(json.dumps(profiles, indent=2), encoding="utf-8")
    print(f"Saved {definition['title']} profile #{profile['id']}. Run main.py to send updates.")


def _message(domain: str, profile: dict) -> str:
    definition = DOMAIN_DEFINITIONS[domain]
    greeting = {"hindi": "Namaste", "telugu": "Namaskaram"}.get(profile["language"], "Hello")
    lines = [f"{greeting} {profile['name']} ({profile['location']}), VillageNova {definition['title']} daily update:"]
    lines.extend(message.format(**profile) for message in definition["messages"])
    return "\n".join(lines)


def run(domain: str, folder: Path) -> None:
    definition = DOMAIN_DEFINITIONS[domain]
    profiles_file, outbox_file = _paths(folder)
    profiles = _load(profiles_file)
    if not profiles:
        print("No profiles registered. Run agent.py first.")
        return
    for profile in profiles:
        if profile.get("last_sent") and datetime.now() - datetime.fromisoformat(profile["last_sent"]) < timedelta(hours=24):
            print(f"{profile['name']}: skipped (message sent within 24 hours).")
            continue
        message = _message(domain, profile)
        timestamp = datetime.now().isoformat(timespec="seconds")
        with outbox_file.open("a", encoding="utf-8") as stream:
            stream.write(f"[{timestamp}] {profile['channel'].upper()} -> {profile['phone']}: {message}\n")
        profile["last_sent"] = timestamp
        print(f"[DRY RUN] {profile['channel'].upper()} to {profile['phone']}:\n{message}\n")
    profiles_file.write_text(json.dumps(profiles, indent=2), encoding="utf-8")
