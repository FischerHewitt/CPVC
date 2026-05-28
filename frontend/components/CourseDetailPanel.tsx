"use client";

import { useEffect, useState } from "react";
import type { Course, CourseInfo, CourseStatus, Professor } from "@/lib/types";
import { getCourseInfo, getProfessors } from "@/lib/api";
import { expandSlashCourseNumber } from "@/lib/course-status";

interface Props {
  course: Course | null;
  status: CourseStatus | null;
  allCourses: Course[];
  completed: string[];
  inProgress: string[];
  inferred: string[];
  onClose: () => void;
}

const CATEGORY_LABEL: Record<string, string> = {
  major: "Major Requirement",
  support: "Support Requirement",
  concentration: "Concentration",
  ge: "General Education",
};

function norm(courseNumber: string) {
  return courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
}

function hasAnyCourseNumber(normalizedKnownNums: Set<string>, courseNums: string[]) {
  return courseNums.some((num) => normalizedKnownNums.has(norm(num)));
}

function courseNumberCandidates(course: Course) {
  return [
    course.course_number,
    ...course.quarter_equivalents,
    ...(course.auto_satisfied_by ?? []),
    ...expandSlashCourseNumber(course.course_number),
  ];
}

function getLiveStatus(
  course: Course,
  status: CourseStatus | null,
  completedNums: Set<string>,
  inProgressNums: Set<string>,
  inferredNums: Set<string>,
): CourseStatus | null {
  const candidates = courseNumberCandidates(course);
  if (hasAnyCourseNumber(completedNums, candidates)) return "completed";
  if (hasAnyCourseNumber(inferredNums, candidates)) return "inferred";
  if (hasAnyCourseNumber(inProgressNums, candidates)) return "in_progress";
  return status;
}

