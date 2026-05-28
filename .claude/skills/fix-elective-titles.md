Fix missing course titles in an elective picker list by expanding `_CS_STATIC_COURSE_INFO` in `backend/routers/electives.py`.

## When to use

When an elective picker panel shows a course number as both the heading and subtitle (e.g., "CSC 4214" repeated twice), the course is not in `_CS_STATIC_COURSE_INFO` and the `_static_course()` fallback is returning `course_number` as the title.

## What to do

### 1. Identify the affected elective list

The user will name a key (e.g. `cs_external_elective`) or a concentration (e.g. "CS Privacy"). Find the corresponding `_STATIC` list in `backend/routers/electives.py` to get all course numbers used by that picker.

### 2. Find courses missing from `_CS_STATIC_COURSE_INFO`

Collect every course number string in the target list. Cross-reference with the keys in `_CS_STATIC_COURSE_INFO`. The missing ones are the courses that will show a repeated course number as title.

For `cs_external_elective`, these are typically cross-dept courses (AERO, BIO, COMS, EE, ENGL, ENVE, GEOL, GRC, HLTH, IME, ISLA, KINE, MATE, MATH, MCRO, ME, MSCI, PHIL, PHYS, PSY, STAT, etc.).

### 3. Fetch catalog pages per department

Group missing courses by department prefix. For each department, fetch the Cal Poly catalog courses page:

`catalog.calpoly.edu/coursesaz/[dept-lowercase]/`

e.g. `catalog.calpoly.edu/coursesaz/coms/` for COMS courses.

Extract: course number, course title, units. Only add entries for courses actually present in the target elective list — do not bulk-import entire departments.

### 4. Add entries to `_CS_STATIC_COURSE_INFO`

In `backend/routers/electives.py`, add each missing course to `_CS_STATIC_COURSE_INFO` in the appropriate department section (or create a new section comment for new departments). Format:

```python
"DEPT 1234": {"title": "Course Title from Catalog", "units": 3},
```

Units must match the catalog. If a course has a variable unit range (e.g., 1–4), use the typical unit value listed for the course or the unit value listed in the elective list itself.

### 5. Verify

Spot-check 3–5 courses per department via the API:

```bash
cd backend && python3 -c "
import sys; sys.path.insert(0,'.')
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
r = client.get('/electives/KEY_NAME')
courses = r.json()['courses']
for c in courses[:5]:
    print(c['course_number'], '|', c['title'], '|', c['units'])
"
```

Confirm titles are now real course names, not repeated course numbers.

### 6. Run tests

```bash
cd backend && .venv/bin/pytest tests/test_electives_api.py -v -k "KEY_NAME"
```

All tests must pass. If a test asserts a specific title for a course you changed, update it to match the new correct title.

## Note on cross-dept external electives

The `cs_external_elective` list (~136 courses from ~20 departments) is the largest gap. When fixing it, work department by department. The `_static_course()` fallback (returning course_number as title) remains for any courses truly not found in the catalog or left unfixed — it will not break the picker, just show a less informative subtitle.
