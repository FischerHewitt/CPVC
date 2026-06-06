"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { loadSession, saveSession, persistSession } from "@/lib/session";
import { applyAddCustomCourse, applyAssignCustomCourse, applyClearCustomAssignment, applyRemoveCustomCourse, applySetCustomCourseStatus, applyUpdateCustomCourse } from "@/lib/custom-courses";
import {
  getFlowchart, inferPrerequisites, getSession, getGEAreaMap,
  getConcentrations, syncSession,
} from "@/lib/api";
import { mbpFilename } from "@/lib/mbp";
import type {
  Course, CourseSearchResult, CourseStatus, Flowchart,
  FreeElectiveStatus, GEAreaMap, TranscriptSession, Concentration,
} from "@/lib/types";
import { getOtherCredits } from "@/lib/other-credits";
import {
  expandSlashCourseNumber,
  getCourseStatus as resolveCourseStatus,
  norm as normalizeNum,
  toNormalizedSet,
} from "@/lib/course-status";
import { normalizePlannedGEPlaceholderStatuses, withPlannedGECourses } from "@/lib/ge-placeholder";

const COMS_CAPPED = {
  numbers: new Set(["COMS 4400", "COMS 4480", "COMS 4485"]),
  label: "COMS 4400, 4480, and 4485",
  cap: 3,
  electiveKey: "coms_upper_div_elective",
};

export type ToggleResult = { newStatus: CourseStatus | null; openPicker: boolean };

function isFreeElective(course: Course) {
  return course.title.toLowerCase().includes("free elective") || course.course_number.toLowerCase().startsWith("free");
}

