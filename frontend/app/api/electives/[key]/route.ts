import { readFile } from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";
import { parseUnitsRange } from "@/lib/units";

const DATA_DIR = path.resolve(process.cwd(), "../backend/data");

type StaticDefn = { title: string; description: string; courses: string[] };
type CourseInfo = { title: string; units: string | number };

let staticCache: Record<string, StaticDefn> | null = null;
let catalogCache: Record<string, CourseInfo> | null = null;

async function staticElectives(): Promise<Record<string, StaticDefn>> {
  if (staticCache) return staticCache;
  const raw = await readFile(path.join(DATA_DIR, "electives_static.json"), "utf-8");
  staticCache = JSON.parse(raw) as Record<string, StaticDefn>;
  return staticCache;
}

async function courseCatalog(): Promise<Record<string, CourseInfo>> {
  if (catalogCache) return catalogCache;
  const [catRaw, suppRaw] = await Promise.all([
    readFile(path.join(DATA_DIR, "course_catalog.json"), "utf-8").catch(() => "{}"),
    readFile(path.join(DATA_DIR, "course_supplements.json"), "utf-8").catch(() => "{}"),
  ]);
  const catalog = JSON.parse(catRaw) as Record<string, CourseInfo>;
  const supplements = JSON.parse(suppRaw) as Record<string, CourseInfo>;
  catalogCache = { ...catalog, ...supplements };
  return catalogCache;
}

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ key: string }> },
) {
  const { key } = await params;

  try {
    const [electives, catalog] = await Promise.all([staticElectives(), courseCatalog()]);
    const defn = electives[key];
    if (!defn) {
      return NextResponse.json({ detail: `No elective data for key: ${key}` }, { status: 404 });
    }

    const courses = defn.courses
      .map((num) => {
        const info = catalog[num];
        if (!info) return null;
        const unitFields = parseUnitsRange(info.units);
        return { course_number: num, title: info.title ?? "", ...unitFields };
      })
      .filter((c): c is { course_number: string; title: string; units: number } => c !== null);

    return NextResponse.json({ key, title: defn.title, description: defn.description, courses });
  } catch {
    return NextResponse.json({ detail: "Failed to load elective data" }, { status: 500 });
  }
}
