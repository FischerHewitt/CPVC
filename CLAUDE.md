# Mustang Blueprints — Claude Instructions

## Adding a New Major

Tell Claude: **"Add [MAJOR NAME] ([CODE], [TOTAL] units) to the flowchart system."**

Or just say **"Add [MAJOR NAME]"** and Claude will look up the units from the catalog.

Claude will follow this checklist:

1. Fetch the catalog page from catalog.calpoly.edu and extract every course
   with: course number, title, units, term (Freshman Fall → Senior Spring),
   and whether it's a major requirement, support course, or GE.

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

5. If the major has concentrations/emphases/tracks, add them to
   `backend/data/concentrations.py` following the existing pattern.

6. Add a major-specific test in `backend/tests/test_flowchart_data.py`
   that checks: `total_units`, key course titles, categories, at least 2
   prerequisites, GE placeholders, elective placeholder `is_placeholder`,
   and whether the major is/isn't in `CONCENTRATIONS`.

7. Run pytest from the backend directory using `.venv` and confirm all
   tests pass.

8. Do not commit or push when done.

9. Report any catalog ambiguities or elective buckets represented as
   placeholders.
