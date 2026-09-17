"""Daily livelihoods and local opportunity guidance."""

from __future__ import annotations


def get_livelihood_update(work_type: str, need: str, audience: str) -> str:
    """Return practical market or work guidance for livelihoods support."""
    work_type = (work_type or "labour").strip().lower()
    need = (need or "jobs").strip().lower()
    audience = (audience or "general").strip().lower()

    lines = [
        f"Local livelihoods update for {work_type}: check verified panchayat, market board, and local skill centre notices before taking a job.",
        f"For {need}, compare nearby options, daily wages, and customer demand in the local area before accepting work or paying fees.",
        "Keep a simple record of work, payment, orders, and customer contacts so you can protect your income and avoid fraud.",
    ]
    if audience == "women":
        lines.append("Women workers should verify local support groups, SHG networks, and government training programmes before committing to a new opportunity.")
    else:
        lines.append("Use trusted local offices, banks, or registered training centres before sharing documents or paying advance fees.")
    return " ".join(lines)
