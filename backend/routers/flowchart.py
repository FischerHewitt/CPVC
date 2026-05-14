from fastapi import APIRouter, HTTPException
from data.flowcharts import FLOWCHARTS
from services.inference import infer_completed

router = APIRouter()


@router.get("/majors")
def list_majors():
    return {"majors": [{"code": k, "name": v["major"]} for k, v in FLOWCHARTS.items()]}


@router.get("/{major}")
def get_flowchart(major: str):
    key = major.upper()
    if key not in FLOWCHARTS:
        raise HTTPException(status_code=404, detail=f"No flowchart for major: {major}")
    return FLOWCHARTS[key]


@router.post("/{major}/infer")
def infer(major: str, body: dict):
    """
    Given a list of explicitly completed course numbers, return the
    additional courses that can be inferred as completed via prerequisites.
    """
    key = major.upper()
    if key not in FLOWCHARTS:
        raise HTTPException(status_code=404, detail=f"No flowchart for major: {major}")

    completed: set[str] = set(body.get("completed", []))
    # Use all majors' courses so cross-major prereq chains work
    # (e.g. CS student with MATH 143 / Calc III infers Calc I & II via AERO flowchart)
    all_courses = [c for v in FLOWCHARTS.values() for c in v["courses"]]
    inferred = infer_completed(completed, all_courses)

    return {"inferred": sorted(inferred)}
