"use client";

import { useEffect, useRef, useState } from "react";
import type { Course, CourseSearchResult, ElectiveArea, GECourse, Professor, CourseInfo } from "@/lib/types";
import { getElectiveCourses, getPlaceholderElectiveCourses, getProfessors, getCourseInfo } from "@/lib/api";
import { type GEPanelStatus, GE_STATUS_ORDER, GE_STATUS_LABELS, GE_STATUS_STYLES } from "@/lib/status-styles";
import { parseUnitsRange } from "@/lib/units";
import {
  searchFreeElectiveCatalog,
  shouldSearchFreeElectiveCatalog,
  FREE_ELECTIVE_SEARCH_DEBOUNCE_MS,
} from "@/lib/free-elective-search";

// ── Pure helpers (exported for tests) ────────────────────────────────────────

export function electiveCourseActiveStatus(
  completed: boolean,
  inProgress: boolean,
  planned: boolean,
): "completed" | "in_progress" | "planned" | null {
  if (completed) return "completed";
  if (inProgress) return "in_progress";
  if (planned) return "planned";
  return null;
}

/**
 * Returns what onSetSlotUnits should receive when a status button is clicked:
 * - variable-unit or capped: always (all three statuses) — preserves chosen units for tile badge + panel restore
 * - fixed-unit: only for "planned" (tracks slot occupancy for unit-cap calculation)
 * - Returns undefined when onSetSlotUnits should NOT be called.
 */
export function slotUnitDecision(
  clickedStatus: string,
  activeStatus: string | null,
  isVar: boolean,
  isCapped: boolean,
  chosenUnits: number,
  courseUnits: number,
): number | null | undefined {
  const isVarOrCapped = isVar || isCapped;
  if (!isVarOrCapped && clickedStatus !== "planned") return undefined;
  const effectiveUnits = isVarOrCapped ? chosenUnits : courseUnits;
  return activeStatus === clickedStatus ? null : effectiveUnits;
}

export function isVariableUnit(course: GECourse): boolean {
  return (
    course.units_min !== undefined &&
    course.units_max !== undefined &&
    course.units_min < course.units_max
  );
}

export function filterEligibleCourses(courses: GECourse[], query: string): GECourse[] {
  const q = query.trim().toLowerCase();
  if (!q) return courses;
  return courses.filter((c) =>
    c.course_number.toLowerCase().includes(q) || c.title.toLowerCase().includes(q)
  );
}

export function isOverrideCourse(courseNumber: string, eligibleCourses: GECourse[]): boolean {
  const normalized = courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
  return !eligibleCourses.some(
    (c) => c.course_number.toUpperCase().trim().replace(/\s+/g, " ") === normalized
  );
}

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
  coreqWarning?: string;
  onToggle: (courseNumber: string, units: number) => void;
  onToggleInProgress: (courseNumber: string, units: number) => void;
  onPlan: (courseNumber: string, units: number) => void;
  onSetSlotUnits?: (units: number | null) => void;
  onSelect: (c: GECourse) => void;
}

