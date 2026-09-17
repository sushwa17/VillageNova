"""Support and safety guidance for women-focused services."""

from __future__ import annotations


def get_support_update(interest: str, group: str, support_type: str) -> str:
    """Return actionable guidance for local women support programs."""
    interest = (interest or "health").strip().lower()
    group = (group or "community group").strip()
    support_type = (support_type or "safety").strip().lower()

    lines = [
        f"Women support update: for {interest}, check the nearest local ASHA, ANM, Anganwadi, or panchayat worker for the next service date.",
        f"For {support_type} support, keep your contact list, emergency numbers, and trusted family or community contacts in one safe place.",
        f"If you are part of {group}, keep meeting notes, savings, and any support documents organized and private.",
    ]
    if support_type in {"safety", "violence", "protection"}:
        lines.append("For immediate danger or violence, move to a safe place and contact a trusted person or the official local emergency support service.")
    else:
        lines.append("Use verified local offices and trusted community networks before sharing private details or paying fees.")
    return " ".join(lines)
