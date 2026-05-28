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

export function quarterCandidate(courseNumber: string): string | null {
  const [dept, code] = courseNumber.split(/\s+/);
  if (!dept || !code || !/^\d{4}$/.test(code)) return null;
  return `${dept} ${Number(code.slice(1))}`;
}

export function withQuarterCandidates(courseNums: string[]): string[] {
  const result: string[] = [];
  const seen = new Set<string>();
  for (const courseNumber of courseNums) {
    for (const candidate of [courseNumber, quarterCandidate(courseNumber)]) {
      if (!candidate) continue;
      const normalized = norm(candidate);
      if (seen.has(normalized)) continue;
      seen.add(normalized);
      result.push(candidate);
    }
  }
  return result;
}

export function isFreeElective(course: Course): boolean {
  return course.title.toLowerCase().includes("free elective") || course.course_number.toLowerCase().startsWith("free");
}

// Expands slash-choice course numbers into their individual components.
// Handles two formats:
//   Same-dept:  "CHEM 2240/2242"   → ["CHEM 2240", "CHEM 2242"]
//   Cross-dept: "CSC/CPE 1024"     → ["CSC 1024",  "CPE 1024"]
export function expandSlashCourseNumber(courseNumber: string): string[] {
  if (!courseNumber.includes("/")) return [courseNumber];
  const parts = courseNumber.split("/");
  const first = parts[0].trim();

  // Same-dept format: first part already has "DEPT NUMBER"
  if (/^[A-Z]+\s+/.test(first)) {
    const dept = first.match(/^([A-Z]+)/)?.[1] ?? null;
    return parts.map((p, i) => {
      p = p.trim();
      if (i === 0 || !dept) return p;
      return p.includes(" ") ? p : `${dept} ${p}`;
    });
  }

  // Cross-dept format: first part is dept only, a later part has "DEPT NUMBER"
  const withNumber = parts.find(p => p.trim().includes(" "));
  if (withNumber) {
    const num = withNumber.trim().match(/\s+(\S+)$/)?.[1] ?? "";
    return parts.map(p => {
      p = p.trim();
      return p.includes(" ") ? p : (num ? `${p} ${num}` : p);
    });
  }

  return parts.map(p => p.trim());
}

export function courseCompletionCandidates(course: Course): string[] {
  return [
    course.course_number,
    ...course.quarter_equivalents,
    ...(course.auto_satisfied_by ?? []),
    ...expandSlashCourseNumber(course.course_number),
  ];
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
    const approved = withQuarterCandidates([
      course.course_number,
      ...course.quarter_equivalents,
      ...(geAreaMap[course.course_number] ?? []),
    ]);
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
    const allNums = courseCompletionCandidates(course);
    if (allNums.some((n) => completedNums.has(norm(n)))) return "completed";
    if (allNums.some((n) => inferredNums.has(norm(n)))) return "inferred";
    if (allNums.some((n) => inProgressNums.has(norm(n)))) return "in_progress";
    return "incomplete";
  }

  const allNums = courseCompletionCandidates(course);
  if (allNums.some((n) => completedNums.has(norm(n)))) return "completed";
  if (allNums.some((n) => inferredNums.has(norm(n))))  return "inferred";
  if (allNums.some((n) => inProgressNums.has(norm(n)))) return "in_progress";

  let anyUnmet = false;
  for (const prereqNum of course.prerequisites) {
    const prereq = courseLookup.get(norm(prereqNum));
    if (!prereq) continue;
    const prereqNums = [
      prereq.course_number,
      ...prereq.quarter_equivalents,
      ...expandSlashCourseNumber(prereq.course_number),
    ];
    if (!hasAnyCourseNumber(knownNums, prereqNums)) anyUnmet = true;
  }

  if (!anyUnmet) return "incomplete";
  return "locked";
}
