Add concentrations and catalog tips/notes for a major. Covers steps 5 and 5a of the add-major checklist.

## What to do

### Step 5 — Concentrations (REQUIRED, never skip)

Re-check the catalog page for any concentrations, emphases, tracks, or specializations.

**If concentrations exist:**
- Add them to `backend/data/concentrations.py` following the existing pattern
- Each concentration needs: `id`, `label`, `slot_overrides` (a dict of course id → override fields), and optionally `full_flowchart_key`
- If a concentration replaces a base elective slot with a fixed course, set `"elective_key": None` on that override so it does not inherit the base picker
- **Pattern B (preferred for new concentrations)**: If the concentration has its own Plan of Study Grid (i.e. any required, support, or GE course appears in a different term), register a separate `[CODE]_[CONC]_FLOWCHART` and set `"full_flowchart_key"` in the concentration entry. Use `/add-full-concentration` for the full procedure.
- **Pattern A (slot_overrides only, deprecated for grids that differ from the base)**: Only use `slot_overrides` without `full_flowchart_key` when the concentration differs from the base major *only* in which elective slots are filled — not in the required course schedule. Do not use Pattern A for concentrations whose Plan of Study Grid moves required courses to different terms.
- Look for concentration-specific footnotes on the catalog page or sub-tables; if found, add a `"tips"` key (list of strings) to the matching concentration entry in `concentrations.py`

**If no concentrations exist:**
- Confirm this explicitly in your report
- You will assert `"[CODE]" not in CONCENTRATIONS` in the tests (step `/write-tests`)

Never leave this step unresolved.

### Step 5a — Catalog tips/notes (REQUIRED)

Look for footnotes or numbered notes below the course requirements table or Plan of Study Grid (superscript-referenced: ¹²³…).

Organize them into the `"notes"` field of the major's `FLOWCHARTS` entry:
```python
"notes": [
    {"title": "Flowchart Tips", "items": ["...", "..."]},
    {"title": "GE Tips", "items": ["..."]},
]
```
- `"Flowchart Tips"`: structural rules — term placement, elective restrictions, prereq notes, unit floors
- `"GE Tips"`: courses that satisfy both a major/support requirement and a GE area simultaneously
- Add other section titles if the catalog uses different groupings
- If there are no footnotes, omit the `"notes"` key entirely — do not add an empty list

Do not duplicate concentration-specific tips here; those go in the `"tips"` key of the concentration entry in `concentrations.py`.