export default function CourseDetailPanel({
  course,
  status,
  allCourses,
  completed,
  inProgress,
  inferred,
  onClose,
}: Props) {
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [loadingProfs, setLoadingProfs] = useState(false);
  const [courseInfo, setCourseInfo] = useState<CourseInfo | null>(null);
  const [loadingInfo, setLoadingInfo] = useState(false);
  const courseNumber = course?.course_number;

  useEffect(() => {
    if (!courseNumber) return;
    let cancelled = false;

    setTimeout(() => {
      if (cancelled) return;
      setProfessors([]);
      setLoadingProfs(true);
      setCourseInfo(null);
      setLoadingInfo(true);
    }, 0);

    getCourseInfo(courseNumber)
      .then((nextInfo) => {
        if (!cancelled) setCourseInfo(nextInfo);
      })
      .finally(() => {
        if (!cancelled) setLoadingInfo(false);
      });

    getProfessors(courseNumber)
      .then((nextProfessors) => {
        if (!cancelled) setProfessors(nextProfessors);
      })
      .finally(() => {
        if (!cancelled) setLoadingProfs(false);
      });

    return () => {
      cancelled = true;
    };
  }, [courseNumber]);

  if (!course) return null;

  const completedSet = new Set(completed.map(norm));
  const inProgressSet = new Set(inProgress.map(norm));
  const inferredSet = new Set(inferred.map(norm));
  const liveStatus = getLiveStatus(course, status, completedSet, inProgressSet, inferredSet);
  const knownPrereqSet = new Set([...completed, ...inProgress, ...inferred].map(norm));
  const courseLookup = new Map<string, Course>();
  for (const item of allCourses) {
    for (const candidate of courseNumberCandidates(item)) {
      courseLookup.set(norm(candidate), item);
    }
  }
  const prereqRows = course.prerequisites.map((prereqNumber) => {
    const prereqCourse = courseLookup.get(norm(prereqNumber));
    const candidates = prereqCourse ? courseNumberCandidates(prereqCourse) : [prereqNumber];
    const choices = prereqCourse ? expandSlashCourseNumber(prereqCourse.course_number) : [];
    const met = hasAnyCourseNumber(knownPrereqSet, candidates);
    const isChoice = Boolean(prereqCourse?.course_number.includes("/"));
    const metVia = (met && isChoice) ? (choices.find((c) => knownPrereqSet.has(norm(c))) ?? null) : null;
    return {
      key: prereqNumber,
      course: prereqCourse,
      label: prereqCourse?.course_number ?? prereqNumber,
      met,
      isChoice,
      choices,
      metVia,
    };
  });
  const catalogUrl = `https://catalog.calpoly.edu/courses/${course.course_number.split(" ")[0].toLowerCase()}/`;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/20 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="fixed right-0 top-0 h-full w-[min(560px,100vw)] bg-white shadow-2xl z-50 flex flex-col overflow-y-auto">
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
            {liveStatus === "completed" && (
              <span className="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-1 rounded-full">✓ Completed</span>
            )}
            {liveStatus === "in_progress" && (
              <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-1 rounded-full">In Progress</span>
            )}
            {liveStatus === "inferred" && (
              <span className="bg-green-100 text-green-700 text-xs font-semibold px-2.5 py-1 rounded-full">Inferred from Prereqs</span>
            )}
            {liveStatus === "incomplete" && (
              <span className="bg-yellow-100 text-yellow-800 text-xs font-semibold px-2.5 py-1 rounded-full">Not Yet Taken</span>
            )}
            {liveStatus === "locked" && (
              <span className="bg-gray-100 text-gray-600 text-xs font-semibold px-2.5 py-1 rounded-full">🔒 Prerequisites Needed</span>
            )}
          </div>

          {/* Description */}
          <div>
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Description</div>
            {loadingInfo && <div className="text-xs text-gray-400">Loading…</div>}
            {!loadingInfo && !courseInfo && (
              <div className="text-xs text-gray-400 italic">No catalog description available.</div>
            )}
            {courseInfo && (
              <p className="text-sm text-gray-700 leading-relaxed">{courseInfo.description}</p>
            )}
            <a
              href={catalogUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-500 hover:underline mt-1.5 inline-block"
            >
              View in Cal Poly catalog ↗
            </a>
          </div>

          {/* Lab + lecture breakdown */}
          {course.lab_component && (
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Course Components</div>
              <div className="rounded-lg border border-gray-200 overflow-hidden text-sm">
                <div className="flex items-center justify-between px-3 py-2 bg-gray-50 border-b border-gray-100">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400">📖</span>
                    <span className="font-medium text-gray-700">Lecture</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-gray-500 text-xs">{course.course_number}</span>
                    <span className="font-semibold text-gray-700">{course.lab_component.lecture_units} units</span>
                  </div>
                </div>
                <div className="flex items-center justify-between px-3 py-2 bg-gray-50">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400">🔬</span>
                    <span className="font-medium text-gray-700">Lab</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-gray-500 text-xs">{course.lab_component.course_number}</span>
                    <span className="font-semibold text-gray-700">{course.lab_component.lab_units} unit{course.lab_component.lab_units !== 1 ? 's' : ''}</span>
                  </div>
                </div>
              </div>
              <p className="text-[11px] text-gray-400 mt-1.5">
                Both sections are required and appear separately on your transcript.
              </p>
            </div>
          )}

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
          {prereqRows.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Prerequisites</div>
              <div className="flex flex-col gap-1.5">
                {prereqRows.map((row) => (
                  <div key={row.key} className="flex items-center justify-between gap-3 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">{row.label}</span>
                      {!row.met && row.isChoice && row.choices.length > 1 && (
                        <div className="text-[11px] text-amber-700">
                          Choose one: {row.choices.join(" or ")}
                        </div>
                      )}
                    </div>
                    {row.met ? (
                      <span className="text-green-600 text-xs font-semibold">
                        {"✓ "}{row.metVia ? <span className="underline">{row.metVia}</span> : "Done"}
                      </span>
                    ) : row.isChoice ? (
                      <span className="text-amber-600 text-xs font-semibold">{"⚠ Choice needed"}</span>
                    ) : (
                      <span className="text-red-500 text-xs font-semibold">{"✗ Needed"}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Professors */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Professors</div>
              <a
                href="https://polyratings.dev"
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs font-semibold text-blue-500 uppercase tracking-wide hover:underline"
              >
                PolyRatings ↗
              </a>
            </div>
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
