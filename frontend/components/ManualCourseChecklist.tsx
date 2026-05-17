"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { Course, GEAreaMap, Professor, GECourse } from "@/lib/types";
import { getProfessors, getGECourses, getElectiveCourses } from "@/lib/api";
import {
  toNormalizedSet,
  matchesCourse,
  courseIsCompleted,
  courseIsInProgress,
  geAreaIsKnown,
} from "@/lib/checklist-utils";

// ── Types ─────────────────────────────────────────────────────────────────────

type PopoverTrigger =
  | { type: "professors"; courseNumber: string; rect: DOMRect }
  | { type: "picker"; course: Course; rect: DOMRect };

type ChecklistRow =
  | { type: "course"; course: Course }
  | { type: "ge"; course: Course }
  | { type: "elective"; course: Course };

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
  onTogglePickedCourse: (courseNumber: string) => void;
  onTogglePickedCourseInProgress: (courseNumber: string) => void;
  onImportCSV: (completed: string[], inProgress: string[]) => void;
  onClose: () => void;
}

// ── CSV helpers ───────────────────────────────────────────────────────────────

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

const CATEGORY_ORDER = ["major", "support", "ge", "concentration"] as const;
const CATEGORY_RANK = new Map(CATEGORY_ORDER.map((item, index) => [item, index]));

function norm(s: string) { return s.toUpperCase().trim().replace(/\s+/g, " "); }

function categoryRank(category: string) {
  return CATEGORY_RANK.get(category as (typeof CATEGORY_ORDER)[number]) ?? CATEGORY_ORDER.length;
}

function compareCoursePosition(a: Course, b: Course) {
  return categoryRank(a.category) - categoryRank(b.category)
    || a.grid_col - b.grid_col
    || a.grid_row - b.grid_row
    || a.course_number.localeCompare(b.course_number);
}

// ── ProfessorRow ──────────────────────────────────────────────────────────────

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

// ── FloatingPopover ───────────────────────────────────────────────────────────

interface FloatingPopoverProps {
  trigger: PopoverTrigger;
  completedSet: Set<string>;
  inProgressSet: Set<string>;
  onTogglePicked: (cn: string) => void;
  onTogglePickedInProgress: (cn: string) => void;
  onClose: () => void;
}

