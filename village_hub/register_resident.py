"""Register any village resident for one or more daily information streams."""
from resident_registry import CATEGORIES, add_resident


def ask(prompt: str, options: list[str] | None = None) -> str:
    while True:
        answer = input(prompt).strip()
        if answer and (not options or answer.lower() in [item.lower() for item in options]):
            return answer.lower()
        if options:
            print(f"Choose one of: {', '.join(options)}")
        else:
            print("Please enter a value.")


def run() -> None:
    print("VillageNova - Village Resident Registration")
    name = ask("Name: ")
    location = ask("Village or location: ")
    phone = ask("Phone number: ")
    channel = ask("Channel (SMS/WhatsApp): ", ["sms", "whatsapp"])
    language = ask("Language (English/Hindi/Telugu): ", ["english", "hindi", "telugu"])
    print("Categories: " + ", ".join(f"{key} ({label})" for key, label in CATEGORIES.items()))
    selected = ask("Choose categories separated by commas: ")
    categories = [item.strip().lower() for item in selected.split(",") if item.strip() in CATEGORIES]
    if not categories:
        print("At least one valid category is required.")
        return
    resident_id = add_resident({
        "name": name, "location": location, "phone": phone,
        "channel": channel, "language": {"hindi": "hi", "telugu": "te"}.get(language, "en"),
        "categories": sorted(set(categories)),
    })
    print(f"Saved resident #{resident_id}. Run main.py for the daily digest.")


if __name__ == "__main__":
    run()
