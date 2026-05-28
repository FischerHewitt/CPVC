Move a resolved ambiguity from `catalog_ambiguities.txt` to `completed_ambiguities.txt`.

## What to do

The user will tell you which major/code was fixed and what the resolution was.

### Step 1 — Read both files

Read `catalog_ambiguities.txt` and `completed_ambiguities.txt` in full so you know the exact text to move and where to append.

### Step 2 — Find the entry in `catalog_ambiguities.txt`

Locate the section for the given major. It will start with a separator line and header, e.g.:
```
--------------------------------------------------------------------------------
CODE — Major Name
--------------------------------------------------------------------------------
- ambiguity description
- another ambiguity
```

If only one bullet point within a section is resolved (not the whole section), extract just that bullet and leave the rest.

If the entire section is resolved, extract the whole block including the separator lines.

### Step 3 — Remove it from `catalog_ambiguities.txt`

Edit `catalog_ambiguities.txt` to delete the resolved entry or bullet. Do not leave any `[RESOLVED]` marker, comment, or placeholder — physically remove the text. The file must be clean after the edit.

### Step 4 — Append to `completed_ambiguities.txt`

Append the resolved entry at the bottom of `completed_ambiguities.txt` using this format:
```
--------------------------------------------------------------------------------
CODE — Major Name                                                      [DONE]
--------------------------------------------------------------------------------
- [original ambiguity text]
- Resolution: [what was actually fixed and how]
```

Always write a **Resolution:** line describing what changed in the code — be specific (file name, what value was corrected, why).

### Step 5 — Verify

Read back the bottom of `completed_ambiguities.txt` to confirm the entry was appended correctly, then read the affected section of `catalog_ambiguities.txt` to confirm it is clean with no leftover text or markers.

Report: what was moved, and confirm `catalog_ambiguities.txt` is clean.
