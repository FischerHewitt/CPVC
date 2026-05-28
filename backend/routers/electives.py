import re

from fastapi import APIRouter, HTTPException, Query
from services.catalog import get_course_info, get_dept_courses
import services.elective_catalog as elective_catalog

router = APIRouter()

_build_courses_cache: dict = {}

_COURSE_RE = re.compile(r"(?:(?P<dept>[A-Z]{2,5})\s*)?(?P<num>\d{3,4}[A-Z]?)")


def _build_courses(depts: list[str], min_level: int, max_level: int) -> list[dict]:
    cache_key = (tuple(depts), min_level, max_level)
    if cache_key in _build_courses_cache:
        return _build_courses_cache[cache_key]
    courses = []
    for dept in depts:
        dept_courses = get_dept_courses(dept)
        for course_num in sorted(dept_courses.keys()):
            parts = course_num.split()
            if len(parts) < 2:
                continue
            try:
                level = int(parts[-1])
            except ValueError:
                continue
            if not (min_level <= level <= max_level):
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
    _build_courses_cache[cache_key] = courses
    return courses


def _course_units(info: dict | None, default: int = 3) -> int:
    if not info:
        return default
    raw_units = str(info.get("units", str(default)))
    try:
        return int(raw_units.split("-")[0].split("–")[0])
    except (ValueError, IndexError):
        return default


def _direct_course_numbers(course_number: str, quarter_equivalents: str) -> list[str]:
    text = f"{course_number} {quarter_equivalents}".replace(",", " ")
    courses: list[str] = []
    seen: set[str] = set()
    current_dept: str | None = None
    for match in _COURSE_RE.finditer(text.upper()):
        dept = match.group("dept") or current_dept
        num = match.group("num")
        if not dept:
            continue
        current_dept = dept
        value = f"{dept} {num}"
        if value not in seen:
            seen.add(value)
            courses.append(value)
    return courses


def _build_direct_courses(course_numbers: list[str], fallback_title: str) -> list[dict]:
    courses = []
    for course_number in course_numbers:
        info = get_course_info(course_number)
        courses.append({
            "course_number": course_number,
            "title": info.get("title", fallback_title) if info else fallback_title,
            "units": _course_units(info),
        })
    return courses


@router.get("/auto/placeholder")
def get_placeholder_elective_courses(
    course_id: str = Query(...),
    course_number: str = Query(...),
    title: str = Query(...),
    quarter_equivalents: str = Query(""),
):
    key = elective_catalog.get_placeholder_key(course_id)
    if key:
        if elective_catalog.is_static(key):
            defn = elective_catalog.get_static_elective(key)
            return {"key": f"auto:{course_id}", "title": defn["title"], "description": defn["description"], "courses": defn["courses"]}
        if elective_catalog.is_dynamic(key):
            cfg = elective_catalog.get_dynamic_config(key)
            courses = _build_courses(cfg["depts"], cfg["min_level"], cfg["max_level"])
            if extra_nums := cfg.get("extra_courses"):
                extra = [elective_catalog.resolve_course(n) for n in extra_nums]
                extra = [c for c in extra if c is not None]
                extra_set = {c["course_number"] for c in extra}
                courses = extra + [c for c in courses if c["course_number"] not in extra_set]
            return {"key": f"auto:{course_id}", "title": cfg["title"], "description": cfg["description"], "courses": courses}

    direct_courses = _direct_course_numbers(course_number, quarter_equivalents)
    if direct_courses:
        return {
            "key": f"auto:{course_id}",
            "title": title,
            "description": "Select one of the courses associated with this requirement.",
            "courses": _build_direct_courses(direct_courses, title),
        }

    return {
        "key": f"auto:{course_id}",
        "title": title,
        "description": "No elective options configured for this placeholder.",
        "courses": [],
    }


@router.get("/{key}")
def get_elective_courses(key: str):
    if elective_catalog.is_static(key):
        defn = elective_catalog.get_static_elective(key)
        return {"key": key, "title": defn["title"], "description": defn["description"], "courses": defn["courses"]}
    if elective_catalog.is_dynamic(key):
        cfg = elective_catalog.get_dynamic_config(key)
        courses = _build_courses(cfg["depts"], cfg["min_level"], cfg["max_level"])
        if extra_nums := cfg.get("extra_courses"):
            extra = [elective_catalog.resolve_course(n) for n in extra_nums]
            extra = [c for c in extra if c is not None]
            extra_set = {c["course_number"] for c in extra}
            courses = extra + [c for c in courses if c["course_number"] not in extra_set]
        return {"key": key, "title": cfg["title"], "description": cfg["description"], "courses": courses}
    raise HTTPException(status_code=404, detail=f"No elective data for key: {key}")
