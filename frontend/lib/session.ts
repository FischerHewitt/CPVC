import type { TranscriptSession } from "./types";
import { syncSession } from "./api";

// ─── localStorage (primary offline cache) ────────────────────────────────────

export function saveSession(session: TranscriptSession): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(`cpvc_session_${session.sessionId}`, JSON.stringify(session));
}

export function loadSession(sessionId: string): TranscriptSession | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(`cpvc_session_${sessionId}`);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as TranscriptSession;
  } catch {
    return null;
  }
}

// ─── Write-through: save locally AND push to DB ───────────────────────────────

/**
 * Persist a session update everywhere:
 *   1. Overwrite localStorage immediately (synchronous, instant UI)
 *   2. Push the delta to the backend DB (async, best-effort)
 */
export function persistSession(
  session: TranscriptSession,
  dbDelta?: {
    completed?: string[];
    in_progress?: string[];
    course_positions?: Record<string, unknown>;
    planned_ge_courses?: Record<string, string>;
    planned_ge_units?: Record<string, number>;
    concentration?: string;
  },
): void {
  saveSession(session);

  const delta = dbDelta ?? {
    completed:        session.completed,
    in_progress:      session.inProgress,
    course_positions: (session.coursePositions ?? {}) as Record<string, unknown>,
    planned_ge_courses: session.plannedGECourses ?? {},
    planned_ge_units: session.plannedGEUnits ?? {},
  };

  void syncSession(session.sessionId, delta);
}
