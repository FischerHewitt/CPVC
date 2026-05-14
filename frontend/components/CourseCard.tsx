"use client";

import type { Course, CourseStatus } from "@/lib/types";

interface Props {
  course: Course;
  status: CourseStatus;
  onClick: () => void;
}

const CATEGORY_STYLES: Record<string, { bg: string; border: string; text: string }> = {
  major:         { bg: "#fde68a", border: "#d97706", text: "#78350f" },
  support:       { bg: "#fed7aa", border: "#ea580c", text: "#7c2d12" },
  concentration: { bg: "#f9a8d4", border: "#db2777", text: "#831843" },
  ge:            { bg: "#bbf7d0", border: "#16a34a", text: "#14532d" },
};

export default function CourseCard({ course, status, onClick }: Props) {
  const style = CATEGORY_STYLES[course.category] ?? CATEGORY_STYLES.ge;
  const isClickable = status === "incomplete" || status === "in_progress";

  const opacity =
    status === "completed" ? 0.55 :
    status === "inferred"  ? 0.65 :
    status === "locked"    ? 0.35 :
    1.0;

  const grayscale = status === "locked" ? "grayscale(60%)" : "none";

  if (course.is_placeholder) {
    return (
      <div
        className="rounded border text-center text-[10px] font-medium px-1 py-2 italic"
        style={{ background: style.bg, borderColor: style.border, color: style.text, opacity: 0.5 }}
      >
        {course.title}
      </div>
    );
  }

  return (
    <div
      className={`rounded border text-center px-1 py-2 transition-all select-none
        ${isClickable ? "cursor-pointer hover:scale-[1.03] hover:shadow-md active:scale-[0.98]" : "cursor-default"}`}
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
      {/* Status badge */}
      <div className="flex justify-center mb-0.5 h-3">
        {status === "completed"   && <span className="text-green-800 text-[10px] font-bold">✓</span>}
        {status === "inferred"    && <span className="text-green-700 text-[10px] font-semibold">~✓</span>}
        {status === "in_progress" && <span className="text-blue-700 text-[10px] font-bold">IP</span>}
        {status === "locked"      && <span className="text-gray-500 text-[10px]">🔒</span>}
      </div>

      <div className="text-[11px] font-bold leading-tight">{course.title}</div>
      <div className="text-[10px] mt-0.5 font-medium opacity-75">
        {course.course_number} ({course.units})
      </div>
    </div>
  );
}
