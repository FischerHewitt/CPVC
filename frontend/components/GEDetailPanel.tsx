"use client";

import { useEffect, useState } from "react";
import type { Course, GEArea, GECourse, Professor, CourseInfo } from "@/lib/types";
import { getGECourses, getProfessors, getCourseInfo } from "@/lib/api";

type GEPanelStatus = "planned" | "completed" | "in_progress";
const STATUS_ORDER = ["planned", "in_progress", "completed"] as const;

export function geStatusOrder(): GEPanelStatus[] {
  return [...STATUS_ORDER];
}

const STATUS_LABELS: Record<GEPanelStatus, string> = {
  planned: "Plan",
  completed: "Done",
  in_progress: "IP",
};

export const GE_STATUS_STYLES: Record<GEPanelStatus, {
  activeButton: string;
  inactiveButton: string;
  selectedCard: string;
  selectedRow: string;
  selectedTitle: string;
  selectedText: string;
  selectedSubtleText: string;
}> = {
  planned: {
    activeButton: "border-blue-600 bg-blue-600 text-white",
    inactiveButton: "border-blue-200 text-blue-700 hover:border-blue-400 hover:bg-blue-50",
    selectedCard: "border-blue-200 bg-blue-50",
    selectedRow: "border-blue-300 bg-blue-50/40",
    selectedTitle: "text-blue-900",
    selectedText: "text-blue-800/80",
    selectedSubtleText: "text-blue-800/70",
  },
  completed: {
    activeButton: "border-green-700 bg-green-700 text-white",
    inactiveButton: "border-green-200 text-green-800 hover:border-green-400 hover:bg-green-50",
    selectedCard: "border-green-200 bg-green-50",
    selectedRow: "border-green-300 bg-green-50/40",
    selectedTitle: "text-green-900",
    selectedText: "text-green-800/80",
    selectedSubtleText: "text-green-800/70",
  },
  in_progress: {
    activeButton: "border-orange-600 bg-orange-600 text-white",
    inactiveButton: "border-orange-200 text-orange-700 hover:border-orange-400 hover:bg-orange-50",
    selectedCard: "border-orange-200 bg-orange-50",
    selectedRow: "border-orange-300 bg-orange-50/40",
    selectedTitle: "text-orange-900",
    selectedText: "text-orange-800/80",
    selectedSubtleText: "text-orange-800/70",
  },
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

// ── Course detail sub-panel (shown when user clicks a course title) ───────────

interface CourseDetailProps {
  geCourse: GECourse;
  onBack: () => void;
}

function GECourseDetail({ geCourse, onBack }: CourseDetailProps) {
  const [info, setInfo]               = useState<CourseInfo | null>(null);
  const [loadingInfo, setLoadingInfo] = useState(true);
  const [professors, setProfessors]   = useState<Professor[]>([]);
  const [loadingProfs, setLoadingProfs] = useState(true);

  useEffect(() => {
    let cancelled = false;

    setTimeout(() => {
      if (cancelled) return;
      setInfo(null);
      setProfessors([]);
      setLoadingInfo(true);
      setLoadingProfs(true);
    }, 0);

    getCourseInfo(geCourse.course_number)
      .then((nextInfo) => { if (!cancelled) setInfo(nextInfo); })
      .finally(() => { if (!cancelled) setLoadingInfo(false); });
    getProfessors(geCourse.course_number)
      .then((nextProfessors) => { if (!cancelled) setProfessors(nextProfessors); })
      .finally(() => { if (!cancelled) setLoadingProfs(false); });

    return () => { cancelled = true; };
  }, [geCourse.course_number]);

  const catalogUrl = `https://catalog.calpoly.edu/courses/${geCourse.course_number.split(" ")[0].toLowerCase()}/`;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Back bar */}
      <div className="px-4 py-2.5 border-b border-gray-100 flex items-center gap-2 bg-gray-50 flex-shrink-0">
        <button onClick={onBack}
                className="text-green-800 hover:text-green-700 text-sm font-medium flex items-center gap-1">
          ← Back
        </button>
        <span className="text-gray-300">|</span>
        <span className="text-xs font-semibold text-gray-700">{geCourse.course_number}</span>
        <span className="text-xs text-gray-400">{geCourse.units} units</span>
      </div>

      <div className="flex-1 overflow-y-auto px-5 py-4 flex flex-col gap-5">
        {/* Course title */}
        <div>
          <div className="text-base font-bold text-gray-900 leading-tight">{geCourse.title}</div>
          <a href={catalogUrl} target="_blank" rel="noopener noreferrer"
             className="text-xs text-blue-500 hover:underline mt-0.5 inline-block">
            View in Cal Poly catalog ↗
          </a>
        </div>

        {/* Description */}
        <div>
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Description</div>
          {loadingInfo && <div className="text-xs text-gray-400">Loading…</div>}
          {!loadingInfo && !info && (
            <div className="text-xs text-gray-400 italic">No catalog description available.</div>
          )}
          {info && <p className="text-sm text-gray-700 leading-relaxed">{info.description}</p>}
        </div>

        {/* Prerequisites */}
        {info && info.prerequisites_text && (
          <div>
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Prerequisites</div>
            <p className="text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded px-3 py-2 leading-relaxed">
              {info.prerequisites_text}
            </p>
          </div>
        )}

        {/* Professors */}
        <div>
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Professors</div>
          {loadingProfs && <div className="text-xs text-gray-400">Loading…</div>}
          {!loadingProfs && professors.length === 0 && (
            <div className="text-xs text-gray-400">No professor data available yet.</div>
          )}
          {professors.map((p) => <ProfessorRow key={p.name} prof={p} />)}
        </div>
      </div>
    </div>
  );
}

