"use client";

import { useState } from "react";
import type { Course, CourseStatus, Flowchart, GEAreaMap, TranscriptSession } from "@/lib/types";
import CourseCard from "./CourseCard";

interface Props {
  flowchart: Flowchart;
  session: TranscriptSession;
  inferred: string[];
  geAreaMap: GEAreaMap;
  onCourseClick: (course: Course, status: CourseStatus) => void;
  onToggleCourseCompleted: (course: Course) => void;
  onMoveCourse: (
    courseId: string,
    targetCol: number,
    targetRow: number,
    targetCourseId?: string,
  ) => void;
}

function norm(courseNumber: string) {
  return courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
}

function hasAnyCourseNumber(knownNums: Set<string>, courseNums: string[]) {
  const normalizedKnown = new Set(Array.from(knownNums, norm));
  return courseNums.some((num) => normalizedKnown.has(norm(num)));
}

function getCourseStatus(
  course: Course,
  completedNums: Set<string>,
  inProgressNums: Set<string>,
  inferredNums: Set<string>,
  allCourses: Course[],
  geAreaMap: GEAreaMap,
): CourseStatus {
  // GE placeholder: check if any approved course for this area is completed/in-progress
  if (course.is_placeholder && course.category === "ge") {
    const approved = [
      course.course_number,
      ...course.quarter_equivalents,
      ...(geAreaMap[course.course_number] ?? []),
    ];
    if (hasAnyCourseNumber(completedNums, approved)) return "completed";
    if (hasAnyCourseNumber(inProgressNums, approved)) return "in_progress";
    return "incomplete";
  }
  if (course.is_placeholder) {
    const allNums = [course.course_number, ...course.quarter_equivalents];
    if (allNums.some((n) => completedNums.has(n))) return "completed";
    if (allNums.some((n) => inferredNums.has(n))) return "inferred";
    if (allNums.some((n) => inProgressNums.has(n))) return "in_progress";
    return "incomplete";
  }

  const allNums = [course.course_number, ...course.quarter_equivalents];

  if (allNums.some((n) => completedNums.has(n))) return "completed";
  if (allNums.some((n) => inferredNums.has(n)))  return "inferred";
  if (allNums.some((n) => inProgressNums.has(n))) return "in_progress";

  // Locked if any prerequisite is neither completed nor inferred
  const knownNums = new Set([...completedNums, ...inferredNums, ...inProgressNums]);
  const prereqsMet = course.prerequisites.every((prereqNum) => {
    const prereq = allCourses.find((c) => c.course_number === prereqNum);
    if (!prereq) return true;
    const prereqNums = [prereq.course_number, ...prereq.quarter_equivalents];
    return hasAnyCourseNumber(knownNums, prereqNums);
  });

  return prereqsMet ? "incomplete" : "locked";
}

function buildGrid(courses: Course[], positions: TranscriptSession["coursePositions"] = {}): Map<string, Course> {
  const grid = new Map<string, Course>();
  for (const course of courses) {
    const position = positions[course.id] ?? {
      grid_col: course.grid_col,
      grid_row: course.grid_row,
    };
    grid.set(`${position.grid_col}:${position.grid_row}`, course);
  }
  return grid;
}

function getCoursePosition(course: Course, positions: TranscriptSession["coursePositions"] = {}) {
  return positions[course.id] ?? {
    grid_col: course.grid_col,
    grid_row: course.grid_row,
  };
}

const YEAR_GROUPS = [
  { label: "Freshman",  cols: [0, 1] },
  { label: "Sophomore", cols: [2, 3] },
  { label: "Junior",    cols: [4, 5] },
  { label: "Senior",    cols: [6, 7] },
];

const CATEGORY_LEGEND = [
  { label: "Major",         bg: "#fde68a", border: "#d97706" },
  { label: "Support",       bg: "#fed7aa", border: "#ea580c" },
  { label: "Concentration", bg: "#f9a8d4", border: "#db2777" },
  { label: "Gen Ed",        bg: "#bbf7d0", border: "#16a34a" },
];

