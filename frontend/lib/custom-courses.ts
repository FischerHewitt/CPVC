import type { CourseSearchResult, CustomCourseEntry, TranscriptSession } from "./types";

/**
 * Returns a new session with the given catalog course added as a custom tile
 * in the specified term column. The entry is keyed by the provided id.
 */
export function applyAddCustomCourse(
  session: TranscriptSession,
  col: number,
  course: CourseSearchResult,
  id: string,
  assignedToSlotId?: string,
): TranscriptSession {
  const entry: CustomCourseEntry = {
    course_number: course.course_number,
    title: course.title,
    units: course.units,
    grid_col: col,
    status: "planned",
    ...(assignedToSlotId ? { assignedToSlotId } : {}),
  };
  return {
    ...session,
    customCourses: {
      ...session.customCourses,
      [id]: entry,
    },
  };
}

/**
 * Updates mutable fields of an existing custom course entry (course details and/or slot assignment).
 * Preserves id, grid_col, and status.
 */
export function applyUpdateCustomCourse(
  session: TranscriptSession,
  customId: string,
  updates: Partial<Pick<CustomCourseEntry, "course_number" | "title" | "units" | "assignedToSlotId">>,
): TranscriptSession {
  const entry = session.customCourses?.[customId];
  if (!entry) return session;
  const updated = { ...entry, ...updates };
  if ("assignedToSlotId" in updates && updates.assignedToSlotId === undefined) {
    delete updated.assignedToSlotId;
  }
  return {
    ...session,
    customCourses: { ...session.customCourses, [customId]: updated },
  };
}

/**
 * Updates the status (planned / in_progress / completed) of a custom course.
 */
export function applySetCustomCourseStatus(
  session: TranscriptSession,
  customId: string,
  status: CustomCourseEntry["status"],
): TranscriptSession {
  const entry = session.customCourses?.[customId];
  if (!entry) return session;
  return {
    ...session,
    customCourses: {
      ...session.customCourses,
      [customId]: { ...entry, status },
    },
  };
}

/**
 * Assigns a custom course to a flowchart slot (by slot Course.id).
 * The slot will show a "covered by" badge derived from this at render time.
 */
export function applyAssignCustomCourse(
  session: TranscriptSession,
  customId: string,
  slotId: string,
): TranscriptSession {
  const entry = session.customCourses?.[customId];
  if (!entry) return session;
  return {
    ...session,
    customCourses: {
      ...session.customCourses,
      [customId]: { ...entry, assignedToSlotId: slotId },
    },
  };
}

/**
 * Clears the slot assignment from a custom course entry.
 */
export function applyClearCustomAssignment(
  session: TranscriptSession,
  customId: string,
): TranscriptSession {
  const entry = session.customCourses?.[customId];
  if (!entry) return { ...session, customCourses: { ...(session.customCourses ?? {}) } };
  const { assignedToSlotId: _removed, ...rest } = entry;
  return {
    ...session,
    customCourses: {
      ...session.customCourses,
      [customId]: rest,
    },
  };
}

/**
 * Returns a new session with the specified custom course removed.
 * If the removed course had a slot assignment, no slot-side cleanup is needed
 * (the assignment was stored only on the custom entry).
 */
export function applyRemoveCustomCourse(
  session: TranscriptSession,
  id: string,
): TranscriptSession {
  const next = { ...(session.customCourses ?? {}) };
  delete next[id];
  return { ...session, customCourses: next };
}
