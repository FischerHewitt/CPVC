# Mustang Blueprints — Claude Instructions

## Adding a New Major

Tell Claude: **"Add [MAJOR NAME] ([CODE], [TOTAL] units) to the flowchart system."**

Or just say **"Add [MAJOR NAME]"** and Claude will look up the units from the catalog.

Claude will follow this checklist:

1. Fetch the catalog page from catalog.calpoly.edu and extract every course
   with: course number, title, units, term (Freshman Fall → Senior Spring),
   and whether it's a major requirement, support course, or GE.
   - Verify each tile's units against the catalog. For paired lecture/lab
     requirements or slash-choice placeholders, use the catalog's required
     total units for that slot and make sure the flowchart total still matches
     the program total/range.

2. Add `[CODE]_FLOWCHART` in `backend/data/flowcharts.py`:
   - Prefix all IDs with `[CODE]_` to avoid collisions with other majors
   - `grid_col` 0–7 (Freshman Fall=0, Senior Spring=7), `grid_row` can be 0
     everywhere since `_compact_rows_by_category` handles it
   - `category`: `"major"`, `"support"`, `"ge"`, or `"concentration"`
     (use `"concentration"` for free/unrestricted electives)
   - `is_placeholder: True` for any elective slot, GE area, or placeholder
   - `prerequisites`: add where the prereq course exists in the same
     flowchart — use semester course number strings (e.g. `["AGB 2212"]`).
     **CRITICAL: If you rename a tile's `course_number` (e.g. to a slash-choice
     like `"MATH 1262/1265"`), you MUST update every `prerequisites` list in
     the same flowchart that references the old name.** After any course_number
     change, run the prerequisite validity check:
     `cd backend && python3 -c "import sys; sys.path.insert(0,'.');\
from data.flowcharts import FLOWCHARTS;\
[print(k,c['course_number'],c['id'],missing) for k,fc in FLOWCHARTS.items()\
for c in fc['courses'] if (missing:=[p for p in c['prerequisites']\
if p not in {x['course_number'] for x in fc['courses']}])]"`
   - `quarter_equivalents`: prioritize mappings for every direct semester
     course where one exists — many student transcripts still use quarter
     numbers

3. Call `_compact_rows_by_category([CODE]_FLOWCHART)` in the block near
   the bottom of `flowcharts.py`.

4. Add an entry to the `FLOWCHARTS` dict at the bottom of `flowcharts.py`.
   - **If this is a concentration-specific flowchart** (one whose key will be
     referenced as `full_flowchart_key` in `concentrations.py`), it MUST be
     registered in `concentrations.py` with `"full_flowchart_key": "KEY"` before
     the session ends — otherwise it will appear as a standalone major in the
     upload dropdown. The `/majors` endpoint filters these keys out automatically
     only when they are present in `concentrations.py`.

5. **REQUIRED — do not skip or defer:** While on the catalog page, look
   for any concentrations, emphases, tracks, or specializations.
   - If concentrations exist: add them to `backend/data/concentrations.py`
     following the existing pattern before moving on.
   - If no concentrations exist: confirm this explicitly (note it in your
     report) and write the test assertion `assert "CODE" not in CONCENTRATIONS`.
   Never leave this step unresolved. A major is not complete until
   concentrations are either added or confirmed absent.

5a. **REQUIRED — add catalog tips to the flowchart entry:**
    While on the catalog page, look for footnotes or numbered notes that
    appear below the course requirements table or the Plan of Study Grid.
    These are the superscript-referenced footnotes (¹²³…) explaining rules
    about the flowchart (e.g. unit minimums, course restrictions, GE overlaps,
    upper-division requirements).
    - Organize them into named sections in the `"notes"` field of the major's
      `FLOWCHARTS` entry. Each section is `{"title": "...", "items": [...]}`.
    - Use `"Flowchart Tips"` for structural rules about the flowchart layout
      (term placement, elective restrictions, prerequisite notes, unit floors).
    - Use `"GE Tips"` for notes about courses that satisfy both a major/support
      requirement and a GE area simultaneously.
    - Add other section titles if the catalog groups notes differently.
    - If there are no catalog footnotes, omit the `"notes"` key entirely.
    - **Also look for concentration-specific footnotes or notes** (often on the
      concentration detail page or a sub-table). If found, add a `"tips"`
      key (list of strings) directly to the matching concentration entry in
      `concentrations.py`. These tips will automatically appear under a
      "[Concentration Name] Tips" headline in the Tips panel only when that
      concentration is selected — do not duplicate them in the main flowchart
      notes.

