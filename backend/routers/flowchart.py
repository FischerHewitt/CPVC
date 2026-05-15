from fastapi import APIRouter, HTTPException
from data.flowcharts import FLOWCHARTS
from data.concentrations import CONCENTRATIONS
from services.inference import infer_completed
from services.layout import align_prereq_chains

router = APIRouter()

# Apply chain-alignment layout once at import time so every flowchart response
# has prerequisite sequences (Calc I→II→III, Physics I→II) in the same row.
_ALIGNED_FLOWCHARTS = {
    key: {**fc, "courses": align_prereq_chains(fc["courses"])}
    for key, fc in FLOWCHARTS.items()
}

# Pre-built once at import time; used by /infer for cross-major prereq chains
_ALL_COURSES = [c for v in _ALIGNED_FLOWCHARTS.values() for c in v["courses"]]


@router.get("/majors")
def list_majors():
    return {"majors": [{"code": k, "name": v["major"]} for k, v in _ALIGNED_FLOWCHARTS.items()]}


@router.get("/{major}/concentrations")
def get_concentrations(major: str):
    return {"concentrations": CONCENTRATIONS.get(major.upper(), [])}


@router.get("/{major}")
def get_flowchart(major: str):
    key = major.upper()
    if key not in _ALIGNED_FLOWCHARTS:
        raise HTTPException(status_code=404, detail=f"No flowchart for major: {major}")
    return _ALIGNED_FLOWCHARTS[key]


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
    inferred = infer_completed(completed, _ALL_COURSES)

    return {"inferred": sorted(inferred)}
