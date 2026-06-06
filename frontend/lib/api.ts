import type { CustomCourseEntry, Flowchart, Professor, GEArea, GEAreaMap, ElectiveArea, CourseInfo, TranscriptSession, MajorOption, Concentration, CourseSearchResult, FreeElectiveSelection } from "./types";
import { getPolyRatingsProfessorsForCourse } from "./polyratings";

type StaticFlowchartData = {
  flowcharts: Record<string, Flowchart>;
  concentrations: Record<string, Concentration[]>;
  concentrationFlowchartKeys: string[];
};

type StaticGEData = {
  areas: Record<string, GEArea>;
  areaMap: GEAreaMap;
};

const STATIC_ELECTIVES: Record<string, ElectiveArea> = {
  cs_privacy_security_elective: {
    key: "cs_privacy_security_elective",
    title: "Privacy & Security Concentration Elective",
    description: "Approved elective courses for the Privacy & Security concentration.",
    courses: [
      { course_number: "CSC 3203", title: "Cryptography Engineering and Applications", units: 4 },
      { course_number: "CSC 4210", title: "Software Security", units: 3 },
      { course_number: "CSC 4212", title: "Malware Design and Analysis", units: 3 },
      { course_number: "CSC 4214", title: "Binary Exploitation: Tools and Techniques", units: 3 },
      { course_number: "CSC 4230", title: "Web and Cloud Security", units: 3 },
      { course_number: "CSC 4270", title: "Special Advanced Topics in Computer Security", units: 1 },
      { course_number: "CSC 4291", title: "Seminars in Privacy and Security", units: 1 },
      { course_number: "CSC 4292", title: "Research Experience in Privacy and Security", units: 1 },
      { course_number: "CSC 4293", title: "Projects in Privacy and Security", units: 1 },
      { course_number: "CSC 4310", title: "Compiler Construction", units: 3 },
      { course_number: "CSC 4471", title: "Special Advanced Laboratory", units: 1 },
      { course_number: "CSC 4472", title: "Special Advanced Activity", units: 1 },
      { course_number: "CSC 5201", title: "Computer Security and Privacy", units: 3 },
      { course_number: "CSC 5210", title: "Software Security", units: 3 },
      { course_number: "CSC 5220", title: "Advanced Network Security and Privacy", units: 3 },
      { course_number: "CSC 5270", title: "Special Advanced Topics in Computer Security", units: 1 },
      { course_number: "CSC 5281", title: "System Security", units: 3 },
      { course_number: "CPE 4220", title: "Network Security", units: 3 },
      { course_number: "CPE 4250", title: "Wireless Security", units: 3 },
      { course_number: "CPE 4280", title: "Introduction to Hardware Security", units: 3 },
      { course_number: "CPE 4464", title: "Introduction to Computer Networks", units: 3 },
      { course_number: "CPE 5564", title: "Research Topics in Computer Networks", units: 3 },
    ],
  },
};

const configuredApi = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "");
const API =
  configuredApi ??
  (typeof window !== "undefined" && window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "");

function apiUrl(path: string): string {
  return `${API}${path}`;
}

/**
 * GET JSON from `path` via the configured API URL.
 * When the configured URL differs from the bare path, retries on the same-origin
 * route on any failure so Next.js API routes work as a transparent proxy fallback.
 * Returns null on all failures so callers can fall through to static bundled data.
 */
async function tryApiJson<T>(path: string): Promise<T | null> {
  const primary = apiUrl(path);
  const urls = primary !== path ? [primary, path] : [primary];
  for (const url of urls) {
    try {
      const res = await fetch(url);
      if (res.ok) return res.json() as Promise<T>;
    } catch {}
  }
  return null;
}

async function staticFlowchartData(): Promise<StaticFlowchartData> {
  const data = await import("./static-flowchart-data.json");
  return data.default as unknown as StaticFlowchartData;
}

async function staticFlowchart(majorCode: string): Promise<Flowchart | null> {
  const data = await staticFlowchartData();
  const key = majorCode.toUpperCase();
  const flowchart = data.flowcharts[key] ?? null;
  if (!flowchart || flowchart.notes?.length) return flowchart;

  const baseMajor = Object.entries(data.concentrations).find(([, concentrations]) =>
    concentrations.some((concentration) => concentration.full_flowchart_key === key),
  )?.[0];
  const baseNotes = baseMajor ? data.flowcharts[baseMajor]?.notes : undefined;
  if (!baseNotes?.length) return flowchart;

  return { ...flowchart, notes: baseNotes };
}

