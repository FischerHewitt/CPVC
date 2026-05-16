"use client";

import { useMemo, useRef, useState } from "react";
import type { Course, GEAreaMap, Professor } from "@/lib/types";
import { getProfessors } from "@/lib/api";
import {
  toNormalizedSet,
  matchesCourse,
  courseIsCompleted,
  courseIsInProgress,
  geAreaIsKnown,
} from "@/lib/checklist-utils";

interface Props {
  open: boolean;
  courses: Course[];
  completed: string[];
  inProgress: string[];
  geAreaMap: GEAreaMap;
  plannedGECourses: Record<string, string>;
  onToggleCourse: (course: Course) => void;
  onToggleCourseInProgress: (course: Course) => void;
  onToggleGEArea: (course: Course) => void;
  onToggleGEAreaInProgress: (course: Course) => void;
  onImportCSV: (completed: string[], inProgress: string[]) => void;
  onClose: () => void;
}

function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;
  for (const char of line) {
    if (char === '"') { inQuotes = !inQuotes; }
    else if (char === "," && !inQuotes) { result.push(current.trim()); current = ""; }
    else { current += char; }
  }
  result.push(current.trim());
  return result;
}

function parseCalPolyCSV(text: string): { completed: string[]; inProgress: string[] } | null {
  const lines = text.trim().split(/\r?\n/);
  if (lines.length < 2) return null;
  const header = parseCSVLine(lines[0]);
  const courseIdx = header.findIndex((h) => h.toLowerCase() === "course");
  const statusIdx = header.findIndex((h) => h.toLowerCase() === "status");
  if (courseIdx === -1 || statusIdx === -1) return null;
  const completed: string[] = [];
  const inProgress: string[] = [];
  for (let i = 1; i < lines.length; i++) {
    const cols = parseCSVLine(lines[i]);
    const course = cols[courseIdx]?.trim();
    const status = cols[statusIdx]?.trim();
    if (!course || !status) continue;
    if (["Taken", "Transferred (Course)", "Transferred (Test)"].includes(status)) {
      completed.push(course);
    } else if (status === "In Progress") {
      inProgress.push(course);
    }
  }
  return { completed, inProgress };
}

const CATEGORY_LABELS: Record<string, string> = {
  all: "All",
  major: "Major",
  support: "Support",
  concentration: "Conc.",
  ge: "GE",
};

// ── Professor row ─────────────────────────────────────────────────────────────

function ProfessorRow({ prof }: { prof: Professor }) {
  return (
    <div className="flex items-center justify-between py-1.5 border-b border-gray-100 last:border-0">
      <div>
        <div className="text-xs font-medium text-gray-800">{prof.name}</div>
        <div className="text-[10px] text-gray-400">{prof.num_ratings} ratings</div>
      </div>
      <div className="flex items-center gap-1.5">
        <span className="text-xs font-bold" style={{ color: "var(--cp-green)" }}>
          {prof.overall_score.toFixed(2)}<span className="text-[10px] font-normal text-gray-400">/4</span>
        </span>
        <a href={prof.polyratings_url} target="_blank" rel="noopener noreferrer"
           className="text-[10px] text-blue-500 hover:underline">↗</a>
      </div>
    </div>
  );
}

// ── Regular course row (non-GE) ───────────────────────────────────────────────

interface CourseRowProps {
  course: Course;
  checked: boolean;
  inProgressMatch: boolean;
  onToggle: () => void;
  onToggleInProgress: () => void;
}

