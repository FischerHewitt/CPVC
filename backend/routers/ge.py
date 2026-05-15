from fastapi import APIRouter, HTTPException
from data.ge_courses import GE_COURSES
from services.catalog import get_dept_courses

router = APIRouter()

_GE_AREA_MAP = {
    area_id: [c["course_number"] for c in data["courses"]]
    for area_id, data in GE_COURSES.items()
}

# course_number keys that trigger a dynamic catalog lookup instead of static GE data
_ART_ELECTIVE_KEYS = {"ART 3000+", "ART 3000+ (2)"}


def _build_art_elective_response(area_id: str) -> dict:
    dept_courses = get_dept_courses("art")
    courses = []
    for course_num in sorted(dept_courses.keys()):
        parts = course_num.split()
        if len(parts) < 2:
            continue
        try:
            level = int(parts[-1])
        except ValueError:
            continue
        if not (3000 <= level <= 4999):
            continue
        info = dept_courses[course_num]
        raw_units = str(info.get("units", "4"))
        try:
            units = int(raw_units.split("-")[0].split("–")[0])
        except (ValueError, IndexError):
            units = 4
        courses.append({
            "course_number": course_num,
            "title": info.get("title", ""),
            "units": units,
        })
    return {
        "area_id": area_id,
        "title": "3000–4000 Level Art Course",
        "description": "Any 3000–4000 level ART course. Two are required for the BFA in Art & Design.",
        "courses": courses,
    }


@router.get("/all")
def get_ge_area_map():
    """Return a lightweight map of {area_id -> [course_number, ...]} for all GE areas."""
    return _GE_AREA_MAP


@router.get("/{area_id:path}")
def get_ge_courses(area_id: str):
    area = GE_COURSES.get(area_id)
    if area:
        return {
            "area_id": area_id,
            "title": area["title"],
            "description": area["description"],
            "courses": area["courses"],
        }
    if area_id in _ART_ELECTIVE_KEYS:
        return _build_art_elective_response(area_id)
    raise HTTPException(status_code=404, detail=f"No GE data for area: {area_id}")
