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


def _extract_prereq(block) -> str:
    """Extract prerequisite text from a course block, checking extra and desc elements."""
    for el in block.select(".courseblockextra, .courseblockdesc p, .courseblockdesc"):
        text = el.get_text(" ", strip=True)
        m = re.search(r"[Pp]rerequisites?\s*:\s*(.+?)(?:\.\s|$)", text)
        if m:
            return m.group(1).strip()
    return ""


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
        title_el = block.select_one(".courseblocktitle strong")
        desc_el = block.select_one(".courseblockdesc")
        if not title_el:
            continue

        # e.g. "COMS 1101. Public Speaking. 3 units."
        raw_title = title_el.get_text(" ", strip=True)
        match = re.match(r"^([A-Z]+\s+\d+)\.\s+(.+?)\.\s+([\d.]+)\s+units?\.$", raw_title, re.IGNORECASE)
        if not match:
            continue

        num   = match.group(1).upper()
        title = match.group(2).strip()
        units = match.group(3)
        desc  = desc_el.get_text(" ", strip=True) if desc_el else ""

        courses[num] = {
            "title": title,
            "units": units,
            "description": desc,
            "prerequisites_text": _extract_prereq(block),
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