6. **REQUIRED — wire checklist/sidebar course options for every selectable
   placeholder:**
   - Any slash-choice, support elective, technical elective, concentration
     elective, or other non-GE placeholder that should show course options in
     the Manual Course Checklist must have an `elective_key` in `flowcharts.py`
     or in the relevant concentration `slot_override`.
   - Add a matching entry to **`backend/data/electives_static.json`** (exact
     catalog lists) or **`backend/data/electives_dynamic.json`** (broad catalog
     buckets such as "any 3000–4000 level ME course"). Do NOT edit
     `backend/routers/electives.py` — that file is now only route handlers.
     - Static entry format: `"elective_key": [{"course_number": "...", "title": "...", "units": N}, ...]`
     - Dynamic entry format: `"elective_key": {"department": "...", "min_level": N, "max_level": N, "units": N}`
   - If the placeholder's `course_number` or `quarter_equivalents` would make
     the auto-picker expose old quarter numbers or incomplete options, add an
     entry to **`backend/data/placeholder_keys.json`**: `"placeholder_id": "elective_key"`.
   - Fixed course overrides in `concentrations.py` that replace a base elective
     slot must set `"elective_key": None` so they do not inherit the base
     picker.
   - For every picker option, use the exact catalog course number, title, and
     units.
   - Free/unrestricted elective placeholders may stay without an `elective_key`
     when there is no catalog-restricted course list to show.

7. Add a major-specific test in `backend/tests/test_flowchart_data.py`
   that checks: `total_units`, the sum of tile units when the catalog has a
   fixed total or accepted range, key course titles, categories, at least 2
   prerequisites, GE placeholders, elective placeholder `is_placeholder`,
   and whether the major is/isn't in `CONCENTRATIONS` (must reflect the
   actual result of step 5). Also assert `elective_key` values for every
   catalog-backed placeholder, and assert fixed concentration overrides clear
   inherited `elective_key` values with `None` when needed.

8. Add or update `backend/tests/test_electives_api.py` for every new entry
   added to `electives_static.json`, `electives_dynamic.json`, or
   `placeholder_keys.json` so the Manual Course Checklist can keep loading
   the right course options.

9. Run pytest from the backend directory using `.venv` and confirm all
   tests pass.

10. **REQUIRED — update the frontend fallback lists** in
    `frontend/app/upload/page.tsx`:
    - Add the new major to `FALLBACK_MAJORS`:
      `{ code: "CODE", name: "Full Major Name" },`
    - If concentrations exist, add them to `FALLBACK_CONCENTRATIONS` using the
      `concs(...)` helper with every concentration id and label. Example:
      ```
      CODE: concs(
        ["none", "No Concentration Selected"],
        ["conc_id", "Concentration Label"],
      ),
      ```
    - These fallbacks display when the API is unreachable, so every new major
      must be listed here or it won't appear in the upload dropdown.
    - **Do NOT add concentration-specific flowchart keys to `FALLBACK_MAJORS`.**
      Keys registered in `FLOWCHARTS` that are also referenced as
      `full_flowchart_key` in `concentrations.py` are automatically excluded
      from the `/majors` API response. Only add the base major code (e.g. `"CS"`)
      to `FALLBACK_MAJORS`, never the concentration keys (`"CS_AIML"`, etc.).
    - Run `cd frontend && npm run build` and confirm it completes with no
      errors. The Manual Course Checklist must display rows in this order:
      Major, Support, GE, then Concentration/free-elective items.

11. **REQUIRED — log all ambiguities to `catalog_ambiguities.txt`** in the
    repo root. Append a section for the new major using this format:

    ```
    --------------------------------------------------------------------------------
    [CODE] — [MAJOR NAME]
    --------------------------------------------------------------------------------
    - [Description of ambiguity, e.g. slash-choice tile, unit range variance,
      broad dynamic bucket, missing catalog info, assumed term placement, etc.]
    - ...
    ```

    If the major has zero ambiguities, append:
    ```
    [CODE] — [MAJOR NAME]: no ambiguities.
    ```

    Do not overwrite existing entries. Always append.

12. Do not commit or push when done.

13. Report any catalog ambiguities or elective buckets represented as
    placeholders.
