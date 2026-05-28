Fetch a Cal Poly major's catalog page and extract all course data needed to build a flowchart.

## What to do

The user will give you a major name, code, and optionally a total unit count. If units aren't provided, find them on the catalog page.

1. Fetch `https://catalog.calpoly.edu/collegesanddepartments/` to locate the correct department link if needed, then fetch the major's catalog page (URL pattern: `https://catalog.calpoly.edu/programs/[major-slug]/`).

2. Extract every course in the Plan of Study Grid with:
   - Course number and title
   - Units
   - Term (Freshman Fall → Senior Spring, mapped to `grid_col` 0–7)
   - Category: `"major"`, `"support"`, or `"ge"`
   - Whether it's a placeholder (elective slot, GE area, slash-choice)
   - Prerequisites (only those that appear elsewhere in the same flowchart)

3. For slash-choice tiles (e.g. "CHEM 2240 or CHEM 2242"), use the catalog's required total units for that slot and represent as a single tile with a slash course number (e.g. `"CHEM 2240/2242"`).

4. Verify the sum of all tile units matches the program total (or falls within the stated range).

5. Note any ambiguities: unit range variances, missing catalog info, assumed term placements, broad elective buckets, paired lecture/lab slots, etc.

## Output

Produce a structured summary of all courses grouped by term, clearly listing course number, title, units, category, is_placeholder, prerequisites, and any notes. This output feeds directly into `/build-flowchart`.

Do not write any code yet — just report the extracted data.
