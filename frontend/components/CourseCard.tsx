"use client";

import type { Course, CourseStatus } from "@/lib/types";

interface Props {
  course: Course;
  status: CourseStatus;
  onClick: () => void;
  checked: boolean;
  inProgressChecked: boolean;
  plannedCourseNumber?: string;
  activeGECourseNumber?: string;
  onToggleCompleted: () => void;
  onToggleInProgress: () => void;
}

const CATEGORY_STYLES: Record<string, { bg: string; border: string; text: string }> = {
  major:         { bg: "#bae6fd", border: "#0284c7", text: "#0c4a6e" },
  support:       { bg: "#ede9fe", border: "#7c3aed", text: "#4c1d95" },
  concentration: { bg: "#fce7f3", border: "#be185d", text: "#831843" },
  ge:            { bg: "#dcfce7", border: "#15803d", text: "#14532d" },
};

export default function CourseCard({
  course,
  status,
  onClick,
  checked,
  inProgressChecked,
  plannedCourseNumber,
  activeGECourseNumber,
  onToggleCompleted,
  onToggleInProgress,
}: Props) {
  const style = CATEGORY_STYLES[course.category] ?? CATEGORY_STYLES.ge;
  const isClickable = !course.is_placeholder;

  const opacity =
    status === "completed" ? 0.55 :
    status === "inferred"  ? 0.65 :
    status === "locked"    ? 0.75 :
    1.0;

  const grayscale = status === "locked" ? "grayscale(30%)" : "none";

  if (course.is_placeholder) {
    const isGE = course.category === "ge";
    const geCompleted    = isGE  && status === "completed";
    const geInProgress   = isGE  && status === "in_progress";
    const geLocked       = isGE  && status === "locked";
    const nonGECompleted  = !isGE && status === "completed";
    const nonGEInProgress = !isGE && status === "in_progress";
    return (
      <div
        className={`rounded border text-center text-[10px] font-medium px-1 py-2 transition-all select-none relative
          ${isGE ? "cursor-pointer hover:opacity-90 hover:scale-[1.03] active:scale-[0.98]" : "italic"}`}
        style={{
          background: style.bg,
          borderColor: geCompleted ? "#15803d" : style.border,
          borderWidth: geCompleted ? 2 : 1,
          color: style.text,
          opacity: isGE ? (geCompleted ? 0.6 : 0.75) : (nonGECompleted ? 0.55 : 0.5),
        }}
        onClick={isGE ? onClick : undefined}
      >
        {!isGE && (
          <>
            <label
              className="absolute left-1 top-1 flex h-4 w-4 items-center justify-center rounded border bg-white/85 shadow-sm cursor-pointer"
              title={checked ? "Mark incomplete" : "Mark completed"}
              onClick={(e) => e.stopPropagation()}
              onMouseDown={(e) => e.stopPropagation()}
              draggable={false}
            >
              <input
                type="checkbox"
                checked={checked}
                onChange={onToggleCompleted}
                className="h-3 w-3 accent-green-700 cursor-pointer"
                aria-label={checked ? `Mark ${course.course_number} incomplete` : `Mark ${course.course_number} completed`}
              />
            </label>
            <label
              className={`absolute right-1 top-1 flex h-4 min-w-5 items-center justify-center rounded border px-0.5 text-[8px] font-bold shadow-sm cursor-pointer transition-colors ${
                inProgressChecked && !checked
                  ? "bg-amber-500 border-amber-600 text-white"
                  : "bg-white/85 border-gray-300 text-amber-700"
              }`}
              title={inProgressChecked ? "Remove in progress" : "Mark in progress"}
              onClick={(e) => e.stopPropagation()}
              onMouseDown={(e) => e.stopPropagation()}
              draggable={false}
            >
              <input
                type="checkbox"
                checked={inProgressChecked && !checked}
                onChange={onToggleInProgress}
                className="sr-only"
                aria-label={inProgressChecked ? `Remove ${course.course_number} from in progress` : `Mark ${course.course_number} in progress`}
              />
              IP
            </label>
          </>
        )}
        <div className="flex justify-center mb-0.5 h-3">
          {(geCompleted || nonGECompleted)   && <span className="text-green-800 text-[10px] font-bold">✓</span>}
          {(geInProgress || nonGEInProgress) && <span className="text-amber-600 text-[10px] font-bold">IP</span>}
          {geLocked && <span className="text-[10px]">🔒</span>}
        </div>
        <div className={isGE ? "font-semibold not-italic" : ""}>{course.title}</div>
        {isGE && (geCompleted || geInProgress) && activeGECourseNumber && (
          <div className="text-[9px] mt-0.5 font-bold">{activeGECourseNumber}</div>
        )}
        {isGE && !geCompleted && !geInProgress && plannedCourseNumber && (
          <div className="text-[9px] mt-0.5 font-semibold opacity-80">
            planned: {plannedCourseNumber}
          </div>
        )}
        {isGE && !geCompleted && !geInProgress && !geLocked && (
          <div className="text-[9px] mt-0.5 opacity-70">tap to see courses →</div>
        )}
        {isGE && (geCompleted || geInProgress) && (
          <div className="text-[9px] mt-0.5 opacity-70">tap to change →</div>
        )}
        {geLocked && (
          <div className="text-[9px] mt-0.5 opacity-70">prereqs needed</div>
        )}
      </div>
    );
  }

  return (
    <div
      className={`rounded border text-center px-1 py-2 transition-all select-none relative
        ${isClickable ? "cursor-pointer hover:shadow-md active:scale-[0.99]" : "cursor-default"}`}
      style={{
        background: style.bg,
        borderColor: style.border,
        color: style.text,
        borderWidth: 1.5,
        opacity,
        filter: grayscale,
      }}
      onClick={isClickable ? onClick : undefined}
    >
      <label
        className="absolute left-1 top-1 flex h-4 w-4 items-center justify-center rounded border bg-white/85 shadow-sm cursor-pointer"
        title={checked ? "Mark incomplete" : "Mark completed"}
        onClick={(event) => event.stopPropagation()}
        onMouseDown={(event) => event.stopPropagation()}
        draggable={false}
      >
        <input
          type="checkbox"
          checked={checked}
          onChange={onToggleCompleted}
          className="h-3 w-3 accent-green-700 cursor-pointer"
          aria-label={checked ? `Mark ${course.course_number} incomplete` : `Mark ${course.course_number} completed`}
        />
      </label>
      <label
        className={`absolute right-1 top-1 flex h-4 min-w-5 items-center justify-center rounded border px-0.5 text-[8px] font-bold shadow-sm cursor-pointer transition-colors ${
          inProgressChecked && !checked
            ? "bg-amber-500 border-amber-600 text-white"
            : "bg-white/85 border-gray-300 text-amber-700"
        }`}
        title={inProgressChecked ? "Remove in progress" : "Mark in progress"}
        onClick={(event) => event.stopPropagation()}
        onMouseDown={(event) => event.stopPropagation()}
        draggable={false}
      >
        <input
          type="checkbox"
          checked={inProgressChecked && !checked}
          onChange={onToggleInProgress}
          className="sr-only"
          aria-label={inProgressChecked ? `Remove ${course.course_number} from in progress` : `Mark ${course.course_number} in progress`}
        />
        IP
      </label>

      {/* Status badge */}
      <div className="flex justify-center mb-0.5 h-3">
        {status === "completed"   && <span className="text-green-800 text-[10px] font-bold">✓</span>}
        {status === "inferred"    && <span className="text-green-700 text-[10px] font-semibold">~✓</span>}
        {status === "in_progress" && <span className="text-amber-600 text-[10px] font-bold">IP</span>}
        {status === "locked"      && <span className="text-gray-500 text-[10px]">🔒</span>}
      </div>

      <div className="text-[11px] font-bold leading-tight">{course.title}</div>
      <div className="text-[10px] mt-0.5 font-medium opacity-75">
        {course.course_number} ({course.units})
      </div>
    </div>
  );
}
