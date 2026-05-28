import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import type { Course } from "@/lib/types";
import ManualCourseChecklist from "./ManualCourseChecklist";

const freeElective: Course = {
  id: "FREE1",
  course_number: "Free",
  title: "Free Elective",
  units: 3,
  category: "concentration",
  grid_col: 0,
  grid_row: 0,
  prerequisites: [],
  quarter_equivalents: [],
  is_placeholder: true,
};

describe("ManualCourseChecklist free electives", () => {
  it("shows selected free elective status and picker affordance", () => {
    const html = renderToStaticMarkup(
      <ManualCourseChecklist
        open
        courses={[freeElective]}
        completed={[]}
        inProgress={[]}
        geAreaMap={{}}
        plannedGECourses={{}}
        plannedFreeElectiveCourses={{
          FREE1: {
            course_number: "MU 1010",
            title: "Introduction to Music",
            units: 3,
            status: "planned",
          },
        }}
        onToggleCourse={vi.fn()}
        onToggleCourseInProgress={vi.fn()}
        onToggleGEArea={vi.fn()}
        onToggleGEAreaInProgress={vi.fn()}
        onTogglePickedCourse={vi.fn()}
        onTogglePickedCourseInProgress={vi.fn()}
        onToggleFreeElectiveStatus={vi.fn()}
        onOpenFreeElectivePicker={vi.fn()}
        onImportCSV={vi.fn()}
        onClose={vi.fn()}
      />,
    );

    expect(html).toContain("Selected: MU 1010");
    expect(html).toContain("Introduction to Music");
    expect(html).toContain("Planned");
    expect(html).toContain("Search catalog courses for this free elective");
  });
});
