"""Nutrition guidance for cattle owners."""

from __future__ import annotations

NUTRITION_GUIDE = {
    "cow": {
        "milk": [
            "Provide green fodder like napier, maize, sorghum, and hybrid bajra to support milk production.",
            "Give dry roughage such as wheat straw or paddy straw plus mineral mixture for balanced nutrition.",
            "Keep clean drinking water available and add concentrate feed only as advised by a local veterinarian.",
        ],
        "general": [
            "Feed a mix of green fodder, dry roughage, and a small amount of concentrate for energy and body condition.",
            "Use mineral salt and ensure regular access to clean water and shade.",
            "Avoid mouldy fodder, sudden feed changes, and overfeeding concentrates.",
        ],
    },
    "buffalo": {
        "milk": [
            "Offer lush green fodder, legume fodder, and quality roughage to support higher milk yield.",
            "Add a balanced concentrate mix and mineral supplements based on local veterinary guidance.",
            "Keep water and rest periods consistent, especially during hot weather.",
        ],
        "general": [
            "Use green fodder and dry roughage as the main base, with concentrate feed in measured amounts.",
            "Monitor body condition and provide mineral salt for better health and fertility.",
            "Maintain clean pens and avoid spoiled feed.",
        ],
    },
    "goat": {
        "milk": [
            "Give good-quality green fodder, browse leaves, and roughage; add protein-rich concentrate if needed.",
            "Provide clean water and a mineral supplement for growth and milk production.",
            "Avoid feeding too much grain or spoiled feed.",
        ],
        "general": [
            "Use a mix of green fodder, dry roughage, and small amounts of grains or concentrates.",
            "Keep fresh drinking water and mineral salt always available.",
            "Watch for signs of digestive upset after new feed.",
        ],
    },
    "sheep": {
        "milk": [
            "Provide good roughage and green fodder with enough protein for lactating sheep.",
            "Use grain or concentrate carefully and keep mineral supplements available.",
            "Offer fresh water and avoid dusty feed storage.",
        ],
        "general": [
            "Base the diet on roughage and green fodder, with limited concentrate feed.",
            "Ensure minerals and clean water are available every day.",
            "Rotate grazing and avoid overgrazing on damaged land.",
        ],
    },
}


def get_nutrition_plan(cattle_type: str, purpose: str = "general") -> str:
    """Return simple nutrition guidance for the selected cattle type."""
    normalized_type = (cattle_type or "cow").strip().lower()
    category = purpose.strip().lower() if purpose else "general"
    guide = NUTRITION_GUIDE.get(normalized_type, NUTRITION_GUIDE["cow"])
    plan = guide.get(category, guide["general"])
    return " ".join(plan)
