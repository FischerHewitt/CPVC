from fastapi import APIRouter, HTTPException
from data.flowcharts import FLOWCHARTS
from data.concentrations import CONCENTRATIONS
from services.inference import build_lookup, infer_from_lookup
from services.layout import sort_course_rows_by_category, align_prereq_chains

router = APIRouter()

# Apply the initial visual layout once at import time so every flowchart response
# starts with major/support/concentration/GE courses grouped into clean rows.
_PINNED_LAYOUT_ROWS = {
    "CE": {
        "CE_MATH1261": 2,
        "CE_MATH1262": 2,
        "CE_MATH2263": 2,
    },
}

_ALIGNED_FLOWCHARTS = {
    key: {
        **fc,
        "courses": align_prereq_chains(
            sort_course_rows_by_category(
                fc["courses"],
                column_count=len(fc["columns"]),
                pinned_rows=_PINNED_LAYOUT_ROWS.get(key),
            )
        ),
    }
    for key, fc in FLOWCHARTS.items()
}

# Pre-built once at import time; used by /infer for cross-major prereq chains
_ALL_COURSES = [c for v in _ALIGNED_FLOWCHARTS.values() for c in v["courses"]]
_ALL_COURSES_LOOKUP = build_lookup(_ALL_COURSES)


_CONCENTRATION_FLOWCHART_BASE_MAJOR = {
    conc["full_flowchart_key"]: major_code
    for major_code, concs in CONCENTRATIONS.items()
    for conc in concs
    if "full_flowchart_key" in conc
}

# Only exclude flowchart keys that are concentration-specific (key != major code).
# Base major keys referenced by "none" concentrations (e.g. "CS" → "CS") are real
# majors and must not be filtered out of the /majors list.
_CONCENTRATION_FLOWCHART_KEYS = {
    fk for fk, major_code in _CONCENTRATION_FLOWCHART_BASE_MAJOR.items()
    if fk != major_code
}


def _with_inherited_base_notes(key: str, flowchart: dict) -> dict:
    if flowchart.get("notes"):
        return flowchart

    base_key = _CONCENTRATION_FLOWCHART_BASE_MAJOR.get(key)
    if not base_key:
        return flowchart

    base_notes = _ALIGNED_FLOWCHARTS.get(base_key, {}).get("notes")
    if not base_notes:
        return flowchart

    return {**flowchart, "notes": base_notes}


@router.get("/majors")
def list_majors():
    return {
        "majors": [
            {"code": k, "name": v["major"]}
            for k, v in _ALIGNED_FLOWCHARTS.items()
            if k not in _CONCENTRATION_FLOWCHART_KEYS
        ]
    }


@router.get("/{major}/concentrations")
def get_concentrations(major: str):
    return {"concentrations": CONCENTRATIONS.get(major.upper(), [])}


@router.get("/{major}")
def get_flowchart(major: str):
    key = major.upper()
    if key not in _ALIGNED_FLOWCHARTS:
        raise HTTPException(status_code=404, detail=f"No flowchart for major: {major}")
    return _with_inherited_base_notes(key, _ALIGNED_FLOWCHARTS[key])


@router.post("/{major}/infer")
def infer(major: str, body: dict):
    """
    Given a list of explicitly completed course numbers, return the
    additional courses that can be inferred as completed via prerequisites.
    """
    key = major.upper()
    if key not in _ALIGNED_FLOWCHARTS:
        raise HTTPException(status_code=404, detail=f"No flowchart for major: {major}")

    completed: set[str] = set(body.get("completed", []))
    inferred = infer_from_lookup(completed, _ALL_COURSES_LOOKUP)

    return {"inferred": sorted(inferred)}