function FloatingPopover({
  trigger,
  completedSet,
  inProgressSet,
  onTogglePicked,
  onTogglePickedInProgress,
  onClose,
}: FloatingPopoverProps) {
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [pickerCourses, setPickerCourses] = useState<GECourse[]>([]);
  const [pickerTitle, setPickerTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [courseDetail, setCourseDetail] = useState<string | null>(null);
  const [detailProfs, setDetailProfs] = useState<Professor[]>([]);
  const [detailLoading, setDetailLoading] = useState(false);
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setProfessors([]);
    setPickerCourses([]);
    setCourseDetail(null);

    if (trigger.type === "professors") {
      getProfessors(trigger.courseNumber)
        .then((p) => { if (!cancelled) setProfessors(p); })
        .finally(() => { if (!cancelled) setLoading(false); });
    } else {
      const { course } = trigger;
      const req = course.category === "ge"
        ? getGECourses(course.course_number)
        : getElectiveCourses(course.elective_key!);
      req
        .then((area) => {
          if (!cancelled && area) {
            setPickerCourses(area.courses);
            setPickerTitle(area.title);
          }
        })
        .finally(() => { if (!cancelled) setLoading(false); });
    }
    return () => { cancelled = true; };
  }, [trigger]);

  useEffect(() => {
    if (!courseDetail) return;
    let cancelled = false;
    setDetailLoading(true);
    setDetailProfs([]);
    getProfessors(courseDetail)
      .then((p) => { if (!cancelled) setDetailProfs(p); })
      .finally(() => { if (!cancelled) setDetailLoading(false); });
    return () => { cancelled = true; };
  }, [courseDetail]);

  // Close on outside click
  useEffect(() => {
    function handleMouseDown(e: MouseEvent) {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) {
        onClose();
      }
    }
    document.addEventListener("mousedown", handleMouseDown);
    return () => document.removeEventListener("mousedown", handleMouseDown);
  }, [onClose]);

  // Position the panel to the right of anchor, flip left if it would overflow
  const PANEL_W = trigger.type === "professors" ? 260 : 300;
  const PANEL_MAX_H = trigger.type === "professors" ? 280 : 380;
  const { rect } = trigger;
  const vw = typeof window !== "undefined" ? window.innerWidth : 1200;
  const vh = typeof window !== "undefined" ? window.innerHeight : 900;

  let left = rect.right + 10;
  if (left + PANEL_W > vw - 8) left = rect.left - PANEL_W - 10;
  left = Math.max(8, left);

  let top = rect.top;
  if (top + PANEL_MAX_H > vh - 8) top = vh - PANEL_MAX_H - 8;
  top = Math.max(8, top);

  const showingDetail = trigger.type === "picker" && courseDetail !== null;

  return (
    <div
      ref={panelRef}
      className="fixed z-[60] flex flex-col rounded-lg border border-gray-200 bg-white shadow-2xl overflow-hidden"
      style={{ left, top, width: PANEL_W, maxHeight: PANEL_MAX_H }}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-100 px-3 py-2 bg-gray-50 flex-shrink-0">
        {showingDetail ? (
          <>
            <button
              onClick={() => setCourseDetail(null)}
              className="text-[10px] text-blue-500 hover:text-blue-700 font-medium mr-1 flex-shrink-0"
            >
              ← Back
            </button>
            <span className="text-xs font-semibold text-gray-700 truncate flex-1">
              {courseDetail} — Professors
            </span>
          </>
        ) : (
          <>
            <span className="text-xs font-semibold text-gray-700 truncate flex-1">
              {trigger.type === "professors"
                ? `${trigger.courseNumber} — Professors`
                : pickerTitle || "Course Options"}
            </span>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-700 text-sm leading-none ml-2 flex-shrink-0">×</button>
          </>
        )}
      </div>

      {/* Body */}
      <div className="overflow-y-auto px-3 py-2 flex-1">
        {/* Detail: professor list for a specific picker course */}
        {showingDetail && (
          detailLoading
            ? <div className="py-3 text-xs text-gray-400 text-center">Loading…</div>
            : detailProfs.length === 0
              ? <div className="py-3 text-xs text-gray-400 text-center">No professor data available yet.</div>
              : detailProfs.map((p) => <ProfessorRow key={p.name} prof={p} />)
        )}

        {/* Top-level professor list (trigger.type === "professors") */}
        {!showingDetail && loading && <div className="py-3 text-xs text-gray-400 text-center">Loading…</div>}

        {!showingDetail && trigger.type === "professors" && !loading && (
          professors.length === 0
            ? <div className="py-3 text-xs text-gray-400 text-center">No professor data available yet.</div>
            : professors.map((p) => <ProfessorRow key={p.name} prof={p} />)
        )}

        {/* Course picker list */}
        {!showingDetail && trigger.type === "picker" && !loading && (
          pickerCourses.length === 0
            ? <div className="py-3 text-xs text-gray-400 text-center">No courses available yet.</div>
            : pickerCourses.map((c) => {
                const done = completedSet.has(norm(c.course_number));
                const ip   = inProgressSet.has(norm(c.course_number)) && !done;
                return (
                  <div
                    key={c.course_number}
                    className={`flex items-center gap-2 py-1.5 border-b border-gray-100 last:border-0 ${
                      done ? "opacity-60" : ""
                    }`}
                  >
                    <div className="flex flex-col gap-1 flex-shrink-0">
                      <label className="flex items-center gap-1 text-[10px] font-semibold text-gray-600 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={done}
                          onChange={() => onTogglePicked(c.course_number)}
                          className="h-3 w-3 accent-green-700"
                        />
                        Done
                      </label>
                      <label className="flex items-center gap-1 text-[10px] font-semibold text-amber-700 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={ip}
                          onChange={() => onTogglePickedInProgress(c.course_number)}
                          className="h-3 w-3 accent-amber-600"
                        />
                        IP
                      </label>
                    </div>
                    <div className="min-w-0 flex-1">
                      <button
                        onClick={() => setCourseDetail(c.course_number)}
                        className={`text-xs font-semibold leading-tight text-left hover:underline ${done ? "line-through text-green-800" : "text-blue-700"}`}
                      >
                        {c.course_number}
                      </button>
                      <div className="text-[10px] text-gray-500 leading-tight line-clamp-2">{c.title}</div>
                    </div>
                    <span className="text-[10px] text-gray-400 flex-shrink-0">{c.units}u</span>
                  </div>
                );
              })
        )}
      </div>
    </div>
  );
}