function CourseRow({ course, checked, inProgressMatch, onToggle, onToggleInProgress }: CourseRowProps) {
  const [expanded, setExpanded]     = useState(false);
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [loading, setLoading]       = useState(false);

  function toggleProfs(e: React.MouseEvent) {
    e.stopPropagation();
    if (expanded) { setExpanded(false); return; }
    setExpanded(true);
    if (professors.length > 0) return;
    setLoading(true);
    getProfessors(course.course_number).then(setProfessors).finally(() => setLoading(false));
  }

  return (
    <div className={`rounded border transition-colors overflow-hidden ${
      checked
        ? "border-green-200 bg-green-50"
        : inProgressMatch
          ? "border-blue-200 bg-blue-50"
          : "border-gray-200 bg-white hover:bg-gray-50"
    }`}>
      <div className="flex items-start gap-3 px-3 py-3">
        <div className="flex shrink-0 flex-col gap-2">
          <label className="flex items-center gap-1.5 text-[11px] font-semibold text-gray-600">
            <input
              type="checkbox"
              checked={checked}
              onChange={onToggle}
              className="h-4 w-4 accent-green-700"
              aria-label={checked ? `Mark ${course.course_number} incomplete` : `Mark ${course.course_number} completed`}
            />
            Done
          </label>
          <label className="flex items-center gap-1.5 text-[11px] font-semibold text-amber-700">
            <input
              type="checkbox"
              checked={inProgressMatch && !checked}
              onChange={onToggleInProgress}
              className="h-4 w-4 accent-amber-600"
              aria-label={inProgressMatch ? `Remove ${course.course_number} from in progress` : `Mark ${course.course_number} in progress`}
            />
            IP
          </label>
        </div>
        <span className="min-w-0 flex-1">
          <span className="flex flex-wrap items-center gap-1.5">
            <span className="text-sm font-bold text-gray-800">{course.course_number}</span>
            {inProgressMatch && !checked && (
              <span className="rounded bg-amber-50 px-1.5 py-0.5 text-[10px] font-bold text-amber-700">IP</span>
            )}
            <span className="rounded bg-gray-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-gray-500">
              {CATEGORY_LABELS[course.category] ?? course.category}
            </span>
          </span>
          <span className="mt-0.5 block text-xs leading-snug text-gray-500">{course.title}</span>
          {course.quarter_equivalents.length > 0 && (
            <span className="mt-1 block text-[11px] text-gray-400">
              Also matches {course.quarter_equivalents.join(", ")}
            </span>
          )}
        </span>
        <button
          onClick={toggleProfs}
          className="mt-0.5 shrink-0 rounded border border-gray-200 px-1.5 py-0.5 text-[10px] text-gray-400 transition-colors hover:border-gray-300 hover:text-gray-600"
          title="Show professors"
        >
          {expanded ? "▲" : "▼"}
        </button>
      </div>

      {expanded && (
        <div className="border-t border-gray-100 bg-gray-50/60 px-3 pb-2 pt-1">
          {loading && <div className="py-2 text-xs text-gray-400">Loading professors…</div>}
          {!loading && professors.length === 0 && (
            <div className="py-2 text-xs text-gray-400">No professor data available yet.</div>
          )}
          {professors.map((p) => <ProfessorRow key={p.name} prof={p} />)}
        </div>
      )}
    </div>
  );
}

// ── GE area row ───────────────────────────────────────────────────────────────

interface GERowProps {
  course: Course;
  checked: boolean;
  inProgressMatch: boolean;
  plannedCourse: string | undefined;
  onToggle: () => void;
  onToggleInProgress: () => void;
}

function GEAreaRow({ course, checked, inProgressMatch, plannedCourse, onToggle, onToggleInProgress }: GERowProps) {
  return (
    <div className={`flex items-start gap-3 rounded border px-3 py-3 transition-colors ${
      checked
        ? "border-green-200 bg-green-50"
        : inProgressMatch || plannedCourse
          ? "border-blue-200 bg-blue-50"
          : "border-gray-200 bg-white hover:bg-gray-50"
    }`}>
      <div className="flex shrink-0 flex-col gap-2">
        <label className="flex items-center gap-1.5 text-[11px] font-semibold text-gray-600">
          <input
            type="checkbox"
            checked={checked}
            onChange={onToggle}
            className="h-4 w-4 accent-green-700"
            aria-label={checked ? `Mark ${course.course_number} incomplete` : `Mark ${course.course_number} completed`}
          />
          Done
        </label>
        <label className="flex items-center gap-1.5 text-[11px] font-semibold text-amber-700">
          <input
            type="checkbox"
            checked={inProgressMatch && !checked}
            onChange={onToggleInProgress}
            className="h-4 w-4 accent-amber-600"
            aria-label={inProgressMatch ? `Remove ${course.course_number} from in progress` : `Mark ${course.course_number} in progress`}
          />
          IP
        </label>
      </div>
      <span className="min-w-0 flex-1">
        <span className="flex flex-wrap items-center gap-1.5">
          <span className="text-sm font-bold text-gray-800">{course.course_number}</span>
          {inProgressMatch && !checked && (
            <span className="rounded bg-amber-50 px-1.5 py-0.5 text-[10px] font-bold text-amber-700">IP</span>
          )}
          {plannedCourse && !checked && (
            <span className="rounded bg-blue-100 px-1.5 py-0.5 text-[10px] font-bold text-blue-800">Planned</span>
          )}
          <span className="rounded bg-gray-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-gray-500">GE</span>
        </span>
        <span className="mt-0.5 block text-xs leading-snug text-gray-500">{course.title}</span>
        {plannedCourse && (
          <span className="mt-1 block text-[11px] text-blue-700">Planned: {plannedCourse}</span>
        )}
        {course.quarter_equivalents.length > 0 && (
          <span className="mt-1 block text-[11px] text-gray-400">
            Also matches {course.quarter_equivalents.join(", ")}
          </span>
        )}
      </span>
    </div>
  );
}

