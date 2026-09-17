"""Practical irrigation guidance for local field conditions."""

from __future__ import annotations


def get_irrigation_plan(source: str, crop: str, equipment: str, stage: str = "general") -> str:
    """Return actionable advice for a farm based on source, crop, and irrigation method."""
    source = (source or "borewell").strip().lower()
    crop = (crop or "field crop").strip().lower()
    equipment = (equipment or "drip").strip().lower()
    stage = (stage or "general").strip().lower()

    advice = []
    if source in {"borewell", "well"}:
        advice.append("Check the water table and pump pressure before starting irrigation; avoid running the pump dry.")
    elif source in {"canal", "channel"}:
        advice.append("Confirm the canal turn and queue timing before opening gates or starting the pump.")
    elif source in {"tank", "pond"}:
        advice.append("Monitor tank storage and avoid over-irrigating when water levels are low.")
    else:
        advice.append("Verify the source flow and use the water schedule to prevent waste.")

    if equipment in {"drip", "micro", "sprinkler"}:
        advice.append(f"Use {equipment} irrigation for {crop} to improve water use efficiency and reduce evaporation.")
    else:
        advice.append(f"Inspect pump pipes, filters, and valves before operating irrigation for {crop}.")

    if stage in {"sowing", "seedling", "early growth", "vegetative"}:
        advice.append("Keep the root zone evenly moist without waterlogging during early growth stages.")
    elif stage in {"flowering", "fruiting", "maturity"}:
        advice.append("Avoid stress during flowering and fruit formation; irrigate based on soil moisture and crop stage.")
    else:
        advice.append("Water early morning or evening when possible to reduce evaporation and save energy.")

    advice.append("Check field drains, leaking pipes, and pump wiring before and after irrigation.")
    return " ".join(advice)
