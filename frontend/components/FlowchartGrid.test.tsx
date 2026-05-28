import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import type { CourseStatus, Flowchart, TranscriptSession } from "@/lib/types";
import FlowchartGrid, { countCourseProgress } from "./FlowchartGrid";

const flowchart: Flowchart = {
  major: "Computer Science",
  code: "CS",
  total_units: 120,
  columns: [{ year: "Freshman", term: "Spring" }],
  courses: [
    {
      id: "GE1B",
      course_number: "GE 1B",
      title: "Critical Thinking",
      units: 3,
      category: "ge",
      grid_col: 0,
      grid_row: 0,
      prerequisites: [],
      quarter_equivalents: [],
      is_placeholder: true,
    },
    {
      id: "FREE1",
      course_number: "Free",
      title: "Free Elective",
      units: 3,
      category: "support",
      grid_col: 0,
      grid_row: 1,
      prerequisites: [],
      quarter_equivalents: [],
      is_placeholder: true,
    },
    {
      id: "FREE2",
      course_number: "Free",
      title: "Free Elective",
      units: 3,
      category: "support",
      grid_col: 0,
      grid_row: 2,
      prerequisites: [],
      quarter_equivalents: [],
      is_placeholder: true,
    },
  ],
};

function renderGrid(session: TranscriptSession, geAreaMap: Record<string, string[]>) {
  return renderToStaticMarkup(
    <FlowchartGrid
      flowchart={flowchart}
      session={session}
      inferred={[]}
      geAreaMap={geAreaMap}
      onCourseClick={vi.fn()}
      onToggleCourseCompleted={vi.fn()}
      onToggleCourseInProgress={vi.fn()}
      onMoveCourse={vi.fn()}
    />,
  );
}

describe("FlowchartGrid GE placeholder display", () => {
  it("shows the selected in-progress GE course on the GE 1B tile", () => {
    const html = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: ["COMS 1126"],
    }, { "GE 1B": ["COMS 1126"] });

    expect(html).toContain("Critical Thinking");
    expect(html).toContain("COMS 1126");
    expect(html).toContain("tap to change");
  });

  it("still shows the in-progress GE course when it only exists as the selected planned course", () => {
    const html = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: ["COMS 1126"],
      plannedGECourses: { "GE 1B": "COMS 1126" },
    }, {});

    expect(html).toContain("Critical Thinking");
    expect(html).toContain("COMS 1126");
    expect(html).toContain("tap to change");
  });

  it("shows the selected course instead of the GE placeholder for legacy sessions with both statuses", () => {
    const html = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: ["GE 1B", "COMS 1126"],
      plannedGECourses: { "GE 1B": "COMS 1126" },
    }, { "GE 1B": ["COMS 1126"] });

    expect(html).toContain("COMS 1126");
    expect(html).not.toContain(">GE 1B<");
  });
});

describe("FlowchartGrid free elective display", () => {
  it("shows selected free elective courses by slot without collisions", () => {
    const html = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: [],
      plannedFreeElectiveCourses: {
        FREE1: {
          course_number: "MU 1010",
          title: "Introduction to Music",
          units: 3,
          status: "planned",
        },
        FREE2: {
          course_number: "FSN 2500",
          title: "Food and Nutrition: Customs and Culture",
          units: 4,
          status: "planned",
        },
      },
    }, {});

    expect(html).toContain("Free Elective");
    expect(html).toContain("background:#e5e7eb");
    expect(html).toContain("MU 1010");
    expect(html).toContain("planned: MU 1010 (3)");
    expect(html).toContain("FSN 2500");
    expect(html).toContain("planned: FSN 2500 (4)");
    expect(html).toContain("tap to change");
    expect(html).not.toContain("Introduction to Music");
    expect(html).not.toContain("Food and Nutrition: Customs and Culture");
  });

  it("includes free electives in the legend", () => {
    const html = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: [],
    }, {});

    expect(html).toContain("Free Elective");
    expect(html).toContain("border-color:#6b7280");
  });

  it("counts completed and in-progress free elective selections using selected units", () => {
    const completedHtml = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: [],
      plannedFreeElectiveCourses: {
        FREE1: {
          course_number: "MU 1010",
          title: "Introduction to Music",
          units: 5,
          status: "completed",
        },
      },
    }, {});
    const inProgressHtml = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: [],
      plannedFreeElectiveCourses: {
        FREE1: {
          course_number: "MU 1010",
          title: "Introduction to Music",
          units: 5,
          status: "in_progress",
        },
      },
    }, {});

    expect(completedHtml).toContain("5</span><span class=\"text-gray-400\"> earned");
    expect(inProgressHtml).toContain("+5</span><span class=\"text-gray-400\"> in progress");
  });

  it("uses planned free elective units in term totals without counting them as earned", () => {
    const html = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: [],
      plannedFreeElectiveCourses: {
        FREE1: {
          course_number: "MU 1010",
          title: "Introduction to Music",
          units: 5,
          status: "planned",
        },
      },
    }, {});

    expect(html).toContain("0</span><span class=\"text-gray-400\"> earned");
    expect(html).toContain("rec 11u");
  });
});

describe("FlowchartGrid progress bars", () => {
  it("counts completed, inferred, and in-progress courses separately", () => {
    const statuses = new Map<string, CourseStatus>([
      ["GE1B", "in_progress"],
      ["FREE1", "completed"],
      ["FREE2", "inferred"],
    ]);

    expect(countCourseProgress(flowchart.courses, statuses)).toEqual({
      completed: 1,
      inferred: 1,
      inProgress: 1,
      total: 3,
    });
  });

  it("shows a lighter in-progress segment in the top progress bars", () => {
    const html = renderGrid({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: ["COMS 1126"],
      plannedFreeElectiveCourses: {
        FREE1: {
          course_number: "MU 1010",
          title: "Introduction to Music",
          units: 3,
          status: "in_progress",
        },
      },
    }, { "GE 1B": ["COMS 1126"] });

    expect(html).toContain("+1 IP");
    expect(html).toContain("background:#ddd6fe");
    expect(html).toContain("background:#bbf7d0");
  });
});
