from fastapi import APIRouter, HTTPException, Query
from services.catalog import get_course_info, search_catalog_courses

router = APIRouter()


@router.get("/search")
def course_search(
    q: str = Query("", max_length=80),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    return {"courses": search_catalog_courses(q, limit, offset)}


@router.get("/{course_number:path}")
def course_info(course_number: str):
    info = get_course_info(course_number)
    if not info:
        raise HTTPException(status_code=404, detail=f"No catalog data for {course_number}")
    return {"course_number": course_number, **info}
