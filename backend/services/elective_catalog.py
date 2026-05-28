"""ElectiveCatalog: authoritative course info and elective definitions.

Course resolution — two layers merged at load time:
  Layer 1 — course_catalog.json: auto-generated from flowchart data via
             scripts/build_course_catalog.py. Re-run after editing flowcharts.py.
  Layer 2 — course_supplements.json: hand-maintained entries for courses that
             appear in elective option lists but not in any flowchart. Supplements
             override the catalog when the same course_number appears in both.

Elective definitions — three JSON files:
  electives_static.json   — static elective option lists (course numbers only)
  electives_dynamic.json  — dynamic elective configs (dept + level range)
  placeholder_keys.json   — placeholder_id → elective_key mapping
"""
import json
from pathlib import Path
from typing import TypedDict

_DATA_DIR = Path(__file__).parent.parent / "data"

_catalog: dict[str, dict] = {}
_static_electives: dict[str, dict] = {}   # key → {title, description, courses: [resolved dicts]}
_dynamic_configs: dict[str, dict] = {}    # key → {title, description, depts, min_level, max_level, ...}
_placeholder_keys: dict[str, str] = {}    # placeholder_id → elective_key
_loaded = False


class CourseInfo(TypedDict):
    title: str
    units: int


def _load() -> None:
    global _catalog, _static_electives, _dynamic_configs, _placeholder_keys, _loaded

    # ── Course catalog (Layer 1 + Layer 2) ───────────────────────────────────
    merged: dict[str, dict] = {}
    for fname in ("course_catalog.json", "course_supplements.json"):
        p = _DATA_DIR / fname
        if p.exists():
            with open(p) as f:
                merged.update(json.load(f))
    _catalog = merged

    # ── Static elective definitions ───────────────────────────────────────────
    static_path = _DATA_DIR / "electives_static.json"
    if static_path.exists():
        with open(static_path) as f:
            raw_static: dict[str, dict] = json.load(f)
        resolved: dict[str, dict] = {}
        for key, defn in raw_static.items():
            courses = []
            for num in defn.get("courses", []):
                info = merged.get(num)
                if info:
                    courses.append({"course_number": num, **info})
                # Unresolvable numbers are silently skipped; they should not
                # exist after a complete migration + supplement seeding.
            resolved[key] = {
                "title": defn["title"],
                "description": defn["description"],
                "courses": courses,
            }
        _static_electives = resolved

    # ── Dynamic elective configs ──────────────────────────────────────────────
    dynamic_path = _DATA_DIR / "electives_dynamic.json"
    if dynamic_path.exists():
        with open(dynamic_path) as f:
            _dynamic_configs = json.load(f)

    # ── Placeholder key mapping ───────────────────────────────────────────────
    keys_path = _DATA_DIR / "placeholder_keys.json"
    if keys_path.exists():
        with open(keys_path) as f:
            _placeholder_keys = json.load(f)

    _loaded = True


def _ensure_loaded() -> None:
    if not _loaded:
        _load()


# ── Public API ────────────────────────────────────────────────────────────────

def resolve_course(course_number: str) -> dict | None:
    """Return {course_number, title, units} for a known course, or None."""
    _ensure_loaded()
    info = _catalog.get(course_number)
    if info is None:
        return None
    return {"course_number": course_number, **info}


def get_catalog() -> dict[str, CourseInfo]:
    """Return the full {course_number: {title, units}} mapping."""
    _ensure_loaded()
    return _catalog


def get_static_elective(key: str) -> dict | None:
    """Return fully resolved {key, title, description, courses} for a static elective, or None."""
    _ensure_loaded()
    defn = _static_electives.get(key)
    if defn is None:
        return None
    return {"key": key, **defn}


def get_dynamic_config(key: str) -> dict | None:
    """Return the raw dynamic config {title, description, depts, min_level, max_level, ...}, or None."""
    _ensure_loaded()
    return _dynamic_configs.get(key)


def get_placeholder_key(course_id: str) -> str | None:
    """Return the registered elective key for a placeholder course ID, or None."""
    _ensure_loaded()
    return _placeholder_keys.get(course_id)


def is_static(key: str) -> bool:
    _ensure_loaded()
    return key in _static_electives


def is_dynamic(key: str) -> bool:
    _ensure_loaded()
    return key in _dynamic_configs


def get_dynamic_configs() -> dict[str, dict]:
    """Return the full {key: config} mapping of all dynamic elective configs."""
    _ensure_loaded()
    return _dynamic_configs


def reload() -> None:
    """Force a reload from disk — useful in tests."""
    global _loaded
    _loaded = False
    _load()
