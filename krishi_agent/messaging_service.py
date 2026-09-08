"""
Sends the advisory to the farmer, over SMS or WhatsApp.

MOCK_MODE=true (the default) never contacts a real network — it writes
to data/outbox.log and prints to the console, so you can verify the
entire pipeline end-to-end for free before paying for anything.

Going live uses Twilio, since it's the fastest way to get a working
WhatsApp sender for testing (Twilio's WhatsApp sandbox is free to join).
For production at scale you'd eventually look at Meta's WhatsApp
Business Cloud API directly (no per-message Twilio markup, but more
setup/verification) — this module is the one place you'd change.
"""
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTBOX_LOG = os.path.join(DATA_DIR, "outbox.log")


def _dry_run_send(to: str, channel: str, message: str) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {channel.upper()} -> {to}: {message}\n"
    with open(OUTBOX_LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"  [DRY RUN] {channel.upper()} to {to}: {message}")
    return "dry-run-sent"


def send_message(to: str, channel: str, message: str) -> str:
    """channel: 'sms' or 'whatsapp'. Returns a status string (a Twilio SID when live)."""
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
    if mock_mode:
        return _dry_run_send(to, channel, message)

    from twilio.rest import Client  # imported lazily - only required once you go live
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        raise RuntimeError("MOCK_MODE is off but TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN are missing in .env")
    client = Client(sid, token)

    if channel == "whatsapp":
        from_number = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
        msg = client.messages.create(from_=from_number, body=message, to=f"whatsapp:{to}")
    else:
        from_number = os.getenv("TWILIO_SMS_FROM")
        if not from_number:
            raise RuntimeError("TWILIO_SMS_FROM is missing in .env")
        msg = client.messages.create(from_=from_number, body=message, to=to)
    return msg.sid
