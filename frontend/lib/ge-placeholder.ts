import type { Course, GEAreaMap, TranscriptSession } from "./types";
import { hasAnyCourseNumber, norm, withQuarterCandidates } from "./course-status";

function uniqueCourseNumbers(courseNumbers: Array<string | undefined>): string[] {
  const seen = new Set<string>();
  const result: string[] = [];
  for (const courseNumber of courseNumbers) {
    if (!courseNumber) continue;
    const normalized = norm(courseNumber);
    if (seen.has(normalized)) continue;
    seen.add(normalized);
    result.push(courseNumber);
  }
  return result;
}

export function withPlannedGECourses(
  geAreaMap: GEAreaMap,
  plannedGECourses: Record<string, string>,
): GEAreaMap {
  const next = { ...geAreaMap };
  for (const [areaId, selectedCourse] of Object.entries(plannedGECourses)) {
    const existing = next[areaId] ?? [];
    if (!existing.some((num) => norm(num) === norm(selectedCourse))) {
      next[areaId] = [...existing, selectedCourse];
    }
  }
  return next;
}

export function gePlaceholderCandidates(
  course: Course,
  geAreaMap: GEAreaMap,
  plannedGECourses: Record<string, string> = {},
): string[] {
  return uniqueCourseNumbers(withQuarterCandidates([
    plannedGECourses[course.course_number],
    ...(geAreaMap[course.course_number] ?? []),
    ...course.quarter_equivalents,
    course.course_number,
  ].filter((courseNumber): courseNumber is string => Boolean(courseNumber))));
}

export function gePlaceholderDisplayData(
  course: Course,
  completedNums: Set<string>,
  inProgressNums: Set<string>,
  geAreaMap: GEAreaMap,
  plannedGECourses: Record<string, string> = {},
) {
  const approved = gePlaceholderCandidates(course, geAreaMap, plannedGECourses);
  return {
    checked: hasAnyCourseNumber(completedNums, approved),
    inProgressChecked: hasAnyCourseNumber(inProgressNums, approved),
    plannedCourseNumber: plannedGECourses[course.course_number],
    activeCourseNumber:
      approved.find((candidate) => completedNums.has(norm(candidate)) || inProgressNums.has(norm(candidate))),
  };
}

export function normalizePlannedGEPlaceholderStatuses(session: TranscriptSession): {
  session: TranscriptSession;
  changed: boolean;
} {
  const plannedGECourses = session.plannedGECourses ?? {};
  const plannedByArea = new Map(
    Object.entries(plannedGECourses)
      .filter(([, selectedCourse]) => selectedCourse)
      .map(([areaId, selectedCourse]) => [norm(areaId), selectedCourse]),
  );

  if (plannedByArea.size === 0) return { session, changed: false };

  const normalizeList = (courseNumbers: string[]) => {
    let changed = false;
    const seen = new Set<string>();
    const next: string[] = [];

    for (const courseNumber of courseNumbers) {
      const replacement = plannedByArea.get(norm(courseNumber)) ?? courseNumber;
      const normalized = norm(replacement);
      if (replacement !== courseNumber) changed = true;
      if (seen.has(normalized)) {
        changed = true;
        continue;
      }
      seen.add(normalized);
      next.push(replacement);
    }

    return { courseNumbers: next, changed };
  };

  const completed = normalizeList(session.completed);
  const inProgress = normalizeList(session.inProgress);
  const changed = completed.changed || inProgress.changed;

  if (!changed) return { session, changed: false };
  return {
    session: {
      ...session,
      completed: completed.courseNumbers,
      inProgress: inProgress.courseNumbers,
    },
    changed: true,
  };
}
