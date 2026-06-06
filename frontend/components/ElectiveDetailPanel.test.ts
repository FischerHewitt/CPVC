import { describe, expect, it } from "vitest";
import { labCoreqWarning, filterEligibleCourses, isOverrideCourse } from "./ElectiveDetailPanel";

describe("labCoreqWarning", () => {
  it("returns undefined for a non-lab course number", () => {
    expect(labCoreqWarning("ME 3339", new Set(), new Set(), new Set())).toBeUndefined();
    expect(labCoreqWarning("EE 3302", new Set(), new Set(), new Set())).toBeUndefined();
    expect(labCoreqWarning("CSC 4210", new Set(), new Set(), new Set())).toBeUndefined();
  });

  it("returns a warning when the lecture coreq is absent from all sets", () => {
    const warning = labCoreqWarning("ME 3339L", new Set(), new Set(), new Set());
    expect(warning).toMatch(/ME 3339/);
    expect(warning).toMatch(/concurrent enrollment/i);
    expect(warning).toMatch(/advisor/i);
  });

  it("returns undefined when the lecture is in completedSet", () => {
    expect(
      labCoreqWarning("ME 3339L", new Set(["ME 3339"]), new Set(), new Set()),
    ).toBeUndefined();
  });

  it("returns undefined when the lecture is in inProgressSet", () => {
    expect(
      labCoreqWarning("ME 3339L", new Set(), new Set(["ME 3339"]), new Set()),
    ).toBeUndefined();
  });

  it("returns undefined when the lecture is a flowchart tile (option B — planned)", () => {
    expect(
      labCoreqWarning("ME 3339L", new Set(), new Set(), new Set(["ME 3339"])),
    ).toBeUndefined();
  });

  it("handles EE lab suffix the same way", () => {
    const warning = labCoreqWarning("EE 3302L", new Set(), new Set(), new Set());
    expect(warning).toMatch(/EE 3302/);
    expect(warning).not.toMatch(/EE 3302L/);
  });

  it("is case-insensitive when matching course numbers", () => {
    expect(
      labCoreqWarning("ME 3339L", new Set(["me 3339"]), new Set(), new Set()),
    ).toBeUndefined();
  });
});

const MOCK_COURSES = [
  { course_number: "CSC 4100", title: "Algorithm Engineering", units: 4 },
  { course_number: "CSC 4200", title: "Programming Languages", units: 4 },
  { course_number: "CSC 4300", title: "Compiler Construction", units: 4 },
];

describe("filterEligibleCourses", () => {
  it("returns all courses when query is empty", () => {
    expect(filterEligibleCourses(MOCK_COURSES, "")).toHaveLength(3);
    expect(filterEligibleCourses(MOCK_COURSES, "   ")).toHaveLength(3);
  });

  it("filters by course number substring (case-insensitive)", () => {
    const result = filterEligibleCourses(MOCK_COURSES, "4100");
    expect(result).toHaveLength(1);
    expect(result[0].course_number).toBe("CSC 4100");
  });

  it("filters by course number prefix case-insensitively", () => {
    const result = filterEligibleCourses(MOCK_COURSES, "csc");
    expect(result).toHaveLength(3);
  });

  it("filters by title substring (case-insensitive)", () => {
    const result = filterEligibleCourses(MOCK_COURSES, "compiler");
    expect(result).toHaveLength(1);
    expect(result[0].course_number).toBe("CSC 4300");
  });

  it("returns empty array when no courses match", () => {
    expect(filterEligibleCourses(MOCK_COURSES, "BIOMED")).toHaveLength(0);
  });

  it("matches partial title words", () => {
    const result = filterEligibleCourses(MOCK_COURSES, "lang");
    expect(result).toHaveLength(1);
    expect(result[0].course_number).toBe("CSC 4200");
  });
});

describe("isOverrideCourse", () => {
  it("returns false when course number is in the eligible list", () => {
    expect(isOverrideCourse("CSC 4100", MOCK_COURSES)).toBe(false);
  });

  it("returns true when course number is not in the eligible list", () => {
    expect(isOverrideCourse("DATA 4010", MOCK_COURSES)).toBe(true);
  });

  it("is case-insensitive", () => {
    expect(isOverrideCourse("csc 4100", MOCK_COURSES)).toBe(false);
    expect(isOverrideCourse("CSC 4100", MOCK_COURSES)).toBe(false);
  });

  it("normalizes whitespace", () => {
    expect(isOverrideCourse("CSC  4100", MOCK_COURSES)).toBe(false);
  });

  it("returns true for an empty eligible list", () => {
    expect(isOverrideCourse("CSC 4100", [])).toBe(true);
  });
});
