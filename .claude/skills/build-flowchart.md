Build the flowchart data structure in `backend/data/flowcharts.py` for a new major.

## What to do

Use the course data from `/fetch-catalog` (or already available in context) to complete steps 2–4 of the add-major checklist.

### Step 2 — Write `[CODE]_FLOWCHART`

Add the flowchart constant to `backend/data/flowcharts.py`. Rules:
- Prefix every `id` with `[CODE]_` (e.g. `"CS_csc1024"`) to avoid collisions with other majors
- **For concentration-specific flowcharts**, use a short ALL_CAPS concentration prefix for tiles unique to that concentration (e.g. `AIML_`, `PRIV_`, `GRAPH_`). Shared tiles copied from the base major keep their original `[CODE]_` prefixed IDs. Never re-use an `id` that already exists in any other `FLOWCHARTS` entry.
- `grid_col` 0–7 maps to Freshman Fall → Senior Spring; set `grid_row: 0` everywhere (`_compact_rows_by_category` handles final row placement)
- `category`: `"major"`, `"support"`, `"ge"`, or `"concentration"` (use `"concentration"` for free/unrestricted elective slots)
- `is_placeholder: True` for any elective slot, GE area, or slash-choice placeholder
- `prerequisites`: list semester course number strings that appear elsewhere in this flowchart (e.g. `["CSC 1024"]`); never reference courses not in the flowchart
- `quarter_equivalents`: map every direct semester course to its quarter equivalent(s) where one exists

After writing the flowchart, run the prerequisite validity check to catch any dangling prereq references:
```
cd backend && python3 -c "import sys; sys.path.insert(0,'.');\
from data.flowcharts import FLOWCHARTS;\
[print(k,c['course_number'],c['id'],missing) for k,fc in FLOWCHARTS.items()\
for c in fc['courses'] if (missing:=[p for p in c['prerequisites']\
if p not in {x['course_number'] for x in fc['courses']}])]"
```
Fix any reported mismatches before continuing.

### Step 3 — Call `_compact_rows_by_category`

Find the block near the bottom of `flowcharts.py` where other majors call `_compact_rows_by_category(...)` and add:
```python
_compact_rows_by_category([CODE]_FLOWCHART)
```

### Step 4 — Add to `FLOWCHARTS` dict

Add an entry at the bottom of `flowcharts.py`:
```python
FLOWCHARTS["[CODE]"] = [CODE]_FLOWCHART
```

Notes and tips fields come later in `/add-concentrations`. Do not add a `"notes"` key yet.

If this is a concentration-specific flowchart (its key will be referenced as `full_flowchart_key` in `concentrations.py`), note that — it must be registered in `concentrations.py` before the session ends or it will appear as a standalone major in the upload dropdown.
