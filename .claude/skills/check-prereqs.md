Run the prerequisite validity check to find dangling prereq references in flowcharts.

Catches cases where a tile's `prerequisites` list references a course number that doesn't exist in the same flowchart — most commonly caused by renaming a `course_number` (e.g. to a slash-choice like `"MATH 1262/1265"`) without updating the `prerequisites` lists of downstream tiles.

## What to do

Run from the repo root:

```bash
cd backend && python3 -c "
import sys; sys.path.insert(0,'.')
from data.flowcharts import FLOWCHARTS
[print(k, c['course_number'], c['id'], missing)
 for k, fc in FLOWCHARTS.items()
 for c in fc['courses']
 if (missing := [p for p in c['prerequisites']
                 if p not in {x['course_number'] for x in fc['courses']}])]
"
```

If the user provides a major code (e.g. `/check-prereqs CS`), scope the check to that flowchart only by filtering `FLOWCHARTS.items()` — or just run the full check and filter the output.

## Output

- If no output: all prereqs are valid. Report "No dangling prerequisites found."
- If there is output: each line is `[FLOWCHART_KEY] [course_number] [tile_id] [list of missing prereq strings]`. Report every mismatch and identify the likely cause (usually a renamed `course_number` that was not updated in downstream `prerequisites` lists). Do not auto-fix — report and let the user decide.
