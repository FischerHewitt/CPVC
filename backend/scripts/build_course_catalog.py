#!/usr/bin/env python3
"""
Build backend/data/course_catalog.json from FLOWCHARTS data.

Extracts every non-placeholder course from every flowchart, deduplicates by
course_number (first occurrence wins), and writes a {course_number: {title, units}}
mapping used by the ElectiveCatalog service for elective resolution.

Run after updating flowcharts.py to keep the catalog in sync:
    cd backend && python3 scripts/build_course_catalog.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from data.flowcharts import FLOWCHARTS

# Strip trailing GE-area annotations that some flowcharts append to course titles,
# e.g. "Calculus I (GE 2)" → "Calculus I", "College Physics I (GE 5A/5C)" → "College Physics I"
_GE_SUFFIX = re.compile(r"\s*\(GE[^)]*\)\s*$", re.IGNORECASE)
# Strip USCP / UD4 / USCP, UD4 style suffixes too
_ATTR_SUFFIX = re.compile(r"\s*\([A-Z0-9 ,/]+\)\s*$")


def _clean_title(title: str) -> str:
    title = _GE_SUFFIX.sub("", title).strip()
    title = _ATTR_SUFFIX.sub("", title).strip()
    return title


def build_catalog() -> tuple[dict[str, dict], list[str]]:
    catalog: dict[str, dict] = {}
    conflicts: list[str] = []

    for major_key, flowchart in FLOWCHARTS.items():
        for course in flowchart["courses"]:
            if course["is_placeholder"]:
                continue
            num = course["course_number"]
            entry = {"title": _clean_title(course["title"]), "units": course["units"]}
            if num in catalog:
                if catalog[num] != entry:
                    conflicts.append(
                        f"{num}: existing={catalog[num]} new={entry} (seen in {major_key})"
                    )
                continue
            catalog[num] = entry

    return catalog, conflicts


def main() -> None:
    catalog, conflicts = build_catalog()

    if conflicts:
        print(f"WARNING: {len(conflicts)} course number conflict(s) — keeping first occurrence:")
        for c in conflicts:
            print(f"  {c}")

    out_path = Path(__file__).parent.parent / "data" / "course_catalog.json"
    with open(out_path, "w") as f:
        json.dump(catalog, f, indent=2, sort_keys=True)

    print(f"Wrote {len(catalog)} courses to {out_path}")


if __name__ == "__main__":
    main()
