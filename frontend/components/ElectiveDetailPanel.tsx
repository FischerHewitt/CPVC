"use client";

import { useEffect, useRef, useState } from "react";
import type { Course, ElectiveArea, GECourse, Professor, CourseInfo } from "@/lib/types";
import { getElectiveCourses, getPlaceholderElectiveCourses, getProfessors, getCourseInfo } from "@/lib/api";

// ── Professor row (shared style with GEDetailPanel) ───────────────────────────

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

// ── Course detail sub-panel ───────────────────────────────────────────────────

function ElectiveCourseDetail({ course, onBack }: { course: GECourse; onBack: () => void }) {
  const [info, setInfo]                 = useState<CourseInfo | null>(null);
  const [loadingInfo, setLoadingInfo]   = useState(true);
  const [professors, setProfessors]     = useState<Professor[]>([]);
  const [loadingProfs, setLoadingProfs] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setTimeout(() => {
      if (cancelled) return;
      setInfo(null); setProfessors([]); setLoadingInfo(true); setLoadingProfs(true);
    }, 0);
    getCourseInfo(course.course_number)
      .then((i) => { if (!cancelled) setInfo(i); })
      .finally(() => { if (!cancelled) setLoadingInfo(false); });
    getProfessors(course.course_number)
      .then((p) => { if (!cancelled) setProfessors(p); })
      .finally(() => { if (!cancelled) setLoadingProfs(false); });
    return () => { cancelled = true; };
  }, [course.course_number]);

  const catalogUrl = `https://catalog.calpoly.edu/courses/${course.course_number.split(" ")[0].toLowerCase()}/`;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-4 py-2.5 border-b border-gray-100 flex items-center gap-2 bg-gray-50 flex-shrink-0">
        <button onClick={onBack} className="text-green-800 hover:text-green-700 text-sm font-medium flex items-center gap-1">
          ← Back
        </button>
        <span className="text-gray-300">|</span>
        <span className="text-xs font-semibold text-gray-700">{course.course_number}</span>
        <span className="text-xs text-gray-400">{course.units} units</span>
      </div>

      <div className="flex-1 overflow-y-auto px-5 py-4 flex flex-col gap-5">
        <div>
          <div className="text-base font-bold text-gray-900 leading-tight">{course.title}</div>
          <a href={catalogUrl} target="_blank" rel="noopener noreferrer"
             className="text-xs text-blue-500 hover:underline mt-0.5 inline-block">
            View in Cal Poly catalog ↗
          </a>
        </div>

        <div>
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Description</div>
          {loadingInfo && <div className="text-xs text-gray-400">Loading…</div>}
          {!loadingInfo && !info && <div className="text-xs text-gray-400 italic">No catalog description available.</div>}
          {info && <p className="text-sm text-gray-700 leading-relaxed">{info.description}</p>}
        </div>

        {info?.prerequisites_text && (
          <div>
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Prerequisites</div>
            <p className="text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded px-3 py-2 leading-relaxed">
              {info.prerequisites_text}
            </p>
          </div>
        )}

        <div>
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Professors</div>
          {loadingProfs && <div className="text-xs text-gray-400">Loading…</div>}
          {!loadingProfs && professors.length === 0 && <div className="text-xs text-gray-400">No professor data available yet.</div>}
          {professors.map((p) => <ProfessorRow key={p.name} prof={p} />)}
        </div>
      </div>
    </div>
  );
}

// ── Course list row ───────────────────────────────────────────────────────────

interface ElectiveCourseRowProps {
  course: GECourse;
  completed: boolean;
  inProgress: boolean;
  planned: boolean;
  isCapped?: boolean;
  plannedSlotUnits?: number;
  onToggle: (courseNumber: string, units: number) => void;
  onToggleInProgress: (courseNumber: string, units: number) => void;
  onPlan: (courseNumber: string, units: number) => void;
  onSelect: (c: GECourse) => void;
}

