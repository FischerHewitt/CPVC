"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { loadSession } from "@/lib/session";
import { getFlowchart, inferPrerequisites } from "@/lib/api";
import type { Course, CourseStatus, Flowchart, TranscriptSession } from "@/lib/types";
import FlowchartGrid from "@/components/FlowchartGrid";
import CourseDetailPanel from "@/components/CourseDetailPanel";

export default function FlowchartPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();

  const [session, setSession] = useState<TranscriptSession | null>(null);
  const [flowchart, setFlowchart] = useState<Flowchart | null>(null);
  const [inferred, setInferred] = useState<string[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<CourseStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const s = loadSession(sessionId);
    if (!s) { router.replace("/"); return; }
    setSession(s);

    getFlowchart(s.major)
      .then(async (fc) => {
        setFlowchart(fc);
        // Run inference once we have both the session and flowchart
        const inf = await inferPrerequisites(s.major, s.completed);
        setInferred(inf);
      })
      .catch(() => setError("Could not load flowchart. Make sure the backend is running."));
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

  const allKnown = new Set([...session.completed, ...session.inProgress, ...inferred]);

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
          <div className="flex items-baseline gap-3 mb-5">
            <h1 className="text-lg font-bold" style={{ color: "var(--cp-green)" }}>
              {flowchart.major}
            </h1>
            <span className="text-gray-400 text-sm">4-Year Semester Flowchart</span>
          </div>

          <FlowchartGrid
            flowchart={flowchart}
            session={session}
            inferred={inferred}
            onCourseClick={(course, status) => {
              setSelectedCourse(course);
              setSelectedStatus(status);
            }}
          />
        </div>
      </main>

      <CourseDetailPanel
        course={selectedCourse}
        status={selectedStatus}
        allCourses={flowchart.courses}
        completedSet={allKnown}
        onClose={() => { setSelectedCourse(null); setSelectedStatus(null); }}
      />
    </div>
  );
}