function ElectiveCourseRow({
  course,
  completed,
  inProgress,
  planned,
  isCapped,
  plannedSlotUnits,
  coreqWarning,
  onToggle,
  onToggleInProgress,
  onPlan,
  onSetSlotUnits,
  onSelect,
}: ElectiveCourseRowProps) {
  const [expanded, setExpanded]         = useState(false);
  const [professors, setProfessors]     = useState<Professor[]>([]);
  const [loading, setLoading]           = useState(false);
  const [warnDismissed, setWarnDismissed] = useState(false);

  const isVar = isVariableUnit(course);
  const defaultChosenUnits = isVar ? (course.units_min ?? course.units) : course.units;
  const [chosenUnits, setChosenUnits] = useState(plannedSlotUnits ?? defaultChosenUnits);

  const prevPlannedSlotUnits = useRef(plannedSlotUnits);
  useEffect(() => {
    if (prevPlannedSlotUnits.current !== plannedSlotUnits) {
      prevPlannedSlotUnits.current = plannedSlotUnits;
      setChosenUnits(plannedSlotUnits ?? defaultChosenUnits);
    }
  }, [plannedSlotUnits, defaultChosenUnits]);

  const activeStatus = electiveCourseActiveStatus(completed, inProgress, planned);

  function toggleProfs(e: React.MouseEvent) {
    e.stopPropagation();
    if (expanded) { setExpanded(false); return; }
    setExpanded(true);
    if (professors.length > 0) return;
    setLoading(true);
    getProfessors(course.course_number).then(setProfessors).finally(() => setLoading(false));
  }

  function handleStatusButton(status: GEPanelStatus) {
    const effectiveUnits = (isVar || isCapped) ? chosenUnits : course.units;
    if (status === "planned") {
      onPlan(course.course_number, effectiveUnits);
    } else if (status === "in_progress") {
      onToggleInProgress(course.course_number, effectiveUnits);
    } else {
      onToggle(course.course_number, effectiveUnits);
    }
    const decision = slotUnitDecision(status, activeStatus, isVar, isCapped ?? false, chosenUnits, course.units);
    if (decision !== undefined) onSetSlotUnits?.(decision);
  }

  function handlePillClick(u: number) {
    setChosenUnits(u);
    if (activeStatus) onSetSlotUnits?.(u);
  }

  const rowStyle = activeStatus ? GE_STATUS_STYLES[activeStatus].selectedRow : "border-gray-100";

  return (
    <div className={`border rounded-lg overflow-hidden mb-1.5 transition-colors ${rowStyle}`}>
      <div className="flex items-center px-3 py-2.5 hover:bg-gray-50/50 transition-colors gap-2">
        {/* Course name + subtitle */}
        <button className="flex-1 text-left min-w-0" onClick={() => onSelect(course)}>
          <div className={`text-sm font-semibold hover:text-green-800 transition-colors leading-tight ${
            activeStatus === "completed"
              ? "text-green-800 line-through opacity-70"
              : activeStatus
                ? GE_STATUS_STYLES[activeStatus].selectedTitle
                : "text-gray-800"
          }`}>
            {course.course_number}
          </div>
          <div className="text-xs text-gray-500 leading-tight line-clamp-2">{course.title}</div>
        </button>

        {/* Plan / IP / Done buttons */}
        <div className="flex gap-1 flex-shrink-0">
          {GE_STATUS_ORDER.map((status) => {
            const style = GE_STATUS_STYLES[status];
            return (
              <button
                key={status}
                onClick={(e) => { e.stopPropagation(); handleStatusButton(status); }}
                className={`rounded border px-1.5 py-0.5 text-[10px] font-semibold transition-colors ${
                  activeStatus === status ? style.activeButton : `bg-white ${style.inactiveButton}`
                }`}
              >
                {GE_STATUS_LABELS[status]}
              </button>
            );
          })}
        </div>

        {/* Unit label / pills */}
        <div className="flex items-center gap-0.5 flex-shrink-0">
          {(isVar || isCapped) && activeStatus ? (
            /* Variable-unit or capped pills — shown when any status is active */
            <>
              {Array.from(
                { length: (isCapped ? 3 : (course.units_max ?? course.units)) - ((isCapped ? 1 : course.units_min) ?? 1) + 1 },
                (_, i) => (isCapped ? 1 : (course.units_min ?? 1)) + i,
              ).map((u) => (
                <button
                  key={u}
                  onClick={(e) => { e.stopPropagation(); handlePillClick(u); }}
                  className={`text-[9px] w-5 h-5 rounded border font-bold transition-colors ${
                    chosenUnits === u
                      ? "bg-blue-600 border-blue-600 text-white"
                      : "border-gray-300 text-gray-400 hover:border-blue-400 hover:text-blue-600"
                  }`}
                >
                  {u}
                </button>
              ))}
              <span className="text-xs text-gray-400 ml-0.5">u</span>
            </>
          ) : isVar ? (
            /* Variable-unit, no active status — show range label */
            <span className="text-xs text-gray-400">{course.units_min}–{course.units_max}u</span>
          ) : (
            /* Fixed-unit — always show static label */
            <span className="text-xs text-gray-400">{isCapped ? chosenUnits : course.units}u</span>
          )}
        </div>

        {/* Prof dropdown toggle */}
        <button onClick={toggleProfs}
                className="text-[10px] text-gray-400 hover:text-gray-600 px-1.5 py-0.5 rounded border border-gray-200 hover:border-gray-300 transition-colors flex-shrink-0"
                title="Show professors">
          {expanded ? "▲" : "▼"}
        </button>
      </div>

      {coreqWarning && !warnDismissed && (
        <div className="px-3 py-1.5 border-t border-amber-200 bg-amber-50 text-[11px] text-amber-800 flex items-start justify-between gap-2">
          <span>⚠ {coreqWarning}</span>
          <button
            onClick={(e) => { e.stopPropagation(); setWarnDismissed(true); }}
            className="flex-shrink-0 text-amber-600 hover:text-amber-900 leading-none"
            title="Dismiss"
          >×</button>
        </div>
      )}
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
  flowchartCourseNumbers?: Set<string>;
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

export function labCoreqWarning(
  courseNumber: string,
  completedSet: Set<string>,
  inProgressSet: Set<string>,
  flowchartCourseNumbers: Set<string>,
): string | undefined {
  if (!courseNumber.match(/\d[A-Z]$/)) return undefined;
  const lectureNumber = courseNumber.replace(/([A-Z])$/, "");
  const known = new Set([...completedSet, ...inProgressSet, ...flowchartCourseNumbers].map(norm));
  if (known.has(norm(lectureNumber))) return undefined;
  return `Lab course — requires concurrent enrollment in ${lectureNumber}. Confirm with your advisor.`;
}

export default function ElectiveDetailPanel({
  course,
  completedSet,
  inProgressSet,
  plannedElectiveCourses,
  flowchartCourseNumbers = new Set(),
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

  // In-list search filter (Issue #9)
  const [listFilter, setListFilter] = useState("");

  // Elective override state (Issues #10, #11)
  const [accordionOpen, setAccordionOpen]       = useState(false);
  const [overrideQuery, setOverrideQuery]       = useState("");
  const [overrideResults, setOverrideResults]   = useState<CourseSearchResult[]>([]);
  const [overrideCourse, setOverrideCourse]     = useState<GECourse | null>(null);
  const overrideDebounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const electiveKey = course?.elective_key;

  // Load area and reconstruct override card on panel open (Issues #10, #11)
  useEffect(() => {
    let cancelled = false;
    if (!course) {
      setTimeout(() => {
        if (!cancelled) {
          setSelected(null);
          setOverrideCourse(null);
          setAccordionOpen(false);
          setListFilter("");
          setOverrideQuery("");
          setOverrideResults([]);
        }
      }, 0);
      return () => { cancelled = true; };
    }
    const plannedAtOpen = plannedElectiveCourses[course.course_number];
    setTimeout(() => {
      if (cancelled) return;
      setArea(null); setSelected(null); setLoading(true);
      setOverrideCourse(null); setAccordionOpen(false);
      setListFilter(""); setOverrideQuery(""); setOverrideResults([]);
    }, 0);
    const request = electiveKey ? getElectiveCourses(electiveKey) : getPlaceholderElectiveCourses(course);
    request
      .then((a) => {
        if (!cancelled) {
          setArea(a);
          // Issue #11: reconstruct override card if planned course isn't in the eligible list
          if (a && plannedAtOpen && isOverrideCourse(plannedAtOpen, a.courses)) {
            getCourseInfo(plannedAtOpen).then((info) => {
              if (!cancelled) {
                setOverrideCourse(
                  info
                    ? { course_number: plannedAtOpen, title: info.title, units: Number(info.units) || 0 }
                    : { course_number: plannedAtOpen, title: "", units: 0 }
                );
              }
            });
          }
        }
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [course, electiveKey]);

  // Debounced override catalog search
  useEffect(() => {
    if (overrideDebounceRef.current) clearTimeout(overrideDebounceRef.current);
    if (!shouldSearchFreeElectiveCatalog(overrideQuery)) { setOverrideResults([]); return; }
    overrideDebounceRef.current = setTimeout(async () => {
      const found = await searchFreeElectiveCatalog(overrideQuery);
      setOverrideResults(found);
    }, FREE_ELECTIVE_SEARCH_DEBOUNCE_MS);
    return () => { if (overrideDebounceRef.current) clearTimeout(overrideDebounceRef.current); };
  }, [overrideQuery]);

  if (!course) return null;

  // Derive override course's current status from session state
  const overrideStatus: GEPanelStatus | undefined = (() => {
    if (!overrideCourse) return undefined;
    if (hasElectiveStatus(overrideCourse, completedSet)) return "completed";
    if (hasElectiveStatus(overrideCourse, inProgressSet)) return "in_progress";
    if (plannedElectiveCourses[course.course_number] === overrideCourse.course_number) return "planned";
    return undefined;
  })();

  function handleOverrideSelect(result: CourseSearchResult) {
    if (!course) return;
    const eligibleCourses = area?.courses ?? [];
    const inList = eligibleCourses.find(
      (c) => norm(c.course_number) === norm(result.course_number)
    );
    setAccordionOpen(false);
    setOverrideQuery("");
    setOverrideResults([]);
    if (inList) {
      // Course is in the eligible list — treat as a normal selection
      onPlanElectiveCourse(course, inList.course_number, inList.units);
      setOverrideCourse(null);
    } else {
      // Genuine override — store it and show the override card
      const overrideEntry: GECourse = { course_number: result.course_number, title: result.title, units: result.units };
      setOverrideCourse(overrideEntry);
      onPlanElectiveCourse(course, result.course_number, result.units);
    }
  }

  function chooseOverrideCourse(status: GEPanelStatus) {
    if (!course || !overrideCourse) return;
    const willClear = status === overrideStatus;
    if (status === "planned") onPlanElectiveCourse(course, overrideCourse.course_number, overrideCourse.units);
    else if (status === "completed") onToggleElectiveCourse(course, overrideCourse.course_number, overrideCourse.units);
    else onToggleElectiveCourseInProgress(course, overrideCourse.course_number, overrideCourse.units);
    if (willClear) setOverrideCourse(null);
  }

  function clearOverrideSelection() {
    if (course && overrideCourse) {
      if (overrideStatus === "completed") onToggleElectiveCourse(course, overrideCourse.course_number, overrideCourse.units);
      else if (overrideStatus === "in_progress") onToggleElectiveCourseInProgress(course, overrideCourse.course_number, overrideCourse.units);
      else if (overrideStatus === "planned") onPlanElectiveCourse(course, overrideCourse.course_number, overrideCourse.units);
    }
    setOverrideCourse(null);
  }

  const visibleCourses = filterEligibleCourses(area?.courses ?? [], listFilter);

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
            <>
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

                {/* In-list search filter (Issue #9) */}
                {area && (
                  <input
                    value={listFilter}
                    onChange={(e) => setListFilter(e.target.value)}
                    placeholder="Search by course number or title…"
                    className="mb-3 w-full rounded border border-gray-200 px-3 py-1.5 text-xs outline-none focus:border-blue-400"
                  />
                )}

                {loading && <div className="text-xs text-gray-400">Loading…</div>}
                {!loading && !area && (
                  <div className="text-xs text-gray-400">No course list available for this elective yet.</div>
                )}
                {!loading && area && visibleCourses.length === 0 && listFilter && (
                  <div className="text-xs text-gray-400 py-2">No matches for "{listFilter}".</div>
                )}
                {visibleCourses.map((c) => {
                  const isCapped = cappedCourseConfig?.numbers.has(c.course_number) ?? false;
                  const isPlanned = plannedElectiveCourses[course.course_number] === c.course_number;
                  const isVar = isVariableUnit(c);
                  return (
                    <div key={c.course_number}>
                      <ElectiveCourseRow
                        course={c}
                        completed={hasElectiveStatus(c, completedSet)}
                        inProgress={hasElectiveStatus(c, inProgressSet)}
                        planned={isPlanned}
                        isCapped={isCapped}
                        plannedSlotUnits={(isCapped || isVar) && isPlanned ? plannedSlotUnits : undefined}
                        coreqWarning={labCoreqWarning(c.course_number, completedSet, inProgressSet, flowchartCourseNumbers)}
                        onToggle={(courseNumber, units) => onToggleElectiveCourse(course, courseNumber, units)}
                        onToggleInProgress={(courseNumber, units) => onToggleElectiveCourseInProgress(course, courseNumber, units)}
                        onPlan={(courseNumber, units) => {
                          const deselecting = plannedElectiveCourses[course.course_number] === courseNumber;
                          onPlanElectiveCourse(course, courseNumber, units);
                          if (!deselecting) setOverrideCourse(null);
                        }}
                        onSetSlotUnits={onSetSlotUnits && currentSlotId
                          ? (units) => onSetSlotUnits(currentSlotId, units)
                          : undefined}
                        onSelect={setSelected}
                      />
                    </div>
                  );
                })}
              </div>

              {/* Override accordion (Issues #10, #11) */}
              <div className="flex-shrink-0 border-t-2" style={{ borderColor: "var(--cp-green)" }}>
                {overrideCourse ? (
                  /* Override card */
                  <div className="px-5 py-3" style={{ background: "#f0f7f4" }}>
                    <div className={`rounded border p-3 ${overrideStatus ? GE_STATUS_STYLES[overrideStatus].selectedCard : "border-gray-200 bg-white"}`}>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <div className="min-w-0">
                          <div className={`text-sm font-bold ${overrideStatus ? GE_STATUS_STYLES[overrideStatus].selectedTitle : "text-gray-900"}`}>
                            {overrideCourse.course_number}
                          </div>
                          {overrideCourse.title && (
                            <div className={`text-xs ${overrideStatus ? GE_STATUS_STYLES[overrideStatus].selectedText : "text-gray-600"}`}>
                              {overrideCourse.title}
                            </div>
                          )}
                          <div className={`text-[11px] ${overrideStatus ? GE_STATUS_STYLES[overrideStatus].selectedSubtleText : "text-gray-400"}`}>
                            {overrideCourse.units}u · override selection
                          </div>
                        </div>
                        <button
                          onClick={clearOverrideSelection}
                          className="rounded border border-gray-200 bg-white px-2 py-1 text-[10px] font-semibold text-gray-600 hover:border-gray-300 flex-shrink-0"
                        >
                          Clear
                        </button>
                      </div>
                      <div className="flex gap-1.5 items-center">
                        {GE_STATUS_ORDER.map((status) => {
                          const style = GE_STATUS_STYLES[status];
                          return (
                            <button
                              key={status}
                              onClick={() => chooseOverrideCourse(status)}
                              className={`rounded border px-2 py-1 text-xs font-semibold transition-colors ${
                                overrideStatus === status ? style.activeButton : `bg-white ${style.inactiveButton}`
                              }`}
                            >
                              {GE_STATUS_LABELS[status]}
                            </button>
                          );
                        })}
                        <span className="text-xs text-gray-400 ml-1">{overrideCourse.units}u</span>
                      </div>
                    </div>
                  </div>
                ) : (
                  /* "Can't find your course?" accordion */
                  <>
                    <button
                      onClick={() => setAccordionOpen((o) => !o)}
                      className="w-full flex items-center justify-between px-5 py-2.5 text-xs transition-colors"
                      style={accordionOpen
                        ? { background: "var(--cp-green)", color: "white" }
                        : { background: "#f0f7f4", color: "var(--cp-green)" }}
                    >
                      <span className="font-semibold">Can&apos;t find your course?</span>
                      <span style={{ opacity: 0.7 }}>{accordionOpen ? "▲" : "▼"}</span>
                    </button>
                    {accordionOpen && (
                      <div className="px-5 pb-3 pt-2 flex flex-col gap-2" style={{ background: "#f0f7f4" }}>
                        <div className="relative">
                          <input
                            autoFocus
                            placeholder="Search catalog for any course…"
                            value={overrideQuery}
                            onChange={(e) => setOverrideQuery(e.target.value)}
                            className="w-full rounded border px-3 py-1.5 text-xs bg-white outline-none"
                            style={{ borderColor: "var(--cp-green)" }}
                          />
                          {overrideResults.length > 0 && (
                            <div className="absolute bottom-full left-0 right-0 mb-1 rounded border border-gray-200 bg-white shadow-md max-h-40 overflow-y-auto z-10">
                              {overrideResults.map((r) => {
                                const inList = area?.courses.some((c) => norm(c.course_number) === norm(r.course_number));
                                return (
                                  <button
                                    key={r.course_number}
                                    onClick={() => handleOverrideSelect(r)}
                                    className="block w-full text-left px-3 py-2 text-xs hover:bg-gray-50 border-b border-gray-50 last:border-0"
                                  >
                                    <span className="font-bold font-mono">{r.course_number}</span>
                                    <span className="ml-1.5 text-gray-500">{r.title}</span>
                                    <span className="ml-1 text-gray-400">· {r.units}u</span>
                                    {inList && <span className="ml-2 text-[10px] font-semibold" style={{ color: "var(--cp-green)" }}>in list</span>}
                                  </button>
                                );
                              })}
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}
