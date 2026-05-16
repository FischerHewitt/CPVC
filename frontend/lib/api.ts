import type { Flowchart, Professor, GEArea, GEAreaMap, ElectiveArea, CourseInfo, TranscriptSession, MajorOption, Concentration } from "./types";

const configuredApi = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "");
const API =
  configuredApi ??
  (typeof window !== "undefined" && window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "");

function apiUrl(path: string): string {
  return `${API}${path}`;
}

async function responseError(res: Response, action: string): Promise<Error> {
  const body = await res.text();
  const detail = body ? ` ${body}` : "";
  return new Error(`${action} failed (${res.status}) at ${res.url}.${detail}`);
}

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
  const res = await fetch(apiUrl("/api/transcript/parse"), { method: "POST", body: form });
  if (!res.ok) throw await responseError(res, "Transcript parsing");
  return res.json();
}

export async function parseCsvTranscript(file: File, major: string): Promise<{
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
  const res = await fetch(apiUrl("/api/transcript/parse-csv"), { method: "POST", body: form });
  if (!res.ok) throw await responseError(res, "CSV parsing");
  return res.json();
}

export async function sendContactMessage(payload: {
  name: string;
  email: string;
  category: string;
  custom_subject: string;
  message: string;
}): Promise<void> {
  const res = await fetch(apiUrl("/api/contact/send"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw await responseError(res, "Sending message");
}

export async function getFlowchart(majorCode: string): Promise<Flowchart> {
  const res = await fetch(apiUrl(`/api/flowchart/${majorCode}`));
  if (!res.ok) throw await responseError(res, `Loading ${majorCode} flowchart`);
  return res.json();
}

export async function getConcentrations(majorCode: string): Promise<Concentration[]> {
  try {
    const res = await fetch(apiUrl(`/api/flowchart/${majorCode}/concentrations`));
    if (!res.ok) return [];
    const data = await res.json();
    return data.concentrations ?? [];
  } catch {
    return [];
  }
}

export async function getMajors(): Promise<MajorOption[]> {
  const res = await fetch(apiUrl("/api/flowchart/majors"));
  if (!res.ok) throw await responseError(res, "Loading majors");
  const data = await res.json();
  return data.majors ?? [];
}

export async function inferPrerequisites(
  majorCode: string,
  completed: string[],
): Promise<string[]> {
  const res = await fetch(apiUrl(`/api/flowchart/${majorCode}/infer`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) return [];
  const data = await res.json();
  return data.inferred ?? [];
}

export async function getProfessors(courseNumber: string): Promise<Professor[]> {
  const res = await fetch(apiUrl(`/api/professors/${encodeURIComponent(courseNumber)}`));
  if (!res.ok) return [];
  const data = await res.json();
  return data.professors ?? [];
}

export async function getCourseInfo(courseNumber: string): Promise<CourseInfo | null> {
  try {
    const res = await fetch(apiUrl(`/api/courses/${encodeURIComponent(courseNumber)}`));
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export async function getGEAreaMap(): Promise<GEAreaMap> {
  try {
    const res = await fetch(apiUrl("/api/ge/all"));
    if (!res.ok) return {};
    return res.json();
  } catch {
    return {};
  }
}

export async function getGECourses(areaId: string): Promise<GEArea | null> {
  const res = await fetch(apiUrl(`/api/ge/${encodeURIComponent(areaId)}`));
  if (!res.ok) return null;
  return res.json();
}

export async function getElectiveCourses(electiveKey: string): Promise<ElectiveArea | null> {
  const res = await fetch(apiUrl(`/api/electives/${encodeURIComponent(electiveKey)}`));
  if (!res.ok) return null;
  return res.json();
}

export async function getPlaceholderElectiveCourses(course: {
  id: string;
  course_number: string;
  title: string;
  quarter_equivalents: string[];
}): Promise<ElectiveArea | null> {
  const params = new URLSearchParams({
    course_id: course.id,
    course_number: course.course_number,
    title: course.title,
    quarter_equivalents: course.quarter_equivalents.join(","),
  });
  const res = await fetch(apiUrl(`/api/electives/auto/placeholder?${params.toString()}`));
  if (!res.ok) return null;
  return res.json();
}

/** Fetch a session from the backend DB. Returns null if not found. */
export async function getSession(sessionId: string): Promise<TranscriptSession | null> {
  try {
    const res = await fetch(apiUrl(`/api/sessions/${sessionId}`));
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
      concentration: data.concentration ?? undefined,
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
    concentration?: string;
  },
): Promise<void> {
  try {
    await fetch(apiUrl(`/api/sessions/${sessionId}`), {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });
  } catch {
    // silently ignore — localStorage is the fallback
  }
}