export function useFlowchartSession(sessionId: string) {
  const router = useRouter();

  const [session, setSession] = useState<TranscriptSession | null>(null);
  const [flowchart, setFlowchart] = useState<Flowchart | null>(null);
  const [inferred, setInferred] = useState<string[]>([]);
  const [geAreaMap, setGEAreaMap] = useState<GEAreaMap>({});
  const [concentrations, setConcentrations] = useState<Concentration[]>([]);
  const [concentrationFlowchart, setConcentrationFlowchart] = useState<Flowchart | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [syncMissing, setSyncMissing] = useState(false);
  const [myNotesText, setMyNotesText] = useState("");

  const onSyncMissing = useCallback(() => setSyncMissing(true), []);

  const activeConcentration = useMemo(
    () => concentrations.find((c) => c.id === (session?.concentration ?? "none")),
    [concentrations, session?.concentration],
  );

  const resolvedFlowchart: Flowchart | null = useMemo(() => {
    if (!flowchart) return null;
    if (activeConcentration?.full_flowchart_key) return concentrationFlowchart;
    if (!activeConcentration || Object.keys(activeConcentration.slot_overrides).length === 0) return flowchart;
    const overriddenCourses = flowchart.courses.map((course) => {
      const override = activeConcentration.slot_overrides[course.id];
      return override ? { ...course, ...override } : course;
    });
    const extraCourses = (activeConcentration.extra_courses ?? []).map((c) => ({ elective_key: undefined, ...c }));
    return { ...flowchart, courses: [...overriddenCourses, ...extraCourses] };
  }, [activeConcentration, concentrationFlowchart, flowchart]);

  const otherCredits = useMemo(() => {
    if (!session || !resolvedFlowchart) return [];
    return getOtherCredits(
      resolvedFlowchart.courses,
      session.completed,
      session.inProgress,
      geAreaMap,
      session.plannedGECourses ?? {},
      session.plannedFreeElectiveCourses ?? {},
    );
  }, [geAreaMap, resolvedFlowchart, session]);

  const statusCompletedNums = useMemo(() => toNormalizedSet(session?.completed ?? []), [session]);
  const statusInProgressNums = useMemo(() => toNormalizedSet(session?.inProgress ?? []), [session]);
  const statusInferredNums = useMemo(() => toNormalizedSet(inferred), [inferred]);
  const statusKnownNums = useMemo(
    () => new Set([...statusCompletedNums, ...statusInProgressNums, ...statusInferredNums]),
    [statusCompletedNums, statusInProgressNums, statusInferredNums],
  );
  const statusGEAreaMap = useMemo(
    () => withPlannedGECourses(geAreaMap, session?.plannedGECourses ?? {}),
    [geAreaMap, session],
  );
  const statusCourseLookup = useMemo(() => {
    const lookup = new Map<string, Course>();
    if (!resolvedFlowchart) return lookup;
    for (const item of resolvedFlowchart.courses) {
      lookup.set(normalizeNum(item.course_number), item);
      for (const q of item.quarter_equivalents) lookup.set(normalizeNum(q), item);
      for (const comp of expandSlashCourseNumber(item.course_number)) lookup.set(normalizeNum(comp), item);
    }
    return lookup;
  }, [resolvedFlowchart]);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      const localSession = loadSession(sessionId);
      let s = await getSession(sessionId);
      if (s && localSession) {
        s = {
          ...s,
          concentration: s.concentration ?? localSession.concentration,
          coursePositions: Object.keys(s.coursePositions ?? {}).length > 0
            ? s.coursePositions : localSession.coursePositions,
          plannedGECourses: Object.keys(s.plannedGECourses ?? {}).length > 0
            ? s.plannedGECourses : localSession.plannedGECourses,
          plannedFreeElectiveCourses: Object.keys(s.plannedFreeElectiveCourses ?? {}).length > 0
            ? s.plannedFreeElectiveCourses : localSession.plannedFreeElectiveCourses,
        };
      }
      if (!s) s = localSession;
      if (!s) { router.replace("/"); return; }
      const normalized = normalizePlannedGEPlaceholderStatuses(s);
      s = normalized.session;
      saveSession(s);
      if (normalized.changed) void syncSession(s.sessionId, { completed: s.completed, in_progress: s.inProgress }).then((r) => { if (r === "missing") onSyncMissing(); });
      if (!cancelled) {
        setSession(s);
        setMyNotesText(s.notes ?? "");
      }
      getGEAreaMap().then((map) => { if (!cancelled) setGEAreaMap(map); });
      getConcentrations(s.major).then((list) => { if (!cancelled) setConcentrations(list); });
      inferPrerequisites(s.major, s.completed).then((inf) => { if (!cancelled) setInferred(inf); });
      getFlowchart(s.major)
        .then((fc) => { if (!cancelled) setFlowchart(fc); })
        .catch((e) => {
          console.error(e);
          if (!cancelled) setError("Could not load flowchart from the deployed backend. Check the API deployment and NEXT_PUBLIC_API_URL.");
        });
    }
    void load();
    return () => { cancelled = true; };
  }, [sessionId, router]);

  useEffect(() => {
    const key = activeConcentration?.full_flowchart_key;
    if (!key) return;
    let cancelled = false;
    getFlowchart(key).then((fc) => { if (!cancelled) setConcentrationFlowchart(fc); });
    return () => { cancelled = true; };
  }, [activeConcentration?.full_flowchart_key]);

  // ── Internal helpers ──────────────────────────────────────────────────────

  const refreshInferred = useCallback(async (nextSession: TranscriptSession) => {
    const inf = await inferPrerequisites(nextSession.major, nextSession.completed);
    setInferred(inf);
  }, []);

  const rememberGEAreaCourses = useCallback((areaId: string, courseNumbers: string[]) => {
    setGEAreaMap((cur) => ({ ...cur, [areaId]: courseNumbers }));
  }, []);

  const rememberGEAreaCourse = useCallback((areaId: string, courseNumber: string) => {
    setGEAreaMap((cur) => {
      const existing = cur[areaId] ?? [];
      if (existing.some((n) => normalizeNum(n) === normalizeNum(courseNumber))) return cur;
      return { ...cur, [areaId]: [...existing, courseNumber] };
    });
  }, []);

  const courseCandidateSet = useCallback((course: Course) =>
    new Set([course.course_number, ...course.quarter_equivalents].map(normalizeNum)),
  []);

  const courseCompletionCandidateSet = useCallback((course: Course) =>
    new Set([course.course_number, ...course.quarter_equivalents, ...(course.auto_satisfied_by ?? [])].map(normalizeNum)),
  []);

  const courseNumberCandidateSet = useCallback((courseNumber: string) => {
    const [dept, code] = courseNumber.split(/\s+/);
    const q = dept && /^\d{4}$/.test(code ?? "") ? `${dept} ${Number(code.slice(1))}` : null;
    return new Set([courseNumber, q].filter(Boolean).map((n) => normalizeNum(n as string)));
  }, []);

  const geAreaCandidateSet = useCallback((course: Course) => {
    if (!session) return new Set<string>();
    return new Set([
      (session.plannedGECourses ?? {})[course.course_number],
      course.course_number,
      ...course.quarter_equivalents,
      ...(geAreaMap[course.course_number] ?? []),
    ].filter(Boolean).map((n) => normalizeNum(n as string)));
  }, [geAreaMap, session]);

  const electiveRemoveSet = useCallback((placeholder: Course, courseNumber: string) => {
    const s = new Set([placeholder.course_number, ...placeholder.quarter_equivalents].map(normalizeNum));
    for (const c of courseNumberCandidateSet(courseNumber)) s.add(c);
    return s;
  }, [courseNumberCandidateSet]);

  const expandWithElectedCourse = useCallback((base: Set<string>, course: Course): Set<string> => {
    if (!session || !course.is_placeholder || course.category === "ge") return base;
    const elected = (session.plannedGECourses ?? {})[course.course_number];
    if (!elected) return base;
    const expanded = new Set(base);
    for (const c of courseNumberCandidateSet(elected)) expanded.add(c);
    return expanded;
  }, [session, courseNumberCandidateSet]);

  // ── Internal free-elective status update (returns whether picker should open) ──

  const setFreeElectiveStatusInternal = useCallback((placeholder: Course, status: FreeElectiveStatus): { openPicker: boolean } => {
    if (!session) return { openPicker: false };
    const current = (session.plannedFreeElectiveCourses ?? {})[placeholder.id];
    if (!current) return { openPicker: true };
    const plannedFreeElectiveCourses = {
      ...(session.plannedFreeElectiveCourses ?? {}),
      [placeholder.id]: { ...current, status },
    };
    const next = { ...session, plannedFreeElectiveCourses };
    setSession(next);
    persistSession(next, { planned_free_elective_courses: plannedFreeElectiveCourses }, onSyncMissing);
    return { openPicker: false };
  }, [session]);

  // ── Public actions ────────────────────────────────────────────────────────

  const statusForCourse = useCallback((course: Course): CourseStatus => {
    if (!session) return "incomplete";
    const free = course.is_placeholder && isFreeElective(course)
      ? (session.plannedFreeElectiveCourses ?? {})[course.id]
      : undefined;
    if (free?.status === "completed") return "completed";
    if (free?.status === "in_progress") return "in_progress";
    return resolveCourseStatus(
      course,
      statusCompletedNums, statusInProgressNums, statusInferredNums,
      statusKnownNums, statusCourseLookup, statusGEAreaMap,
    );
  }, [session, statusCompletedNums, statusInProgressNums, statusInferredNums, statusKnownNums, statusCourseLookup, statusGEAreaMap]);

  const getCappedCourseConfig = useCallback((selectedElectiveCourse: Course | null) => {
    if (!selectedElectiveCourse || !resolvedFlowchart || !session) return undefined;
    if (selectedElectiveCourse.elective_key !== COMS_CAPPED.electiveKey) return undefined;
    const totalAcrossSlots = resolvedFlowchart.courses
      .filter((c) => c.is_placeholder && c.elective_key === COMS_CAPPED.electiveKey)
      .reduce((sum, c) => sum + ((session.plannedCourseUnits ?? {})[c.id] ?? 0), 0);
    return { numbers: COMS_CAPPED.numbers, cap: COMS_CAPPED.cap, label: COMS_CAPPED.label, totalAcrossSlots };
  }, [resolvedFlowchart, session]);

  const changeConcentration = useCallback((newId: string) => {
    if (!session) return;
    const next = { ...session, concentration: newId };
    setSession(next);
    saveSession(next);
    void syncSession(session.sessionId, { concentration: newId }).then((r) => { if (r === "missing") onSyncMissing(); });
  }, [session]);

  const toggleCourseCompleted = useCallback((course: Course, selectedCourseId?: string): ToggleResult => {
    if (!session) return { newStatus: null, openPicker: false };
    if (course.is_placeholder && isFreeElective(course)) {
      const curStatus = (session.plannedFreeElectiveCourses ?? {})[course.id]?.status;
      const { openPicker } = setFreeElectiveStatusInternal(course, curStatus === "completed" ? "planned" : "completed");
      return { newStatus: null, openPicker };
    }
    const baseCourseNums = course.is_placeholder && course.category === "ge"
      ? geAreaCandidateSet(course) : courseCompletionCandidateSet(course);
    const isCompleted = session.completed.some((n) => baseCourseNums.has(normalizeNum(n)));
    const ownNums = course.is_placeholder && course.category === "ge"
      ? geAreaCandidateSet(course) : courseCandidateSet(course);
    const removeNums = isCompleted ? expandWithElectedCourse(ownNums, course) : ownNums;
    const completed = isCompleted
      ? session.completed.filter((n) => !removeNums.has(normalizeNum(n)))
      : [...session.completed.filter((n) => !removeNums.has(normalizeNum(n))), course.course_number];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((n) => !removeNums.has(normalizeNum(n)));
    const next = { ...session, completed, inProgress };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress }, onSyncMissing);
    void refreshInferred(next);
    return {
      newStatus: selectedCourseId === course.id ? (isCompleted ? "incomplete" : "completed") : null,
      openPicker: false,
    };
  }, [session, geAreaCandidateSet, courseCompletionCandidateSet, courseCandidateSet, expandWithElectedCourse, refreshInferred, setFreeElectiveStatusInternal]);

  const toggleCourseInProgress = useCallback((course: Course, selectedCourseId?: string): ToggleResult => {
    if (!session) return { newStatus: null, openPicker: false };
    if (course.is_placeholder && isFreeElective(course)) {
      const curStatus = (session.plannedFreeElectiveCourses ?? {})[course.id]?.status;
      const { openPicker } = setFreeElectiveStatusInternal(course, curStatus === "in_progress" ? "planned" : "in_progress");
      return { newStatus: null, openPicker };
    }
    const baseCourseNums = course.is_placeholder && course.category === "ge"
      ? geAreaCandidateSet(course) : courseCompletionCandidateSet(course);
    const isInProgress = session.inProgress.some((n) => baseCourseNums.has(normalizeNum(n)));
    const ownNums = course.is_placeholder && course.category === "ge"
      ? geAreaCandidateSet(course) : courseCandidateSet(course);
    const removeNums = isInProgress ? expandWithElectedCourse(ownNums, course) : ownNums;
    const inProgress = isInProgress
      ? session.inProgress.filter((n) => !removeNums.has(normalizeNum(n)))
      : [...session.inProgress.filter((n) => !removeNums.has(normalizeNum(n))), course.course_number];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((n) => !removeNums.has(normalizeNum(n)));
    const next = { ...session, completed, inProgress };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress }, onSyncMissing);
    void refreshInferred(next);
    return {
      newStatus: selectedCourseId === course.id ? (isInProgress ? "incomplete" : "in_progress") : null,
      openPicker: false,
    };
  }, [session, geAreaCandidateSet, courseCompletionCandidateSet, courseCandidateSet, expandWithElectedCourse, refreshInferred, setFreeElectiveStatusInternal]);

  const toggleGECourse = useCallback((areaId: string, courseNumber: string) => {
    if (!session) return;
    rememberGEAreaCourse(areaId, courseNumber);
    const removeSet = new Set(courseNumberCandidateSet(courseNumber));
    removeSet.add(normalizeNum(areaId));
    const isCompleted = session.completed.some((n) => removeSet.has(normalizeNum(n)));
    const completed = isCompleted
      ? session.completed.filter((n) => !removeSet.has(normalizeNum(n)))
      : [...session.completed.filter((n) => !removeSet.has(normalizeNum(n))), courseNumber];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((n) => !removeSet.has(normalizeNum(n)));
    const plannedGECourses = { ...(session.plannedGECourses ?? {}) };
    if (isCompleted && !inProgress.some((n) => removeSet.has(normalizeNum(n)))) {
      if (plannedGECourses[areaId] === courseNumber) delete plannedGECourses[areaId];
    } else {
      plannedGECourses[areaId] = courseNumber;
    }
    const next = { ...session, completed, inProgress, plannedGECourses };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress, planned_ge_courses: plannedGECourses }, onSyncMissing);
    void refreshInferred(next);
  }, [session, rememberGEAreaCourse, courseNumberCandidateSet, refreshInferred]);

  const toggleGECourseInProgress = useCallback((areaId: string, courseNumber: string) => {
    if (!session) return;
    rememberGEAreaCourse(areaId, courseNumber);
    const removeSet = new Set(courseNumberCandidateSet(courseNumber));
    removeSet.add(normalizeNum(areaId));
    const isInProgress = session.inProgress.some((n) => removeSet.has(normalizeNum(n)));
    const inProgress = isInProgress
      ? session.inProgress.filter((n) => !removeSet.has(normalizeNum(n)))
      : [...session.inProgress.filter((n) => !removeSet.has(normalizeNum(n))), courseNumber];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((n) => !removeSet.has(normalizeNum(n)));
    const plannedGECourses = { ...(session.plannedGECourses ?? {}) };
    if (isInProgress && !completed.some((n) => removeSet.has(normalizeNum(n)))) {
      if (plannedGECourses[areaId] === courseNumber) delete plannedGECourses[areaId];
    } else {
      plannedGECourses[areaId] = courseNumber;
    }
    const next = { ...session, completed, inProgress, plannedGECourses };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress, planned_ge_courses: plannedGECourses }, onSyncMissing);
    void refreshInferred(next);
  }, [session, rememberGEAreaCourse, courseNumberCandidateSet, refreshInferred]);

  const toggleGEArea = useCallback((course: Course) => {
    if (!session) return;
    const candidateSet = geAreaCandidateSet(course);
    const selected = (session.plannedGECourses ?? {})[course.course_number] ?? course.course_number;
    const isCompleted = session.completed.some((n) => candidateSet.has(normalizeNum(n)));
    const completed = isCompleted
      ? session.completed.filter((n) => !candidateSet.has(normalizeNum(n)))
      : [...session.completed.filter((n) => !candidateSet.has(normalizeNum(n))), selected];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((n) => !candidateSet.has(normalizeNum(n)));
    const next = { ...session, completed, inProgress };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress }, onSyncMissing);
    void refreshInferred(next);
  }, [session, geAreaCandidateSet, refreshInferred]);

  const toggleGEAreaInProgress = useCallback((course: Course) => {
    if (!session) return;
    const candidateSet = geAreaCandidateSet(course);
    const selected = (session.plannedGECourses ?? {})[course.course_number] ?? course.course_number;
    const isInProgress = session.inProgress.some((n) => candidateSet.has(normalizeNum(n)));
    const inProgress = isInProgress
      ? session.inProgress.filter((n) => !candidateSet.has(normalizeNum(n)))
      : [...session.inProgress.filter((n) => !candidateSet.has(normalizeNum(n))), selected];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((n) => !candidateSet.has(normalizeNum(n)));
    const next = { ...session, completed, inProgress };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress }, onSyncMissing);
    void refreshInferred(next);
  }, [session, geAreaCandidateSet, refreshInferred]);

  const planGECourse = useCallback((areaId: string, courseNumber: string, units: number) => {
    if (!session) return;
    const plannedGECourses = { ...(session.plannedGECourses ?? {}) };
    const plannedGEUnits = { ...(session.plannedGEUnits ?? {}) };
    if (plannedGECourses[areaId] === courseNumber) {
      delete plannedGECourses[areaId];
      delete plannedGEUnits[areaId];
    } else {
      plannedGECourses[areaId] = courseNumber;
      plannedGEUnits[areaId] = units;
    }
    const next = { ...session, plannedGECourses, plannedGEUnits };
    setSession(next);
    persistSession(next, { planned_ge_courses: plannedGECourses, planned_ge_units: plannedGEUnits }, onSyncMissing);
  }, [session]);

  const toggleElectiveCourse = useCallback((placeholder: Course, courseNumber: string, units: number) => {
    if (!session) return;
    const removeSet = electiveRemoveSet(placeholder, courseNumber);
    const placeholderCandidate = normalizeNum(placeholder.course_number);
    const isCompleted = session.completed.some((n) => removeSet.has(normalizeNum(n)));
    const completed = isCompleted
      ? session.completed.filter((n) => !removeSet.has(normalizeNum(n)))
      : [...session.completed.filter((n) => !removeSet.has(normalizeNum(n))), courseNumber, placeholder.course_number];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((n) => !removeSet.has(normalizeNum(n)));
    const plannedGECourses = { ...(session.plannedGECourses ?? {}), [placeholder.course_number]: courseNumber };
    const plannedGEUnits = { ...(session.plannedGEUnits ?? {}), [placeholder.course_number]: units };
    if (isCompleted && !session.inProgress.some((n) => normalizeNum(n) === placeholderCandidate)) {
      delete plannedGECourses[placeholder.course_number];
      delete plannedGEUnits[placeholder.course_number];
    }
    const next = { ...session, completed, inProgress, plannedGECourses, plannedGEUnits };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress, planned_ge_courses: plannedGECourses, planned_ge_units: plannedGEUnits }, onSyncMissing);
    void refreshInferred(next);
  }, [session, electiveRemoveSet, refreshInferred]);

  const toggleElectiveCourseInProgress = useCallback((placeholder: Course, courseNumber: string, units: number) => {
    if (!session) return;
    const removeSet = electiveRemoveSet(placeholder, courseNumber);
    const placeholderCandidate = normalizeNum(placeholder.course_number);
    const isInProgress = session.inProgress.some((n) => removeSet.has(normalizeNum(n)));
    const inProgress = isInProgress
      ? session.inProgress.filter((n) => !removeSet.has(normalizeNum(n)))
      : [...session.inProgress.filter((n) => !removeSet.has(normalizeNum(n))), courseNumber, placeholder.course_number];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((n) => !removeSet.has(normalizeNum(n)));
    const plannedGECourses = { ...(session.plannedGECourses ?? {}), [placeholder.course_number]: courseNumber };
    const plannedGEUnits = { ...(session.plannedGEUnits ?? {}), [placeholder.course_number]: units };
    if (isInProgress && !session.completed.some((n) => normalizeNum(n) === placeholderCandidate)) {
      delete plannedGECourses[placeholder.course_number];
      delete plannedGEUnits[placeholder.course_number];
    }
    const next = { ...session, completed, inProgress, plannedGECourses, plannedGEUnits };
    setSession(next);
    persistSession(next, { completed, in_progress: inProgress, planned_ge_courses: plannedGECourses, planned_ge_units: plannedGEUnits }, onSyncMissing);
    void refreshInferred(next);
  }, [session, electiveRemoveSet, refreshInferred]);

  const planElectiveCourse = useCallback((placeholder: Course, courseNumber: string, units: number) => {
    planGECourse(placeholder.course_number, courseNumber, units);
  }, [planGECourse]);

  const chooseFreeElectiveCourse = useCallback((placeholder: Course, result: CourseSearchResult, status: FreeElectiveStatus) => {
    if (!session) return;
    const plannedFreeElectiveCourses = {
      ...(session.plannedFreeElectiveCourses ?? {}),
      [placeholder.id]: { course_number: result.course_number, title: result.title, units: result.units, status },
    };
    const next = { ...session, plannedFreeElectiveCourses };
    setSession(next);
    persistSession(next, { planned_free_elective_courses: plannedFreeElectiveCourses }, onSyncMissing);
  }, [session]);

  const addCustomCourse = useCallback((col: number, course: CourseSearchResult, id: string, assignedToSlotId?: string) => {
    if (!session) return;
    const next = applyAddCustomCourse(session, col, course, id, assignedToSlotId);
    setSession(next);
    persistSession(next, { planned_custom_courses: next.customCourses ?? {} }, onSyncMissing);
  }, [session]);

  const assignCustomCourse = useCallback((customId: string, slotId: string) => {
    if (!session) return;
    const next = applyAssignCustomCourse(session, customId, slotId);
    setSession(next);
    persistSession(next, { planned_custom_courses: next.customCourses ?? {} }, onSyncMissing);
  }, [session]);

  const clearCustomAssignment = useCallback((customId: string) => {
    if (!session) return;
    const next = applyClearCustomAssignment(session, customId);
    setSession(next);
    persistSession(next, { planned_custom_courses: next.customCourses ?? {} }, onSyncMissing);
  }, [session]);

  const updateCustomCourse = useCallback((id: string, updates: Parameters<typeof applyUpdateCustomCourse>[2]) => {
    if (!session) return;
    const next = applyUpdateCustomCourse(session, id, updates);
    setSession(next);
    persistSession(next, { planned_custom_courses: next.customCourses ?? {} }, onSyncMissing);
  }, [session]);

  const setCustomCourseStatus = useCallback((id: string, status: Parameters<typeof applySetCustomCourseStatus>[2]) => {
    if (!session) return;
    const next = applySetCustomCourseStatus(session, id, status);
    setSession(next);
    persistSession(next, { planned_custom_courses: next.customCourses ?? {} }, onSyncMissing);
  }, [session]);

  const removeCustomCourse = useCallback((id: string) => {
    if (!session) return;
    const next = applyRemoveCustomCourse(session, id);
    setSession(next);
    persistSession(next, { planned_custom_courses: next.customCourses ?? {} }, onSyncMissing);
  }, [session]);

  const setFreeElectiveStatus = useCallback((placeholder: Course, status: FreeElectiveStatus): { openPicker: boolean } => {
    return setFreeElectiveStatusInternal(placeholder, status);
  }, [setFreeElectiveStatusInternal]);

  const clearFreeElectiveCourse = useCallback((placeholder: Course) => {
    if (!session) return;
    const plannedFreeElectiveCourses = { ...(session.plannedFreeElectiveCourses ?? {}) };
    delete plannedFreeElectiveCourses[placeholder.id];
    const next = { ...session, plannedFreeElectiveCourses };
    setSession(next);
    persistSession(next, { planned_free_elective_courses: plannedFreeElectiveCourses }, onSyncMissing);
  }, [session]);

  const setSlotUnits = useCallback((courseId: string, units: number | null) => {
    if (!session) return;
    const plannedCourseUnits = { ...(session.plannedCourseUnits ?? {}) };
    if (units === null) delete plannedCourseUnits[courseId];
    else plannedCourseUnits[courseId] = units;
    const next = { ...session, plannedCourseUnits };
    setSession(next);
    persistSession(next, { planned_course_units: plannedCourseUnits }, onSyncMissing);
  }, [session]);

  const moveCourse = useCallback((courseId: string, targetCol: number, targetRow: number, targetCourseId?: string) => {
    if (!session || !resolvedFlowchart) return;
    const dragged = resolvedFlowchart.courses.find((c) => c.id === courseId);
    if (!dragged) return;
    const positions = { ...(session.coursePositions ?? {}) };
    const draggedPos = positions[courseId] ?? { grid_col: dragged.grid_col, grid_row: dragged.grid_row };
    positions[courseId] = { grid_col: targetCol, grid_row: targetRow };
    if (targetCourseId) positions[targetCourseId] = draggedPos;
    const next = { ...session, coursePositions: positions };
    setSession(next);
    persistSession(next, { course_positions: positions as Record<string, unknown> }, onSyncMissing);
  }, [session, resolvedFlowchart]);

  const resetCourseLayout = useCallback(() => {
    if (!session) return;
    const next = { ...session, coursePositions: {} };
    setSession(next);
    persistSession(next, { course_positions: {} }, onSyncMissing);
  }, [session]);

  const downloadSession = useCallback(() => {
    if (!session) return;
    const blob = new Blob([JSON.stringify(session, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = mbpFilename(session);
    a.click();
    URL.revokeObjectURL(url);
  }, [session]);

  const importCSV = useCallback((csvCompleted: string[], csvInProgress: string[]) => {
    if (!session) return;
    const next = { ...session, completed: csvCompleted, inProgress: csvInProgress };
    setSession(next);
    persistSession(next, { completed: csvCompleted, in_progress: csvInProgress }, onSyncMissing);
    void refreshInferred(next);
  }, [session, refreshInferred]);

  const updateMyNotes = useCallback((text: string) => {
    if (!session) return;
    setMyNotesText(text);
    const next = { ...session, notes: text };
    setSession(next);
    saveSession(next);
  }, [session]);

  const togglePickedCourse = useCallback((courseNumber: string) => {
    if (!session) return;
    const n = normalizeNum(courseNumber);
    const isIn = session.completed.some((c) => normalizeNum(c) === n);
    const nextCompleted = isIn
      ? session.completed.filter((c) => normalizeNum(c) !== n)
      : [...session.completed, courseNumber];
    const next = { ...session, completed: nextCompleted };
    setSession(next);
    persistSession(next, { completed: nextCompleted }, onSyncMissing);
    void refreshInferred(next);
  }, [session, refreshInferred]);

  const togglePickedCourseInProgress = useCallback((courseNumber: string) => {
    if (!session) return;
    const n = normalizeNum(courseNumber);
    const isIn = session.inProgress.some((c) => normalizeNum(c) === n);
    const nextInProgress = isIn
      ? session.inProgress.filter((c) => normalizeNum(c) !== n)
      : [...session.inProgress, courseNumber];
    const next = { ...session, inProgress: nextInProgress };
    setSession(next);
    persistSession(next, { in_progress: nextInProgress }, onSyncMissing);
  }, [session]);

  return {
    session,
    flowchart,
    resolvedFlowchart,
    inferred,
    geAreaMap,
    concentrations,
    activeConcentration,
    otherCredits,
    error,
    syncMissing,
    myNotesText,
    statusCompletedNums,
    statusInProgressNums,
    statusInferredNums,
    statusGEAreaMap,
    statusForCourse,
    getCappedCourseConfig,
    rememberGEAreaCourses,
    changeConcentration,
    toggleCourseCompleted,
    toggleCourseInProgress,
    toggleGECourse,
    toggleGECourseInProgress,
    toggleGEArea,
    toggleGEAreaInProgress,
    planGECourse,
    toggleElectiveCourse,
    toggleElectiveCourseInProgress,
    planElectiveCourse,
    chooseFreeElectiveCourse,
    setFreeElectiveStatus,
    clearFreeElectiveCourse,
    addCustomCourse,
    updateCustomCourse,
    assignCustomCourse,
    clearCustomAssignment,
    setCustomCourseStatus,
    removeCustomCourse,
    setSlotUnits,
    moveCourse,
    resetCourseLayout,
    downloadSession,
    importCSV,
    updateMyNotes,
    togglePickedCourse,
    togglePickedCourseInProgress,
  };
}
