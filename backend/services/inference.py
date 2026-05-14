"""
Prerequisite inference: if a student completed course X, they must have
completed all prerequisites of X (recursively). We surface these as
"inferred" completions so the UI can distinguish explicit vs. inferred.
"""

from data.flowcharts import Course


def build_lookup(courses: list[Course]) -> dict[str, Course]:
    """Map every known number (semester + quarter equivalents) → course."""
    lookup: dict[str, Course] = {}
    for c in courses:
        lookup[c["course_number"]] = c
        for q in c["quarter_equivalents"]:
            lookup[q] = c
    return lookup


def infer_completed(
    explicitly_completed: set[str],
    courses: list[Course],
) -> set[str]:
    """
    Return the set of course numbers (semester + quarter) that can be
    inferred as completed because they are prerequisites of explicitly
    completed courses.

    e.g. If the student completed MATH 2263 (Calc III), and MATH 2263
    requires MATH 1262 (Calc II) which requires MATH 1261 (Calc I),
    then MATH 1261 and MATH 1262 are both returned as inferred.
    """
    lookup = build_lookup(courses)
    inferred: set[str] = set()

    # BFS from each explicitly completed course, walking prereqs backwards
    queue = list(explicitly_completed)
    visited: set[str] = set(explicitly_completed)

    while queue:
        num = queue.pop()
        course = lookup.get(num)
        if not course:
            continue

        for prereq_num in course["prerequisites"]:
            prereq = lookup.get(prereq_num)
            if not prereq:
                continue

            # Collect all numbers for this prereq course
            all_nums = {prereq["course_number"]} | set(prereq["quarter_equivalents"])

            # Only infer if not already explicitly known
            already_known = all_nums & explicitly_completed
            if not already_known:
                new_nums = all_nums - visited
                if new_nums:
                    inferred |= new_nums
                    visited |= new_nums
                    # Keep traversing upward through this prereq's own prereqs
                    queue.append(prereq["course_number"])

    return inferred
