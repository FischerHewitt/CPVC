"""
PolyRatings integration.

Fetches the full professor list from professors.all once per CACHE_TTL_SECONDS,
builds a course-number index, and returns filtered results on demand.

PolyRatings still stores quarter-system course numbers (CSC 101, etc.) for
all historical ratings.  We search by both the semester course number AND every
quarter equivalent so students see results regardless of which system was used.
"""

import re
import time
import httpx
from dataclasses import dataclass
from data.flowcharts import FLOWCHARTS

API_BASE   = "https://api-prod.polyratings.org"
PR_BASE    = "https://polyratings.dev"
CACHE_TTL  = 6 * 60 * 60  # 6 hours


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


_COURSE_RE = re.compile(r"(?P<dept>[A-Z]{2,5})\s*(?P<num>\d{3,4}[A-Z]?)")


def _extract_course_numbers(text: str) -> set[str]:
    return {f"{match.group('dept')} {match.group('num')}" for match in _COURSE_RE.finditer(text.upper())}


_STATIC_QUARTER_EQUIVALENTS: dict[str, set[str]] = {
    "CSC 3001": {"CSC 364", "CSC 464"},
    "CSC 3203": {"CSC 323"},
    "CSC 3445": {"CSC 445"},
    "CSC 3660": {"CSC 365"},
    "CSC 4160": {"CSC 402"},
    "CSC 4161": {"CSC 405", "CSC 406", "CSC 491", "CSC 492"},
    "CSC 4460": {"CSC 491", "CSC 492"},
    "CSC 4461": {"CSC 491", "CSC 492"},
    "CSC 4553": {"CSC 453", "CPE 453"},
    "CSC 4669": {"CSC 469"},
    "CPE 1000": {"CPE 100"},
    "CPE 2301": {"CPE 133"},
    "CPE 4220": {"CPE 422"},
    "CPE 4280": {"CPE 426"},
    "CPE 4669": {"CPE 469"},
    "DATA 4460": {"CSC 491", "CSC 492"},
    "ENGR 4464": {"CSC 491", "CSC 492"},
    "MATH 2031": {"MATH 248"},
}


def _build_index(professors: list[dict]) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for prof in professors:
        for course in prof.get("courses", []):
            keys = {_norm(course), *{_norm(num) for num in _extract_course_numbers(course)}}
            for key in keys:
                index.setdefault(key, []).append(prof)
    return index


def _fetch_all() -> list[dict]:
    resp = httpx.get(f"{API_BASE}/professors.all", timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    # tRPC shape: {"result": {"data": [...]}}
    return payload["result"]["data"]


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

    for semester, quarters in _STATIC_QUARTER_EQUIVALENTS.items():
        nums = {_norm(semester), *{_norm(q) for q in quarters}}
        for n in nums:
            lookup.setdefault(n, set()).update(nums)
    return lookup


_QUARTER_LOOKUP: dict[str, set[str]] = _build_quarter_lookup()


def _derive_quarter_candidates(normed: str) -> set[str]:
    """
    Generate conservative quarter-number candidates for semester courses.
    Lower-division examples often prepend a leading digit to the old number
    (COMS 1101 -> COMS 101). Upper-division semester courses that end in 0
    often append that 0 to the old 3-digit course (CSC 4710 -> CSC 471).
    """
    candidates: set[str] = set()
    parts = normed.split()
    if len(parts) == 2:
        dept, code = parts
        if len(code) == 4 and code.isdigit():
            stripped = str(int(code[1:]))  # "0101" -> "101", preserves "101"
            candidates.add(f"{dept} {stripped}")
            if int(code) >= 3000 and code.endswith("0"):
                candidates.add(f"{dept} {code[:3]}")
    return candidates


# ── cache class ───────────────────────────────────────────────────────────────

class PolyRatingsCache:
    """Thread-safe-enough in-memory TTL cache for the PolyRatings professor list."""

    def __init__(self) -> None:
        self._professors: list[dict] | None = None
        self._ts: float = 0.0
        self._index: dict[str, list[dict]] = {}

    def reset(self) -> None:
        """Clear cached state. Used by tests."""
        self._professors = None
        self._ts = 0.0
        self._index = {}

    def _ensure(self) -> None:
        if self._professors is not None and (time.time() - self._ts) < CACHE_TTL:
            return
        self._professors = _fetch_all()
        self._index = _build_index(self._professors)
        self._ts = time.time()

    def warm(self) -> None:
        """Pre-warm the cache. Safe to call from a background thread."""
        self._ensure()

    def get_professors_for_course(self, course_number: str) -> list[Professor]:
        """
        Return professors who have taught this course, sorted by numEvals desc.
        Searches the semester number, all FLOWCHARTS-based quarter equivalents, and
        a heuristic-derived quarter candidate (strip leading digit of 4-digit codes).
        """
        try:
            self._ensure()
        except Exception:
            return []

        normed = _norm(course_number)
        requested_numbers = {_norm(num) for num in _extract_course_numbers(course_number)} or {normed}
        search_keys: set[str] = set()
        for requested in requested_numbers:
            search_keys.add(requested)
            search_keys.update(_QUARTER_LOOKUP.get(requested, set()))
            search_keys.update(_derive_quarter_candidates(requested))

        seen_ids: set[str] = set()
        matched: list[dict] = []
        for key in search_keys:
            for prof in self._index.get(key, []):
                if prof["id"] not in seen_ids:
                    seen_ids.add(prof["id"])
                    matched.append(prof)

        matched.sort(key=lambda p: (p.get("numEvals", 0), p.get("overallRating", 0)), reverse=True)

        return [
            Professor(
                name=f"{p['firstName']} {p['lastName']}",
                overall_score=round(p.get("overallRating", 0.0), 2),
                num_ratings=p.get("numEvals", 0),
                polyratings_url=f"{PR_BASE}/professor/{p['id']}",
            )
            for p in matched
            if p.get("numEvals", 0) > 0
        ]


# ── module singleton + dependency ─────────────────────────────────────────────

_cache = PolyRatingsCache()


def get_polyratings_cache() -> PolyRatingsCache:
    """FastAPI dependency — returns the shared PolyRatingsCache singleton."""
    return _cache


# ── backwards-compatible free functions ───────────────────────────────────────

def warm_cache() -> None:
    """Pre-warm the PolyRatings cache. Intended to be called from the app lifespan."""
    _cache.warm()


def get_professors_for_course(course_number: str) -> list[Professor]:
    """Module-level shim kept for direct callers outside of FastAPI routes."""
    return _cache.get_professors_for_course(course_number)
