Log all ambiguities encountered while adding a major to `catalog_ambiguities.txt`. Covers step 11 of the add-major checklist.

## What to do

Append a section to `catalog_ambiguities.txt` in the repo root. Always append — never overwrite existing entries.

### Format when ambiguities exist

```
--------------------------------------------------------------------------------
[CODE] — [MAJOR NAME]
--------------------------------------------------------------------------------
- [Description of ambiguity]
- [Description of ambiguity]
```

### Format when no ambiguities exist

```
[CODE] — [MAJOR NAME]: no ambiguities.
```

### What counts as an ambiguity

- Slash-choice tile where the catalog lists two courses as interchangeable
- Unit range variance (e.g. "12–16 units of electives" represented as a fixed count)
- Broad dynamic elective bucket (e.g. "any 3000–4000 level ME course")
- Missing catalog info (course not found, title unclear, units not listed)
- Assumed term placement (course had no term specified in the Plan of Study Grid)
- Paired lecture/lab where combined units were estimated
- Any other judgment call made while building the flowchart

After appending, read back the bottom of `catalog_ambiguities.txt` to confirm the entry was added correctly and is properly formatted.

Finally, report a summary of all ambiguities to the user so they can decide whether any need follow-up.
