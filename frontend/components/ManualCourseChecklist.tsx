"use client";

import { useMemo, useState } from "react";
import type { Course, GEAreaMap } from "@/lib/types";

interface Props {
  open: boolean;
  courses: Course[];
  completed: string[];
  inProgress: string[];
  geAreaMap: GEAreaMap;
  plannedGECourses: Record<string, string>;
  onToggleCourse: (course: Course) => void;
  onToggleCourseInProgress: (course: Course) => void;
  onToggleGEArea: (course: Course) => void;
  onToggleGEAreaInProgress: (course: Course) => void;
  onClose: () => void;
}

const CATEGORY_LABELS: Record<string, string> = {
  all: "All",
  major: "Major",
  support: "Support",
  concentration: "Conc.",
  ge: "GE",
};

function matchesCourse(course: Course, query: string) {
  const haystack = [
    course.course_number,
    course.title,
    course.category,
    ...course.quarter_equivalents,
  ].join(" ").toLowerCase();
  return haystack.includes(query.toLowerCase().trim());
}

function norm(courseNumber: string) {
  return courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
}

function courseIsCompleted(course: Course, completed: Set<string>) {
  const normalizedCompleted = new Set(Array.from(completed, norm));
  return [course.course_number, ...course.quarter_equivalents].some((num) => normalizedCompleted.has(norm(num)));
}

function courseIsInProgress(course: Course, inProgress: Set<string>) {
  const normalizedInProgress = new Set(Array.from(inProgress, norm));
  return [course.course_number, ...course.quarter_equivalents].some((num) => normalizedInProgress.has(norm(num)));
}

function geAreaCandidates(course: Course, geAreaMap: GEAreaMap) {
  return [
    course.course_number,
    ...course.quarter_equivalents,
    ...(geAreaMap[course.course_number] ?? []),
  ];
}

function geAreaIsKnown(course: Course, geAreaMap: GEAreaMap, known: Set<string>) {
  const normalizedKnown = new Set(Array.from(known, norm));
  return geAreaCandidates(course, geAreaMap).some((candidate) => normalizedKnown.has(norm(candidate)));
}

