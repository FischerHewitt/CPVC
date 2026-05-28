import type { Professor } from "./types";

type RawPolyRatingsProfessor = {
  id: string;
  firstName: string;
  lastName: string;
  courses?: string[];
  overallRating?: number;
  numEvals?: number;
};

type PolyRatingsPayload = {
  result?: {
    data?: RawPolyRatingsProfessor[];
  };
};

const POLYRATINGS_API_BASE = "https://api-prod.polyratings.org";
const POLYRATINGS_PROFILE_BASE = "https://polyratings.dev";

const COURSE_RE = /([A-Z]{2,5})\s*(\d{3,4}[A-Z]?)/g;
const DEPT_ALIASES: Record<string, string[]> = {
  EGL: ["ENGL"],
};

let professorCache: Promise<RawPolyRatingsProfessor[]> | null = null;

function normCourse(courseNumber: string): string {
  return courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
}

function extractCourseNumbers(text: string): Set<string> {
  const courses = new Set<string>();
  for (const match of text.toUpperCase().matchAll(COURSE_RE)) {
    const dept = match[1];
    const num = match[2];
    if (dept && num) courses.add(`${dept} ${num}`);
  }
  return courses;
}

function departmentVariants(dept: string): Set<string> {
  return new Set([dept, ...(DEPT_ALIASES[dept] ?? [])]);
}

function deriveQuarterCandidates(courseNumber: string): Set<string> {
  const candidates = new Set<string>();
  const [dept, code] = normCourse(courseNumber).split(/\s+/);
  if (!dept || !code || !/^\d{4}$/.test(code)) return candidates;

  for (const deptVariant of departmentVariants(dept)) {
    candidates.add(`${deptVariant} ${String(Number(code.slice(1)))}`);
    if (Number(code) >= 3000 && code.endsWith("0")) {
      candidates.add(`${deptVariant} ${code.slice(0, 3)}`);
    }
  }
  return candidates;
}

function searchKeysForCourse(courseNumber: string): Set<string> {
  const requested = extractCourseNumbers(courseNumber);
  if (requested.size === 0) requested.add(normCourse(courseNumber));

  const keys = new Set<string>();
  for (const course of requested) {
    const [dept, code] = normCourse(course).split(/\s+/);
    const depts = dept ? departmentVariants(dept) : new Set<string>();
    for (const deptVariant of depts) {
      if (code) keys.add(`${deptVariant} ${code}`);
    }
    for (const candidate of deriveQuarterCandidates(course)) {
      keys.add(candidate);
    }
  }
  return keys;
}

function indexKeysForPolyRatingsCourse(course: string): Set<string> {
  const keys = new Set([normCourse(course)]);
  for (const extracted of extractCourseNumbers(course)) {
    keys.add(normCourse(extracted));
  }
  return keys;
}

function buildIndex(professors: RawPolyRatingsProfessor[]): Map<string, RawPolyRatingsProfessor[]> {
  const index = new Map<string, RawPolyRatingsProfessor[]>();
  for (const professor of professors) {
    for (const course of professor.courses ?? []) {
      for (const key of indexKeysForPolyRatingsCourse(course)) {
        index.set(key, [...(index.get(key) ?? []), professor]);
      }
    }
  }
  return index;
}

async function fetchAllProfessors(): Promise<RawPolyRatingsProfessor[]> {
  const res = await fetch(`${POLYRATINGS_API_BASE}/professors.all`);
  if (!res.ok) return [];
  const payload = (await res.json()) as PolyRatingsPayload;
  return payload.result?.data ?? [];
}

export function resetPolyRatingsCacheForTests(): void {
  professorCache = null;
}

export async function getPolyRatingsProfessorsForCourse(courseNumber: string): Promise<Professor[]> {
  professorCache ??= fetchAllProfessors().catch((error) => {
    professorCache = null;
    throw error;
  });

  const allProfessors = await professorCache;
  const index = buildIndex(allProfessors);
  const searchKeys = searchKeysForCourse(courseNumber);
  const seen = new Set<string>();
  const matched: RawPolyRatingsProfessor[] = [];

  for (const key of searchKeys) {
    for (const professor of index.get(key) ?? []) {
      if (seen.has(professor.id)) continue;
      seen.add(professor.id);
      matched.push(professor);
    }
  }

  return matched
    .filter((professor) => (professor.numEvals ?? 0) > 0)
    .sort((a, b) => {
      const evalDiff = (b.numEvals ?? 0) - (a.numEvals ?? 0);
      if (evalDiff !== 0) return evalDiff;
      return (b.overallRating ?? 0) - (a.overallRating ?? 0);
    })
    .map((professor) => ({
      name: `${professor.firstName} ${professor.lastName}`,
      overall_score: Number((professor.overallRating ?? 0).toFixed(2)),
      num_ratings: professor.numEvals ?? 0,
      polyratings_url: `${POLYRATINGS_PROFILE_BASE}/professor/${professor.id}`,
    }));
}
