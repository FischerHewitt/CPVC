# Flowchart Migration: Per-Concentration Full Flowcharts

## What this is

Every major and concentration at Cal Poly SLO needs its own complete, independent flowchart.
Currently, many concentrations share a base flowchart and only override a few slots (`slot_overrides`).
This migration replaces that pattern with a full `full_flowchart_key` entry for every concentration.

## Source of truth

**`FlowchartPdf/General Curriculum in Computer Science.txt`**

This is a tab-delimited text export of the complete Cal Poly SLO catalog flowchart document.
It contains ~200+ grids covering all 65 majors and every concentration. Structure per grid:

```
General Curriculum in Computer Science - BS in Computer Science
First Year
	Term 1
	Units
	CSC/CPE 1000
	Computing Majors Orientation
	1
	...
	Units
	14
	Term 2
	...
	Total Units
	120
	1
Required in Major or Support; also satisfies General Education (GE) requirement.
	2
A minimum of 23 units is...
```

- Non-tab line = section header (major/concentration title)
- `\tTerm N` = start of a term (maps to `grid_col` 0–7)
- `\tCourse Number` followed by `\tTitle` followed by `\tUnits` = one course row
- `\tor Course Number` = slash-choice alternative for the previous course
- `\tUnits\n\tN` = term unit total (skip, use for validation only)
- `\tTotal Units\n\tN` = flowchart total (maps to `total_units`)
- Numbered lines after `Total Units` = footnotes → `notes` field

## Design decisions

### 1. Every concentration gets a full flowchart

All concentrations in `concentrations.py` must have a `full_flowchart_key` pointing to a
dedicated entry in `FLOWCHARTS`. The `slot_overrides` pattern is deprecated for all new work.

### 2. "Concentration Not Yet Declared" updates the base major flowchart in place

The "Concentration Not Yet Declared" grid from the txt is the canonical base curriculum
for each major. It is used to **validate and update** the existing base flowchart entry
(e.g., `CS`, `AERO`, `ME`) rather than creating a new separate entry.

The `full_flowchart_key` for the "not yet declared" concentration therefore points to the
base major key (e.g., `"full_flowchart_key": "CS"` for CS General Curriculum).

Example — CS general curriculum becomes "General Computer Science Curriculum" but keeps
the `CS` key in `FLOWCHARTS`. Its entry is updated in place against the txt.

### 3. Preserve existing prerequisites, quarter_equivalents, and elective_keys

The txt does not contain prerequisites, quarter_equivalents, or elective_key values.
When generating or updating a flowchart:

- **Course exists in current flowchart** → copy its `prerequisites`, `quarter_equivalents`,
  and `elective_key` into the new entry unchanged.
- **Course is new** (appears in a concentration flowchart with no current entry) → leave
  `prerequisites: []`, `quarter_equivalents: []`, `elective_key` absent.
  Mark for manual validation afterward.

### 4. Scope for this migration

**In scope:**
- Validate and update all 65 existing base major flowcharts against the txt
- Build full `FLOWCHARTS` entries for every concentration currently in `concentrations.py`
  that lacks a `full_flowchart_key`
- Register each new entry as `full_flowchart_key` in `concentrations.py`

**Out of scope (separate step):**
- Adding brand-new majors not currently in `FLOWCHARTS` at all (e.g., majors visible in
  the txt that have no current entry)

### 5. Upload page concentration picker behavior

No change. Majors with no concentrations continue to hide the concentration picker.
Majors with concentrations show the picker as today.
`FALLBACK_MAJORS` and `FALLBACK_CONCENTRATIONS` in `frontend/app/upload/page.tsx` must be
updated to include every new concentration.

## Implementation plan

### Step 1 — Write the txt parser (`backend/scripts/parse_flowchart_txt.py`)

Parse `FlowchartPdf/General Curriculum in Computer Science.txt` into a list of structured
dicts, one per flowchart grid:

```python
{
    "title": "Artificial Intelligence and Machine Learning Concentration - BS in Computer Science",
    "degree": "BS in Computer Science",
    "major_name": "Computer Science",
    "concentration_name": "Artificial Intelligence and Machine Learning Concentration",
    "total_units": 120,
    "terms": [
        {
            "year": 1,       # 1-4
            "term": 1,       # 1 or 2
            "grid_col": 0,   # 0-7
            "courses": [
                {
                    "course_number": "CSC/CPE 1000",
                    "title": "Computing Majors Orientation",
                    "units": 1,
                    "is_placeholder": False,
                    "or_alternatives": [],  # for slash-choice rows
                    "footnote_refs": [],    # superscript numbers found on the row
                }
            ],
            "term_units": 14
        }
    ],
    "footnotes": {
        "1": "Required in Major or Support; also satisfies General Education (GE) requirement.",
        "2": "A minimum of 23 units..."
    }
}
```

