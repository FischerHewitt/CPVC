#!/usr/bin/env python3
"""
Seed backend/data/course_supplements.json with courses that appear in elective
option lists but are not present in course_catalog.json (i.e., they do not appear
as a required non-placeholder tile in any major's flowchart).

Currently sources from _CS_STATIC_COURSE_INFO in routers/electives.py.
As more majors are migrated to the new elective format, re-run this script or
manually add entries to course_supplements.json for any newly introduced orphans.

Run from backend/:
    python3 scripts/seed_course_supplements.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DATA_DIR = Path(__file__).parent.parent / "data"


def main() -> None:
    with open(DATA_DIR / "course_catalog.json") as f:
        catalog: dict[str, dict] = json.load(f)

    supplements_path = DATA_DIR / "course_supplements.json"
    with open(supplements_path) as f:
        existing_supplements: dict[str, dict] = json.load(f)

    # Import _CS_STATIC_COURSE_INFO without triggering the full router side-effects
    # by reaching into the module after import.
    from routers.electives import _CS_STATIC_COURSE_INFO

    new_entries: dict[str, dict] = {}
    skipped_compound = 0

    for course_number, info in _CS_STATIC_COURSE_INFO.items():
        # Skip compound entries like "CSC 4160 and CSC 4161" — not a single course number
        if " and " in course_number:
            skipped_compound += 1
            continue
        # Skip if already in catalog or already in supplements
        if course_number in catalog or course_number in existing_supplements:
            continue
        new_entries[course_number] = info

    merged = {**existing_supplements, **new_entries}

    with open(supplements_path, "w") as f:
        json.dump(merged, f, indent=2, sort_keys=True)

    print(f"Skipped {skipped_compound} compound entries (e.g. 'CSC 4160 and CSC 4161')")
    print(f"Added {len(new_entries)} new orphan courses to course_supplements.json")
    print(f"Total supplement entries: {len(merged)}")

    if new_entries:
        print("\nNew entries:")
        for num in sorted(new_entries):
            print(f"  {num}: {new_entries[num]['title']} ({new_entries[num]['units']} units)")


if __name__ == "__main__":
    main()