export default function ManualCourseChecklist({
  open,
  courses,
  completed,
  inProgress,
  geAreaMap,
  plannedGECourses,
  onToggleCourse,
  onToggleCourseInProgress,
  onToggleGEArea,
  onToggleGEAreaInProgress,
  onClose,
}: Props) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");

  const completedSet = useMemo(() => new Set(completed), [completed]);
  const inProgressSet = useMemo(() => new Set(inProgress), [inProgress]);

  const gePlaceholders = useMemo(
    () => courses.filter((course) => course.is_placeholder && course.category === "ge"),
    [courses],
  );

  const selectableCourses = useMemo(
    () => courses.filter((course) => !course.is_placeholder),
    [courses],
  );

  const availableCategories = useMemo(
    () => {
      const categories = Array.from(new Set(selectableCourses.map((course) => course.category)));
      if (gePlaceholders.length > 0 && !categories.includes("ge")) categories.push("ge");
      return ["all", ...categories];
    },
    [gePlaceholders.length, selectableCourses],
  );

  const visibleCourses = selectableCourses.filter((course) => {
    if (category !== "all" && course.category !== category) return false;
    if (query.trim() && !matchesCourse(course, query)) return false;
    return true;
  });

  const visibleGEAreas = gePlaceholders.filter((course) => {
    if (category !== "all" && category !== "ge") return false;
    if (query.trim() && !matchesCourse(course, query)) return false;
    return true;
  });

  const completedCount = selectableCourses.filter((course) => courseIsCompleted(course, completedSet)).length;
  const geCompletedCount = gePlaceholders.filter((course) => geAreaIsKnown(course, geAreaMap, completedSet)).length;
  const inProgressCount = selectableCourses.filter((course) => {
    return !courseIsCompleted(course, completedSet) && courseIsInProgress(course, inProgressSet);
  }).length;
  const geInProgressCount = gePlaceholders.filter((course) => {
    return !geAreaIsKnown(course, geAreaMap, completedSet) && geAreaIsKnown(course, geAreaMap, inProgressSet);
  }).length;
  const totalTracked = selectableCourses.length + gePlaceholders.length;

  if (!open) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/20 z-40 transition-opacity" onClick={onClose} />

      <div className="fixed left-1/2 top-1/2 z-50 flex max-h-[82vh] w-[min(720px,calc(100vw-2rem))] -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-lg border border-gray-200 bg-white shadow-2xl">
        <div className="flex items-start justify-between gap-4 border-b border-gray-100 px-5 py-4">
          <div>
            <div className="text-base font-bold" style={{ color: "var(--cp-green)" }}>
              Manual Course Checklist
            </div>
            <div className="mt-0.5 text-xs text-gray-500">
              {completedCount + geCompletedCount} completed · {inProgressCount + geInProgressCount} in progress · {totalTracked} tracked
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-2xl leading-none text-gray-400 hover:text-gray-700"
            aria-label="Close checklist"
          >
            ×
          </button>
        </div>

        <div className="border-b border-gray-100 px-5 py-3">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search course number, title, GE area, or quarter equivalent"
              className="min-w-0 flex-1 rounded border border-gray-300 px-3 py-2 text-sm outline-none focus:border-green-700"
            />
            <div className="flex flex-wrap gap-1">
              {availableCategories.map((item) => (
                <button
                  key={item}
                  onClick={() => setCategory(item)}
                  className={`rounded border px-2.5 py-1.5 text-xs font-semibold transition-colors ${
                    category === item
                      ? "border-green-800 bg-green-50 text-green-900"
                      : "border-gray-200 text-gray-500 hover:bg-gray-50"
                  }`}
                >
                  {CATEGORY_LABELS[item]}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="overflow-y-auto px-5 py-3">
          {visibleCourses.length === 0 && visibleGEAreas.length === 0 && (
            <div className="py-10 text-center text-sm text-gray-400">No matching courses.</div>
          )}

          <div className="grid gap-2 sm:grid-cols-2">
            {visibleCourses.map((course) => {
              const checked = courseIsCompleted(course, completedSet);
              const inProgressMatch = courseIsInProgress(course, inProgressSet);

              return (
                <div
                  key={course.id}
                  className={`flex items-start gap-3 rounded border px-3 py-3 transition-colors ${
                    checked
                      ? "border-green-200 bg-green-50"
                      : inProgressMatch
                        ? "border-blue-200 bg-blue-50"
                        : "border-gray-200 bg-white hover:bg-gray-50"
                  }`}
                >
                  <div className="flex shrink-0 flex-col gap-2">
                    <label className="flex items-center gap-1.5 text-[11px] font-semibold text-gray-600">
                      <input
                        type="checkbox"
                        checked={checked}
                        onChange={() => onToggleCourse(course)}
                        className="h-4 w-4 accent-green-700"
                        aria-label={checked ? `Mark ${course.course_number} incomplete` : `Mark ${course.course_number} completed`}
                      />
                      Done
                    </label>
                    <label className="flex items-center gap-1.5 text-[11px] font-semibold text-blue-700">
                      <input
                        type="checkbox"
                        checked={inProgressMatch && !checked}
                        onChange={() => onToggleCourseInProgress(course)}
                        className="h-4 w-4 accent-blue-700"
                        aria-label={inProgressMatch ? `Remove ${course.course_number} from in progress` : `Mark ${course.course_number} in progress`}
                      />
                      IP
                    </label>
                  </div>
                  <span className="min-w-0 flex-1">
                    <span className="flex flex-wrap items-center gap-1.5">
                      <span className="text-sm font-bold text-gray-800">{course.course_number}</span>
                      {inProgressMatch && !checked && (
                        <span className="rounded bg-blue-50 px-1.5 py-0.5 text-[10px] font-bold text-blue-700">
                          IP
                        </span>
                      )}
                      <span className="rounded bg-gray-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-gray-500">
                        {CATEGORY_LABELS[course.category] ?? course.category}
                      </span>
                    </span>
                    <span className="mt-0.5 block text-xs leading-snug text-gray-500">{course.title}</span>
                    {course.quarter_equivalents.length > 0 && (
                      <span className="mt-1 block text-[11px] text-gray-400">
                        Also matches {course.quarter_equivalents.join(", ")}
                      </span>
                    )}
                  </span>
                </div>
              );
            })}

            {visibleGEAreas.map((course) => {
              const checked = geAreaIsKnown(course, geAreaMap, completedSet);
              const inProgressMatch = geAreaIsKnown(course, geAreaMap, inProgressSet);
              const plannedCourse = plannedGECourses[course.course_number];

              return (
                <div
                  key={course.id}
                  className={`flex items-start gap-3 rounded border px-3 py-3 transition-colors ${
                    checked
                      ? "border-green-200 bg-green-50"
                      : inProgressMatch || plannedCourse
                        ? "border-blue-200 bg-blue-50"
                        : "border-gray-200 bg-white hover:bg-gray-50"
                  }`}
                >
                  <div className="flex shrink-0 flex-col gap-2">
                    <label className="flex items-center gap-1.5 text-[11px] font-semibold text-gray-600">
                      <input
                        type="checkbox"
                        checked={checked}
                        onChange={() => onToggleGEArea(course)}
                        className="h-4 w-4 accent-green-700"
                        aria-label={checked ? `Mark ${course.course_number} incomplete` : `Mark ${course.course_number} completed`}
                      />
                      Done
                    </label>
                    <label className="flex items-center gap-1.5 text-[11px] font-semibold text-blue-700">
                      <input
                        type="checkbox"
                        checked={inProgressMatch && !checked}
                        onChange={() => onToggleGEAreaInProgress(course)}
                        className="h-4 w-4 accent-blue-700"
                        aria-label={inProgressMatch ? `Remove ${course.course_number} from in progress` : `Mark ${course.course_number} in progress`}
                      />
                      IP
                    </label>
                  </div>
                  <span className="min-w-0 flex-1">
                    <span className="flex flex-wrap items-center gap-1.5">
                      <span className="text-sm font-bold text-gray-800">{course.course_number}</span>
                      {inProgressMatch && !checked && (
                        <span className="rounded bg-blue-50 px-1.5 py-0.5 text-[10px] font-bold text-blue-700">
                          IP
                        </span>
                      )}
                      {plannedCourse && !checked && (
                        <span className="rounded bg-blue-100 px-1.5 py-0.5 text-[10px] font-bold text-blue-800">
                          Planned
                        </span>
                      )}
                      <span className="rounded bg-gray-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-gray-500">
                        GE
                      </span>
                    </span>
                    <span className="mt-0.5 block text-xs leading-snug text-gray-500">{course.title}</span>
                    {plannedCourse && (
                      <span className="mt-1 block text-[11px] text-blue-700">
                        Planned: {plannedCourse}
                      </span>
                    )}
                    {course.quarter_equivalents.length > 0 && (
                      <span className="mt-1 block text-[11px] text-gray-400">
                        Also matches {course.quarter_equivalents.join(", ")}
                      </span>
                    )}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </>
  );
}
