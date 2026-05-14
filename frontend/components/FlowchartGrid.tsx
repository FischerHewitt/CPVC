"use client";

import type { Course, CourseStatus, Flowchart, TranscriptSession } from "@/lib/types";
import CourseCard from "./CourseCard";

interface Props {
  flowchart: Flowchart;
  session: TranscriptSession;
  inferred: string[];
  onCourseClick: (course: Course, status: CourseStatus) => void;
}

function getCourseStatus(
  course: Course,
  completedNums: Set<string>,
  inProgressNums: Set<string>,
  inferredNums: Set<string>,
  allCourses: Course[],
): CourseStatus {
  if (course.is_placeholder) return "incomplete";

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
    return prereqNums.some((n) => knownNums.has(n));
  });

  return prereqsMet ? "incomplete" : "locked";
}

function buildGrid(courses: Course[]): Map<number, Course[]> {
  const grid = new Map<number, Course[]>();
  for (const course of courses) {
    if (!grid.has(course.grid_col)) grid.set(course.grid_col, []);
    const col = grid.get(course.grid_col)!;
    col[course.grid_row] = course;
  }
  return grid;
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

export default function FlowchartGrid({ flowchart, session, inferred, onCourseClick }: Props) {
  const completedNums  = new Set(session.completed);
  const inProgressNums = new Set(session.inProgress);
  const inferredNums   = new Set(inferred);
  const grid = buildGrid(flowchart.courses);

  const nonPlaceholders = flowchart.courses.filter((c) => !c.is_placeholder);
  const completedCount = nonPlaceholders.filter((c) => {
    const allNums = [c.course_number, ...c.quarter_equivalents];
    return allNums.some((n) => completedNums.has(n));
  }).length;
  const inferredCount = nonPlaceholders.filter((c) => {
    const allNums = [c.course_number, ...c.quarter_equivalents];
    return !allNums.some((n) => completedNums.has(n)) && allNums.some((n) => inferredNums.has(n));
  }).length;
  const totalRequired = nonPlaceholders.length;

  const maxRows = Math.max(...Array.from(grid.values()).map((col) => col.length));

  return (
    <div className="flex flex-col gap-4">
      {/* Progress */}
      <div className="flex items-center gap-3 px-1">
        <div className="flex-1 bg-gray-200 rounded-full h-2 overflow-hidden">
          {/* Inferred layer */}
          <div className="h-full rounded-full flex">
            <div
              className="h-full transition-all"
              style={{ width: `${(completedCount / totalRequired) * 100}%`, background: "var(--cp-green)" }}
            />
            <div
              className="h-full transition-all"
              style={{ width: `${(inferredCount / totalRequired) * 100}%`, background: "#86efac" }}
            />
          </div>
        </div>
        <span className="text-sm font-medium text-gray-600 whitespace-nowrap">
          {completedCount} done · {inferredCount} inferred · {totalRequired} total
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
            {flowchart.columns.map((col, i) => (
              <div key={i} className="text-center text-xs font-semibold py-0.5 rounded"
                   style={{ background: "#1e6348", color: "white" }}>
                {col.term}
              </div>
            ))}
          </div>

          {/* Course rows */}
          {Array.from({ length: maxRows }).map((_, rowIdx) => (
            <div key={rowIdx} className="grid grid-cols-8 gap-1 mb-1">
              {Array.from({ length: 8 }).map((_, colIdx) => {
                const col = grid.get(colIdx) ?? [];
                const course = col[rowIdx];
                if (!course) return <div key={colIdx} />;
                const status = getCourseStatus(
                  course, completedNums, inProgressNums, inferredNums, flowchart.courses
                );
                return (
                  <div key={colIdx}>
                    <CourseCard
                      course={course}
                      status={status}
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
