# VillageNova Roadmap

## Current foundation

- Register residents once through `village_hub/register_resident.py`.
- Keep the canonical registry at `village_hub/data/residents.xlsx`.
- Keep each domain workbook and dry-run outbox under `village_hub/data/`.
- Run one hub command for daily delivery with a 24-hour per-resident gate.
- Use the hub runtime directly for dry-run testing and resident inspection.

## Delivery order

1. Stabilize storage: migrate legacy JSON and outside data files, verify
   workbook headers, and keep backups before cleanup.
2. Complete farmer integration: link farmer crop, stage, weather, and mandi
   details to the canonical hub resident ID.
3. Link domain memberships to hub resident IDs instead of duplicating name,
   phone, and location fields.
4. Replace mock feeds one provider at a time with source labels, timeouts, and
   deterministic fallbacks.
5. Schedule the hub daily and enable live messaging only after credentials and
   resident consent are configured.

## Rules

- Add a domain in its own agent module, but never add another resident store.
- `village_hub/main.py` is the only cross-domain orchestrator.
- `MOCK_MODE=true` remains the development default.
- Do not delete legacy data until it has been migrated and backed up.