function ElectiveCourseRow({
  course,
  completed,
  inProgress,
  planned,
  isCapped,
  plannedSlotUnits,
  onToggle,
  onToggleInProgress,
  onPlan,
  onSelect,
}: ElectiveCourseRowProps) {
  const [expanded, setExpanded]     = useState(false);
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [loading, setLoading]       = useState(false);
  const [chosenUnits, setChosenUnits] = useState(plannedSlotUnits ?? 1);
  const prevPlannedSlotUnits = useRef(plannedSlotUnits);
  useEffect(() => {
    if (prevPlannedSlotUnits.current !== plannedSlotUnits) {
      prevPlannedSlotUnits.current = plannedSlotUnits;
      setChosenUnits(plannedSlotUnits ?? 1);
    }
  }, [plannedSlotUnits]);

  function toggleProfs(e: React.MouseEvent) {
    e.stopPropagation();
    if (expanded) { setExpanded(false); return; }
    setExpanded(true);
    if (professors.length > 0) return;
    setLoading(true);
    getProfessors(course.course_number).then(setProfessors).finally(() => setLoading(false));
  }

  return (
    <div className={`border rounded-lg overflow-hidden mb-1.5 transition-colors ${
      completed
        ? "border-green-300 bg-green-50/40"
        : inProgress
          ? "border-blue-300 bg-blue-50/50"
          : planned
            ? "border-blue-200 bg-blue-50/40"
            : "border-gray-100"
    }`}>
      <div className="flex items-center px-3 py-2.5 hover:bg-gray-50 transition-colors gap-2">
        <div className="flex flex-shrink-0 flex-col gap-1.5">
          <label className="flex items-center gap-1 text-[10px] font-semibold text-gray-600" title={completed ? "Mark not taken" : "Mark as completed"}>
            <input
              type="checkbox"
              checked={completed}
              onChange={() => onToggle(course.course_number, course.units)}
              className="h-3.5 w-3.5 accent-green-700 cursor-pointer"
              onClick={(e) => e.stopPropagation()}
            />
            Done
          </label>
          <label className="flex items-center gap-1 text-[10px] font-semibold text-amber-700" title={inProgress ? "Remove in progress" : "Mark in progress"}>
            <input
              type="checkbox"
              checked={inProgress && !completed}
              onChange={() => onToggleInProgress(course.course_number, course.units)}
              className="h-3.5 w-3.5 accent-amber-600 cursor-pointer"
              onClick={(e) => e.stopPropagation()}
            />
            IP
          </label>
        </div>

        <button className="flex-1 text-left min-w-0" onClick={() => onSelect(course)}>
          <div className={`text-sm font-semibold hover:text-green-800 transition-colors leading-tight ${
            completed ? "text-green-800 line-through opacity-70" : inProgress ? "text-blue-800" : "text-gray-800"
          }`}>
            {course.course_number}
          </div>
          <div className="text-xs text-gray-500 leading-tight line-clamp-2">{course.title}</div>
        </button>
        <div className="flex items-center gap-1.5 flex-shrink-0">
          {inProgress && !completed && (
            <span className="rounded bg-amber-100 px-1.5 py-0.5 text-[10px] font-bold text-amber-800">
              IP
            </span>
          )}
          {isCapped && (
            <div className="flex gap-0.5" title="Units to count toward requirement">
              {[1, 2, 3].map((u) => (
                <button
                  key={u}
                  onClick={(e) => { e.stopPropagation(); setChosenUnits(u); }}
                  className={`text-[9px] w-5 h-5 rounded border font-bold transition-colors ${
                    chosenUnits === u
                      ? "bg-blue-600 border-blue-600 text-white"
                      : "border-gray-300 text-gray-400 hover:border-blue-400 hover:text-blue-600"
                  }`}
                >
                  {u}
                </button>
              ))}
            </div>
          )}
          <button
            onClick={(e) => { e.stopPropagation(); onPlan(course.course_number, isCapped ? chosenUnits : course.units); }}
            className={`text-[10px] px-1.5 py-0.5 rounded border transition-colors ${
              planned
                ? "border-blue-300 bg-blue-100 text-blue-800"
                : "border-gray-200 text-gray-400 hover:border-blue-300 hover:text-blue-700"
            }`}
            title={planned ? "Remove selected course" : "Select this course"}
          >
            {planned ? "Selected" : "Select"}
          </button>
          <span className="text-xs text-gray-400">{isCapped ? chosenUnits : course.units}u</span>
          <button onClick={toggleProfs}
                  className="text-[10px] text-gray-400 hover:text-gray-600 px-1.5 py-0.5 rounded border border-gray-200 hover:border-gray-300 transition-colors"
                  title="Show professors">
            {expanded ? "▲" : "▼"}
          </button>
        </div>
      </div>
      {expanded && (
        <div className="px-3 pb-2 border-t border-gray-100 bg-gray-50/60">
          {loading && <div className="text-xs text-gray-400 py-2">Loading professors…</div>}
          {!loading && professors.length === 0 && <div className="text-xs text-gray-400 py-2">No professor data available yet.</div>}
          {professors.map((p) => <ProfessorRow key={p.name} prof={p} />)}
        </div>
      )}
    </div>
  );
}

