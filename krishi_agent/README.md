# Krishi Setu — Backend Agent

This is the backend half of the project: a farmer-registration agent plus
an advisory pipeline that sends crop/weather alerts over SMS or WhatsApp,
with everything logged to an Excel workbook.

It's the counterpart to the browser prototype from earlier — that one is
a demo/UX mockup with sliders standing in for real data; this is actual
code you run, that writes real files and (once you add API keys) sends
real messages.

## How it fits together

```
agent.py  ──registers a farmer──▶  data/farmers.xlsx ("Farmers" sheet)
                                          │
main.py ──reads farmers, then for each one:──┘
   │
   ├─ weather_service.py   (today's rain/temp/wind for their village)
   ├─ mandi_service.py     (this week's price change for their crop)
   ├─ advisory_engine.py   (turns conditions + crop stage into ONE message)
   └─ messaging_service.py (sends it via SMS/WhatsApp, or logs a dry run)
                                          │
                          data/farmers.xlsx ("DeliveryLog" sheet)
```

## Setup (VS Code)

1. Open this folder in VS Code (`File > Open Folder…`).
2. Open a terminal (`` Ctrl+` ``) and create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```
   If VS Code prompts "Select Interpreter", pick the `.venv` one.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add an OpenWeather API key.

## Try it

```
python agent.py     # register 2-3 test farmers — answer the prompts
python main.py       # runs the pipeline and prints what it WOULD send
```

Open `data/farmers.xlsx` afterwards — you'll see the `Farmers` sheet with
what you registered, and `DeliveryLog` with what was generated for each.
`data/outbox.log` has the same messages in plain text.

Run `main.py` again within 24 hours and a farmer is skipped automatically;
after 24 hours, each farmer receives a new personalized message.

## Going live

1. **Weather:** get a free key at openweathermap.org and add it to
   `OPENWEATHER_API_KEY` in `.env`. Weather is live and fails clearly when the
   key is missing or the API is unavailable; it does not use mock data.
   *Note: the free tier's cloud-cover % is used as a rough stand-in for
   rain probability — for a real probability figure, move to the One
   Call API (still free tier) or IMD's own data feed.*
2. **Messaging:** create a free Twilio account and join the WhatsApp
   sandbox (twilio.com/whatsapp) — it gives you a test number and a
   join code in minutes. Put `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN`
   into `.env`.
3. **Mandi prices:** create a free key at data.gov.in and set
   `DATA_GOV_API_KEY` plus the Agmarknet `AGMARKNET_RESOURCE_ID` in `.env`.
   The service uses the farmer's crop and location's market, with a local
   fallback if the API is unavailable.
4. **GPS location:** registration asks only for a village, town, or district.
   In live mode, that place is resolved through OpenWeather geocoding when
   its key is present, otherwise OpenStreetMap Nominatim is used.
5. Set `MOCK_MODE=false` in `.env` when you are ready to enable the other
   live providers. Re-run `main.py`.

## Known simplifications, on purpose

- Mandi data can still use deterministic mock values until its provider is
   configured. Weather always comes from OpenWeather once its key is set.
- Messaging defaults to a dry run (logs only) so you can't accidentally
  spend money or spam a real phone number while developing.
- The registration and advisory agents are transparent rule-based flows:
   the message includes the farmer's name, place, crop, stage, live weather,
   mandi price, and the reason for the selected action. An LLM can be added
   later as a language layer without allowing it to bypass the safety rules.

## Running on a schedule

Once you're happy with it, schedule `main.py` hourly or daily. The 24-hour
gate prevents duplicate messages even if the task runs frequently:
- **Linux/Mac:** `crontab -e`, add
   `0 * * * * /path/to/.venv/bin/python /path/to/main.py`
- **Windows:** Task Scheduler → create a task running
   `.venv\Scripts\python.exe main.py` every hour.