async function staticGEData(): Promise<StaticGEData> {
  const data = await import("./static-ge-data.json");
  return data.default as unknown as StaticGEData;
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
  const data = await tryApiJson<Flowchart>(`/api/flowchart/${majorCode}`);
  if (data) return data;
  const fallback = await staticFlowchart(majorCode);
  if (fallback) return fallback;
  throw new Error(`Loading ${majorCode} flowchart failed.`);
}

export async function getConcentrations(majorCode: string): Promise<Concentration[]> {
  const data = await tryApiJson<{ concentrations: Concentration[] }>(`/api/flowchart/${majorCode}/concentrations`);
  if (data) return data.concentrations ?? [];
  const staticData = await staticFlowchartData();
  return staticData.concentrations[majorCode.toUpperCase()] ?? [];
}

export async function getMajors(): Promise<MajorOption[]> {
  const data = await tryApiJson<{ majors: MajorOption[] }>("/api/flowchart/majors");
  if (data) return data.majors ?? [];
  const staticData = await staticFlowchartData();
  const concentrationKeys = new Set(staticData.concentrationFlowchartKeys);
  return Object.entries(staticData.flowcharts)
    .filter(([code]) => !concentrationKeys.has(code))
    .map(([code, flowchart]) => ({ code, name: flowchart.major }));
}

export async function inferPrerequisites(
  majorCode: string,
  completed: string[],
): Promise<string[]> {
  try {
    const res = await fetch(apiUrl(`/api/flowchart/${majorCode}/infer`), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed }),
    });
    if (!res.ok) return [];
    const data = await res.json();
    return data.inferred ?? [];
  } catch {
    return [];
  }
}

export async function getProfessors(courseNumber: string): Promise<Professor[]> {
  try {
    const res = await fetch(apiUrl(`/api/professors/${encodeURIComponent(courseNumber)}`));
    if (res.ok) {
      const professors: Professor[] = (await res.json()).professors ?? [];
      if (professors.length > 0) return professors;
    }
  } catch {}

  try {
    return await getPolyRatingsProfessorsForCourse(courseNumber);
  } catch {
    return [];
  }
}

export async function getCourseInfo(courseNumber: string): Promise<CourseInfo | null> {
  return tryApiJson<CourseInfo>(`/api/courses/${encodeURIComponent(courseNumber)}`);
}

export async function searchCatalogCourses(query: string, limit = 20, offset = 0): Promise<CourseSearchResult[]> {
  const params = new URLSearchParams({ q: query, limit: String(limit), offset: String(offset) });
  const data = await tryApiJson<{ courses: CourseSearchResult[] }>(`/api/courses/search?${params}`);
  return data?.courses ?? [];
}

export async function getGEAreaMap(): Promise<GEAreaMap> {
  const data = await tryApiJson<GEAreaMap>("/api/ge/all");
  if (data) return data;
  const staticData = await staticGEData();
  return staticData.areaMap;
}

export async function getGECourses(areaId: string): Promise<GEArea | null> {
  const data = await tryApiJson<GEArea>(`/api/ge/${encodeURIComponent(areaId)}`);
  if (data) return data;
  const staticData = await staticGEData();
  return staticData.areas[areaId] ?? null;
}

export async function getElectiveCourses(electiveKey: string): Promise<ElectiveArea | null> {
  const data = await tryApiJson<ElectiveArea>(`/api/electives/${encodeURIComponent(electiveKey)}`);
  return data ?? STATIC_ELECTIVES[electiveKey] ?? null;
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
  return tryApiJson<ElectiveArea>(`/api/electives/auto/placeholder?${params}`);
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
      plannedCourseUnits: data.planned_course_units ?? {},
      plannedFreeElectiveCourses: data.planned_free_elective_courses ?? {},
      concentration: data.concentration ?? undefined,
    };
  } catch {
    return null;
  }
}

/** Persist session changes back to the DB (best-effort, never throws). */
export type SyncResult = "ok" | "missing" | "error";

export async function syncSession(
  sessionId: string,
  updates: {
    completed?: string[];
    in_progress?: string[];
    course_positions?: Record<string, unknown>;
    planned_ge_courses?: Record<string, string>;
    planned_ge_units?: Record<string, number>;
    planned_course_units?: Record<string, number>;
    planned_free_elective_courses?: Record<string, FreeElectiveSelection>;
    planned_custom_courses?: Record<string, CustomCourseEntry>;
    concentration?: string;
  },
): Promise<SyncResult> {
  try {
    const res = await fetch(apiUrl(`/api/sessions/${sessionId}`), {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });
    if (res.status === 404) return "missing";
    if (!res.ok) return "error";
    return "ok";
  } catch {
    return "error";
  }
}