// ── Main panel ────────────────────────────────────────────────────────────────

interface CappedCourseConfig {
  numbers: Set<string>;
  cap: number;
  label: string;
  totalAcrossSlots: number;
}

interface Props {
  course: Course | null;
  completedSet: Set<string>;
  inProgressSet: Set<string>;
  plannedElectiveCourses: Record<string, string>;
  currentSlotId?: string;
  plannedSlotUnits?: number;
  cappedCourseConfig?: CappedCourseConfig;
  onToggleElectiveCourse: (placeholder: Course, courseNumber: string, units: number) => void;
  onToggleElectiveCourseInProgress: (placeholder: Course, courseNumber: string, units: number) => void;
  onPlanElectiveCourse: (placeholder: Course, courseNumber: string, units: number) => void;
  onSetSlotUnits?: (courseId: string, units: number | null) => void;
  onClose: () => void;
}

function norm(courseNumber: string) {
  return courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
}

function quarterCandidate(courseNumber: string) {
  const [dept, code] = courseNumber.split(/\s+/);
  if (!dept || !code || !/^\d{4}$/.test(code)) return null;
  return `${dept} ${Number(code.slice(1))}`;
}

function hasElectiveStatus(option: GECourse, knownSet: Set<string>) {
  const normalizedKnown = new Set(Array.from(knownSet, norm));
  const candidate = quarterCandidate(option.course_number);
  return normalizedKnown.has(norm(option.course_number)) || (candidate ? normalizedKnown.has(norm(candidate)) : false);
}

