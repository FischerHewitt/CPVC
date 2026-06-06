"use client";

import { useMemo, useState } from "react";
import type { Course, CourseStatus, CustomCourseEntry, Flowchart, GEAreaMap, TranscriptSession } from "@/lib/types";
import { norm, toNormalizedSet, hasAnyCourseNumber, isFreeElective, getCourseStatus, expandSlashCourseNumber, courseCompletionCandidates } from "@/lib/course-status";
import { gePlaceholderDisplayData, withPlannedGECourses } from "@/lib/ge-placeholder";
import CourseCard, { CATEGORY_STYLES } from "./CourseCard";

interface Props {
  flowchart: Flowchart;
  session: TranscriptSession;
  inferred: string[];
  geAreaMap: GEAreaMap;
  highlightedCourseIds?: Set<string>;
  onCourseClick: (course: Course, status: CourseStatus) => void;
  onToggleCourseCompleted: (course: Course) => void;
  onToggleCourseInProgress: (course: Course) => void;
  onMoveCourse: (
    courseId: string,
    targetCol: number,
    targetRow: number,
    targetCourseId?: string,
  ) => void;
  onAddCourse?: (col: number) => void;
  onClearCustomAssignment?: (customId: string) => void;
  onRemoveCustomCourse?: (customId: string) => void;
  onSetCustomCourseStatus?: (customId: string, status: CustomCourseEntry["status"]) => void;
  onCustomCourseClick?: (customId: string, entry: CustomCourseEntry) => void;
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


const CATEGORY_LEGEND = [
  { label: "Major",         ...CATEGORY_STYLES.major },
  { label: "Support",       ...CATEGORY_STYLES.support },
  { label: "Concentration", ...CATEGORY_STYLES.concentration },
  { label: "Free Elective", ...CATEGORY_STYLES.free },
  { label: "Gen Ed",        ...CATEGORY_STYLES.ge },
];

type ProgressCounts = {
  completed: number;
  inferred: number;
  inProgress: number;
  total: number;
};

function progressWidth(count: number, total: number) {
  return total > 0 ? `${(count / total) * 100}%` : "0%";
}

function ProgressBar({
  label,
  counts,
  colors,
}: {
  label: string;
  counts: ProgressCounts;
  colors: { label: string; completed: string; inferred: string; inProgress: string };
}) {
  const earned = counts.completed + counts.inferred;
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="font-semibold" style={{ color: colors.label }}>{label}</span>
        <span className="flex items-center gap-1.5 text-gray-500">
          <span>{earned}/{counts.total}</span>
          {counts.inProgress > 0 && (
            <span className="font-semibold opacity-80" style={{ color: colors.inProgress }}>+{counts.inProgress} IP</span>
          )}
        </span>
      </div>
      <div className="bg-gray-200 rounded-full h-2 overflow-hidden flex">
        <div className="h-full transition-all" style={{ width: progressWidth(counts.completed, counts.total), background: colors.completed }} />
        <div className="h-full transition-all" style={{ width: progressWidth(counts.inferred, counts.total), background: colors.inferred }} />
        <div className="h-full transition-all" style={{ width: progressWidth(counts.inProgress, counts.total), background: colors.inProgress }} />
      </div>
    </div>
  );
}

export function countCourseProgress(courses: Course[], statuses: Map<string, CourseStatus>): ProgressCounts {
  let completed = 0;
  let inferred = 0;
  let inProgress = 0;
  for (const course of courses) {
    const status = statuses.get(course.id);
    if (status === "completed") completed++;
    else if (status === "inferred") inferred++;
    else if (status === "in_progress") inProgress++;
  }
  return { completed, inferred, inProgress, total: courses.length };
}

