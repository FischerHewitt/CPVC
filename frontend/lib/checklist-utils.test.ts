import { describe, it, expect } from "vitest";
import {
  norm,
  toNormalizedSet,
  matchesCourse,
  courseIsCompleted,
  courseIsInProgress,
  geAreaIsKnown,
} from "./checklist-utils";
import type { Course } from "./types";

function makeCourse(partial: Partial<Course> = {}): Course {
  return {
    id: "test",
    course_number: "CSC 101",
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

describe("norm", () => {
  it("uppercases and trims surrounding whitespace", () => {
    expect(norm("  csc 101  ")).toBe("CSC 101");
  });

  it("collapses multiple interior spaces", () => {
    expect(norm("CSC  101")).toBe("CSC 101");
  });

  it("leaves already-normalized strings unchanged", () => {
    expect(norm("MATH 141")).toBe("MATH 141");
  });
});

describe("toNormalizedSet", () => {
  it("normalizes all entries and deduplicates", () => {
    const set = toNormalizedSet(["csc 101", "CSC 101", "  EE 200  "]);
    expect(set.has("CSC 101")).toBe(true);
    expect(set.has("EE 200")).toBe(true);
    expect(set.size).toBe(2);
  });
});

describe("matchesCourse", () => {
  it("returns true for empty query", () => {
    expect(matchesCourse(makeCourse(), "")).toBe(true);
    expect(matchesCourse(makeCourse(), "   ")).toBe(true);
  });

  it("matches by course number (case-insensitive)", () => {
    const course = makeCourse({ course_number: "CSC 101" });
    expect(matchesCourse(course, "csc 101")).toBe(true);
    expect(matchesCourse(course, "CSC")).toBe(true);
  });

  it("matches by title", () => {
    const course = makeCourse({ title: "Data Structures" });
    expect(matchesCourse(course, "data structures")).toBe(true);
    expect(matchesCourse(course, "STRUCT")).toBe(true);
  });

  it("matches by quarter equivalent", () => {
    const course = makeCourse({ quarter_equivalents: ["CSC 202"] });
    expect(matchesCourse(course, "CSC 202")).toBe(true);
  });

  it("returns false for unrelated query", () => {
    const course = makeCourse({ course_number: "CSC 101", title: "Intro", quarter_equivalents: [] });
    expect(matchesCourse(course, "MATH")).toBe(false);
  });
});

describe("courseIsCompleted", () => {
  it("returns true when course number is in the completed set", () => {
    const course = makeCourse({ course_number: "CSC 101" });
    expect(courseIsCompleted(course, toNormalizedSet(["csc 101"]))).toBe(true);
  });

  it("returns true when a quarter equivalent is completed", () => {
    const course = makeCourse({ course_number: "CSC 101", quarter_equivalents: ["CSC 102"] });
    expect(courseIsCompleted(course, toNormalizedSet(["CSC 102"]))).toBe(true);
  });

  it("returns false when neither course nor equivalents are completed", () => {
    const course = makeCourse({ course_number: "CSC 101", quarter_equivalents: [] });
    expect(courseIsCompleted(course, toNormalizedSet(["MATH 141"]))).toBe(false);
  });
});

describe("courseIsInProgress", () => {
  it("returns true when the course number is in-progress", () => {
    const course = makeCourse({ course_number: "CSC 101" });
    expect(courseIsInProgress(course, toNormalizedSet(["CSC 101"]))).toBe(true);
  });

  it("returns true when a quarter equivalent is in-progress", () => {
    const course = makeCourse({ quarter_equivalents: ["CSC 102"] });
    expect(courseIsInProgress(course, toNormalizedSet(["csc 102"]))).toBe(true);
  });

  it("returns false when course is not in-progress", () => {
    const course = makeCourse({ course_number: "CSC 101" });
    expect(courseIsInProgress(course, toNormalizedSet([]))).toBe(false);
  });
});

describe("geAreaIsKnown", () => {
  it("returns true when the geAreaMap has a completed course for this area", () => {
    const placeholder = makeCourse({ course_number: "GE 1A", is_placeholder: true, category: "ge" });
    const geAreaMap = { "GE 1A": ["ENGL 134"] };
    expect(geAreaIsKnown(placeholder, geAreaMap, toNormalizedSet(["ENGL 134"]))).toBe(true);
  });

  it("returns true when the placeholder course_number itself is in the known set", () => {
    const placeholder = makeCourse({ course_number: "GE 2", is_placeholder: true, category: "ge", quarter_equivalents: [] });
    expect(geAreaIsKnown(placeholder, {}, toNormalizedSet(["GE 2"]))).toBe(true);
  });

  it("returns false when no candidate is in the known set", () => {
    const placeholder = makeCourse({ course_number: "GE 3", is_placeholder: true, category: "ge" });
    const geAreaMap = { "GE 3": ["COMM 101"] };
    expect(geAreaIsKnown(placeholder, geAreaMap, toNormalizedSet(["ENGL 134"]))).toBe(false);
  });

  it("returns false when geAreaMap has no entry for this course", () => {
    const placeholder = makeCourse({ course_number: "GE 4", is_placeholder: true, category: "ge", quarter_equivalents: [] });
    expect(geAreaIsKnown(placeholder, {}, toNormalizedSet(["ENGL 134"]))).toBe(false);
  });
});
