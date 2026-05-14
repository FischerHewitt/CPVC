from fastapi import APIRouter, HTTPException
from services.catalog import get_course_info

router = APIRouter()


@router.get("/{course_number:path}")
def course_info(course_number: str):
    info = get_course_info(course_number)
    if not info:
        raise HTTPException(status_code=404, detail=f"No catalog data for {course_number}")
    return {"course_number": course_number, **info}
