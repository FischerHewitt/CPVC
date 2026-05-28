# Poly Planner Catalog Snapshot

This directory contains a local snapshot imported from:

`https://api.polyplanner.pro/catalogs`

The API shape is documented at:

`https://about.polyplanner.pro/docs/dev-guide/load-catalog-data`

`catalogs.json` includes the published `2022-2026` quarter catalog and the
published `2026-2028` semester catalog as returned by the Poly Planner Pro API.

`catalog-data/` is generated from `catalogs.json` with:

`backend/.venv/bin/python backend/scripts/export_polyplanner_catalog_data.py`

The generated folder follows the documented Poly Planner Pro loader structure:
catalog-level courses and general education files, plus one folder per degree
containing requirements, technical electives, mappings, and flowchart templates.
