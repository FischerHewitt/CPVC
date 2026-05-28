Wire elective picker options for every selectable placeholder in a major. Covers step 6 of the add-major checklist.

## What to do

For every non-GE placeholder tile that should show course options in the Manual Course Checklist:

### 1. Set `elective_key` on the tile

In `backend/data/flowcharts.py`, add `"elective_key": "KEY_NAME"` to the placeholder's dict. Convention: `[CODE]_[descriptor]` (e.g. `"CS_tech_elective"`).

Skip `elective_key` only for free/unrestricted elective placeholders with no catalog-restricted course list.

### 2. Add a static or dynamic entry in the JSON data files

- **`backend/data/electives_static.json`**: exact catalog list — use for slash-choices, support electives, and concentration electives with a defined course list. Format:
  ```json
  "elective_key": [{"course_number": "...", "title": "...", "units": N}, ...]
  ```
- **`backend/data/electives_dynamic.json`**: broad catalog bucket — use when the catalog says something like "any 3000–4000 level ME course." Format:
  ```json
  "elective_key": {"department": "ME", "min_level": 3000, "max_level": 4000, "units": N}
  ```

Do NOT edit `backend/routers/electives.py` — that file is route handlers only.

### 3. Check `placeholder_keys.json`

If the placeholder's `course_number` or `quarter_equivalents` would cause the auto-picker to expose old quarter numbers or return incomplete options, add an entry to `backend/data/placeholder_keys.json`:
```json
"placeholder_id": "elective_key"
```

### 4. Concentration slot overrides

For concentration `slot_overrides` that replace a base elective with a fixed course (not a choice list), set `"elective_key": None` so the override does not inherit the base key and expose irrelevant options.

### Checklist before moving on

- Every catalog-backed placeholder has an `elective_key`
- Every `elective_key` has a matching `_STATIC` or `_DYNAMIC` entry
- All `_STATIC` entries use exact catalog course numbers, titles, and units
- Fixed concentration overrides have `"elective_key": None`
