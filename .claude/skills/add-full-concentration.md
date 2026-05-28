Add a new concentration that requires a completely independent flowchart (Pattern B / full_flowchart_key). Use this when the concentration moves required, support, or GE courses to different terms — not just swapping elective slots.

If the concentration only changes which elective slots are filled, use slot_overrides instead (Pattern A — covered in `/add-concentrations`).

See also: `flowchart-concentration-mapping.txt` in the repo root for the full rationale and a CS-concentration breakdown as a worked example.

## When to use Pattern B

Look at the concentration's Plan of Study Grid in the catalog. If any required course (major, support, or GE) appears in a different term than the base major flowchart, you need Pattern B. If only elective/capstone slots differ, use Pattern A.

## Steps

### 0. Verify the source flowchart against the PDF BEFORE building

**Do this first, before writing any code.**

Source-of-truth files live in `/Users/fischerhewitt/Documents/CPVC/FlowchartPdf/`:
- HTML exports (Google Docs) — **preferred**: strip tags with Python regex to extract plain text for the relevant major section.
- `allMajors.pdf` — fallback if the HTML section is missing or ambiguous. The Read tool's internal renderer does not work; use `pdftotext` via Bash.
- `parsed_flowcharts.json` / `merged_concentration_entries.json` — pre-parsed grids from the migration pipeline; check these first before re-parsing from PDF.

**HTML extraction (preferred):**
```python
import re
with open('/Users/fischerhewitt/Documents/CPVC/FlowchartPdf/[SomeName].html', 'r') as f:
    html = f.read()
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'[ \t]+', ' ', text)
idx = text.find('[Major Name]')
print(text[idx:idx+5000])
```

**PDF fallback:**
```bash
pdftotext -f [START_PAGE] -l [END_PAGE] /Users/fischerhewitt/Documents/CPVC/FlowchartPdf/allMajors.pdf -
```

Cross-check the concentration's Plan of Study Grid against:
1. The base `[CODE]_FLOWCHART` tiles — confirm every course number, unit count, and term (grid_col) matches
2. The concentration-specific tiles — confirm override courses match exactly

If anything in the base flowchart is wrong, fix it first. Do not build a concentration flowchart on top of a bad base.

### 1. Build the independent flowchart

In `backend/data/flowcharts.py`, define a new list:

```python
[CODE]_[CONC]_FLOWCHART: list[Course] = [ ... ]
```

- Base it on the existing `[CODE]_FLOWCHART` — copy all shared tiles verbatim (same `id`, `course_number`, etc.)
- For tiles that move to a different term, update `grid_col` on the copied tile
- For new required courses added by the concentration, add new tiles with a concentration-specific `id` prefix
- For concentration elective slots, add placeholder tiles with `is_placeholder: True` and an `elective_key`
- **ID prefix convention**: concentration-unique tile IDs should use a short ALL_CAPS prefix derived from the concentration name (e.g. `AIML_`, `PRIV_`, `GRAPH_`) — not `CONC_`. This avoids collisions when multiple concentrations share a base major. Never re-use an `id` that already exists in any other flowchart in the same `FLOWCHARTS` dict.

### 2. Compact rows

Add a `_compact_rows_by_category([CODE]_[CONC]_FLOWCHART)` call in the compaction block near the bottom of `flowcharts.py` (alongside the other `_compact_rows_by_category` calls).

### 3. Register in FLOWCHARTS

```python
"[CODE]_[CONC]": {
    "major": "[Major Name]",
    "total_units": [N],
    "columns": [...],  # copy from base flowchart
    "courses": [CODE]_[CONC]_FLOWCHART,
}
```

The `/majors` API automatically excludes this key from the upload dropdown once step 4 is done (via `_CONCENTRATION_FLOWCHART_KEYS` filter in `routers/flowchart.py`).

### 4. Add concentration entry in concentrations.py

```python
{
    "id": "conc_id",
    "name": "Concentration Display Name",
    "full_flowchart_key": "[CODE]_[CONC]",
    "slot_overrides": {},
}
```

This is what causes the `/majors` filter to exclude `"[CODE]_[CONC]"` from the dropdown. **Do not skip this step** — without it the concentration appears as a standalone major.

### 5. Wire elective pickers

For every concentration-specific placeholder tile, follow the `/wire-electives` skill to add entries in `backend/data/electives_static.json` or `backend/data/electives_dynamic.json`. Do NOT edit `backend/routers/electives.py` — that file is route handlers only.

### 6. Add catalog tips (if applicable)

If the concentration catalog page has footnotes or special rules, add a `"tips"` key (list of strings) to the concentration entry in `concentrations.py`. These appear in the Tips panel only when the concentration is selected.

### 7. Write tests

In `backend/tests/test_flowchart_data.py`, add assertions for:
- `total_units == [N]`
- The key tiles that changed (moved courses: correct `grid_col`; new courses: correct `course_number`, `units`, `category`)
- `"full_flowchart_key": "[CODE]_[CONC]"` in the concentration entry
- Elective placeholder `is_placeholder == True` and `elective_key` values

In `backend/tests/test_electives_api.py`, add tests for every new `_STATIC` or `_DYNAMIC` elective key.

### 8. Update frontend fallback

In `frontend/app/upload/page.tsx`, add the concentration to `FALLBACK_CONCENTRATIONS` under the base major code:

```typescript
[CODE]: concs(
    ...existing,
    ["conc_id", "Concentration Display Name"],
),
```

**Do NOT add `"[CODE]_[CONC]"` to `FALLBACK_MAJORS`** — only the base code (e.g. `"CS"`) belongs there.

### 9. Run tests and build

```bash
cd backend && .venv/bin/pytest
cd frontend && npm run build
```

Both must pass with no errors before the work is done.

### 10. Verify the dropdown

After starting the dev server, confirm: the base major appears once in the upload dropdown, the new concentration appears in the concentration picker, and no standalone `[CODE]_[CONC]` entry exists.

### 11. Log ambiguities

Run `/log-ambiguities` for any unit assumptions, slash-choice tiles, or term placements inferred rather than read directly from the catalog.

## Checklist

- [ ] Independent flowchart defined with concentration-prefixed unique tile IDs
- [ ] `_compact_rows_by_category` called for the new flowchart
- [ ] Registered in `FLOWCHARTS` dict
- [ ] `full_flowchart_key` entry added in `concentrations.py`
- [ ] Elective pickers wired for all concentration-specific placeholders
- [ ] Tests written and passing
- [ ] Frontend fallback updated (concentration only, not FALLBACK_MAJORS)
- [ ] `npm run build` passes
- [ ] Ambiguities logged
