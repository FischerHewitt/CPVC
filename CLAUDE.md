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
     flowchart — use semester course number strings (e.g. `["AGB 2212"]`)
   - `quarter_equivalents`: prioritize mappings for every direct semester
     course where one exists — many student transcripts still use quarter
     numbers

3. Call `_compact_rows_by_category([CODE]_FLOWCHART)` in the block near
   the bottom of `flowcharts.py`.

4. Add an entry to the `FLOWCHARTS` dict at the bottom of `flowcharts.py`.

5. **REQUIRED — do not skip or defer:** While on the catalog page, look
   for any concentrations, emphases, tracks, or specializations.
   - If concentrations exist: add them to `backend/data/concentrations.py`
     following the existing pattern before moving on.
   - If no concentrations exist: confirm this explicitly (note it in your
     report) and write the test assertion `assert "CODE" not in CONCENTRATIONS`.
   Never leave this step unresolved. A major is not complete until
   concentrations are either added or confirmed absent.

6. **REQUIRED — wire checklist/sidebar course options for every selectable
   placeholder:**
   - Any slash-choice, support elective, technical elective, concentration
     elective, or other non-GE placeholder that should show course options in
     the Manual Course Checklist must have an `elective_key` in `flowcharts.py`
     or in the relevant concentration `slot_override`.
   - Add a matching `_STATIC` or `_DYNAMIC` entry in
     `backend/routers/electives.py`. Use `_STATIC` for exact catalog lists and
     `_DYNAMIC` only for broad catalog buckets such as "any 3000–4000 level ME
     course".
   - If the placeholder's `course_number` or `quarter_equivalents` would make
     the auto-picker expose old quarter numbers or incomplete options, add the
     placeholder id to `_PLACEHOLDER_ELECTIVE_KEY`.
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

8. Add or update `backend/tests/test_electives_api.py` for every new
   `_STATIC`, `_DYNAMIC`, or `_PLACEHOLDER_ELECTIVE_KEY` path so the Manual
   Course Checklist can keep loading the right course options.

9. Run pytest from the backend directory using `.venv` and confirm all
   tests pass.

10. If frontend checklist behavior changed, run the frontend tests and build.
    The Manual Course Checklist should display rows in this order: Major,
    Support, GE, then Concentration/free-elective items.

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
