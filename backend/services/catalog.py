"""
Fetch and cache Cal Poly catalog course descriptions.
Scrapes catalog.calpoly.edu/courses/{dept}/ on-demand, caches per department.
"""

import re
import time
import json
import httpx
from bs4 import BeautifulSoup
from functools import lru_cache
from pathlib import Path

CATALOG_BASE = "https://catalog.calpoly.edu/courses"
CACHE_TTL = 24 * 60 * 60  # 24 hours
POLYPLANNER_COURSES_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "polyplanner"
    / "catalog-data"
    / "2026-2028"
    / "courses.json"
)

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

    if courses:
        return courses

    course_heading = re.compile(
        r"^([A-Z]{2,6}(?:/[A-Z]{2,6})?\s+\d{4}[A-Z]?)\s+(.+?)\s+\(([\d][\d.\-–]*)\s+units?\)$"
    )
    current_num: str | None = None
    current_desc: list[str] = []

    for raw_line in soup.get_text("\n", strip=True).splitlines():
        line = raw_line.strip()
        match = course_heading.match(line)
        if match:
            if current_num:
                courses[current_num]["description"] = " ".join(current_desc).strip()

            current_num = match.group(1).upper()
            courses[current_num] = {
                "title": match.group(2).strip(),
                "units": match.group(3).replace("–", "-"),
                "description": "",
            }
            current_desc = []
            continue

        if current_num:
            current_desc.append(line)

    if current_num:
        courses[current_num]["description"] = " ".join(current_desc).strip()

    return courses


@lru_cache(maxsize=1)
def _polyplanner_courses_by_dept() -> dict[str, dict[str, dict]]:
    """Return bundled semester catalog courses grouped by lowercase department."""
    try:
        with POLYPLANNER_COURSES_PATH.open("r", encoding="utf-8") as file:
            rows = json.load(file)
    except Exception:
        return {}

    grouped: dict[str, dict[str, dict]] = {}
    for row in rows:
        subject = str(row.get("courseSubject", "")).strip().upper()
        number = str(row.get("courseNumber", "")).strip().upper()
        if not subject or not number:
            continue

        course_number = f"{subject} {number}"
        grouped.setdefault(subject.lower(), {})[course_number] = {
            "title": str(row.get("displayName") or "").strip(),
            "units": str(row.get("units") or "").strip(),
            "description": str(row.get("desc") or "").strip(),
            "prerequisites_text": str(row.get("prerequisite") or "").strip(),
        }
    return grouped


def _bundled_dept(dept: str) -> dict[str, dict]:
    return _polyplanner_courses_by_dept().get(dept.lower(), {})


def _first_unit_value(units: str) -> int:
    match = re.search(r"\d+", str(units))
    return int(match.group(0)) if match else 0


def _compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def search_catalog_courses(query: str, limit: int = 20, offset: int = 0) -> list[dict]:
    """Search bundled semester catalog courses and return normalized summaries."""
    q = " ".join(query.split()).lower()
    q_compact = _compact(query)

    scored: list[tuple[int, str, dict]] = []
    tokens = [token for token in q.split() if token]
    for dept_courses in _polyplanner_courses_by_dept().values():
        for course_number, info in dept_courses.items():
            title = str(info.get("title") or "").strip()
            units = str(info.get("units") or "").strip()
            course_lower = course_number.lower()
            compact_number = _compact(course_number)
            compact_haystack = _compact(f"{course_number} {title}")
            haystack = f"{course_lower} {title.lower()}"

            token_match = bool(tokens) and all(token in haystack for token in tokens)
            browsing = not q and not q_compact
            if not browsing and q not in haystack and q_compact not in compact_haystack and not token_match:
                continue

            rank = 50
            if browsing:
                rank = 100
            elif q_compact and compact_number == q_compact:
                rank = 0
            elif q_compact and compact_number.startswith(q_compact):
                rank = 5
            elif q and course_lower.startswith(q):
                rank = 10
            elif q_compact and q_compact in compact_number:
                rank = 15
            elif token_match:
                rank = 20
            elif q and q in title.lower():
                rank = 25

            scored.append((
                rank,
                course_number,
                {
                    "course_number": course_number,
                    "title": title,
                    "units": _first_unit_value(units),
                },
            ))

    scored.sort(key=lambda item: (item[0], item[1]))
    start = max(0, offset)
    end = start + max(1, min(limit, 50))
    return [item[2] for item in scored[start:end]]


def _ensure_dept(dept: str) -> dict[str, dict]:
    entry = _dept_cache.get(dept)
    if entry and (time.time() - entry["fetched_at"]) < CACHE_TTL:
        return entry["courses"]
    courses = _fetch_dept(dept)
    if not courses:
        courses = _bundled_dept(dept)
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
