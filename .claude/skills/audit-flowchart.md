Audit an existing flowchart for correctness: unit totals, tile ID prefixes, grid_col range, prerequisite validity, and elective_key coverage.

## What to do

The user will name a major code (e.g. `/audit-flowchart CS`) or concentration flowchart key (e.g. `/audit-flowchart CS_AIML`). Run all checks below and report every finding.

### 1. Unit totals per term

Sum tile units for each `grid_col` value (0 = Freshman Fall … 7 = Senior Spring, or 0–9 for 5-year programs). Compare against the program total in the FLOWCHARTS entry (`total_units`). Report any term-level imbalance and whether the sum matches the total.

```python
cd backend && python3 -c "
import sys; sys.path.insert(0,'.')
from data.flowcharts import FLOWCHARTS
key = 'CODE'
fc = FLOWCHARTS[key]
from collections import defaultdict
totals = defaultdict(int)
for c in fc['courses']:
    totals[c['grid_col']] += c['units']
for col in sorted(totals):
    print(f'col {col}: {totals[col]}u')
print('Total:', sum(totals.values()), '/', fc['total_units'])
"
```

### 2. Tile ID prefix consistency

Every tile whose `id` is unique to this flowchart (not shared with other majors) should be prefixed with the flowchart key prefix (e.g. `AIML_`, `GAME_`, `PRIV_`). List any tiles whose `id` does not start with an expected prefix.

For concentration-specific flowcharts (full_flowchart_key pattern), shared base tiles (e.g. `CSC1001`, `MATH1261`) are expected — flag only tiles that look like they should be unique but aren't prefixed.

### 3. Grid_col range (4-year vs 5-year)

Check whether any tile uses `grid_col >= 8`. If so, confirm the major is a known 5-year program (currently: ARCH). If the catalog says 4 years but tiles have `grid_col 8–9`, that's a bug.

### 4. Prerequisite validity

Run `/check-prereqs [CODE]` logic scoped to this flowchart key. Report any dangling prerequisite references (prereq string not found as a `course_number` in the same flowchart).

### 5. Elective_key coverage

For every tile with `"is_placeholder": True` that is not a GE tile (category != "ge"), check whether it has an `elective_key`. Report any placeholder missing an `elective_key` that appears to have a catalog-backed course list (concentration electives, support electives, slash-choice tiles). Free/unrestricted electives without a defined course list may legitimately omit `elective_key`.

### 6. Units vs catalog

For any tile whose `units` value was flagged in an ambiguity or looks unusual (e.g., 4u for a course that's typically 3u), cross-reference `catalog_ambiguities.txt` and flag it. Do not auto-fix — just surface it.

## Output format

Report in sections: **Unit Totals**, **Tile ID Prefixes**, **Grid Col Range**, **Prerequisites**, **Elective Keys**, **Unit Flags**. Use "✓ OK" when a check passes and list specific findings when something needs attention.
