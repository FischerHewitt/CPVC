import { describe, expect, it } from "vitest";
import {
  filterGECourses,
  GE_STATUS_STYLES,
  getGECoursePanelStatus,
  selectedGECourse,
  geStatusOrder,
} from "./GEDetailPanel";
import type { GECourse } from "@/lib/types";

const courses: GECourse[] = [
  { course_number: "CHIN 1141", title: "Elementary Chinese Language and Culture I Study Abroad", units: 3 },
  { course_number: "COMS 1126", title: "Argument and Advocacy", units: 3 },
  { course_number: "ENGL 2230", title: "British Literature: Beginnings to 1789", units: 3 },
];

describe("GEDetailPanel helpers", () => {
  it("uses blue, green, and orange styles for planned, done, and in-progress states", () => {
    expect(GE_STATUS_STYLES.planned.activeButton).toContain("bg-blue-600");
    expect(GE_STATUS_STYLES.completed.activeButton).toContain("bg-green-700");
    expect(GE_STATUS_STYLES.in_progress.activeButton).toContain("bg-orange-600");
  });

  it("orders actions from left to right as Plan, IP, Done", () => {
    expect(geStatusOrder()).toEqual(["planned", "in_progress", "completed"]);
  });

  it("detects planned, completed, and in-progress course statuses", () => {
    expect(getGECoursePanelStatus(courses[0], new Set(), new Set(), "CHIN 1141")).toBe("planned");
    expect(getGECoursePanelStatus(courses[1], new Set(["COMS 1126"]), new Set(), undefined)).toBe("completed");
    expect(getGECoursePanelStatus(courses[2], new Set(), new Set(["ENGL 2230"]), undefined)).toBe("in_progress");
  });

  it("matches quarter course numbers for completed and in-progress status checks", () => {
    expect(getGECoursePanelStatus(courses[1], new Set(["COMS 126"]), new Set(), undefined)).toBe("completed");
    expect(getGECoursePanelStatus(courses[2], new Set(), new Set(["ENGL 230"]), undefined)).toBe("in_progress");
  });

  it("chooses the selected course with completed taking priority over in-progress and planned", () => {
    const selected = selectedGECourse(
      courses,
      new Set(["COMS 1126"]),
      new Set(["ENGL 2230"]),
      "CHIN 1141",
    );

    expect(selected).toEqual({ course: courses[1], status: "completed" });
  });

  it("filters GE courses by course number or title", () => {
    expect(filterGECourses(courses, "chin").map((course) => course.course_number)).toEqual(["CHIN 1141"]);
    expect(filterGECourses(courses, "advocacy").map((course) => course.course_number)).toEqual(["COMS 1126"]);
    expect(filterGECourses(courses, "not real")).toEqual([]);
  });
});