Parsing rules:
- `grid_col` = `(year - 1) * 2 + (term - 1)`, so Year 1 Term 1 → 0, Year 4 Term 2 → 7
- `grid_row` = 0 for all (let `_compact_rows_by_category` handle it)
- Slash-choice rows (`\tor X`) → set `is_placeholder: True`, combine into
  `course_number` as `"X/Y"` format matching existing conventions
- GE placeholders (`"General Education Requirement (1A)"`) → `category: "ge"`,
  `is_placeholder: True`
- Free/concentration elective placeholders → `category: "concentration"`,
  `is_placeholder: True`
- All other courses → `category` inferred from course prefix and position (see Step 2)

### Step 2 — Category inference

The txt does not label categories explicitly. Infer them:

- GE slots: match `"General Education Requirement"` in course_number/title → `"ge"`
- Free Elective / Concentration Elective / Technical Elective in title → `"concentration"`
- Everything else: look up in the existing flowchart for that major; if found, copy category.
  If not found, default to `"major"` and flag for review.

### Step 3 — Generate/update flowchart entries

For each parsed grid:

1. Look up the corresponding entry in `FLOWCHARTS` (by major code + concentration label).
2. For every course in the parsed grid:
   - If a matching course (same `course_number`) exists in the current flowchart entry,
     copy `prerequisites`, `quarter_equivalents`, `elective_key` from the current entry.
   - Otherwise create a skeleton course with empty/default values.
3. Write the updated entry back to `flowcharts.py`.

For the **"Concentration Not Yet Declared"** grid: update the base major entry in place
(diff only; report what changed).

For **new concentration flowcharts** (no existing `FLOWCHARTS` entry): create a new entry
following the naming convention `MAJOR_CONCENTRATION` (e.g., `BUS_ACCOUNTING`).

### Step 4 — Update concentrations.py

For every new `FLOWCHARTS` entry created in Step 3, set `full_flowchart_key` on the
corresponding concentration in `concentrations.py`.

### Step 5 — Update frontend/app/upload/page.tsx

Add all new concentrations to `FALLBACK_CONCENTRATIONS` using the `concs()` helper.

### Step 6 — Run tests

```bash
cd backend && .venv/bin/pytest
cd frontend && npm run build
```

Fix any failures before moving on.

### Step 7 — Discover majors missing from the application

After parsing the txt, compare every section header against the current `FLOWCHARTS` keys.
Write any major (degree program) present in the txt but absent from `FLOWCHARTS` to:

**`handoff/missing-majors.md`**

Format:
```
# Majors in txt not yet in FLOWCHARTS

- Art and Design (BFA) — concentrations: Graphic Design, Photography and Video, Studio Art
- [Major Name] ([Degree]) — concentrations: ...
```

This file is the backlog for the "add brand-new majors" step that is out of scope for this
migration. Do not add these majors during this migration — only document them here.

### Step 8 — Manual validation pass

For every flowchart whose courses changed (Step 3 diff output):
- Verify prerequisites still make sense for the new course list.
- Verify `quarter_equivalents` still apply.
- Verify `elective_key` values point to the right picker.
- Add missing prerequisites/quarter_equivalents/elective_keys for new courses.

## ID scheme for course tiles

**Shared courses** (same `course_number` exists in the base major flowchart): reuse the base major's `id` exactly. This preserves `course_positions` data when users switch concentrations.

**Concentration-unique courses** (not in the base major): `SLUG_COURSENUMBER` where SLUG is a short uppercase abbreviation of the concentration label. Example: `AIML_DATA3301`, `GAME_CSC3710`. The SLUG mapping is defined explicitly in the parser, not auto-generated at runtime.

**No global uniqueness required.** IDs only need to be unique within a single flowchart. The backend `_ALL_COURSES_LOOKUP` is keyed by `course_number`, not `id`.

## Unit ranges

Tiles with range units (e.g., "3-4") store `"units_display": "3-4"` in the intermediate JSON. When writing to `flowcharts.py`, use the minimum integer for `units` and store the display string separately. The tile frontend change to render "3-4" instead of "3" is a **separate task** tracked in `handoff/tile-unit-range-display.md`.

## Naming conventions

New concentration flowchart keys follow the pattern `MAJORCODE_SLUG`:

| Major | Concentration | Key |
|-------|--------------|-----|
| BUS | Accounting | `BUS_ACCOUNTING` |
| BUS | Entrepreneurship | `BUS_ENTREPRENEURSHIP` |
| COMS | Journalism | `COMS_JOURNALISM` |

