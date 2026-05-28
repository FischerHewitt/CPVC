from fastapi import APIRouter, Depends
from services.polyratings import PolyRatingsCache, get_polyratings_cache

router = APIRouter()


@router.get("/{course_number:path}")
def get_professors(
    course_number: str,
    cache: PolyRatingsCache = Depends(get_polyratings_cache),
):
    professors = cache.get_professors_for_course(course_number)
    return {
        "course_number": course_number,
        "professors": [
            {
                "name":            p.name,
                "overall_score":   p.overall_score,
                "num_ratings":     p.num_ratings,
                "polyratings_url": p.polyratings_url,
            }
            for p in professors
        ],
    }
