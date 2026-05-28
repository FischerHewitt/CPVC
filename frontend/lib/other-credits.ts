import type { Course, FreeElectiveSelection, GEAreaMap } from "./types";
import { norm } from "./course-status";

export type OtherCreditStatus = "completed" | "in_progress";

export interface OtherCredit {
  courseNumber: string;
  status: OtherCreditStatus;
}

export function isTransferCreditPlaceholder(courseNumber: string): boolean {
  return /\b\d*TR\b/i.test(courseNumber);
}

export function isCalPolyCourseLike(courseNumber: string): boolean {
  return /^[A-Z]{2,5}\s+\d{2,4}[A-Z]?$/i.test(courseNumber.trim());
}

export function getOtherCredits(
  courses: Course[],
  completed: string[],
  inProgress: string[],
  geAreaMap: GEAreaMap,
  plannedCourseSelections: Record<string, string> = {},
  plannedFreeElectiveCourses: Record<string, FreeElectiveSelection> = {},
): OtherCredit[] {
  const counted = new Set<string>();

  for (const course of courses) {
    counted.add(norm(course.course_number));
    for (const equivalent of course.quarter_equivalents) {
      counted.add(norm(equivalent));
    }
    if (course.is_placeholder && course.category === "ge") {
      for (const approvedCourse of geAreaMap[course.course_number] ?? []) {
        counted.add(norm(approvedCourse));
      }
    }
  }

  for (const selectedCourse of Object.values(plannedCourseSelections)) {
    counted.add(norm(selectedCourse));
  }
  for (const selectedCourse of Object.values(plannedFreeElectiveCourses)) {
    counted.add(norm(selectedCourse.course_number));
  }

  const completedSet = new Set(completed.map(norm));
  const imported = [
    ...completed.map((courseNumber): OtherCredit => ({ courseNumber, status: "completed" })),
    ...inProgress
      .filter((courseNumber) => !completedSet.has(norm(courseNumber)))
      .map((courseNumber): OtherCredit => ({ courseNumber, status: "in_progress" })),
  ];

  const seen = new Set<string>();
  return imported.filter(({ courseNumber }) => {
    const normalized = norm(courseNumber);
    if (seen.has(normalized)) return false;
    seen.add(normalized);
    return !counted.has(normalized)
      && !isTransferCreditPlaceholder(courseNumber)
      && isCalPolyCourseLike(courseNumber);
  });
}
