import { describe, expect, it } from "vitest";
import type { Course } from "./types";
import {
  getOtherCredits,
  isCalPolyCourseLike,
  isTransferCreditPlaceholder,
} from "./other-credits";

const courses: Course[] = [
  {
    id: "CSC1001",
    course_number: "CSC 1001",
    title: "Fundamentals of Computer Science",
    units: 4,
    category: "major",
    grid_col: 0,
    grid_row: 0,
    prerequisites: [],
    quarter_equivalents: ["CSC 101"],
    is_placeholder: false,
  },
  {
    id: "GE4A",
    course_number: "GE 4A",
    title: "American Institutions",
    units: 3,
    category: "ge",
    grid_col: 1,
    grid_row: 0,
    prerequisites: [],
    quarter_equivalents: [],
    is_placeholder: true,
  },
];

describe("other credits", () => {
  it("filters transfer credit placeholders", () => {
    expect(isTransferCreditPlaceholder("MATH 1TR")).toBe(true);
    expect(isTransferCreditPlaceholder("PHYS 2TR")).toBe(true);
    expect(isTransferCreditPlaceholder("CSC 490")).toBe(false);
  });

  it("recognizes regular Cal Poly-style course numbers", () => {
    expect(isCalPolyCourseLike("CSC 490")).toBe(true);
    expect(isCalPolyCourseLike("ME 471")).toBe(true);
    expect(isCalPolyCourseLike("MATH 1TR")).toBe(false);
    expect(isCalPolyCourseLike("GE 4A")).toBe(false);
  });

  it("returns imported courses that do not satisfy current flowchart slots", () => {
    expect(getOtherCredits(
      courses,
      ["CSC 101", "HIST 2202", "CSC 490", "MATH 1TR"],
      ["ME 470", "ME 471"],
      { "GE 4A": ["HIST 2202"] },
    )).toEqual([
      { courseNumber: "CSC 490", status: "completed" },
      { courseNumber: "ME 470", status: "in_progress" },
      { courseNumber: "ME 471", status: "in_progress" },
    ]);
  });

  it("does not list a course selected into a planned placeholder", () => {
    expect(getOtherCredits(
      courses,
      ["CSC 490"],
      ["ME 470"],
      {},
      { "Conc.": "CSC 490" },
    )).toEqual([
      { courseNumber: "ME 470", status: "in_progress" },
    ]);
  });

  it("does not list a course selected into a free elective slot", () => {
    expect(getOtherCredits(
      courses,
      ["MU 1010", "ME 470"],
      [],
      {},
      {},
      {
        FREE1: {
          course_number: "MU 1010",
          title: "Introduction to Music",
          units: 3,
          status: "completed",
        },
      },
    )).toEqual([
      { courseNumber: "ME 470", status: "completed" },
    ]);
  });
});
