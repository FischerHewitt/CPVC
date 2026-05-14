"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { loadSession, saveSession, persistSession } from "@/lib/session";
import { getFlowchart, inferPrerequisites, getSession, getGEAreaMap } from "@/lib/api";
import type { Course, CourseStatus, Flowchart, GEAreaMap, TranscriptSession } from "@/lib/types";
import FlowchartGrid from "@/components/FlowchartGrid";
import CourseDetailPanel from "@/components/CourseDetailPanel";
import GEDetailPanel from "@/components/GEDetailPanel";
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
  const [geAreaMap, setGEAreaMap] = useState<GEAreaMap>({});
  const [checklistOpen, setChecklistOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

      // Fetch GE area map in parallel with flowchart
      getGEAreaMap().then((map) => { if (!cancelled) setGEAreaMap(map); });

      getFlowchart(s.major)
        .then(async (fc) => {
          if (cancelled) return;
          setFlowchart(fc);
          const inf = await inferPrerequisites(s!.major, s!.completed);
          if (!cancelled) setInferred(inf);
        })
        .catch(() => {
          if (!cancelled) setError("Could not load flowchart. Make sure the backend is running.");
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

  if (!session || !flowchart) {
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

  const toggleGECourse = (courseNumber: string) => {
    const isCompleted = session.completed.includes(courseNumber);
    const completed = isCompleted
      ? session.completed.filter((n) => n !== courseNumber)
      : [...session.completed, courseNumber];
    const nextSession = { ...session, completed };
    setSession(nextSession);
    persistSession(nextSession, { completed });
    void refreshInferred(nextSession);
  };

  const toggleGEArea = (course: Course) => {
    const normalize = (courseNumber: string) => courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
    const candidates = [
      course.course_number,
      ...course.quarter_equivalents,
      ...(geAreaMap[course.course_number] ?? []),
    ];
    const candidateSet = new Set(candidates.map(normalize));
    const isCompleted = session.completed.some((courseNumber) => candidateSet.has(normalize(courseNumber)));

    const completed = isCompleted
      ? session.completed.filter((courseNumber) => !candidateSet.has(normalize(courseNumber)))
      : [...session.completed, course.course_number];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((courseNumber) => !candidateSet.has(normalize(courseNumber)));

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

  const toggleCourseCompleted = (course: Course) => {
    if (course.is_placeholder && course.category === "ge") return;

    const allCourseNums = new Set([course.course_number, ...course.quarter_equivalents]);
    const isCompleted = session.completed.some((courseNum) => allCourseNums.has(courseNum));
    const completed = isCompleted
      ? session.completed.filter((courseNum) => !allCourseNums.has(courseNum))
      : [...session.completed.filter((courseNum) => !allCourseNums.has(courseNum)), course.course_number];
    const inProgress = isCompleted
      ? session.inProgress
      : session.inProgress.filter((courseNum) => !allCourseNums.has(courseNum));

    const nextSession = { ...session, completed, inProgress };
    setSession(nextSession);
    persistSession(nextSession, { completed, in_progress: inProgress });
    void refreshInferred(nextSession);

    if (selectedCourse?.id === course.id) {
      setSelectedStatus(isCompleted ? "incomplete" : "completed");
    }
  };

  const moveCourse = (
    courseId: string,
    targetCol: number,
    targetRow: number,
    targetCourseId?: string,
  ) => {
    const draggedCourse = flowchart.courses.find((course) => course.id === courseId);
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

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--cp-bg)" }}>
      {/* Header */}
      <header style={{ background: "var(--cp-green)" }} className="px-6 py-3 flex items-center gap-4">
        <button onClick={() => router.push("/")} className="text-white/70 hover:text-white text-sm">← Back</button>
        <div className="text-white font-bold text-sm">{session.studentName}</div>
        <div className="text-white/60 text-sm">·</div>
        <div className="text-white/80 text-sm">{flowchart.major}</div>
        <div className="ml-auto text-white font-bold text-sm">CAL POLY</div>
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
              onClick={() => setChecklistOpen(true)}
              className="w-fit rounded border border-green-800 px-3 py-2 text-sm font-semibold text-green-900 transition-colors hover:bg-green-50"
            >
              Course Checklist
            </button>
          </div>

          <FlowchartGrid
            flowchart={flowchart}
            session={session}
            inferred={inferred}
            geAreaMap={geAreaMap}
            onToggleCourseCompleted={toggleCourseCompleted}
            onMoveCourse={moveCourse}
            onCourseClick={(course, status) => {
              if (course.is_placeholder && course.category === "ge") {
                setSelectedGECourse(course);
                setSelectedCourse(null);
              } else {
                setSelectedCourse(course);
                setSelectedStatus(status);
                setSelectedGECourse(null);
              }
            }}
          />
        </div>
      </main>

      <CourseDetailPanel
        course={selectedCourse}
        status={selectedStatus}
        allCourses={flowchart.courses}
        completed={session.completed}
        inProgress={session.inProgress}
        inferred={inferred}
        onClose={() => { setSelectedCourse(null); setSelectedStatus(null); }}
      />

      <GEDetailPanel
        course={selectedGECourse}
        completedSet={new Set(session.completed)}
        plannedGECourses={session.plannedGECourses ?? {}}
        onToggleGECourse={toggleGECourse}
        onPlanGECourse={planGECourse}
        onClose={() => setSelectedGECourse(null)}
      />

      <ManualCourseChecklist
        open={checklistOpen}
        courses={flowchart.courses}
        completed={session.completed}
        inProgress={session.inProgress}
        geAreaMap={geAreaMap}
        plannedGECourses={session.plannedGECourses ?? {}}
        onToggleCourse={toggleCourseCompleted}
        onToggleGEArea={toggleGEArea}
        onClose={() => setChecklistOpen(false)}
      />
    </div>
  );
}