export default function ElectiveDetailPanel({
  course,
  completedSet,
  inProgressSet,
  plannedElectiveCourses,
  currentSlotId,
  plannedSlotUnits,
  cappedCourseConfig,
  onToggleElectiveCourse,
  onToggleElectiveCourseInProgress,
  onPlanElectiveCourse,
  onSetSlotUnits,
  onClose,
}: Props) {
  const [area, setArea]         = useState<ElectiveArea | null>(null);
  const [loading, setLoading]   = useState(false);
  const [selected, setSelected] = useState<GECourse | null>(null);

  const electiveKey = course?.elective_key;

  useEffect(() => {
    let cancelled = false;
    if (!course) {
      setTimeout(() => { if (!cancelled) setSelected(null); }, 0);
      return () => { cancelled = true; };
    }
    setTimeout(() => {
      if (cancelled) return;
      setArea(null); setSelected(null); setLoading(true);
    }, 0);
    const request = electiveKey ? getElectiveCourses(electiveKey) : getPlaceholderElectiveCourses(course);
    request
      .then((a) => { if (!cancelled) setArea(a); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [course, electiveKey]);

  if (!course) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/20 z-40 transition-opacity" onClick={onClose} />

      <div className="fixed right-0 top-0 h-full w-[min(560px,100vw)] bg-white shadow-2xl z-50 flex flex-col">
        {/* Header */}
        <div className="px-5 py-4 border-b border-white/20 flex items-start justify-between flex-shrink-0"
             style={{ background: "var(--cp-green)" }}>
          <div>
            <div className="text-white/70 text-xs font-medium">{course.course_number}</div>
            <div className="text-white font-bold text-base leading-tight mt-0.5">{course.title}</div>
            <div className="text-white/70 text-xs mt-1">
              {course.category === "support" ? "Support Requirement" : "Elective Requirement"}
            </div>
          </div>
          <button onClick={onClose} className="text-white/70 hover:text-white text-xl leading-none ml-3 mt-0.5">×</button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-hidden flex flex-col">
          {selected ? (
            <ElectiveCourseDetail course={selected} onBack={() => setSelected(null)} />
          ) : (
            <div className="flex-1 overflow-y-auto px-5 py-4">
              {area && <p className="text-xs text-gray-500 mb-3">{area.description}</p>}

              {cappedCourseConfig && cappedCourseConfig.totalAcrossSlots > 0 && (
                <div className={`mb-3 rounded px-3 py-2 text-xs border ${
                  cappedCourseConfig.totalAcrossSlots > cappedCourseConfig.cap
                    ? "bg-red-50 border-red-200 text-red-800"
                    : "bg-amber-50 border-amber-200 text-amber-800"
                }`}>
                  {cappedCourseConfig.totalAcrossSlots > cappedCourseConfig.cap ? "⚠️" : "ℹ️"}{" "}
                  <strong>{cappedCourseConfig.label}</strong> are limited to{" "}
                  <strong>{cappedCourseConfig.cap} units</strong> combined toward Major Electives.
                  {" "}Currently planned: <strong>{cappedCourseConfig.totalAcrossSlots}u</strong>.
                  {cappedCourseConfig.totalAcrossSlots > cappedCourseConfig.cap && (
                    <span> You may not be able to count all of these units — check with your advisor.</span>
                  )}
                </div>
              )}

              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                Eligible Courses
                {area && (
                  <span className="ml-1 font-normal normal-case text-gray-400">
                    — click a course for description
                  </span>
                )}
              </div>

              {loading && <div className="text-xs text-gray-400">Loading…</div>}
              {!loading && !area && (
                <div className="text-xs text-gray-400">No course list available for this elective yet.</div>
              )}
              {area?.courses.map((c) => {
                const isCapped = cappedCourseConfig?.numbers.has(c.course_number) ?? false;
                const isPlanned = plannedElectiveCourses[course.course_number] === c.course_number;
                return (
                  <ElectiveCourseRow
                    key={c.course_number}
                    course={c}
                    completed={hasElectiveStatus(c, completedSet)}
                    inProgress={hasElectiveStatus(c, inProgressSet)}
                    planned={isPlanned}
                    isCapped={isCapped}
                    plannedSlotUnits={isCapped && isPlanned ? plannedSlotUnits : undefined}
                    onToggle={(courseNumber, units) => onToggleElectiveCourse(course, courseNumber, units)}
                    onToggleInProgress={(courseNumber, units) => onToggleElectiveCourseInProgress(course, courseNumber, units)}
                    onPlan={(courseNumber, units) => {
                      const deselecting = plannedElectiveCourses[course.course_number] === courseNumber;
                      onPlanElectiveCourse(course, courseNumber, units);
                      if (isCapped && onSetSlotUnits && currentSlotId) {
                        onSetSlotUnits(currentSlotId, deselecting ? null : units);
                      }
                    }}
                    onSelect={setSelected}
                  />
                );
              })}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
