"""
Fetch and cache Cal Poly catalog course descriptions.
Scrapes catalog.calpoly.edu/courses/{dept}/ on-demand, caches per department.
"""

import re
import time
import httpx
from bs4 import BeautifulSoup

CATALOG_BASE = "https://catalog.calpoly.edu/courses"
CACHE_TTL = 24 * 60 * 60  # 24 hours

# dept_lower -> {"fetched_at": float, "courses": {course_number: {title, description, units}}}
_dept_cache: dict[str, dict] = {}


def _dept_key(course_number: str) -> str:
    """Return lowercase department prefix, e.g. 'COMS 1101' -> 'coms'."""
    return course_number.strip().split()[0].lower()


def _fetch_dept(dept: str) -> dict[str, dict]:
    """Scrape all courses from catalog page for this department."""
    url = f"{CATALOG_BASE}/{dept}/"
    try:
        resp = httpx.get(url, timeout=10, follow_redirects=True)
        resp.raise_for_status()
    except Exception:
        return {}

    soup = BeautifulSoup(resp.text, "html.parser")
    courses: dict[str, dict] = {}

    for block in soup.select(".courseblock"):
        code_el  = block.select_one(".courseblockcode")
        title_el = block.select_one(".courseblock__title")
        hours_el = block.select_one(".courseblock__hours")
        desc_el  = block.select_one(".courseblock__description")

        if not code_el or not title_el:
            continue

        num   = code_el.get_text(" ", strip=True).upper()
        title = title_el.get_text(" ", strip=True)

        # "(4 units)" or "(1-4 units)" or "(1 unit)"
        hours_text = hours_el.get_text(" ", strip=True) if hours_el else ""
        units_match = re.search(r"([\d][\d.\-–]*)\s+units?", hours_text, re.IGNORECASE)
        units = units_match.group(1) if units_match else ""

        desc = desc_el.get_text(" ", strip=True) if desc_el else ""

        courses[num] = {
            "title": title,
            "units": units,
            "description": desc,
        }

    return courses


def _ensure_dept(dept: str) -> dict[str, dict]:
    entry = _dept_cache.get(dept)
    if entry and (time.time() - entry["fetched_at"]) < CACHE_TTL:
        return entry["courses"]
    courses = _fetch_dept(dept)
    _dept_cache[dept] = {"fetched_at": time.time(), "courses": courses}
    return courses


def get_course_info(course_number: str) -> dict | None:
    """Return {title, units, description} for a course number, or None if not found."""
    dept = _dept_key(course_number)
    courses = _ensure_dept(dept)
    normalized = " ".join(course_number.upper().split())
    return courses.get(normalized)


def get_dept_courses(dept: str) -> dict[str, dict]:
    """Return all courses for a department, fetched and cached from catalog."""
    return _ensure_dept(dept.lower())
