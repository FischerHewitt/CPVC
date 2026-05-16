"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { loadSession, saveSession, persistSession } from "@/lib/session";
import { getFlowchart, inferPrerequisites, getSession, getGEAreaMap, getConcentrations, syncSession } from "@/lib/api";
import type { Course, CourseStatus, Flowchart, GEAreaMap, TranscriptSession, Concentration } from "@/lib/types";
import FlowchartGrid from "@/components/FlowchartGrid";
import CourseDetailPanel from "@/components/CourseDetailPanel";
import GEDetailPanel from "@/components/GEDetailPanel";
import ElectiveDetailPanel from "@/components/ElectiveDetailPanel";
import ManualCourseChecklist from "@/components/ManualCourseChecklist";

export default function FlowchartPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();

  const [session, setSession] = useState<TranscriptSession | null>(null);
  const [flowchart, setFlowchart] = useState<Flowchart | null>(null);
  const [inferred, setInferred] = useState<string[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<CourseStatus | null>(null);
  const [selectedGECourse, setSelectedGECourse] = useState<Course | null>(null);
  const [selectedElectiveCourse, setSelectedElectiveCourse] = useState<Course | null>(null);
  const [geAreaMap, setGEAreaMap] = useState<GEAreaMap>({});
  const [checklistOpen, setChecklistOpen] = useState(false);
  const [concentrations, setConcentrations] = useState<Concentration[]>([]);
  const [error, setError] = useState<string | null>(null);

  const activeConcentration = useMemo(
    () => concentrations.find((c) => c.id === (session?.concentration ?? "none")),
    [concentrations, session?.concentration],
  );

  const resolvedFlowchart: Flowchart | null = useMemo(() => {
    if (!flowchart) return null;
    if (!activeConcentration || Object.keys(activeConcentration.slot_overrides).length === 0) {
      return flowchart;
    }

    return {
      ...flowchart,
      courses: flowchart.courses.map((course) => {
        const override = activeConcentration.slot_overrides[course.id];
        if (!override) return course;
        return { ...course, ...override };
      }),
    };
  }, [activeConcentration, flowchart]);

  const rememberGEAreaCourses = useCallback((areaId: string, courseNumbers: string[]) => {
    setGEAreaMap((current) => ({
      ...current,
      [areaId]: courseNumbers,
    }));
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      // Try backend first, fall back to localStorage
      const localSession = loadSession(sessionId);
      let s = await getSession(sessionId);
      if (s && localSession) {
        s = {
          ...s,
          coursePositions: Object.keys(s.coursePositions ?? {}).length > 0
            ? s.coursePositions
            : localSession.coursePositions,
          plannedGECourses: Object.keys(s.plannedGECourses ?? {}).length > 0
            ? s.plannedGECourses
            : localSession.plannedGECourses,
        };
      }
      if (!s) s = localSession;
      if (!s) { router.replace("/"); return; }

      // Write backend data into localStorage so it's available offline
      saveSession(s);
      if (!cancelled) setSession(s);

      // Fire all background fetches in parallel
      getGEAreaMap().then((map) => { if (!cancelled) setGEAreaMap(map); });
      getConcentrations(s.major).then((list) => { if (!cancelled) setConcentrations(list); });
      inferPrerequisites(s.major, s.completed).then((inf) => { if (!cancelled) setInferred(inf); });

      getFlowchart(s.major)
        .then((fc) => {
          if (!cancelled) setFlowchart(fc);
        })
        .catch((e) => {
          console.error(e);
          if (!cancelled) {
            setError("Could not load flowchart from the deployed backend. Check the API deployment and NEXT_PUBLIC_API_URL.");
          }
        });
    }

    void load();

    return () => {
      cancelled = true;
    };
  }, [sessionId, router]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--cp-bg)" }}>
        <div className="text-center">
          <div className="text-red-500 font-semibold mb-2">{error}</div>
          <button onClick={() => router.push("/")} className="text-sm text-gray-500 underline">← Start over</button>
        </div>
      </div>
    );
  }

  if (!session || !flowchart || !resolvedFlowchart) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--cp-bg)" }}>
        <div className="text-gray-400 text-sm">Loading flowchart…</div>
      </div>
    );
  }

  const refreshInferred = async (nextSession: TranscriptSession) => {
    const inf = await inferPrerequisites(nextSession.major, nextSession.completed);
    setInferred(inf);
  };

  const normalizeCourseNumber = (courseNumber: string) => courseNumber.toUpperCase().trim().replace(/\s+/g, " ");

  const isFreeElective = (course: Course) =>
    course.title.toLowerCase().includes("free elective") || course.course_number.toLowerCase().startsWith("free");

  const courseCandidateSet = (course: Course) => {
    return new Set([course.course_number, ...course.quarter_equivalents].map(normalizeCourseNumber));
  };

  const geAreaCandidateSet = (course: Course) => {
    return new Set([
      course.course_number,
      ...course.quarter_equivalents,
      ...(geAreaMap[course.course_number] ?? []),
    ].map(normalizeCourseNumber));
  };

  const courseNumberCandidateSet = (courseNumber: string) => {
    const [dept, code] = courseNumber.split(/\s+/);
    const quarterEquivalent = dept && /^\d{4}$/.test(code ?? "")
      ? `${dept} ${Number(code.slice(1))}`
      : null;
    return new Set([courseNumber, quarterEquivalent].filter(Boolean).map((num) => normalizeCourseNumber(num as string)));
  };

  const toggleGECourse = (areaId: string, courseNumber: string) => {
    const candidateSet = courseNumberCandidateSet(courseNumber);
    const areaCandidate = normalizeCourseNumber(areaId);
    const removeSet = new Set(candidateSet);
    removeSet.add(areaCandidate);

    const isCompleted = session.completed.some((num) => removeSet.has(normalizeCourseNumber(num)));
    const completed = isCompleted
      ? session.completed.filter((num) => !removeSet.has(normalizeCourseNumber(num)))
      : [
          ...session.completed.filter((num) => !removeSet.has(normalizeCourseNumber(num))),
          courseNumber,
          areaId,
        ];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((num) => !removeSet.has(normalizeCourseNumber(num)));
    const nextSession = { ...session, completed, inProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress });
    void refreshInferred(nextSession);
  };

  const toggleGECourseInProgress = (areaId: string, courseNumber: string) => {
    const candidateSet = courseNumberCandidateSet(courseNumber);
    const areaCandidate = normalizeCourseNumber(areaId);
    const removeSet = new Set(candidateSet);
    removeSet.add(areaCandidate);

    const isInProgress = session.inProgress.some((num) => removeSet.has(normalizeCourseNumber(num)));

    const inProgress = isInProgress
      ? session.inProgress.filter((num) => !removeSet.has(normalizeCourseNumber(num)))
      : [
          ...session.inProgress.filter((num) => !removeSet.has(normalizeCourseNumber(num))),
          courseNumber,
          areaId,
        ];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((num) => !removeSet.has(normalizeCourseNumber(num)));
    const nextSession = { ...session, completed, inProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress });
    void refreshInferred(nextSession);
  };

  const toggleGEArea = (course: Course) => {
    const candidateSet = geAreaCandidateSet(course);
    const isCompleted = session.completed.some((courseNumber) => candidateSet.has(normalizeCourseNumber(courseNumber)));

    const completed = isCompleted
      ? session.completed.filter((courseNumber) => !candidateSet.has(normalizeCourseNumber(courseNumber)))
      : [...session.completed, course.course_number];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((courseNumber) => !candidateSet.has(normalizeCourseNumber(courseNumber)));

    const nextSession = { ...session, completed, inProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress });
    void refreshInferred(nextSession);
  };

  const toggleGEAreaInProgress = (course: Course) => {
    const candidateSet = geAreaCandidateSet(course);
    const isInProgress = session.inProgress.some((courseNumber) => candidateSet.has(normalizeCourseNumber(courseNumber)));

    const inProgress = isInProgress
      ? session.inProgress.filter((courseNumber) => !candidateSet.has(normalizeCourseNumber(courseNumber)))
      : [
          ...session.inProgress.filter((courseNumber) => !candidateSet.has(normalizeCourseNumber(courseNumber))),
          course.course_number,
        ];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((courseNumber) => !candidateSet.has(normalizeCourseNumber(courseNumber)));

    const nextSession = { ...session, completed, inProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress });
    void refreshInferred(nextSession);
  };

  const planGECourse = (areaId: string, courseNumber: string, units: number) => {
    const plannedGECourses = { ...(session.plannedGECourses ?? {}) };
    const plannedGEUnits   = { ...(session.plannedGEUnits   ?? {}) };

    if (plannedGECourses[areaId] === courseNumber) {
      delete plannedGECourses[areaId];
      delete plannedGEUnits[areaId];
    } else {
      plannedGECourses[areaId] = courseNumber;
      plannedGEUnits[areaId]   = units;
    }

    const nextSession = { ...session, plannedGECourses, plannedGEUnits };
    setSession(nextSession);
    persistSession(nextSession, { planned_ge_courses: plannedGECourses, planned_ge_units: plannedGEUnits });
  };

  const electiveRemoveSet = (placeholder: Course, courseNumber: string) => {
    const removeSet = courseCandidateSet(placeholder);
    for (const candidate of courseNumberCandidateSet(courseNumber)) {
      removeSet.add(candidate);
    }
    return removeSet;
  };

  const toggleElectiveCourse = (placeholder: Course, courseNumber: string) => {
    const removeSet = electiveRemoveSet(placeholder, courseNumber);
    const placeholderCandidate = normalizeCourseNumber(placeholder.course_number);
    const isCompleted = session.completed.some((num) => removeSet.has(normalizeCourseNumber(num)));
    const completed = isCompleted
      ? session.completed.filter((num) => !removeSet.has(normalizeCourseNumber(num)))
      : [
          ...session.completed.filter((num) => !removeSet.has(normalizeCourseNumber(num))),
          courseNumber,
          placeholder.course_number,
        ];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((num) => !removeSet.has(normalizeCourseNumber(num)));
    const plannedGECourses = {
      ...(session.plannedGECourses ?? {}),
      [placeholder.course_number]: courseNumber,
    };
    if (isCompleted && !session.inProgress.some((num) => normalizeCourseNumber(num) === placeholderCandidate)) {
      delete plannedGECourses[placeholder.course_number];
    }
    const nextSession = { ...session, completed, inProgress, plannedGECourses };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress, planned_ge_courses: plannedGECourses });
    void refreshInferred(nextSession);
  };

  const toggleElectiveCourseInProgress = (placeholder: Course, courseNumber: string) => {
    const removeSet = electiveRemoveSet(placeholder, courseNumber);
    const placeholderCandidate = normalizeCourseNumber(placeholder.course_number);
    const isInProgress = session.inProgress.some((num) => removeSet.has(normalizeCourseNumber(num)));
    const inProgress = isInProgress
      ? session.inProgress.filter((num) => !removeSet.has(normalizeCourseNumber(num)))
      : [
          ...session.inProgress.filter((num) => !removeSet.has(normalizeCourseNumber(num))),
          courseNumber,
          placeholder.course_number,
        ];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((num) => !removeSet.has(normalizeCourseNumber(num)));
    const plannedGECourses = {
      ...(session.plannedGECourses ?? {}),
      [placeholder.course_number]: courseNumber,
    };
    if (isInProgress && !session.completed.some((num) => normalizeCourseNumber(num) === placeholderCandidate)) {
      delete plannedGECourses[placeholder.course_number];
    }
    const nextSession = { ...session, completed, inProgress, plannedGECourses };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress, planned_ge_courses: plannedGECourses });
    void refreshInferred(nextSession);
  };

  const planElectiveCourse = (placeholder: Course, courseNumber: string, units: number) => {
    planGECourse(placeholder.course_number, courseNumber, units);
  };

  const toggleCourseCompleted = (course: Course) => {
    if (course.is_placeholder && !isFreeElective(course)) return;

    const allCourseNums = courseCandidateSet(course);
    const isCompleted = session.completed.some((courseNum) => allCourseNums.has(normalizeCourseNumber(courseNum)));
    const completed = isCompleted
      ? session.completed.filter((courseNum) => !allCourseNums.has(normalizeCourseNumber(courseNum)))
      : [...session.completed.filter((courseNum) => !allCourseNums.has(normalizeCourseNumber(courseNum))), course.course_number];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((courseNum) => !allCourseNums.has(normalizeCourseNumber(courseNum)));

    const nextSession = { ...session, completed, inProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress });
    void refreshInferred(nextSession);

    if (selectedCourse?.id === course.id) {
      setSelectedStatus(isCompleted ? "incomplete" : "completed");
    }
  };

  const toggleCourseInProgress = (course: Course) => {
    if (course.is_placeholder && !isFreeElective(course)) return;

    const allCourseNums = courseCandidateSet(course);
    const isInProgress = session.inProgress.some((courseNum) => allCourseNums.has(normalizeCourseNumber(courseNum)));
    const inProgress = isInProgress
      ? session.inProgress.filter((courseNum) => !allCourseNums.has(normalizeCourseNumber(courseNum)))
      : [
          ...session.inProgress.filter((courseNum) => !allCourseNums.has(normalizeCourseNumber(courseNum))),
          course.course_number,
        ];
    const completed = isInProgress
      ? session.completed
      : session.completed.filter((courseNum) => !allCourseNums.has(normalizeCourseNumber(courseNum)));

    const nextSession = { ...session, completed, inProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress });
    void refreshInferred(nextSession);

    if (selectedCourse?.id === course.id) {
      setSelectedStatus(isInProgress ? "incomplete" : "in_progress");
    }
  };

  const moveCourse = (
    courseId: string,
    targetCol: number,
    targetRow: number,
    targetCourseId?: string,
  ) => {
    const draggedCourse = resolvedFlowchart.courses.find((course) => course.id === courseId);
    if (!draggedCourse) return;

    const positions = { ...(session.coursePositions ?? {}) };
    const draggedPosition = positions[courseId] ?? {
      grid_col: draggedCourse.grid_col,
      grid_row: draggedCourse.grid_row,
    };

    positions[courseId] = { grid_col: targetCol, grid_row: targetRow };

    if (targetCourseId) {
      positions[targetCourseId] = draggedPosition;
    }

    const nextSession = { ...session, coursePositions: positions };
    setSession(nextSession);
    persistSession(nextSession, { course_positions: positions as Record<string, unknown> });
  };

  const resetCourseLayout = () => {
    const nextSession = { ...session, coursePositions: {} };
    setSession(nextSession);
    persistSession(nextSession, { course_positions: {} });
  };

  const changeConcentration = (newId: string) => {
    const nextSession = { ...session, concentration: newId === "none" ? undefined : newId };
    setSession(nextSession);
    saveSession(nextSession);
    void syncSession(session.sessionId, { concentration: newId === "none" ? undefined : newId });
  };

  const importCSV = (csvCompleted: string[], csvInProgress: string[]) => {
    const nextSession = { ...session, completed: csvCompleted, inProgress: csvInProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed: csvCompleted, in_progress: csvInProgress });
    void refreshInferred(nextSession);
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--cp-bg)" }}>
      {/* Header */}
      <header
        className="px-6 py-3 flex items-center gap-4 flex-wrap relative"
        style={{
          background: "#002D72",
          backgroundImage: [
            "linear-gradient(rgba(255,255,255,0.06) 1px, transparent 1px)",
            "linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px)",
          ].join(", "),
          backgroundSize: "22px 22px",
          borderBottom: "2px solid rgba(255,255,255,0.18)",
        }}
      >
        <button onClick={() => router.push("/")} className="text-white/60 hover:text-white text-sm font-mono">← Back</button>
        <div className="text-white font-bold text-sm font-mono">{session.studentName}</div>
        <div className="text-white/50 text-sm">·</div>
        <div className="text-white/75 text-sm font-mono">{flowchart.major}</div>
        {concentrations.length > 0 && (
          <>
            <div className="text-white/35 text-sm">·</div>
            <select
              value={session.concentration ?? "none"}
              onChange={(e) => changeConcentration(e.target.value)}
              className="text-sm rounded px-2 py-0.5 font-mono"
              style={{ background: "rgba(255,255,255,0.12)", color: "white", border: "1px solid rgba(255,255,255,0.25)" }}
            >
              {concentrations.map((c) => (
                <option key={c.id} value={c.id} style={{ background: "#002D72", color: "white" }}>
                  {c.label}
                </option>
              ))}
            </select>
          </>
        )}
        <div className="ml-auto flex items-center gap-4">
          <Link href="/support" className="text-white/60 hover:text-white text-sm transition-colors font-mono">Support</Link>
          <div className="flex items-center gap-2">
            <Image src="/mb-logo.png" alt="Mustang Blueprints" width={28} height={28} className="rounded flex-shrink-0" style={{ border: "2px solid rgba(255,255,255,0.85)" }} />
            <span className="text-white font-bold text-xs font-mono tracking-widest uppercase">Mustang Blueprints</span>
          </div>
        </div>
      </header>

      <main className="flex-1 p-6">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-5">
          <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-baseline gap-3">
              <h1 className="text-lg font-bold" style={{ color: "var(--cp-green)" }}>
                {flowchart.major}
              </h1>
              <span className="text-gray-400 text-sm">4-Year Semester Flowchart</span>
            </div>
            <button
              onClick={resetCourseLayout}
              className="w-fit rounded border border-gray-300 px-3 py-2 text-sm font-semibold text-gray-600 transition-colors hover:bg-gray-50"
            >
              Reset Layout
            </button>
            <button
              onClick={() => setChecklistOpen(true)}
              className="w-fit rounded border border-green-800 px-3 py-2 text-sm font-semibold text-green-900 transition-colors hover:bg-green-50"
            >
              Course Checklist
            </button>
          </div>

          <FlowchartGrid
            flowchart={resolvedFlowchart}
            session={session}
            inferred={inferred}
            geAreaMap={geAreaMap}
            onToggleCourseCompleted={toggleCourseCompleted}
            onToggleCourseInProgress={toggleCourseInProgress}
            onMoveCourse={moveCourse}
            onCourseClick={(course, status) => {
              if (course.is_placeholder && (course.category === "ge" || course.course_number.startsWith("ART 3000+"))) {
                setSelectedGECourse(course);
                setSelectedCourse(null);
                setSelectedElectiveCourse(null);
              } else if (course.is_placeholder && !isFreeElective(course)) {
                setSelectedElectiveCourse(course);
                setSelectedCourse(null);
                setSelectedGECourse(null);
              } else {
                setSelectedCourse(course);
                setSelectedStatus(status);
                setSelectedGECourse(null);
                setSelectedElectiveCourse(null);
              }
            }}
          />
        </div>
      </main>

      <CourseDetailPanel
        course={selectedCourse}
        status={selectedStatus}
        allCourses={resolvedFlowchart.courses}
        completed={session.completed}
        inProgress={session.inProgress}
        inferred={inferred}
        onClose={() => { setSelectedCourse(null); setSelectedStatus(null); }}
      />

      <GEDetailPanel
        course={selectedGECourse}
        completedSet={new Set(session.completed)}
        inProgressSet={new Set(session.inProgress)}
        plannedGECourses={session.plannedGECourses ?? {}}
        onToggleGECourse={toggleGECourse}
        onToggleGECourseInProgress={toggleGECourseInProgress}
        onPlanGECourse={planGECourse}
        onAreaLoaded={rememberGEAreaCourses}
        onClose={() => setSelectedGECourse(null)}
      />

      <ElectiveDetailPanel
        course={selectedElectiveCourse}
        completedSet={new Set(session.completed)}
        inProgressSet={new Set(session.inProgress)}
        plannedElectiveCourses={session.plannedGECourses ?? {}}
        onToggleElectiveCourse={toggleElectiveCourse}
        onToggleElectiveCourseInProgress={toggleElectiveCourseInProgress}
        onPlanElectiveCourse={planElectiveCourse}
        onClose={() => setSelectedElectiveCourse(null)}
      />

      {/* Disclaimer */}
      <footer className="px-6 py-3 text-center text-xs text-gray-400 border-t border-gray-100 bg-white">
        Mustang Blueprints is an independent student project — <strong>not affiliated with Cal Poly</strong>. Always verify your plan with your academic advisor.
      </footer>

      <ManualCourseChecklist
        open={checklistOpen}
        courses={resolvedFlowchart.courses}
        completed={session.completed}
        inProgress={session.inProgress}
        geAreaMap={geAreaMap}
        plannedGECourses={session.plannedGECourses ?? {}}
        onToggleCourse={toggleCourseCompleted}
        onToggleCourseInProgress={toggleCourseInProgress}
        onToggleGEArea={toggleGEArea}
        onToggleGEAreaInProgress={toggleGEAreaInProgress}
        onImportCSV={importCSV}
        onClose={() => setChecklistOpen(false)}
      />
    </div>
  );
}