// ── Main panel ────────────────────────────────────────────────────────────────

export default function ManualCourseChecklist({
  open,
  courses,
  completed,
  inProgress,
  geAreaMap,
  plannedGECourses,
  onToggleCourse,
  onToggleCourseInProgress,
  onToggleGEArea,
  onToggleGEAreaInProgress,
  onImportCSV,
  onClose,
}: Props) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [showImport, setShowImport] = useState(false);
  const [csvFeedback, setCsvFeedback] = useState<{ type: "success" | "error"; msg: string } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  function handleCSVFile(file: File) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target?.result as string;
      const result = parseCalPolyCSV(text);
      if (!result) {
        setCsvFeedback({ type: "error", msg: "Couldn't parse this file. Make sure it's a Cal Poly course list CSV." });
        return;
      }
      onImportCSV(result.completed, result.inProgress);
      setCsvFeedback({ type: "success", msg: `Imported ${result.completed.length} completed and ${result.inProgress.length} in-progress courses.` });
    };
    reader.readAsText(file);
  }

  const completedSet = useMemo(() => toNormalizedSet(completed), [completed]);
  const inProgressSet = useMemo(() => toNormalizedSet(inProgress), [inProgress]);

  const gePlaceholders = useMemo(
    () => courses.filter((course) => course.is_placeholder && course.category === "ge"),
    [courses],
  );

  const selectableCourses = useMemo(
    () => courses.filter((course) => !course.is_placeholder),
    [courses],
  );

  const availableCategories = useMemo(
    () => {
      const categories = Array.from(new Set(selectableCourses.map((course) => course.category)));
      if (gePlaceholders.length > 0 && !categories.includes("ge")) categories.push("ge");
      return ["all", ...categories];
    },
    [gePlaceholders.length, selectableCourses],
  );

  const visibleCourses = useMemo(() => {
    const q = query.trim();
    return selectableCourses.filter((course) => {
      if (category !== "all" && course.category !== category) return false;
      if (q && !matchesCourse(course, q)) return false;
      return true;
    });
  }, [selectableCourses, category, query]);

  const visibleGEAreas = useMemo(() => {
    const q = query.trim();
    return gePlaceholders.filter((course) => {
      if (category !== "all" && category !== "ge") return false;
      if (q && !matchesCourse(course, q)) return false;
      return true;
    });
  }, [gePlaceholders, category, query]);

  const { completedCount, geCompletedCount, inProgressCount, geInProgressCount, totalTracked } =
    useMemo(() => ({
      completedCount: selectableCourses.filter((c) => courseIsCompleted(c, completedSet)).length,
      geCompletedCount: gePlaceholders.filter((c) => geAreaIsKnown(c, geAreaMap, completedSet)).length,
      inProgressCount: selectableCourses.filter(
        (c) => !courseIsCompleted(c, completedSet) && courseIsInProgress(c, inProgressSet)
      ).length,
      geInProgressCount: gePlaceholders.filter(
        (c) => !geAreaIsKnown(c, geAreaMap, completedSet) && geAreaIsKnown(c, geAreaMap, inProgressSet)
      ).length,
      totalTracked: selectableCourses.length + gePlaceholders.length,
    }), [selectableCourses, gePlaceholders, completedSet, inProgressSet, geAreaMap]);

  if (!open) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/20 z-40 transition-opacity" onClick={onClose} />

      <div className="fixed left-1/2 top-1/2 z-50 flex max-h-[82vh] w-[min(720px,calc(100vw-2rem))] -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-lg border border-gray-200 bg-white shadow-2xl">
        <div className="flex items-start justify-between gap-4 border-b border-gray-100 px-5 py-4">
          <div>
            <div className="text-base font-bold" style={{ color: "var(--cp-green)" }}>
              Manual Course Checklist
            </div>
            <div className="mt-0.5 text-xs text-gray-500">
              {completedCount + geCompletedCount} completed · {inProgressCount + geInProgressCount} in progress · {totalTracked} tracked
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => { setShowImport((v) => !v); setCsvFeedback(null); }}
              className="rounded border border-gray-200 px-2.5 py-1 text-xs font-medium text-gray-600 hover:bg-gray-50"
            >
              Import CSV
            </button>
            <button
              onClick={onClose}
              className="text-2xl leading-none text-gray-400 hover:text-gray-700"
              aria-label="Close checklist"
            >
              ×
            </button>
          </div>
        </div>

        {showImport && (
          <div className="border-b border-gray-100 bg-gray-50 px-5 py-4">
            <div className="mb-2 text-xs font-semibold text-gray-700">How to get your CSV</div>
            <ol className="mb-3 ml-4 list-decimal space-y-1 text-xs text-gray-600">
              <li>Log in at <strong>my.calpoly.edu</strong></li>
              <li>Go to <strong>Student Center</strong></li>
              <li>Click <strong>Academics</strong> → <strong>Course History</strong></li>
              <li>Click <strong>Download</strong> or <strong>Export as CSV</strong></li>
            </ol>
            <label className="flex cursor-pointer items-center gap-2 rounded border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 w-fit">
              <span>Choose CSV file</span>
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                className="hidden"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleCSVFile(file);
                  e.target.value = "";
                }}
              />
            </label>
            {csvFeedback && (
              <div className={`mt-2 text-xs font-medium ${csvFeedback.type === "success" ? "text-green-700" : "text-red-600"}`}>
                {csvFeedback.msg}
              </div>
            )}
          </div>
        )}

        <div className="border-b border-gray-100 px-5 py-3">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search course number, title, GE area, or quarter equivalent"
              className="min-w-0 flex-1 rounded border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-700"
            />
            <div className="flex flex-wrap gap-1">
              {availableCategories.map((item) => (
                <button
                  key={item}
                  onClick={() => setCategory(item)}
                  className={`rounded border px-2.5 py-1.5 text-xs font-semibold transition-colors ${
                    category === item
                      ? "border-green-800 bg-green-50 text-green-900"
                      : "border-gray-200 text-gray-500 hover:bg-gray-50"
                  }`}
                >
                  {CATEGORY_LABELS[item]}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="overflow-y-auto px-5 py-3">
          {visibleCourses.length === 0 && visibleGEAreas.length === 0 && (
            <div className="py-10 text-center text-sm text-gray-400">No matching courses.</div>
          )}

          <div className="grid gap-2 sm:grid-cols-2">
            {visibleCourses.map((course) => (
              <CourseRow
                key={course.id}
                course={course}
                checked={courseIsCompleted(course, completedSet)}
                inProgressMatch={courseIsInProgress(course, inProgressSet)}
                onToggle={() => onToggleCourse(course)}
                onToggleInProgress={() => onToggleCourseInProgress(course)}
              />
            ))}

            {visibleGEAreas.map((course) => (
              <GEAreaRow
                key={course.id}
                course={course}
                checked={geAreaIsKnown(course, geAreaMap, completedSet)}
                inProgressMatch={geAreaIsKnown(course, geAreaMap, inProgressSet)}
                plannedCourse={plannedGECourses[course.course_number]}
                onToggle={() => onToggleGEArea(course)}
                onToggleInProgress={() => onToggleGEAreaInProgress(course)}
              />
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
