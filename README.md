# VillageNova

VillageNova is a rural intelligence platform for the whole village.

## Project structure

```text
Krishisetu/
  krishi_agent/       Farmer crop, weather, mandi, and advisory service
  cattle_agent/       Cattle owner registration and animal-care advisories
  irrigation_agent/   Water, pump, canal, and irrigation updates
  livelihoods_agent/  Jobs, workers, artisans, shops, and schemes
  women_support/      Women-focused health, safety, training, and schemes
  health_agent/       Health-centre, sanitation, and nutrition information
  education_agent/    Schools, scholarships, and skills information
  public_services_agent/ Panchayat, utilities, pensions, and public schemes
  village_updates/    Common news, government notices, health, and education
  village_hub/        Shared resident registry and daily digest runner
```

`krishi_agent` remains the completed Krishi Setu farmer module. The other folders are
separate domain modules, and `village_hub` combines their updates for each
resident according to the work and interests they selected.

## Run the village-wide prototype

From this folder:

```powershell
cd village_hub
..\krishi_agent\.venv\Scripts\python.exe register_resident.py
..\krishi_agent\.venv\Scripts\python.exe main.py
```

The prototype uses mock updates and a dry-run outbox by default. It does not
send real messages. Resident data is stored in
`village_hub/data/residents.xlsx`:

- `Residents`: one row per registered resident and their selected domains.
- `DeliveryLog`: one row per personalized message sent to each resident.

If an older `residents.json` exists, the first run imports it automatically.

Each resident can choose multiple categories, for example:

```text
cattle, irrigation, livelihoods
```

Supported categories are `farmer`, `cattle`, `irrigation`, `livelihoods`,
`women`, `student`, `health`, `public_services`, and `general`.

## Daily automation

Schedule `village_hub/main.py` with Windows Task Scheduler once per day. The
hub keeps a 24-hour delivery gate per resident, matching the farmer module.
Each resident is processed separately and receives only their selected domain
updates; no resident receives another resident's selected categories.
Future live integrations can be added inside each domain folder without
mixing their logic into the hub.

## Run an individual agent

Every non-farmer domain has its own `agent.py` and `main.py`. Registration is
stored separately for that department in `data/<agent-name>.xlsx`, with a
`Profiles` sheet for registrations and a `DeliveryLog` sheet for sent
messages. Each department also writes its own `data/outbox.log`; no agent
shares another agent's profile or outbox. Hindi and Telugu registrations
receive localized message templates with their saved name, location, and
domain details included.

Example for cattle owners:

```powershell
cd cattle_agent
..\krishi_agent\.venv\Scripts\python.exe agent.py
..\krishi_agent\.venv\Scripts\python.exe main.py
```

The same pattern works in `irrigation_agent`, `livelihoods_agent`,
`women_support`, `health_agent`, `education_agent`, `public_services_agent`,
and `village_updates`. Each agent asks domain-specific questions and sends
only that department's updates to its own registered profiles. Existing
`profiles.json` files are imported into the department workbook the first time
the agent runs after this change.

To generate a fresh message on every delivery for free, install Ollama, run
`ollama pull llama3.2`, and copy `krishi_agent/.env.example` to
`krishi_agent/.env`. The default configuration uses Ollama locally at
`http://localhost:11434/v1` and does not need an API key. You can instead set
`OPENAI_API_KEY`, `OPENAI_MODEL`, and `OPENAI_BASE_URL` for a paid or hosted
OpenAI-compatible provider. Without a reachable provider, agents use the
verified fallback messages. The farmer module keeps its rule-based weather
and mandi advisories so safety recommendations remain grounded in actual
conditions.
The normal 24-hour delivery gate remains enabled; set `SEND_EVERY_RUN=true`
in `.env` when testing and you need a new generated message on every run.

## Safety and privacy

Keep phone numbers and API keys out of Git. The domain modules should publish
verified, local, actionable information and clearly label emergency contacts
or official sources. Set `MOCK_MODE=false` only after configuring and testing
real providers.