Use uppercase, underscores, no spaces. Derive the slug from the concentration label by
uppercasing and replacing spaces/punctuation with underscores.
Trim trailing `_CONCENTRATION` from the slug (e.g., "Accounting Concentration" → `BUS_ACCOUNTING`).

## What currently exists vs. what needs to be built

### Already have full concentration flowcharts (no action needed except validation)
CS (5 concentration keys), CPE (6), CE (5), ME (4), AERO (2), EE (2), EIM (3), BIOC (1), CHEM (1), MATH (1)

### Need full concentration flowcharts built (currently slot_overrides only)
Check `concentrations.py` for every entry missing `full_flowchart_key`.
Majors known to need work: BUS, COMS, JOUR, KINE, POLS, SOC, GRC, FSN, ANTGEOG, BIO, BMED, WVIT, and others.

## Files to modify

| File | Change |
|------|--------|
| `backend/data/flowcharts.py` | Update 65 base entries; add N new concentration entries |
| `backend/data/concentrations.py` | Add `full_flowchart_key` to all slot-override concentrations |
| `frontend/app/upload/page.tsx` | Add new concentrations to `FALLBACK_CONCENTRATIONS` |
| `backend/tests/test_flowchart_data.py` | Add/update tests for every modified major |
| `backend/tests/test_electives_api.py` | Add tests for any new elective_key entries |
| `catalog_ambiguities.txt` | Log any ambiguities discovered during parsing |

## New file to create

| File | Purpose |
|------|---------|
| `backend/scripts/parse_flowchart_txt.py` | One-time parser; run it, inspect output, then commit the generated data |

---

## Final step — update project skills

After the migration is complete and tests pass, update the following skills in
`.claude/skills/` so future Claude sessions don't generate code against the old patterns.

### `.claude/skills/add-full-concentration.md`

**Step 0 — source references**: Replace the HTML/PDF source instructions with:
- Primary source: `FlowchartPdf/General Curriculum in Computer Science.txt` (tab-delimited, parseable)
- Parsed intermediate: `FlowchartPdf/parsed_flowcharts.json` (run `python3 backend/scripts/parse_flowchart_txt.py` to regenerate)
- For majors not in the txt (see `handoff/missing-majors.md`), fall back to `catalog.calpoly.edu`

**ID scheme**: Update to match the confirmed convention:
- Courses shared with the base major → reuse the base major's `id`
- Concentration-unique courses → `SLUG_COURSENUMBER` (short uppercase abbreviation of concentration)

**Elective wiring**: The skill references `backend/routers/electives.py` for `_STATIC`/`_DYNAMIC`
entries. This is outdated — electives now live in `backend/data/electives_static.json` and
`backend/data/electives_dynamic.json`. Update all references accordingly.

### `.claude/skills/add-concentrations.md`

**Deprecate slot_overrides (Pattern A) for new work**: Add a note at the top:

> All new concentrations should use Pattern B (`full_flowchart_key`) — see
> `/add-full-concentration`. Pattern A (`slot_overrides`) is no longer used for
> new concentrations. `slot_overrides` on existing entries may remain for legacy
> compatibility but should not be added to new entries.

Keep the `"elective_key": None` guidance — it still applies to fixed overrides in
any remaining legacy slot_overrides entries.

### `.claude/skills/wire-electives.md`

**Fix stale file references**: The skill says to add `_STATIC` and `_DYNAMIC` entries in
`backend/routers/electives.py`. This is wrong — those now live in JSON files:
- Static lists → `backend/data/electives_static.json`
- Dynamic buckets → `backend/data/electives_dynamic.json`
- Placeholder key overrides → `backend/data/placeholder_keys.json`

Update every `electives.py` reference in the skill to point to the correct JSON files.
The route handlers in `electives.py` are now read-only; do not edit them.

### `.claude/skills/build-flowchart.md`

**ID prefix convention**: The skill says prefix all IDs with `[CODE]_`. Add a note:

> For concentration-specific flowcharts (those registered with `full_flowchart_key`),
> use the concentration key as the prefix for concentration-unique tiles (e.g. `AIML_`,
> `ACCT_`). Tiles shared with the base major reuse the base major's `id` exactly — do
> not re-prefix them with the concentration key.

### Skills that do NOT need changes

`audit-flowchart.md`, `check-prereqs.md`, `fetch-catalog.md`, `fix-elective-titles.md`,
`log-ambiguities.md`, `resolve-ambiguity.md`, `run-tests.md`, `update-frontend.md`,
`write-tests.md` — these describe processes that are unchanged by the migration.
