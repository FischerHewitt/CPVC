#!/usr/bin/env python3
"""
Migrate elective definitions from routers/electives.py Python dicts to JSON files.

Produces:
  backend/data/electives_static.json    — static elective definitions
                                          (courses stored as number strings)
  backend/data/electives_dynamic.json   — dynamic elective configs
                                          (dept + level range; extra_courses as numbers)
  backend/data/placeholder_keys.json    — placeholder_id → elective_key mapping

Also updates course_supplements.json with any orphan courses discovered in the
elective lists (courses whose title/units are in the Python dicts but not yet in
course_catalog.json or course_supplements.json).

Safe to re-run — existing supplement entries are preserved; only new orphans added.

Run from backend/:
    python3 scripts/migrate_electives_to_json.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from routers.electives import (
    _DYNAMIC,
    _PLACEHOLDER_ELECTIVE_KEY,
    _STATIC,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_known() -> dict[str, dict]:
    with open(DATA_DIR / "course_catalog.json") as f:
        known = json.load(f)
    with open(DATA_DIR / "course_supplements.json") as f:
        known.update(json.load(f))
    return known


def _load_supplements() -> dict[str, dict]:
    with open(DATA_DIR / "course_supplements.json") as f:
        return json.load(f)


def migrate_static(
    known: dict[str, dict],
    supplements: dict[str, dict],
) -> tuple[dict[str, dict], int]:
    """Convert _STATIC course dicts → course-number strings.

    Any course number not yet in known is added to supplements using the title
    and units from the existing Python dict.
    Returns (electives_static_dict, count_new_orphans).
    """
    result: dict[str, dict] = {}
    new_orphans = 0

    for key, defn in _STATIC.items():
        course_numbers: list[str] = []
        for course in defn.get("courses", []):
            num = course["course_number"]
            if " and " in num:
                # Compound entries (e.g. "CSC 4160 and CSC 4161") are not
                # standalone catalog lookups — skip them.
                continue
            if num not in known and num not in supplements:
                supplements[num] = {
                    "title": course["title"],
                    "units": course["units"],
                }
                known[num] = supplements[num]
                new_orphans += 1
            course_numbers.append(num)

        result[key] = {
            "title": defn["title"],
            "description": defn["description"],
            "courses": course_numbers,
        }

    return result, new_orphans


def migrate_dynamic(
    known: dict[str, dict],
    supplements: dict[str, dict],
) -> dict[str, dict]:
    """Dump _DYNAMIC as JSON, converting extra_courses dicts → number strings."""
    result: dict[str, dict] = {}

    for key, defn in _DYNAMIC.items():
        entry: dict = {
            "title": defn["title"],
            "description": defn["description"],
            "depts": defn["depts"],
            "min_level": defn["min_level"],
            "max_level": defn["max_level"],
        }
        if "extra_courses" in defn:
            extra_numbers: list[str] = []
            for course in defn["extra_courses"]:
                num = course["course_number"]
                if num not in known and num not in supplements:
                    supplements[num] = {
                        "title": course["title"],
                        "units": course["units"],
                    }
                    known[num] = supplements[num]
                extra_numbers.append(num)
            entry["extra_courses"] = extra_numbers
        result[key] = entry

    return result


def main() -> None:
    known = _load_known()
    supplements = _load_supplements()

    static_data, new_orphans = migrate_static(known, supplements)
    dynamic_data = migrate_dynamic(known, supplements)

    # Write electives_static.json
    static_path = DATA_DIR / "electives_static.json"
    with open(static_path, "w") as f:
        json.dump(static_data, f, indent=2, sort_keys=True)
    print(f"Wrote {len(static_data)} static elective definitions → {static_path}")

    # Write electives_dynamic.json
    dynamic_path = DATA_DIR / "electives_dynamic.json"
    with open(dynamic_path, "w") as f:
        json.dump(dynamic_data, f, indent=2, sort_keys=True)
    print(f"Wrote {len(dynamic_data)} dynamic elective configs → {dynamic_path}")

    # Write placeholder_keys.json
    keys_path = DATA_DIR / "placeholder_keys.json"
    with open(keys_path, "w") as f:
        json.dump(_PLACEHOLDER_ELECTIVE_KEY, f, indent=2, sort_keys=True)
    print(f"Wrote {len(_PLACEHOLDER_ELECTIVE_KEY)} placeholder key mappings → {keys_path}")

    # Update supplements
    with open(DATA_DIR / "course_supplements.json", "w") as f:
        json.dump(supplements, f, indent=2, sort_keys=True)
    print(f"Added {new_orphans} new orphan courses → course_supplements.json "
          f"(total: {len(supplements)})")


if __name__ == "__main__":
    main()
