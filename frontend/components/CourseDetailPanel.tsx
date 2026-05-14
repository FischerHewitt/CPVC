"use client";

import { useEffect, useState } from "react";
import type { Course, CourseStatus, Professor } from "@/lib/types";
import { getProfessors } from "@/lib/api";

interface Props {
  course: Course | null;
  status: CourseStatus | null;
  allCourses: Course[];
  completedSet: Set<string>;
  onClose: () => void;
}

const CATEGORY_LABEL: Record<string, string> = {
  major: "Major Requirement",
  support: "Support Requirement",
  concentration: "Concentration",
  ge: "General Education",
};

export default function CourseDetailPanel({ course, status, allCourses, completedSet, onClose }: Props) {
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [loadingProfs, setLoadingProfs] = useState(false);

  useEffect(() => {
    if (!course) return;
    setProfessors([]);
    setLoadingProfs(true);
    getProfessors(course.course_number)
      .then(setProfessors)
      .finally(() => setLoadingProfs(false));
  }, [course?.course_number]);

  if (!course) return null;

  const prereqCourses = allCourses.filter((c) =>
    course.prerequisites.includes(c.course_number)
  );

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/20 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="fixed right-0 top-0 h-full w-80 bg-white shadow-2xl z-50 flex flex-col overflow-y-auto">
        {/* Header */}
        <div className="px-5 py-4 border-b border-gray-100 flex items-start justify-between"
             style={{ background: "var(--cp-green)" }}>
          <div>
            <div className="text-white/70 text-xs font-medium">{course.course_number}</div>
            <div className="text-white font-bold text-base leading-tight mt-0.5">{course.title}</div>
            <div className="text-white/70 text-xs mt-1">
              {course.units} units · {CATEGORY_LABEL[course.category]}
            </div>
          </div>
          <button onClick={onClose} className="text-white/70 hover:text-white text-xl leading-none ml-3 mt-0.5">×</button>
        </div>

        <div className="flex-1 px-5 py-4 flex flex-col gap-5">
          {/* Status */}
          <div className="flex items-center gap-2">
            {status === "completed" && (
              <span className="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-1 rounded-full">✓ Completed</span>
            )}
            {status === "in_progress" && (
              <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-1 rounded-full">In Progress</span>
            )}
            {status === "incomplete" && (
              <span className="bg-yellow-100 text-yellow-800 text-xs font-semibold px-2.5 py-1 rounded-full">Not Yet Taken</span>
            )}
            {status === "locked" && (
              <span className="bg-gray-100 text-gray-600 text-xs font-semibold px-2.5 py-1 rounded-full">🔒 Prerequisites Needed</span>
            )}
          </div>

          {/* Quarter equivalents */}
          {course.quarter_equivalents.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Quarter Equivalent</div>
              <div className="flex flex-wrap gap-1.5">
                {course.quarter_equivalents.map((q) => (
                  <span key={q} className="bg-gray-100 text-gray-700 text-xs px-2 py-0.5 rounded font-mono">{q}</span>
                ))}
              </div>
            </div>
          )}

          {/* Prerequisites */}
          {prereqCourses.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Prerequisites</div>
              <div className="flex flex-col gap-1.5">
                {prereqCourses.map((p) => (
                  <div key={p.id} className="flex items-center justify-between text-sm">
                    <span className="font-medium text-gray-700">{p.course_number}</span>
                    {completedSet.has(p.course_number) ? (
                      <span className="text-green-600 text-xs font-semibold">✓ Done</span>
                    ) : (
                      <span className="text-red-500 text-xs font-semibold">✗ Needed</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Professors */}
          <div>
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Professors</div>
            {loadingProfs && <div className="text-xs text-gray-400">Loading…</div>}
            {!loadingProfs && professors.length === 0 && (
              <div className="text-xs text-gray-400">No professor data available yet.</div>
            )}
            {professors.map((prof) => (
              <div key={prof.name} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                <div>
                  <div className="text-sm font-medium text-gray-800">{prof.name}</div>
                  <div className="text-xs text-gray-400">{prof.num_ratings} ratings</div>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="text-sm font-bold" style={{ color: "var(--cp-green)" }}>
                    {prof.overall_score.toFixed(2)}<span className="text-xs font-normal text-gray-400">/4</span>
                  </span>
                  <a
                    href={prof.polyratings_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-blue-500 hover:underline"
                  >
                    ↗
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
