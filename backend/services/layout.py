"""
Auto-layout: reassign grid_row values so prerequisite chains stay horizontally aligned.
grid_col is never changed (semester placement is academically fixed).

Algorithm (per column, left-to-right):
  1. "Chain" courses (have in-flowchart prereqs) inherit the row of their
     primary predecessor. Conflicts within the same column are resolved by
     bumping later courses down.
  2. "Free" courses (no in-flowchart prereqs) fill the remaining gaps in
     their original relative order, so no empty rows are left behind.
"""

from collections import defaultdict


def align_prereq_chains(courses: list[dict]) -> list[dict]:
    # Build lookup by course_number; prefer non-placeholder for prereq resolution
    by_number: dict[str, dict] = {}
    for c in courses:
        num = c["course_number"]
        if num not in by_number or not c["is_placeholder"]:
            by_number[num] = c

    assigned: dict[str, int] = {}  # course id -> final grid_row

    cols = sorted(set(c["grid_col"] for c in courses))

    for col in cols:
        col_courses = sorted(
            (c for c in courses if c["grid_col"] == col),
            key=lambda c: c["grid_row"],
        )

        chained: list[tuple[dict, int]] = []  # (course, preferred_row)
        free: list[dict] = []

        for course in col_courses:
            in_data = [by_number[p] for p in course["prerequisites"] if p in by_number]
            if in_data:
                # Primary prereq: the one that appears latest (highest grid_col)
                primary = max(in_data, key=lambda p: p["grid_col"])
                preferred = assigned.get(primary["id"], primary["grid_row"])
                chained.append((course, preferred))
            else:
                free.append(course)

        # Place chain courses at their preferred rows (bump on conflict)
        chained.sort(key=lambda x: (x[1], x[0]["grid_row"]))
        used: set[int] = set()
        for course, preferred in chained:
            row = preferred
            while row in used:
                row += 1
            used.add(row)
            assigned[course["id"]] = row

        # Fill free courses into unused rows, preserving their relative order
        if used:
            candidate_limit = max(used) + 1 + len(free)
        else:
            candidate_limit = len(free)
        free_slots = [r for r in range(candidate_limit) if r not in used]
        # Extend if we ran out of slots (shouldn't normally happen)
        r = candidate_limit
        while len(free_slots) < len(free):
            if r not in used:
                free_slots.append(r)
            r += 1

        for i, course in enumerate(free):
            assigned[course["id"]] = free_slots[i]

    return [{**c, "grid_row": assigned.get(c["id"], c["grid_row"])} for c in courses]
