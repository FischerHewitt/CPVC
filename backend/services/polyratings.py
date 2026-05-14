"""
PolyRatings integration.

Fetches the full professor list from professors.all once per CACHE_TTL_SECONDS,
builds a course-number index, and returns filtered results on demand.

PolyRatings still stores quarter-system course numbers (CSC 101, etc.) for
all historical ratings.  We search by both the semester course number AND every
quarter equivalent so students see results regardless of which system was used.
"""

import time
import json
import httpx
from dataclasses import dataclass
from data.flowcharts import FLOWCHARTS

API_BASE   = "https://api-prod.polyratings.org"
PR_BASE    = "https://polyratings.dev"
CACHE_TTL  = 6 * 60 * 60  # 6 hours

# ── in-memory cache ──────────────────────────────────────────────────────────
_cache_professors: list[dict] | None = None
_cache_ts: float = 0.0
# index: normalised course number -> list of professor dicts
_course_index: dict[str, list[dict]] = {}


@dataclass
class Professor:
    name: str
    overall_score: float
    num_ratings: int
    polyratings_url: str


# ── helpers ──────────────────────────────────────────────────────────────────

def _norm(course_number: str) -> str:
    """Normalise for comparison: upper-case, single space, strip."""
    parts = course_number.upper().split()
    return " ".join(parts)


def _build_index(professors: list[dict]) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for prof in professors:
        for course in prof.get("courses", []):
            key = _norm(course)
            index.setdefault(key, []).append(prof)
    return index


def _fetch_all() -> list[dict]:
    resp = httpx.get(f"{API_BASE}/professors.all", timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    # tRPC shape: {"result": {"data": [...]}}
    return payload["result"]["data"]


def _ensure_cache() -> None:
    global _cache_professors, _cache_ts, _course_index
    if _cache_professors is not None and (time.time() - _cache_ts) < CACHE_TTL:
        return
    _cache_professors = _fetch_all()
    _course_index     = _build_index(_cache_professors)
    _cache_ts         = time.time()


# ── build reverse lookup: semester course_number -> quarter equivalents ───────

def _build_quarter_lookup() -> dict[str, set[str]]:
    """Map every semester course number to its known quarter equivalents (+ itself)."""
    lookup: dict[str, set[str]] = {}
    for fc in FLOWCHARTS.values():
        for course in fc["courses"]:
            nums: set[str] = {_norm(course["course_number"])}
            for q in course["quarter_equivalents"]:
                nums.add(_norm(q))
            for n in nums:
                lookup.setdefault(n, set()).update(nums)
    return lookup


_QUARTER_LOOKUP: dict[str, set[str]] = _build_quarter_lookup()


def warm_cache() -> None:
    """Pre-warm the PolyRatings cache. Intended to be called from the app lifespan."""
    _ensure_cache()


def _derive_quarter_candidates(normed: str) -> set[str]:
    """
    Heuristic: Cal Poly semester numbers often prepend a leading digit to the
    old 3-digit quarter number.  e.g. COMS 1101 -> COMS 101, ENGL 1134 -> ENGL 134.
    Generate candidate quarter numbers by stripping the first digit of a 4-digit code.
    """
    candidates: set[str] = set()
    parts = normed.split()
    if len(parts) == 2:
        dept, code = parts
        if len(code) == 4 and code.isdigit():
            stripped = str(int(code[1:]))  # "0101" -> "101", preserves "101"
            candidates.add(f"{dept} {stripped}")
    return candidates


# ── public API ────────────────────────────────────────────────────────────────

def get_professors_for_course(course_number: str) -> list[Professor]:
    """
    Return professors who have taught this course, sorted by numEvals desc.
    Searches the semester number, all FLOWCHARTS-based quarter equivalents, and
    a heuristic-derived quarter candidate (strip leading digit of 4-digit codes).
    """
    try:
        _ensure_cache()
    except Exception:
        return []

    normed = _norm(course_number)
    search_keys: set[str] = {normed}
    search_keys.update(_QUARTER_LOOKUP.get(normed, set()))
    search_keys.update(_derive_quarter_candidates(normed))

    seen_ids: set[str] = set()
    matched: list[dict] = []
    for key in search_keys:
        for prof in _course_index.get(key, []):
            if prof["id"] not in seen_ids:
                seen_ids.add(prof["id"])
                matched.append(prof)

    # Sort: most-reviewed first, then by rating
    matched.sort(key=lambda p: (p.get("numEvals", 0), p.get("overallRating", 0)), reverse=True)

    return [
        Professor(
            name=f"{p['firstName']} {p['lastName']}",
            # PolyRatings uses 0-4 scale; convert to 0-10 for readability, or keep as-is
            overall_score=round(p.get("overallRating", 0.0), 2),
            num_ratings=p.get("numEvals", 0),
            polyratings_url=f"{PR_BASE}/professor/{p['id']}",
        )
        for p in matched
        if p.get("numEvals", 0) > 0
    ]