// ── Course list row ───────────────────────────────────────────────────────────

interface CourseRowProps {
  geCourse: GECourse;
  status?: GEPanelStatus;
  onChoose: (courseNumber: string, units: number, status: GEPanelStatus) => void;
  onSelect: (c: GECourse) => void;
}

function GECourseRow({
  geCourse,
  status,
  onChoose,
  onSelect,
}: CourseRowProps) {
  const [expanded, setExpanded]     = useState(false);
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [loading, setLoading]       = useState(false);
  const selectedStyles = status ? GE_STATUS_STYLES[status] : null;

  function toggleProfs(e: React.MouseEvent) {
    e.stopPropagation();
    if (expanded) { setExpanded(false); return; }
    setExpanded(true);
    if (professors.length > 0) return;
    setLoading(true);
    getProfessors(geCourse.course_number)
      .then(setProfessors)
      .finally(() => setLoading(false));
  }

  return (
    <div className={`border rounded-lg overflow-hidden mb-1.5 transition-colors ${
      selectedStyles ? selectedStyles.selectedRow : "border-gray-100"
    }`}>
      <div className="flex items-center px-3 py-2.5 hover:bg-gray-50 transition-colors gap-2">
        {/* Clickable title → detail view */}
        <button className="flex-1 text-left min-w-0" onClick={() => onSelect(geCourse)}>
          <div className={`text-sm font-semibold hover:text-green-800 transition-colors leading-tight ${
            selectedStyles ? selectedStyles.selectedTitle : "text-gray-800"
          }`}>
            {geCourse.course_number}
          </div>
          <div className="text-xs text-gray-500 leading-tight line-clamp-2">{geCourse.title}</div>
        </button>

        <div className="flex items-center gap-1.5 flex-shrink-0">
          {STATUS_ORDER.map((nextStatus) => {
            const style = GE_STATUS_STYLES[nextStatus];
            return (
              <button
                key={nextStatus}
                onClick={(e) => {
                  e.stopPropagation();
                  onChoose(geCourse.course_number, geCourse.units, nextStatus);
                }}
                className={`text-[10px] px-1.5 py-0.5 rounded border font-semibold transition-colors ${
                  status === nextStatus ? style.activeButton : style.inactiveButton
                }`}
                title={`${STATUS_LABELS[nextStatus]} ${geCourse.course_number}`}
              >
                {STATUS_LABELS[nextStatus]}
              </button>
            );
          })}
          <span className="text-xs text-gray-400">{geCourse.units}u</span>
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
          {!loading && professors.length === 0 && (
            <div className="text-xs text-gray-400 py-2">No professor data available yet.</div>
          )}
          {professors.map((p) => <ProfessorRow key={p.name} prof={p} />)}
        </div>
      )}
    </div>
  );
}