export default function FlowchartGrid({
  flowchart,
  session,
  inferred,
  geAreaMap,
  highlightedCourseIds,
  onCourseClick,
  onToggleCourseCompleted,
  onToggleCourseInProgress,
  onMoveCourse,
  onAddCourse,
  onClearCustomAssignment,
  onRemoveCustomCourse,
  onSetCustomCourseStatus,
  onCustomCourseClick,
}: Props) {
  const completedNums  = useMemo(() => toNormalizedSet(session.completed), [session.completed]);
  const inProgressNums = useMemo(() => toNormalizedSet(session.inProgress), [session.inProgress]);
  const inferredNums   = useMemo(() => toNormalizedSet(inferred), [inferred]);
  const knownNums      = useMemo(() => new Set([...completedNums, ...inferredNums, ...inProgressNums]), [completedNums, inferredNums, inProgressNums]);
  const positions = useMemo(() => session.coursePositions ?? {}, [session.coursePositions]);
  const plannedGECourses = useMemo(() => session.plannedGECourses ?? {}, [session.plannedGECourses]);
  const plannedFreeElectiveCourses = useMemo(() => session.plannedFreeElectiveCourses ?? {}, [session.plannedFreeElectiveCourses]);
  const effectiveGEAreaMap = useMemo(() => withPlannedGECourses(geAreaMap, plannedGECourses), [geAreaMap, plannedGECourses]);
  const grid = useMemo(() => buildGrid(flowchart.courses, positions), [flowchart.courses, positions]);
  const courseLookup = useMemo(() => {
    const lookup = new Map<string, Course>();
    for (const course of flowchart.courses) {
      lookup.set(norm(course.course_number), course);
      if (course.course_number.includes("/")) {
        for (const component of expandSlashCourseNumber(course.course_number)) {
          lookup.set(norm(component), course);
        }
      }
    }
    return lookup;
  }, [flowchart.courses]);
  const [draggedCourseId, setDraggedCourseId] = useState<string | null>(null);

  // ── Memoized per-course status (avoids recomputing on every render/drag) ───
  const courseStatuses = useMemo(
    () =>
      new Map(
        flowchart.courses.map((course) => {
          const freeSelection = isFreeElective(course) ? plannedFreeElectiveCourses[course.id] : undefined;
          const status = freeSelection?.status === "completed"
            ? "completed"
            : freeSelection?.status === "in_progress"
              ? "in_progress"
              : getCourseStatus(course, completedNums, inProgressNums, inferredNums, knownNums, courseLookup, effectiveGEAreaMap);
          return [course.id, status];
        })
      ),
    [flowchart.courses, completedNums, inProgressNums, inferredNums, knownNums, courseLookup, effectiveGEAreaMap, plannedFreeElectiveCourses]
  );

  // ── Memoized per-course display data (checked, plannedCourseNumber, etc.) ──
  const courseDisplayData = useMemo(() => {
    const map = new Map<string, {
      checked: boolean;
      inProgressChecked: boolean;
      plannedCourseNumber: string | undefined;
      activeCourseNumber: string | undefined;
    }>();
    for (const course of flowchart.courses) {
      if (course.is_placeholder && course.category === "ge") {
        map.set(course.id, gePlaceholderDisplayData(course, completedNums, inProgressNums, effectiveGEAreaMap, plannedGECourses));
      } else if (course.is_placeholder && isFreeElective(course)) {
        const freeSelection = plannedFreeElectiveCourses[course.id];
        map.set(course.id, {
          checked: freeSelection?.status === "completed",
          inProgressChecked: freeSelection?.status === "in_progress",
          plannedCourseNumber: freeSelection?.status === "planned" ? freeSelection.course_number : undefined,
          activeCourseNumber: freeSelection?.status !== "planned" ? freeSelection?.course_number : undefined,
        });
      } else if (course.is_placeholder && !isFreeElective(course)) {
        const active = course.quarter_equivalents.find((c) => completedNums.has(norm(c)) || inProgressNums.has(norm(c)));
        // Concentration/support elective placeholders are keyed by course.id in plannedGECourses
        // so that multiple tiles sharing the same course_number (e.g. "Conc.") don't collide.
        const plannedForSlot = plannedGECourses[course.id] ?? plannedGECourses[course.course_number];
        map.set(course.id, {
          checked: hasAnyCourseNumber(completedNums, courseCompletionCandidates(course)),
          inProgressChecked: hasAnyCourseNumber(inProgressNums, courseCompletionCandidates(course)),
          plannedCourseNumber: plannedForSlot,
          activeCourseNumber: plannedForSlot ?? active,
        });
      } else {
        map.set(course.id, {
          checked: hasAnyCourseNumber(completedNums, courseCompletionCandidates(course)),
          inProgressChecked: hasAnyCourseNumber(inProgressNums, courseCompletionCandidates(course)),
          plannedCourseNumber: undefined,
          activeCourseNumber: undefined,
        });
      }
    }
    return map;
  }, [flowchart.courses, completedNums, inProgressNums, effectiveGEAreaMap, plannedGECourses, plannedFreeElectiveCourses]);

  const requiredCourses = useMemo(() => flowchart.courses.filter((c) => c.is_required !== false), [flowchart.courses]);
  const majorCourses   = useMemo(() => requiredCourses.filter((c) => c.category === "major"),   [requiredCourses]);
  const supportCourses = useMemo(() => requiredCourses.filter((c) => c.category === "support"), [requiredCourses]);
  const gePlaceholders = useMemo(() => requiredCourses.filter((c) => c.category === "ge" && c.is_placeholder), [requiredCourses]);

  // ── Total units ────────────────────────────────────────────────────────────
  const plannedGEUnits    = useMemo(() => session.plannedGEUnits    ?? {}, [session.plannedGEUnits]);
  const plannedCourseUnits = useMemo(() => session.plannedCourseUnits ?? {}, [session.plannedCourseUnits]);

  function effectiveUnits(course: Course): number {
    if (course.is_required === false) return 0;
    if (course.is_placeholder && isFreeElective(course)) {
      return plannedFreeElectiveCourses[course.id]?.units ?? course.units;
    }
    if (course.is_placeholder && !isFreeElective(course)) {
      // Per-slot unit override (e.g. variable-unit elective choices) takes priority
      return plannedCourseUnits[course.id] ?? plannedGEUnits[course.course_number] ?? course.units;
    }
    return course.units;
  }

  const { earnedUnits, inProgressUnits } = useMemo(() => {
    let earnedUnits = 0;
    let inProgressUnits = 0;
    for (const course of flowchart.courses) {
      const status = courseStatuses.get(course.id)!;
      const u = effectiveUnits(course);
      if (status === "completed" || status === "inferred") earnedUnits += u;
      else if (status === "in_progress") inProgressUnits += u;
    }
    for (const entry of Object.values(session.customCourses ?? {})) {
      if (entry.status === "completed") earnedUnits += entry.units;
      else if (entry.status === "in_progress") inProgressUnits += entry.units;
    }
    return { earnedUnits, inProgressUnits };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [flowchart.courses, courseStatuses, plannedGEUnits, plannedFreeElectiveCourses, session.customCourses]);

  const totalUnits = flowchart.total_units;

  // ── Per-column unit totals ─────────────────────────────────────────────────
  const numCols = flowchart.columns.length;
  const { recommendedUnitsPerCol, currentUnitsPerCol } = useMemo(() => {
    const recommended = Array<number>(numCols).fill(0);
    const current     = Array<number>(numCols).fill(0);
    for (const course of flowchart.courses) {
      const u = effectiveUnits(course);
      recommended[course.grid_col] += u;
      const pos = getCoursePosition(course, positions);
      current[pos.grid_col] += u;
    }
    return { recommendedUnitsPerCol: recommended, currentUnitsPerCol: current };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [flowchart.courses, positions, plannedGEUnits, plannedFreeElectiveCourses, numCols]);

  const yearGroups = useMemo(() => {
    const groups: Array<{ label: string; count: number }> = [];
    for (const col of flowchart.columns) {
      if (groups.length > 0 && groups[groups.length - 1].label === col.year) {
        groups[groups.length - 1].count++;
      } else {
        groups.push({ label: col.year, count: 1 });
      }
    }
    return groups;
  }, [flowchart.columns]);

  const majorProgress = useMemo(() => countCourseProgress(majorCourses, courseStatuses), [majorCourses, courseStatuses]);
  const supportProgress = useMemo(() => countCourseProgress(supportCourses, courseStatuses), [supportCourses, courseStatuses]);
  const geProgress = useMemo(() => countCourseProgress(gePlaceholders, courseStatuses), [gePlaceholders, courseStatuses]);

  const maxRows = useMemo(
    () => Math.max(...flowchart.courses.map((c) => getCoursePosition(c, positions).grid_row + 1), 1),
    [flowchart.courses, positions]
  ) + (draggedCourseId ? 1 : 0);

  // Map from flowchart course.id → [customId, entry] for assigned custom courses
  const coveredByMap = useMemo(() => {
    const map = new Map<string, [string, CustomCourseEntry]>();
    for (const [id, entry] of Object.entries(session.customCourses ?? {})) {
      if (entry.assignedToSlotId) map.set(entry.assignedToSlotId, [id, entry]);
    }
    return map;
  }, [session.customCourses]);

  // Map from course.id → course for looking up slot labels on custom tiles
  const courseById = useMemo(() => {
    const map = new Map<string, Course>();
    for (const c of flowchart.courses) map.set(c.id, c);
    return map;
  }, [flowchart.courses]);

  const handleDrop = (targetCol: number, targetRow: number, targetCourse?: Course) => {
    if (!draggedCourseId || draggedCourseId === targetCourse?.id) return;
    onMoveCourse(draggedCourseId, targetCol, targetRow, targetCourse?.id);
    setDraggedCourseId(null);
  };

  return (
    <div className="flex flex-col gap-4">
      {/* Per-category progress bars */}
      <div className="grid grid-cols-3 gap-3 px-1">
        <ProgressBar
          label="Major"
          counts={majorProgress}
          colors={{ label: "#0369a1", completed: "#0284c7", inferred: "#7dd3fc", inProgress: "#bae6fd" }}
        />
        <ProgressBar
          label="Support"
          counts={supportProgress}
          colors={{ label: "#6d28d9", completed: "#7c3aed", inferred: "#c4b5fd", inProgress: "#ddd6fe" }}
        />
        <ProgressBar
          label="Gen Ed"
          counts={geProgress}
          colors={{ label: "#166534", completed: "#15803d", inferred: "#86efac", inProgress: "#bbf7d0" }}
        />
      </div>

      {/* Total units summary */}
      <div className="flex items-center gap-3 px-1 text-xs text-gray-600 border-t border-gray-100 pt-3 -mt-1">
        <span className="font-semibold text-gray-700">Units:</span>
        <span>
          <span className="font-bold text-blue-800">{earnedUnits}</span>
          <span className="text-gray-400"> earned</span>
        </span>
        {inProgressUnits > 0 && (
          <span>
            <span className="font-bold text-amber-600">+{inProgressUnits}</span>
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
          <div className="grid gap-1 mb-1" style={{ gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))` }}>
            {yearGroups.map((yg) => (
              <div key={yg.label} className="text-center text-xs font-bold uppercase tracking-wider py-1 rounded"
                   style={{ gridColumn: `span ${yg.count}`, background: "var(--cp-green)", color: "white" }}>
                {yg.label}
              </div>
            ))}
          </div>

          {/* Term sub-headers */}
          <div className="grid gap-1 mb-2" style={{ gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))` }}>
            {flowchart.columns.map((col, i) => {
              const rec = recommendedUnitsPerCol[i] ?? 0;
              const cur = currentUnitsPerCol[i] ?? 0;
              const over  = cur > rec;
              const under = cur < rec;
              return (
                <div key={i} className="text-center text-xs font-semibold rounded overflow-hidden"
                     style={{ background: "var(--cp-green-light)", color: "white" }}>
                  <div className="py-0.5">{col.term}</div>
                  <div className="border-t border-white/20 px-1 py-1 flex flex-col items-center gap-0.5">
                    <div className="text-[9px] font-normal opacity-70 leading-none">rec {rec}u</div>
                    <div className={`text-[11px] font-bold leading-none ${over ? "text-yellow-300" : under ? "text-white/60" : "text-white"}`}>
                      {cur}u
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Course rows */}
          {Array.from({ length: maxRows }).map((_, rowIdx) => (
            <div key={rowIdx} className="grid gap-1 mb-1" style={{ gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))` }}>
              {Array.from({ length: numCols }).map((_, colIdx) => {
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
                const status = courseStatuses.get(course.id)!;
                const display = courseDisplayData.get(course.id)!;
                const covering = coveredByMap.get(course.id);
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
                    {covering && (
                      <div className="mb-1 flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] font-bold"
                           style={{ background: "#fed7aa", color: "#9a3412", border: "1px solid #fb923c" }}>
                        <span>covered by {covering[1].course_number}</span>
                        <button
                          className="ml-auto hover:text-red-700"
                          onClick={(e) => { e.stopPropagation(); onClearCustomAssignment?.(covering[0]); }}
                        >✕</button>
                      </div>
                    )}
                    <CourseCard
                      course={course}
                      status={status}
                      checked={display.checked}
                      inProgressChecked={display.inProgressChecked}
                      plannedCourseNumber={display.plannedCourseNumber}
                      activeCourseNumber={display.activeCourseNumber}
                      plannedUnits={course.is_placeholder ? effectiveUnits(course) : undefined}
                      freeElectiveSelection={plannedFreeElectiveCourses[course.id]}
                      searchHighlighted={highlightedCourseIds?.has(course.id)}
                      onToggleCompleted={() => onToggleCourseCompleted(course)}
                      onToggleInProgress={() => onToggleCourseInProgress(course)}
                      onClick={() => onCourseClick(course, status)}
                    />
                  </div>
                );
              })}
            </div>
          ))}

          {/* Custom course tiles — rendered below flowchart tiles, grouped by column */}
          {session.customCourses && Object.keys(session.customCourses).length > 0 && (
            <div className="grid gap-1 mt-1" style={{ gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))` }}>
              {Array.from({ length: numCols }).map((_, colIdx) => {
                const colEntries = Object.entries(session.customCourses ?? {})
                  .filter(([, e]) => e.grid_col === colIdx) as [string, CustomCourseEntry][];
                return (
                  <div key={colIdx} className="flex flex-col gap-1">
                    {colEntries.map(([id, entry]) => {
                      const colors = CATEGORY_STYLES.custom;
                      return (
                        <div
                          key={id}
                          className="rounded border text-center transition-all select-none relative cursor-pointer hover:shadow-md active:scale-[0.99]"
                          style={{ background: colors.bg, borderColor: colors.border, borderWidth: 1.5, color: colors.text }}
                          onClick={() => onCustomCourseClick?.(id, entry)}
                        >
                          {/* Checkbox — absolute top-left, matching CourseCard */}
                          <label
                            className="absolute left-1 top-1 flex h-4 w-4 items-center justify-center rounded border bg-white/85 shadow-sm cursor-pointer"
                            title={entry.status === "completed" ? "Mark incomplete" : "Mark completed"}
                            onClick={(e) => e.stopPropagation()}
                            onMouseDown={(e) => e.stopPropagation()}
                          >
                            <input
                              type="checkbox"
                              checked={entry.status === "completed"}
                              onChange={() => onSetCustomCourseStatus?.(id, entry.status === "completed" ? "planned" : "completed")}
                              className="h-3 w-3 accent-green-700 cursor-pointer"
                            />
                          </label>
                          {/* IP button — absolute top-right, matching CourseCard */}
                          <label
                            className={`absolute right-1 top-1 flex h-4 min-w-5 items-center justify-center rounded border px-0.5 text-[8px] font-bold shadow-sm cursor-pointer transition-colors ${
                              entry.status === "in_progress"
                                ? "bg-amber-500 border-amber-600 text-white"
                                : "bg-white/85 border-gray-300 text-amber-700"
                            }`}
                            title={entry.status === "in_progress" ? "Remove in progress" : "Mark in progress"}
                            onClick={(e) => e.stopPropagation()}
                            onMouseDown={(e) => e.stopPropagation()}
                          >
                            <input
                              type="checkbox"
                              checked={entry.status === "in_progress"}
                              onChange={() => onSetCustomCourseStatus?.(id, entry.status === "in_progress" ? "planned" : "in_progress")}
                              className="sr-only"
                            />
                            IP
                          </label>
                          {/* Content — matches CourseCard px-1 py-2 */}
                          <div className="px-1 py-2">
                            {/* Status badge row */}
                            <div className="flex justify-center mb-0.5 h-3">
                              {entry.status === "completed"  && <span className="text-green-800 text-[10px] font-bold">✓</span>}
                              {entry.status === "in_progress" && <span className="text-amber-600 text-[10px] font-bold">IP</span>}
                            </div>
                            {/* Title first (bold), then course number (units) — matches CourseCard */}
                            <div className="text-[11px] font-bold leading-tight">{entry.title}</div>
                            <div className="text-[10px] mt-0.5 font-medium opacity-75">
                              {entry.course_number} ({entry.units})
                            </div>
                            {entry.assignedToSlotId && courseById.get(entry.assignedToSlotId) && (
                              <div className="text-[9px] mt-0.5 opacity-70">
                                → {courseById.get(entry.assignedToSlotId)!.course_number}
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          )}

          {/* Add course buttons — one per column */}
          {onAddCourse && (
            <div className="grid gap-1 mt-1" style={{ gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))` }}>
              {Array.from({ length: numCols }).map((_, colIdx) => (
                <button
                  key={colIdx}
                  onClick={() => onAddCourse(colIdx)}
                  className="rounded border border-dashed border-gray-300 py-1.5 text-xs text-gray-400 hover:border-green-500 hover:text-green-700 transition-colors"
                >
                  + add course
                </button>
              ))}
            </div>
          )}
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
          <span className="font-bold text-amber-600">IP</span> In Progress
        </div>
        <div className="flex items-center gap-1.5">
          <span>🔒</span> Prereqs needed
        </div>
        <div className="flex items-center gap-1.5">
          <span className="font-bold text-gray-500">NR</span> Not required
        </div>
      </div>
    </div>
  );
}
