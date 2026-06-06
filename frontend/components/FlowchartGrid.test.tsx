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

describe("FlowchartGrid custom course tiles", () => {
  it("renders an add-course button per column when onAddCourse is provided", () => {
    const html = renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{ sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [] }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
      />
    );
    expect(html).toContain("add course");
  });

  it("does not render an add-course button when onAddCourse is not provided", () => {
    const html = renderGrid(
      { sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [] },
      {},
    );
    expect(html).not.toContain("add course");
  });

  it("renders custom course tiles in their assigned column", () => {
    const html = renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{
          sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [],
          customCourses: {
            "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 0, status: "planned" },
          },
        }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
      />
    );
    expect(html).toContain("ACCT 221");
    expect(html).toContain("Accounting");
  });

  it("styles custom tiles with the free-elective grey color", () => {
    const html = renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{
          sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [],
          customCourses: {
            "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 0, status: "planned" },
          },
        }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
      />
    );
    expect(html).toContain("#e5e7eb"); // grey, matching free elective tiles
  });
});

describe("FlowchartGrid custom tile layout", () => {
  function renderTile(overrides: Partial<import("@/lib/types").CustomCourseEntry> = {}) {
    return renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{
          sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [],
          customCourses: {
            "uuid-1": {
              course_number: "ACCT 221",
              title: "Accounting for Non-Business Majors",
              units: 4,
              grid_col: 0,
              status: "planned",
              ...overrides,
            },
          },
        }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
        onClearCustomAssignment={vi.fn()}
        onRemoveCustomCourse={vi.fn()}
        onSetCustomCourseStatus={vi.fn()}
        onCustomCourseClick={vi.fn()}
      />
    );
  }

  it("renders title before course number (title is prominent, number is secondary)", () => {
    const html = renderTile();

    const titlePos  = html.indexOf("Accounting for Non-Business Majors");
    const numberPos = html.indexOf("ACCT 221");

    expect(titlePos).toBeGreaterThan(-1);
    expect(numberPos).toBeGreaterThan(-1);
    expect(titlePos).toBeLessThan(numberPos);
  });

  it("shows units in parentheses format matching other tiles", () => {
    const html = renderTile();

    expect(html).toContain("ACCT 221 (4)");
    expect(html).not.toContain("4u");
  });

  it("checkbox is checked when status is completed", () => {
    const html = renderTile({ status: "completed" });
    // React static markup renders checked={true} as checked=""
    expect(html).toContain('checked=""');
  });

  it("checkbox is not checked when status is planned", () => {
    const html = renderTile({ status: "planned" });
    expect(html).not.toContain('checked=""');
  });

  it("IP badge is highlighted (bg-amber-500) when status is in_progress", () => {
    const html = renderTile({ status: "in_progress" });
    expect(html).toContain("bg-amber-500");
  });

  it("IP badge is not highlighted when status is planned", () => {
    const html = renderTile({ status: "planned" });
    expect(html).not.toContain("bg-amber-500");
  });

  it("shows ✓ status badge (text-green-800) when completed", () => {
    const html = renderTile({ status: "completed" });
    // text-green-800 is specific to the status badge ✓; the legend uses text-green-700
    expect(html).toContain("text-green-800");
  });

  it("shows IP status badge inside content area when in_progress", () => {
    const html = renderTile({ status: "in_progress" });
    // The status-badge span uses text-[10px] which the legend IP span does not
    expect(html).toContain('text-[10px] font-bold">IP');
  });

  it("shows no status badge markup when planned", () => {
    const html = renderTile({ status: "planned" });
    expect(html).not.toContain("text-green-800");       // no ✓ badge
    expect(html).not.toContain('text-[10px] font-bold">IP'); // no IP badge
  });

  it("shows assignment label with slot course number when assignedToSlotId matches", () => {
    // GE1B is in the flowchart fixture at grid_col: 0
    const html = renderTile({ assignedToSlotId: "GE1B" });
    // Assignment renders "→ GE 1B"; other tiles render "tap to see courses →" (arrow at end)
    expect(html).toContain("→ GE 1B");
  });

  it("does not show assignment label when no slot is assigned", () => {
    const html = renderTile();
    // "→ " followed by a course number only appears for the assignment label
    expect(html).not.toContain("→ GE 1B");
    expect(html).not.toContain("→ ACCT");
  });

  it("tile is clickable (cursor-pointer class present)", () => {
    const html = renderTile();
    expect(html).toContain("cursor-pointer");
  });
});

describe("FlowchartGrid custom course unit totals", () => {
  function renderWithCustom(customCourses: TranscriptSession["customCourses"]) {
    return renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{ sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [], customCourses }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
        onClearCustomAssignment={vi.fn()}
        onRemoveCustomCourse={vi.fn()}
        onSetCustomCourseStatus={vi.fn()}
      />
    );
  }

  it("counts completed custom course units as earned", () => {
    const html = renderWithCustom({
      "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 5, grid_col: 0, status: "completed" },
    });
    expect(html).toContain("5</span><span class=\"text-gray-400\"> earned");
  });

  it("counts in-progress custom course units as in-progress", () => {
    const html = renderWithCustom({
      "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 5, grid_col: 0, status: "in_progress" },
    });
    expect(html).toContain("+5</span><span class=\"text-gray-400\"> in progress");
  });

  it("does not count planned custom course units", () => {
    const html = renderWithCustom({
      "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 5, grid_col: 0, status: "planned" },
    });
    expect(html).toContain("0</span><span class=\"text-gray-400\"> earned");
    expect(html).not.toContain("+5");
  });
});

describe("FlowchartGrid remove custom tile", () => {
  it("does not show a covered-by badge after the custom course is removed", () => {
    // After removal, session.customCourses is empty — no entry → no badge
    const html = renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{
          sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [],
          customCourses: {},
        }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
        onClearCustomAssignment={vi.fn()}
        onRemoveCustomCourse={vi.fn()}
        onSetCustomCourseStatus={vi.fn()}
      />
    );
    expect(html).not.toContain("covered by");
  });

});

describe("FlowchartGrid requirement assignment", () => {
  it("shows a covered-by badge on a slot when a custom course is assigned to it", () => {
    const html = renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{
          sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [],
          customCourses: {
            "uuid-1": {
              course_number: "ACCT 221", title: "Accounting", units: 4,
              grid_col: 0, status: "planned",
              assignedToSlotId: "GE1B",
            },
          },
        }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
        onClearCustomAssignment={vi.fn()}
      />
    );
    expect(html).toContain("covered by ACCT 221");
  });

  it("shows a counting-toward label on the custom tile when assigned", () => {
    const html = renderToStaticMarkup(
      <FlowchartGrid
        flowchart={flowchart}
        session={{
          sessionId: "t", studentName: "T", major: "CS", completed: [], inProgress: [],
          customCourses: {
            "uuid-1": {
              course_number: "ACCT 221", title: "Accounting", units: 4,
              grid_col: 0, status: "planned",
              assignedToSlotId: "GE1B",
            },
          },
        }}
        inferred={[]}
        geAreaMap={{}}
        onCourseClick={vi.fn()}
        onToggleCourseCompleted={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onMoveCourse={vi.fn()}
        onAddCourse={vi.fn()}
        onClearCustomAssignment={vi.fn()}
      />
    );
    expect(html).toContain("→");
    expect(html).toContain("GE 1B");
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
