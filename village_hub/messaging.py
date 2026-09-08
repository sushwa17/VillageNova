"""Dry-run village messaging adapter."""
import os
from datetime import datetime
from pathlib import Path

OUTBOX = Path(__file__).parent / "data" / "outbox.log"


def send_digest(resident: dict, message: str) -> str:
    if os.getenv("MOCK_MODE", "true").lower() == "true":
        OUTBOX.parent.mkdir(exist_ok=True)
        line = f"[{datetime.now().isoformat(timespec='seconds')}] {resident['channel'].upper()} -> {resident['phone']}: {message}\n"
        OUTBOX.open("a", encoding="utf-8").write(line)
        print(f"  [DRY RUN] {resident['channel'].upper()} to {resident['phone']}: {message}")
        return "dry-run-sent"
    raise RuntimeError("Live village messaging is not configured yet. Keep MOCK_MODE=true until a provider is added.")
