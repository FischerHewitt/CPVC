import type { Course, CourseStatus, GEAreaMap } from "./types";

export function norm(courseNumber: string): string {
  return courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
}

export function toNormalizedSet(courseNums: string[]): Set<string> {
  return new Set(courseNums.map(norm));
}

export function hasAnyCourseNumber(normalizedKnownNums: Set<string>, courseNums: string[]): boolean {
  return courseNums.some((num) => normalizedKnownNums.has(norm(num)));
}

export function isFreeElective(course: Course): boolean {
  return course.title.toLowerCase().includes("free elective") || course.course_number.toLowerCase().startsWith("free");
}

// Expands "CHEM 2240/2242" → ["CHEM 2240", "CHEM 2242"], "BIO 4461/4462/4463" → ["BIO 4461", "BIO 4462", "BIO 4463"]
export function expandSlashCourseNumber(courseNumber: string): string[] {
  if (!courseNumber.includes("/")) return [courseNumber];
  const parts = courseNumber.split("/");
  const first = parts[0].trim();
  const deptMatch = first.match(/^([A-Z]+)\s+/);
  const dept = deptMatch ? deptMatch[1] : null;
  return parts.map((p, i) => {
    p = p.trim();
    if (i === 0 || !dept) return p;
    return p.includes(" ") ? p : `${dept} ${p}`;
  });
}

export function getCourseStatus(
  course: Course,
  completedNums: Set<string>,
  inProgressNums: Set<string>,
  inferredNums: Set<string>,
  knownNums: Set<string>,
  courseLookup: Map<string, Course>,
  geAreaMap: GEAreaMap,
): CourseStatus {
  if (course.is_placeholder && course.category === "ge") {
    const approved = [
      course.course_number,
      ...course.quarter_equivalents,
      ...(geAreaMap[course.course_number] ?? []),
    ];
    if (hasAnyCourseNumber(completedNums, approved)) return "completed";
    if (hasAnyCourseNumber(inProgressNums, approved)) return "in_progress";
    if (course.prerequisites.length > 0) {
      const prereqsMet = course.prerequisites.every((prereqNum) => {
        const prereq = courseLookup.get(norm(prereqNum));
        if (!prereq) return true;
        const prereqNums = [prereq.course_number, ...prereq.quarter_equivalents];
        return hasAnyCourseNumber(knownNums, prereqNums);
      });
      if (!prereqsMet) return "locked";
    }
    return "incomplete";
  }
  if (course.is_placeholder) {
    const allNums = [course.course_number, ...course.quarter_equivalents];
    if (allNums.some((n) => completedNums.has(norm(n)))) return "completed";
    if (allNums.some((n) => inferredNums.has(norm(n)))) return "inferred";
    if (allNums.some((n) => inProgressNums.has(norm(n)))) return "in_progress";
    return "incomplete";
  }

  const allNums = [course.course_number, ...course.quarter_equivalents];
  if (allNums.some((n) => completedNums.has(norm(n)))) return "completed";
  if (allNums.some((n) => inferredNums.has(norm(n))))  return "inferred";
  if (allNums.some((n) => inProgressNums.has(norm(n)))) return "in_progress";

  let anyUnmet = false;
  let allUnmetAreSlash = true;
  for (const prereqNum of course.prerequisites) {
    const prereq = courseLookup.get(norm(prereqNum));
    if (!prereq) continue;
    const prereqNums = [
      prereq.course_number,
      ...prereq.quarter_equivalents,
      ...expandSlashCourseNumber(prereq.course_number),
    ];
    if (!hasAnyCourseNumber(knownNums, prereqNums)) {
      anyUnmet = true;
      if (!prereq.course_number.includes("/")) allUnmetAreSlash = false;
    }
  }

  if (!anyUnmet) return "incomplete";
  if (allUnmetAreSlash) return "prereq_warning";
  return "locked";
}
