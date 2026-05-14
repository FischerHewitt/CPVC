import type { Flowchart, Professor, GEArea, GEAreaMap, CourseInfo, TranscriptSession, MajorOption } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function parseTranscript(file: File, major: string): Promise<{
  session_id: string;
  student_name: string;
  student_id: string;
  major: string;
  completed: string[];
  in_progress: string[];
}> {
  const form = new FormData();
  form.append("file", file);
  form.append("major", major);
  const res = await fetch(`${API}/api/transcript/parse`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getFlowchart(majorCode: string): Promise<Flowchart> {
  const res = await fetch(`${API}/api/flowchart/${majorCode}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getMajors(): Promise<MajorOption[]> {
  const res = await fetch(`${API}/api/flowchart/majors`);
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();
  return data.majors ?? [];
}

export async function inferPrerequisites(
  majorCode: string,
  completed: string[],
): Promise<string[]> {
  const res = await fetch(`${API}/api/flowchart/${majorCode}/infer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) return [];
  const data = await res.json();
  return data.inferred ?? [];
}

export async function getProfessors(courseNumber: string): Promise<Professor[]> {
  const res = await fetch(`${API}/api/professors/${encodeURIComponent(courseNumber)}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.professors ?? [];
}

export async function getCourseInfo(courseNumber: string): Promise<CourseInfo | null> {
  try {
    const res = await fetch(`${API}/api/courses/${encodeURIComponent(courseNumber)}`);
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export async function getGEAreaMap(): Promise<GEAreaMap> {
  try {
    const res = await fetch(`${API}/api/ge/all`);
    if (!res.ok) return {};
    return res.json();
  } catch {
    return {};
  }
}

export async function getGECourses(areaId: string): Promise<GEArea | null> {
  const res = await fetch(`${API}/api/ge/${encodeURIComponent(areaId)}`);
  if (!res.ok) return null;
  return res.json();
}

/** Fetch a session from the backend DB. Returns null if not found. */
export async function getSession(sessionId: string): Promise<TranscriptSession | null> {
  try {
    const res = await fetch(`${API}/api/sessions/${sessionId}`);
    if (!res.ok) return null;
    const data = await res.json();
    return {
      sessionId:       data.session_id,
      studentName:     data.student_name,
      major:           data.major,
      completed:       data.completed   ?? [],
      inProgress:      data.in_progress ?? [],
      coursePositions: data.course_positions ?? {},
      plannedGECourses: data.planned_ge_courses ?? {},
      plannedGEUnits: data.planned_ge_units ?? {},
    };
  } catch {
    return null;
  }
}

/** Persist session changes back to the DB (best-effort, never throws). */
export async function syncSession(
  sessionId: string,
  updates: {
    completed?: string[];
    in_progress?: string[];
    course_positions?: Record<string, unknown>;
    planned_ge_courses?: Record<string, string>;
    planned_ge_units?: Record<string, number>;
  },
): Promise<void> {
  try {
    await fetch(`${API}/api/sessions/${sessionId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });
  } catch {
    // silently ignore — localStorage is the fallback
  }
}
