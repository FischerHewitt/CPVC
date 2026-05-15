import type { Course, GEAreaMap } from "./types";

export function norm(courseNumber: string): string {
  return courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
}

export function toNormalizedSet(courseNums: string[]): Set<string> {
  return new Set(courseNums.map(norm));
}

export function matchesCourse(course: Course, query: string): boolean {
  const q = query.toLowerCase().trim();
  if (!q) return true;
  const haystack = [
    course.course_number,
    course.title,
    course.category,
    ...course.quarter_equivalents,
  ].join(" ").toLowerCase();
  return haystack.includes(q);
}

export function courseIsCompleted(course: Course, completed: Set<string>): boolean {
  return [course.course_number, ...course.quarter_equivalents].some((num) =>
    completed.has(norm(num))
  );
}

export function courseIsInProgress(course: Course, inProgress: Set<string>): boolean {
  return [course.course_number, ...course.quarter_equivalents].some((num) =>
    inProgress.has(norm(num))
  );
}

export function geAreaCandidates(course: Course, geAreaMap: GEAreaMap): string[] {
  return [
    course.course_number,
    ...course.quarter_equivalents,
    ...(geAreaMap[course.course_number] ?? []),
  ];
}

export function geAreaIsKnown(
  course: Course,
  geAreaMap: GEAreaMap,
  known: Set<string>
): boolean {
  return geAreaCandidates(course, geAreaMap).some((candidate) => known.has(norm(candidate)));
}
