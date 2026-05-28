import { readFile } from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";

type RawCatalogCourse = {
  courseSubject?: string;
  courseNumber?: string;
  displayName?: string;
  units?: string;
};

type CatalogCourse = {
  course_number: string;
  title: string;
  units: number;
};

const COURSES_PATH = path.resolve(
  process.cwd(),
  "../backend/data/polyplanner/catalog-data/2026-2028/courses.json",
);

let courseCache: CatalogCourse[] | null = null;

function compact(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]/g, "");
}

function firstUnitValue(units: string | undefined): number {
  const match = String(units ?? "").match(/\d+/);
  return match ? Number(match[0]) : 0;
}

async function catalogCourses(): Promise<CatalogCourse[]> {
  if (courseCache) return courseCache;

  const raw = await readFile(COURSES_PATH, "utf-8");
  const rows = JSON.parse(raw) as RawCatalogCourse[];
  courseCache = rows
    .map((row) => {
      const subject = String(row.courseSubject ?? "").trim().toUpperCase();
      const number = String(row.courseNumber ?? "").trim().toUpperCase();
      if (!subject || !number) return null;
      return {
        course_number: `${subject} ${number}`,
        title: String(row.displayName ?? "").trim(),
        units: firstUnitValue(row.units),
      };
    })
    .filter((course): course is CatalogCourse => Boolean(course))
    .sort((a, b) => a.course_number.localeCompare(b.course_number));

  return courseCache;
}

function searchCourses(courses: CatalogCourse[], query: string, limit: number, offset: number): CatalogCourse[] {
  const q = query.trim().replace(/\s+/g, " ").toLowerCase();
  const qCompact = compact(query);
  const tokens = q.split(" ").filter(Boolean);
  const browsing = !q && !qCompact;

  const scored: Array<[number, string, CatalogCourse]> = [];
  for (const course of courses) {
    const courseLower = course.course_number.toLowerCase();
    const compactNumber = compact(course.course_number);
    const compactHaystack = compact(`${course.course_number} ${course.title}`);
    const haystack = `${courseLower} ${course.title.toLowerCase()}`;
    const tokenMatch = tokens.length > 0 && tokens.every((token) => haystack.includes(token));

    if (!browsing && !haystack.includes(q) && !compactHaystack.includes(qCompact) && !tokenMatch) {
      continue;
    }

    let rank = 50;
    if (browsing) rank = 100;
    else if (qCompact && compactNumber === qCompact) rank = 0;
    else if (qCompact && compactNumber.startsWith(qCompact)) rank = 5;
    else if (q && courseLower.startsWith(q)) rank = 10;
    else if (qCompact && compactNumber.includes(qCompact)) rank = 15;
    else if (tokenMatch) rank = 20;
    else if (q && course.title.toLowerCase().includes(q)) rank = 25;

    scored.push([rank, course.course_number, course]);
  }

  scored.sort((a, b) => a[0] - b[0] || a[1].localeCompare(b[1]));
  return scored.slice(offset, offset + limit).map(([, , course]) => course);
}

export async function GET(request: Request) {
  const url = new URL(request.url);
  const query = url.searchParams.get("q") ?? "";
  const limit = Math.min(50, Math.max(1, Number(url.searchParams.get("limit") ?? 20) || 20));
  const offset = Math.max(0, Number(url.searchParams.get("offset") ?? 0) || 0);

  try {
    const courses = await catalogCourses();
    return NextResponse.json({ courses: searchCourses(courses, query, limit, offset) });
  } catch {
    return NextResponse.json({ courses: [] });
  }
}