export default function FlowchartGrid({
  flowchart,
  session,
  inferred,
  geAreaMap,
  onCourseClick,
  onToggleCourseCompleted,
  onMoveCourse,
}: Props) {
  const completedNums  = new Set(session.completed);
  const inProgressNums = new Set(session.inProgress);
  const inferredNums   = new Set(inferred);
  const positions = session.coursePositions ?? {};
  const grid = buildGrid(flowchart.courses, positions);
  const [draggedCourseId, setDraggedCourseId] = useState<string | null>(null);

  // ── Per-category progress ──────────────────────────────────────────────────
  function isCompletedOrInferred(c: Course) {
    const nums = [c.course_number, ...c.quarter_equivalents];
    return nums.some((n) => completedNums.has(n) || inferredNums.has(n));
  }
  function isDone(c: Course) {
    const nums = [c.course_number, ...c.quarter_equivalents];
    return nums.some((n) => completedNums.has(n));
  }

  const majorCourses   = flowchart.courses.filter((c) => c.category === "major");
  const supportCourses = flowchart.courses.filter((c) => c.category === "support");
  const gePlaceholders = flowchart.courses.filter((c) => c.category === "ge"      && c.is_placeholder);

  // ── Total units ────────────────────────────────────────────────────────────
  const plannedGEUnits = session.plannedGEUnits ?? {};

  function effectiveUnits(course: Course): number {
    if (course.is_placeholder && course.category === "ge") {
      return plannedGEUnits[course.course_number] ?? course.units;
    }
    return course.units;
  }

  let earnedUnits = 0;
  let inProgressUnits = 0;
  for (const course of flowchart.courses) {
    const status = getCourseStatus(course, completedNums, inProgressNums, inferredNums, flowchart.courses, geAreaMap);
    const u = effectiveUnits(course);
    if (status === "completed" || status === "inferred") earnedUnits += u;
    else if (status === "in_progress") inProgressUnits += u;
  }
  const totalUnits = flowchart.total_units;

  // ── Per-column unit totals ─────────────────────────────────────────────────
  const numCols = flowchart.columns.length;
  const recommendedUnitsPerCol = Array<number>(numCols).fill(0);
  const currentUnitsPerCol     = Array<number>(numCols).fill(0);
  for (const course of flowchart.courses) {
    const u = effectiveUnits(course);
    recommendedUnitsPerCol[course.grid_col] += u;
    const pos = getCoursePosition(course, positions);
    currentUnitsPerCol[pos.grid_col] += u;
  }

  const majorDone     = majorCourses.filter(isDone).length;
  const majorInferred = majorCourses.filter((c) => !isDone(c) && isCompletedOrInferred(c)).length;
  const supportDone     = supportCourses.filter(isDone).length;
  const supportInferred = supportCourses.filter((c) => !isDone(c) && isCompletedOrInferred(c)).length;

  const geDone = gePlaceholders.filter((c) => {
    const approved = [
      c.course_number,
      ...c.quarter_equivalents,
      ...(geAreaMap[c.course_number] ?? []),
    ];
    return hasAnyCourseNumber(completedNums, approved);
  }).length;

  const maxRows = Math.max(
    ...flowchart.courses.map((course) => getCoursePosition(course, positions).grid_row + 1),
    1,
  ) + (draggedCourseId ? 1 : 0);

  const handleDrop = (targetCol: number, targetRow: number, targetCourse?: Course) => {
    if (!draggedCourseId || draggedCourseId === targetCourse?.id) return;
    onMoveCourse(draggedCourseId, targetCol, targetRow, targetCourse?.id);
    setDraggedCourseId(null);
  };

  return (
    <div className="flex flex-col gap-4">
      {/* Per-category progress bars */}
      <div className="grid grid-cols-3 gap-3 px-1">
        {/* Major */}
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="font-semibold text-amber-800">Major</span>
            <span className="text-gray-500">{majorDone + majorInferred}/{majorCourses.length}</span>
          </div>
          <div className="bg-gray-200 rounded-full h-2 overflow-hidden flex">
            <div className="h-full transition-all" style={{ width: `${(majorDone / majorCourses.length) * 100}%`, background: "#d97706" }} />
            <div className="h-full transition-all" style={{ width: `${(majorInferred / majorCourses.length) * 100}%`, background: "#fcd34d" }} />
          </div>
        </div>
        {/* Support */}
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="font-semibold text-orange-800">Support</span>
            <span className="text-gray-500">{supportDone + supportInferred}/{supportCourses.length}</span>
          </div>
          <div className="bg-gray-200 rounded-full h-2 overflow-hidden flex">
            <div className="h-full transition-all" style={{ width: `${(supportDone / supportCourses.length) * 100}%`, background: "#ea580c" }} />
            <div className="h-full transition-all" style={{ width: `${(supportInferred / supportCourses.length) * 100}%`, background: "#fdba74" }} />
          </div>
        </div>
        {/* GE */}
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="font-semibold text-green-800">Gen Ed</span>
            <span className="text-gray-500">{geDone}/{gePlaceholders.length}</span>
          </div>
          <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
            <div className="h-full transition-all" style={{ width: `${(geDone / gePlaceholders.length) * 100}%`, background: "#16a34a" }} />
          </div>
        </div>
      </div>

      {/* Total units summary */}
      <div className="flex items-center gap-3 px-1 text-xs text-gray-600 border-t border-gray-100 pt-3 -mt-1">
        <span className="font-semibold text-gray-700">Units:</span>
        <span>
          <span className="font-bold text-green-800">{earnedUnits}</span>
          <span className="text-gray-400"> earned</span>
        </span>
        {inProgressUnits > 0 && (
          <span>
            <span className="font-bold text-blue-700">+{inProgressUnits}</span>
            <span className="text-gray-400"> in progress</span>
          </span>
        )}
        <span className="text-gray-300">·</span>
        <span className="text-gray-500">{totalUnits} total required</span>
        <span className="ml-auto font-semibold" style={{ color: "var(--cp-green)" }}>
          {Math.round((earnedUnits / totalUnits) * 100)}% complete
        </span>
      </div>

      {/* Grid */}
      <div className="overflow-x-auto">
        <div style={{ minWidth: 900 }}>
          {/* Year headers */}
          <div className="grid grid-cols-8 gap-1 mb-1">
            {YEAR_GROUPS.map((yg) => (
              <div key={yg.label} className="col-span-2 text-center text-xs font-bold uppercase tracking-wider py-1 rounded"
                   style={{ background: "var(--cp-green)", color: "white" }}>
                {yg.label}
              </div>
            ))}
          </div>

          {/* Term sub-headers */}
          <div className="grid grid-cols-8 gap-1 mb-2">
            {flowchart.columns.map((col, i) => {
              const rec = recommendedUnitsPerCol[i] ?? 0;
              const cur = currentUnitsPerCol[i] ?? 0;
              return (
                <div key={i} className="text-center text-xs font-semibold rounded overflow-hidden"
                     style={{ background: "#1e6348", color: "white" }}>
                  <div className="py-0.5">{col.term}</div>
                  <div className="border-t border-white/20 px-1 py-0.5 text-[9px] font-normal leading-tight">
                    <span className="opacity-70">rec </span>{rec}u
                    {cur !== rec
                      ? <span className="text-yellow-200"> · {cur}u</span>
                      : <span className="opacity-50"> · {cur}u</span>
                    }
                  </div>
                </div>
              );
            })}
          </div>

          {/* Course rows */}
          {Array.from({ length: maxRows }).map((_, rowIdx) => (
            <div key={rowIdx} className="grid grid-cols-8 gap-1 mb-1">
              {Array.from({ length: 8 }).map((_, colIdx) => {
                const course = grid.get(`${colIdx}:${rowIdx}`);
                if (!course) {
                  return (
                    <div
                      key={colIdx}
                      className={`min-h-[72px] rounded border border-dashed transition-colors ${
                        draggedCourseId ? "border-gray-300 bg-gray-50" : "border-transparent"
                      }`}
                      onDragOver={(event) => event.preventDefault()}
                      onDrop={() => handleDrop(colIdx, rowIdx)}
                    />
                  );
                }
                const status = getCourseStatus(
                  course, completedNums, inProgressNums, inferredNums, flowchart.courses, geAreaMap
                );
                const allNums = [course.course_number, ...course.quarter_equivalents];
                const checked = course.is_placeholder && course.category === "ge"
                  ? hasAnyCourseNumber(completedNums, [
                      course.course_number,
                      ...course.quarter_equivalents,
                      ...(geAreaMap[course.course_number] ?? []),
                    ])
                  : allNums.some((n) => completedNums.has(n));
                const plannedCourseNumber = course.is_placeholder && course.category === "ge"
                  ? session.plannedGECourses?.[course.course_number]
                  : undefined;
                return (
                  <div
                    key={colIdx}
                    draggable
                    className={`rounded ${draggedCourseId === course.id ? "opacity-50" : ""}`}
                    onDragStart={(event) => {
                      setDraggedCourseId(course.id);
                      event.dataTransfer.effectAllowed = "move";
                      event.dataTransfer.setData("text/plain", course.id);
                    }}
                    onDragEnd={() => setDraggedCourseId(null)}
                    onDragOver={(event) => event.preventDefault()}
                    onDrop={() => handleDrop(colIdx, rowIdx, course)}
                  >
                    <CourseCard
                      course={course}
                      status={status}
                      checked={checked}
                      plannedCourseNumber={plannedCourseNumber}
                      onToggleCompleted={() => onToggleCourseCompleted(course)}
                      onClick={() => onCourseClick(course, status)}
                    />
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex gap-4 flex-wrap mt-1 text-xs text-gray-600">
        {CATEGORY_LEGEND.map((item) => (
          <div key={item.label} className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-sm border" style={{ background: item.bg, borderColor: item.border }} />
            {item.label}
          </div>
        ))}
        <div className="flex items-center gap-1.5">
          <span className="font-bold text-green-700">✓</span> Completed
        </div>
        <div className="flex items-center gap-1.5">
          <span className="font-bold" style={{ color: "#16a34a", opacity: 0.6 }}>✓</span> Inferred from prereqs
        </div>
        <div className="flex items-center gap-1.5">
          <span className="font-bold text-blue-600">IP</span> In Progress
        </div>
        <div className="flex items-center gap-1.5">
          <span>🔒</span> Prereqs needed
        </div>
      </div>
    </div>
  );
}
