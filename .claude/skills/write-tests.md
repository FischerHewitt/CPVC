Write backend tests for a newly added major. Covers steps 7 and 8 of the add-major checklist.

## What to do

### Step 7 — `backend/tests/test_flowchart_data.py`

Add a major-specific test class or test function. Assert all of the following:

- **`total_units`**: matches the catalog's stated total (or falls within the accepted range)
- **Tile unit sum**: sum of all tile units equals the expected total
- **Key course titles**: spot-check at least 3–4 important courses by `id` or `course_number` — verify `title` and `units`
- **Categories**: at least one `"major"`, `"support"`, and `"ge"` tile exists; verify specific tiles have the correct category
- **Prerequisites**: at least 2 `prerequisites` lists are non-empty; verify specific prereq relationships
- **GE placeholders**: at least one `is_placeholder: True` tile with `category == "ge"` exists
- **Elective placeholders**: every catalog-backed placeholder has `is_placeholder: True` and the expected `elective_key`
- **Concentrations**: assert either `"[CODE]" in CONCENTRATIONS` or `"[CODE]" not in CONCENTRATIONS` — must match the actual result of `/add-concentrations`
- **Fixed concentration overrides**: if any concentration slot_override replaces a base elective with a fixed course, assert that override's `elective_key` is `None`

### Step 8 — `backend/tests/test_electives_api.py`

For every new `_STATIC`, `_DYNAMIC`, or `_PLACEHOLDER_ELECTIVE_KEY` path added in `/wire-electives`:
- Add a test that calls the electives endpoint for that key and asserts it returns a non-empty list of options
- For `_STATIC` entries, also assert at least one known course number appears in the response
- For `_DYNAMIC` entries, assert the response contains only courses matching the expected department and level range

Do not modify existing tests — only add new ones.
