Update the frontend fallback lists for a newly added major and verify the build. Covers step 10 of the add-major checklist.

## What to do

Open `frontend/app/upload/page.tsx` and update two fallback lists:

### 1. `FALLBACK_MAJORS`

Add the new major:
```ts
{ code: "CODE", name: "Full Major Name" },
```

**Do NOT add concentration-specific flowchart keys here** (e.g. `"CS_AIML"`). Only add the base major code. Keys registered as `full_flowchart_key` in `concentrations.py` are filtered out from the `/majors` API automatically — adding them to `FALLBACK_MAJORS` would make them appear twice.

### 2. `FALLBACK_CONCENTRATIONS` (only if concentrations exist)

Use the `concs(...)` helper:
```ts
CODE: concs(
  ["none", "No Concentration Selected"],
  ["conc_id", "Concentration Label"],
),
```

Every concentration id and label must match exactly what was added to `concentrations.py` in `/add-concentrations`.

If the major has no concentrations, do not add a `FALLBACK_CONCENTRATIONS` entry.

### 3. Verify the build

```bash
cd frontend && npm run build
```

The build must complete with no errors. If it fails, fix the TypeScript or import error before reporting success.

Also verify the Manual Course Checklist row order is: Major → Support → GE → Concentration/free-elective items.