// ── Main panel ────────────────────────────────────────────────────────────────

interface Props {
  course: Course | null;
  completedSet: Set<string>;
  inProgressSet: Set<string>;
  plannedGECourses: Record<string, string>;
  onToggleGECourse: (areaId: string, courseNumber: string) => void;
  onToggleGECourseInProgress: (areaId: string, courseNumber: string) => void;
  onPlanGECourse: (areaId: string, courseNumber: string, units: number) => void;
  onAreaLoaded?: (areaId: string, courseNumbers: string[]) => void;
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

function hasGEStatus(geCourse: GECourse, knownSet: Set<string>) {
  const normalizedKnown = new Set(Array.from(knownSet, norm));
  const candidate = quarterCandidate(geCourse.course_number);
  return normalizedKnown.has(norm(geCourse.course_number)) || (candidate ? normalizedKnown.has(norm(candidate)) : false);
}

export function getGECoursePanelStatus(
  geCourse: GECourse,
  completedSet: Set<string>,
  inProgressSet: Set<string>,
  plannedCourseNumber?: string,
): GEPanelStatus | undefined {
  if (hasGEStatus(geCourse, completedSet)) return "completed";
  if (hasGEStatus(geCourse, inProgressSet)) return "in_progress";
  if (plannedCourseNumber === geCourse.course_number) return "planned";
  return undefined;
}

export function filterGECourses(courses: GECourse[], query: string): GECourse[] {
  const q = query.trim().toLowerCase();
  if (!q) return courses;
  return courses.filter((course) =>
    `${course.course_number} ${course.title}`.toLowerCase().includes(q)
  );
}

export function selectedGECourse(
  courses: GECourse[],
  completedSet: Set<string>,
  inProgressSet: Set<string>,
  plannedCourseNumber?: string,
): { course: GECourse; status: GEPanelStatus } | undefined {
  for (const status of ["completed", "in_progress", "planned"] as const) {
    const match = courses.find((candidate) =>
      getGECoursePanelStatus(candidate, completedSet, inProgressSet, plannedCourseNumber) === status
    );
    if (match) return { course: match, status };
  }
  return undefined;
}

export default function GEDetailPanel({
  course,
  completedSet,
  inProgressSet,
  plannedGECourses,
  onToggleGECourse,
  onToggleGECourseInProgress,
  onPlanGECourse,
  onAreaLoaded,
  onClose,
}: Props) {
  const [area, setArea]         = useState<GEArea | null>(null);
  const [loading, setLoading]   = useState(false);
  const [selected, setSelected] = useState<GECourse | null>(null);
  const [query, setQuery]       = useState("");

  const courseNumber = course?.course_number;

  useEffect(() => {
    let cancelled = false;

    if (!courseNumber) {
      setTimeout(() => { if (!cancelled) setSelected(null); }, 0);
      return () => { cancelled = true; };
    }

    setTimeout(() => {
      if (cancelled) return;
      setArea(null);
      setSelected(null);
      setQuery("");
      setLoading(true);
    }, 0);
    getGECourses(courseNumber)
      .then((a) => {
        if (cancelled) return;
        setArea(a);
        if (a) {
          const courseNumbers = a.courses.map((c) => c.course_number);
          onAreaLoaded?.(courseNumber, courseNumbers);
          if (a.area_id !== courseNumber) onAreaLoaded?.(a.area_id, courseNumbers);
        }
      })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [courseNumber, onAreaLoaded]);

  if (!course) return null;
  const areaId = course.course_number;

  const plannedCourseNumber = plannedGECourses[areaId];
  const selectedCourse = area
    ? selectedGECourse(area.courses, completedSet, inProgressSet, plannedCourseNumber)
    : undefined;
  const selectedStyles = selectedCourse ? GE_STATUS_STYLES[selectedCourse.status] : null;
  const visibleCourses = area ? filterGECourses(area.courses, query) : [];

  function chooseGECourse(courseNumber: string, units: number, status: GEPanelStatus) {
    if (status === "planned") onPlanGECourse(areaId, courseNumber, units);
    else if (status === "completed") onToggleGECourse(areaId, courseNumber);
    else onToggleGECourseInProgress(areaId, courseNumber);
  }

  function clearSelectedCourse() {
    if (!selectedCourse) return;
    const { course: geCourse, status } = selectedCourse;
    chooseGECourse(geCourse.course_number, geCourse.units, status);
  }

  return (
    <>
      <div className="fixed inset-0 bg-black/20 z-40 transition-opacity" onClick={onClose} />

      <div className="fixed right-0 top-0 h-full w-[min(560px,100vw)] bg-white shadow-2xl z-50 flex flex-col">
        {/* Top header — always visible */}
        <div className="px-5 py-4 border-b border-white/20 flex items-start justify-between flex-shrink-0"
             style={{ background: "var(--cp-green)" }}>
          <div>
            <div className="text-white/70 text-xs font-medium">{course.course_number}</div>
            <div className="text-white font-bold text-base leading-tight mt-0.5">{course.title}</div>
            <div className="text-white/70 text-xs mt-1">
              {course.category === "ge" ? "General Education Requirement" : "Major Elective"}
            </div>
          </div>
          <button onClick={onClose} className="text-white/70 hover:text-white text-xl leading-none ml-3 mt-0.5">×</button>
        </div>

        {/* Body — either list or detail view */}
        <div className="flex-1 overflow-hidden flex flex-col">
          {selected ? (
            <GECourseDetail geCourse={selected} onBack={() => setSelected(null)} />
          ) : (
            <div className="flex-1 overflow-y-auto px-5 py-4">
              {selectedCourse && selectedStyles && (
                <div className={`mb-4 rounded-lg border px-3 py-3 ${selectedStyles.selectedCard}`}>
                  <div className="flex items-start gap-2">
                    <div className="min-w-0 flex-1">
                      <div className={`text-sm font-bold ${selectedStyles.selectedTitle}`}>{selectedCourse.course.course_number}</div>
                      <div className={`text-xs ${selectedStyles.selectedText}`}>{selectedCourse.course.title}</div>
                      <div className={`mt-1 text-[11px] ${selectedStyles.selectedSubtleText}`}>{selectedCourse.course.units} units selected</div>
                    </div>
                    <button
                      onClick={clearSelectedCourse}
                      className="rounded border border-gray-200 bg-white px-2 py-1 text-[10px] font-semibold text-gray-700 hover:border-gray-300"
                    >
                      Clear
                    </button>
                  </div>
                  <div className="mt-3 flex gap-1.5">
                    {STATUS_ORDER.map((status) => {
                      const style = GE_STATUS_STYLES[status];
                      return (
                        <button
                          key={status}
                          onClick={() => chooseGECourse(selectedCourse.course.course_number, selectedCourse.course.units, status)}
                          className={`rounded border px-2 py-1 text-xs font-semibold transition-colors ${
                            selectedCourse.status === status ? style.activeButton : `bg-white ${style.inactiveButton}`
                          }`}
                        >
                          {STATUS_LABELS[status]}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search approved GE courses"
                className="mb-3 w-full rounded border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-700"
              />

              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                Approved Courses
              </div>

              {loading && <div className="text-xs text-gray-400">Loading…</div>}
              {!loading && !area && (
                <div className="text-xs text-gray-400">No course list available for this GE area yet.</div>
              )}
              {area && !loading && visibleCourses.length === 0 && (
                <div className="text-xs text-gray-400">No matching courses.</div>
              )}
              {visibleCourses.map((c) => (
                <GECourseRow
                  key={c.course_number}
                  geCourse={c}
                  status={getGECoursePanelStatus(c, completedSet, inProgressSet, plannedCourseNumber)}
                  onChoose={chooseGECourse}
                  onSelect={setSelected}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