// ── CourseRow ─────────────────────────────────────────────────────────────────

interface CourseRowProps {
  course: Course;
  checked: boolean;
  inProgressMatch: boolean;
  onToggle: () => void;
  onToggleInProgress: () => void;
  onOpenPopover: (t: PopoverTrigger) => void;
}

function CourseRow({
  course,
  checked,
  inProgressMatch,
  onToggle,
  onToggleInProgress,
  onOpenPopover,
}: CourseRowProps) {
  const btnRef = useRef<HTMLButtonElement>(null);

  return (
    <div className={`rounded border transition-colors ${
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
          ref={btnRef}
          onClick={(e) => {
            e.stopPropagation();
            const rect = btnRef.current?.getBoundingClientRect();
            if (rect) onOpenPopover({ type: "professors", courseNumber: course.course_number, rect });
          }}
          className="mt-0.5 shrink-0 rounded border border-gray-200 px-1.5 py-0.5 text-[10px] text-gray-400 transition-colors hover:border-gray-300 hover:text-gray-600"
          title="Show professors"
        >
          ▼
        </button>
      </div>
    </div>
  );
}

// ── GEAreaRow ─────────────────────────────────────────────────────────────────

interface GERowProps {
  course: Course;
  checked: boolean;
  inProgressMatch: boolean;
  plannedCourse: string | undefined;
  onToggle: () => void;
  onToggleInProgress: () => void;
  onOpenPicker: (t: PopoverTrigger) => void;
}

function GEAreaRow({
  course,
  checked,
  inProgressMatch,
  plannedCourse,
  onToggle,
  onToggleInProgress,
  onOpenPicker,
}: GERowProps) {
  const rowRef = useRef<HTMLDivElement>(null);

  return (
    <div
      ref={rowRef}
      className={`flex items-start gap-3 rounded border px-3 py-3 transition-colors ${
        checked
          ? "border-green-200 bg-green-50"
          : inProgressMatch || plannedCourse
            ? "border-blue-200 bg-blue-50"
            : "border-gray-200 bg-white hover:bg-gray-50"
      }`}
    >
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
      <button
        onClick={(e) => {
          e.stopPropagation();
          const rect = rowRef.current?.getBoundingClientRect();
          if (rect) onOpenPicker({ type: "picker", course, rect });
        }}
        className="mt-0.5 shrink-0 rounded border border-gray-200 px-1.5 py-0.5 text-[10px] text-gray-400 transition-colors hover:border-blue-300 hover:text-blue-600"
        title="Browse courses for this GE area"
      >
        ▶
      </button>
    </div>
  );
}

// ── ElectivePlaceholderRow ────────────────────────────────────────────────────

interface ElectiveRowProps {
  course: Course;
  checked: boolean;
  inProgressMatch: boolean;
  onToggle: () => void;
  onToggleInProgress: () => void;
  onOpenPicker: (t: PopoverTrigger) => void;
}

function ElectivePlaceholderRow({
  course,
  checked,
  inProgressMatch,
  onToggle,
  onToggleInProgress,
  onOpenPicker,
}: ElectiveRowProps) {
  const rowRef = useRef<HTMLDivElement>(null);

  return (
    <div
      ref={rowRef}
      className={`flex items-start gap-3 rounded border px-3 py-3 transition-colors ${
        checked
          ? "border-green-200 bg-green-50"
          : inProgressMatch
            ? "border-blue-200 bg-blue-50"
            : "border-gray-200 bg-white hover:bg-gray-50"
      }`}
    >
      <div className="flex shrink-0 flex-col gap-2">
        <label className="flex items-center gap-1.5 text-[11px] font-semibold text-gray-600">
          <input
            type="checkbox"
            checked={checked}
            onChange={onToggle}
            className="h-4 w-4 accent-green-700"
            aria-label={checked ? `Mark ${course.title} incomplete` : `Mark ${course.title} completed`}
          />
          Done
        </label>
        <label className="flex items-center gap-1.5 text-[11px] font-semibold text-amber-700">
          <input
            type="checkbox"
            checked={inProgressMatch && !checked}
            onChange={onToggleInProgress}
            className="h-4 w-4 accent-amber-600"
            aria-label={inProgressMatch ? `Remove ${course.title} from in progress` : `Mark ${course.title} in progress`}
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
      </span>
      {course.elective_key && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            const rect = rowRef.current?.getBoundingClientRect();
            if (rect) onOpenPicker({ type: "picker", course, rect });
          }}
          className="mt-0.5 shrink-0 rounded border border-gray-200 px-1.5 py-0.5 text-[10px] text-gray-400 transition-colors hover:border-blue-300 hover:text-blue-600"
          title="Browse courses for this elective"
        >
          ▶
        </button>
      )}
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
  onTogglePickedCourse,
  onTogglePickedCourseInProgress,
  onImportCSV,
  onClose,
}: Props) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [showImport, setShowImport] = useState(false);
  const [csvFeedback, setCsvFeedback] = useState<{ type: "success" | "error"; msg: string } | null>(null);
  const [popover, setPopover] = useState<PopoverTrigger | null>(null);
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

  const completedSet  = useMemo(() => toNormalizedSet(completed),  [completed]);
  const inProgressSet = useMemo(() => toNormalizedSet(inProgress), [inProgress]);

  const gePlaceholders = useMemo(
    () => courses.filter((c) => c.is_placeholder && c.category === "ge"),
    [courses],
  );

  const electivePlaceholders = useMemo(
    () => courses.filter((c) => c.is_placeholder && c.category !== "ge" && c.category !== "concentration"),
    [courses],
  );

  const selectableCourses = useMemo(
    () => courses.filter((c) => !c.is_placeholder),
    [courses],
  );

  const availableCategories = useMemo(() => {
    const cats = Array.from(new Set(selectableCourses.map((c) => c.category)));
    if (gePlaceholders.length > 0 && !cats.includes("ge")) cats.push("ge");
    return ["all", ...cats.sort((a, b) => categoryRank(a) - categoryRank(b) || a.localeCompare(b))];
  }, [gePlaceholders.length, selectableCourses]);

  const visibleCourses = useMemo(() => {
    const q = query.trim();
    return selectableCourses.filter((c) => {
      if (category !== "all" && c.category !== category) return false;
      if (q && !matchesCourse(c, q)) return false;
      return true;
    });
  }, [selectableCourses, category, query]);

  const visibleGEAreas = useMemo(() => {
    const q = query.trim();
    return gePlaceholders.filter((c) => {
      if (category !== "all" && category !== "ge") return false;
      if (q && !matchesCourse(c, q)) return false;
      return true;
    });
  }, [gePlaceholders, category, query]);

  const visibleElectives = useMemo(() => {
    const q = query.trim();
    return electivePlaceholders.filter((c) => {
      if (category !== "all" && c.category !== category) return false;
      if (q && !matchesCourse(c, q)) return false;
      return true;
    });
  }, [electivePlaceholders, category, query]);

  const checklistRows = useMemo<ChecklistRow[]>(() => {
    return [
      ...visibleCourses.map((course): ChecklistRow => ({ type: "course", course })),
      ...visibleGEAreas.map((course): ChecklistRow => ({ type: "ge", course })),
      ...visibleElectives.map((course): ChecklistRow => ({ type: "elective", course })),
    ].sort((a, b) => compareCoursePosition(a.course, b.course));
  }, [visibleCourses, visibleGEAreas, visibleElectives]);

  const { completedCount, geCompletedCount, elecCompletedCount, inProgressCount, geInProgressCount, elecInProgressCount, totalTracked } =
    useMemo(() => ({
      completedCount:     selectableCourses.filter((c) => courseIsCompleted(c, completedSet)).length,
      geCompletedCount:   gePlaceholders.filter((c) => geAreaIsKnown(c, geAreaMap, completedSet)).length,
      elecCompletedCount: electivePlaceholders.filter((c) => courseIsCompleted(c, completedSet)).length,
      inProgressCount:    selectableCourses.filter((c) => !courseIsCompleted(c, completedSet) && courseIsInProgress(c, inProgressSet)).length,
      geInProgressCount:  gePlaceholders.filter((c) => !geAreaIsKnown(c, geAreaMap, completedSet) && geAreaIsKnown(c, geAreaMap, inProgressSet)).length,
      elecInProgressCount: electivePlaceholders.filter((c) => !courseIsCompleted(c, completedSet) && courseIsInProgress(c, inProgressSet)).length,
      totalTracked:       selectableCourses.length + gePlaceholders.length + electivePlaceholders.length,
    }), [selectableCourses, gePlaceholders, electivePlaceholders, completedSet, inProgressSet, geAreaMap]);

  if (!open) return null;

  const allCompleted  = completedCount + geCompletedCount + elecCompletedCount;
  const allInProgress = inProgressCount + geInProgressCount + elecInProgressCount;

  return (
    <>
      <div className="fixed inset-0 bg-black/20 z-40 transition-opacity" onClick={() => { onClose(); setPopover(null); }} />

      <div className="fixed left-1/2 top-1/2 z-50 flex max-h-[82vh] w-[min(720px,calc(100vw-2rem))] -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-lg border border-gray-200 bg-white shadow-2xl">
        <div className="flex items-start justify-between gap-4 border-b border-gray-100 px-5 py-4">
          <div>
            <div className="text-base font-bold" style={{ color: "var(--cp-green)" }}>
              Manual Course Checklist
            </div>
            <div className="mt-0.5 text-xs text-gray-500">
              {allCompleted} completed · {allInProgress} in progress · {totalTracked} tracked
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
              onClick={() => { onClose(); setPopover(null); }}
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
              onChange={(e) => setQuery(e.target.value)}
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
          {checklistRows.length === 0 && (
            <div className="py-10 text-center text-sm text-gray-400">No matching courses.</div>
          )}

          <div className="grid gap-2 sm:grid-cols-2">
            {checklistRows.map(({ type, course }) => {
              if (type === "ge") {
                return (
                  <GEAreaRow
                    key={course.id}
                    course={course}
                    checked={geAreaIsKnown(course, geAreaMap, completedSet)}
                    inProgressMatch={geAreaIsKnown(course, geAreaMap, inProgressSet)}
                    plannedCourse={plannedGECourses[course.course_number]}
                    onToggle={() => onToggleGEArea(course)}
                    onToggleInProgress={() => onToggleGEAreaInProgress(course)}
                    onOpenPicker={setPopover}
                  />
                );
              }

              if (type === "elective") {
                return (
                  <ElectivePlaceholderRow
                    key={course.id}
                    course={course}
                    checked={courseIsCompleted(course, completedSet)}
                    inProgressMatch={courseIsInProgress(course, inProgressSet)}
                    onToggle={() => onToggleGEArea(course)}
                    onToggleInProgress={() => onToggleGEAreaInProgress(course)}
                    onOpenPicker={setPopover}
                  />
                );
              }

              return (
                <CourseRow
                  key={course.id}
                  course={course}
                  checked={courseIsCompleted(course, completedSet)}
                  inProgressMatch={courseIsInProgress(course, inProgressSet)}
                  onToggle={() => onToggleCourse(course)}
                  onToggleInProgress={() => onToggleCourseInProgress(course)}
                  onOpenPopover={setPopover}
                />
              );
            })}
          </div>
        </div>
      </div>

      {popover && (
        <FloatingPopover
          trigger={popover}
          completedSet={completedSet}
          inProgressSet={inProgressSet}
          onTogglePicked={onTogglePickedCourse}
          onTogglePickedInProgress={onTogglePickedCourseInProgress}
          onClose={() => setPopover(null)}
        />
      )}
    </>
  );
}
