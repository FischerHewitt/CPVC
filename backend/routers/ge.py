from fastapi import APIRouter, HTTPException
from data.ge_courses import GE_COURSES

router = APIRouter()

_GE_AREA_MAP = {
    area_id: [c["course_number"] for c in data["courses"]]
    for area_id, data in GE_COURSES.items()
}


@router.get("/all")
def get_ge_area_map():
    """Return a lightweight map of {area_id -> [course_number, ...]} for all GE areas."""
    return _GE_AREA_MAP


@router.get("/{area_id:path}")
def get_ge_courses(area_id: str):
    area = GE_COURSES.get(area_id)
    if not area:
        raise HTTPException(status_code=404, detail=f"No GE data for area: {area_id}")
    return {
        "area_id": area_id,
        "title": area["title"],
        "description": area["description"],
        "courses": area["courses"],
    }
