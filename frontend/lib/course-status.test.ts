import { describe, it, expect } from "vitest";
import { getCourseStatus, toNormalizedSet } from "./course-status";
import type { Course, GEAreaMap } from "./types";

function makeCourse(partial: Partial<Course> = {}): Course {
  return {
    id: "test",
    course_number: "CSC 1024",
    title: "Fundamentals of Computer Science",
    units: 4,
    category: "major",
    grid_col: 0,
    grid_row: 0,
    prerequisites: [],
    quarter_equivalents: [],
    is_placeholder: false,
    ...partial,
  };
}

const emptyLookup = new Map<string, Course>();
const emptyGEMap: GEAreaMap = {};

// ── regular (non-placeholder) courses ────────────────────────────────────────

describe("getCourseStatus — regular course", () => {
  it("returns completed when course_number is in completedNums", () => {
    const course = makeCourse({ course_number: "CSC 1024" });
    const completed = toNormalizedSet(["CSC 1024"]);
    expect(getCourseStatus(course, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("returns completed via quarter_equivalent", () => {
    const course = makeCourse({ course_number: "CSC 1024", quarter_equivalents: ["CSC 101"] });
    const completed = toNormalizedSet(["CSC 101"]);
    expect(getCourseStatus(course, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("returns in_progress", () => {
    const course = makeCourse({ course_number: "MATH 1261" });
    const inProgress = toNormalizedSet(["MATH 1261"]);
    expect(getCourseStatus(course, new Set(), inProgress, new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("in_progress");
  });

  it("returns inferred", () => {
    const course = makeCourse({ course_number: "CSC 1001" });
    const inferred = toNormalizedSet(["CSC 1001"]);
    expect(getCourseStatus(course, new Set(), new Set(), inferred, new Set(), emptyLookup, emptyGEMap)).toBe("inferred");
  });

  it("returns incomplete when prereqs are met", () => {
    const course = makeCourse({ course_number: "CSC 2000", prerequisites: [] });
    expect(getCourseStatus(course, new Set(), new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("incomplete");
  });

  it("returns locked when prereqs are not met", () => {
    const prereq = makeCourse({ course_number: "CSC 1024" });
    const course = makeCourse({ course_number: "CSC 2000", prerequisites: ["CSC 1024"] });
    const lookup = new Map([["CSC 1024", prereq]]);
    expect(getCourseStatus(course, new Set(), new Set(), new Set(), new Set(), lookup, emptyGEMap)).toBe("locked");
  });
});

// ── non-GE placeholder (the bug that was fixed) ───────────────────────────────

describe("getCourseStatus — non-GE placeholder with mixed-case course_number", () => {
  it("returns completed when the mixed-case course_number is in completed (bug regression)", () => {
    // Before the fix, "IE Technical Elective" would NOT match "IE TECHNICAL ELECTIVE"
    // in the normalized completedNums set, so status stayed "incomplete" even after toggling done.
    const elective = makeCourse({
      course_number: "IE Technical Elective",
      title: "IE Technical Elective",
      category: "support",
      is_placeholder: true,
    });
    const completed = toNormalizedSet(["IE Technical Elective"]);
    expect(getCourseStatus(elective, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("returns in_progress when the mixed-case course_number is in inProgress", () => {
    const elective = makeCourse({
      course_number: "ENGR/EE/MATE Elective",
      title: "Engineering Elective",
      category: "support",
      is_placeholder: true,
    });
    const inProgress = toNormalizedSet(["ENGR/EE/MATE Elective"]);
    expect(getCourseStatus(elective, new Set(), inProgress, new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("in_progress");
  });

  it("returns incomplete when neither completed nor in-progress", () => {
    const elective = makeCourse({
      course_number: "Major Elective",
      category: "major",
      is_placeholder: true,
    });
    expect(getCourseStatus(elective, new Set(), new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("incomplete");
  });

  it("matches via quarter_equivalents even for placeholder", () => {
    const elective = makeCourse({
      course_number: "IME 1141/1142/1156",
      category: "support",
      is_placeholder: true,
      quarter_equivalents: ["IME 141", "IME 142"],
    });
    const completed = toNormalizedSet(["IME 141"]);
    expect(getCourseStatus(elective, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });
});

// ── GE placeholder ────────────────────────────────────────────────────────────

describe("getCourseStatus — GE placeholder", () => {
  it("returns completed when GE area course_number itself is in completed", () => {
    const ge = makeCourse({ course_number: "GE 1A", category: "ge", is_placeholder: true });
    const completed = toNormalizedSet(["GE 1A"]);
    expect(getCourseStatus(ge, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("returns completed via quarter_equivalents", () => {
    const ge = makeCourse({
      course_number: "GE 1A",
      category: "ge",
      is_placeholder: true,
      quarter_equivalents: ["ENGL 134", "ENGL 1340"],
    });
    const completed = toNormalizedSet(["ENGL 134"]);
    expect(getCourseStatus(ge, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("returns completed via geAreaMap (approved semester course)", () => {
    const ge = makeCourse({ course_number: "GE 1A", category: "ge", is_placeholder: true });
    const geAreaMap: GEAreaMap = { "GE 1A": ["ENGL 1500", "COMM 101"] };
    const completed = toNormalizedSet(["COMM 101"]);
    expect(getCourseStatus(ge, completed, new Set(), new Set(), new Set(), emptyLookup, geAreaMap)).toBe("completed");
  });

  it("returns in_progress when a geAreaMap course is in-progress", () => {
    const ge = makeCourse({ course_number: "GE 1C", category: "ge", is_placeholder: true });
    const geAreaMap: GEAreaMap = { "GE 1C": ["COMM 101", "COMS 1010"] };
    const inProgress = toNormalizedSet(["COMS 1010"]);
    expect(getCourseStatus(ge, new Set(), inProgress, new Set(), new Set(), emptyLookup, geAreaMap)).toBe("in_progress");
  });

  it("returns incomplete when no approved course is known", () => {
    const ge = makeCourse({ course_number: "GE 3A", category: "ge", is_placeholder: true });
    expect(getCourseStatus(ge, new Set(), new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("incomplete");
  });
});
