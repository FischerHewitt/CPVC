import { describe, it, expect } from "vitest";
import { getCourseStatus, toNormalizedSet, expandSlashCourseNumber } from "./course-status";
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

  it("returns completed via quarter_equivalent that needs norm() (regression)", () => {
    // completedNums is always uppercase-normalized; course_number and quarter_equivalents
    // must also be norm()'d before lookup so mixed-case values still match.
    const course = makeCourse({ course_number: "csc 1024", quarter_equivalents: ["csc 101"] });
    const completed = toNormalizedSet(["CSC 101"]);
    expect(getCourseStatus(course, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("returns in_progress via lowercase course_number (regression)", () => {
    const course = makeCourse({ course_number: "math 1261" });
    const inProgress = toNormalizedSet(["MATH 1261"]);
    expect(getCourseStatus(course, new Set(), inProgress, new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("in_progress");
  });

  it("returns completed when a non-required course is auto-satisfied by a later course", () => {
    const course = makeCourse({
      course_number: "MCRO 2221",
      auto_satisfied_by: ["MCRO 2224"],
      is_required: false,
    });
    const completed = toNormalizedSet(["MCRO 2224"]);
    expect(getCourseStatus(course, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("returns completed when an orientation placeholder is auto-satisfied by quarter CSC 101", () => {
    const course = makeCourse({
      course_number: "CSC/CPE 1000",
      title: "Computing Majors Orientation",
      is_placeholder: true,
      auto_satisfied_by: ["CSC 101"],
    });
    const completed = toNormalizedSet(["CSC 101"]);
    expect(getCourseStatus(course, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
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

// ── expandSlashCourseNumber ───────────────────────────────────────────────────

describe("expandSlashCourseNumber", () => {
  it("returns single-element array when no slash", () => {
    expect(expandSlashCourseNumber("CSC 1024")).toEqual(["CSC 1024"]);
  });

  it("expands two-part slash course", () => {
    expect(expandSlashCourseNumber("CHEM 2240/2242")).toEqual(["CHEM 2240", "CHEM 2242"]);
  });

  it("expands three-part slash course", () => {
    expect(expandSlashCourseNumber("BIO 4461/4462/4463")).toEqual(["BIO 4461", "BIO 4462", "BIO 4463"]);
  });

  it("handles letter suffix variant", () => {
    expect(expandSlashCourseNumber("PLSC 1120/1120L")).toEqual(["PLSC 1120", "PLSC 1120L"]);
  });
});

// ── slash-choice prereq status ────────────────────────────────────────────────

describe("getCourseStatus — slash-choice prereqs", () => {
  it("returns locked when sole unmet prereq is a slash-choice tile", () => {
    const slashTile = makeCourse({ course_number: "CHEM 2240/2242" });
    const course = makeCourse({ course_number: "CHEM 3000", prerequisites: ["CHEM 2240/2242"] });
    const lookup = new Map([
      ["CHEM 2240/2242", slashTile],
      ["CHEM 2240", slashTile],
      ["CHEM 2242", slashTile],
    ]);
    expect(getCourseStatus(course, new Set(), new Set(), new Set(), new Set(), lookup, emptyGEMap)).toBe("locked");
  });

  it("returns incomplete when slash prereq is satisfied via a component number", () => {
    const slashTile = makeCourse({ course_number: "CHEM 2240/2242" });
    const course = makeCourse({ course_number: "CHEM 3000", prerequisites: ["CHEM 2240/2242"] });
    const lookup = new Map([
      ["CHEM 2240/2242", slashTile],
      ["CHEM 2240", slashTile],
      ["CHEM 2242", slashTile],
    ]);
    const known = toNormalizedSet(["CHEM 2240"]);
    expect(getCourseStatus(course, known, new Set(), new Set(), known, lookup, emptyGEMap)).toBe("incomplete");
  });

  it("returns locked (not warning) when unmet prereq is a regular course", () => {
    const prereq = makeCourse({ course_number: "CSC 1024" });
    const course = makeCourse({ course_number: "CSC 2000", prerequisites: ["CSC 1024"] });
    const lookup = new Map([["CSC 1024", prereq]]);
    expect(getCourseStatus(course, new Set(), new Set(), new Set(), new Set(), lookup, emptyGEMap)).toBe("locked");
  });

  it("returns locked when one prereq is a slash tile and another is a definite lock", () => {
    const slashTile = makeCourse({ course_number: "CHEM 2240/2242" });
    const solidPrereq = makeCourse({ course_number: "CSC 1024" });
    const course = makeCourse({ course_number: "CSC 3000", prerequisites: ["CHEM 2240/2242", "CSC 1024"] });
    const lookup = new Map([
      ["CHEM 2240/2242", slashTile],
      ["CHEM 2240", slashTile],
      ["CHEM 2242", slashTile],
      ["CSC 1024", solidPrereq],
    ]);
    expect(getCourseStatus(course, new Set(), new Set(), new Set(), new Set(), lookup, emptyGEMap)).toBe("locked");
  });
});

// ── slash-choice tile completion detection ────────────────────────────────────

describe("getCourseStatus — slash-choice tile self-completion", () => {
  it("marks a slash-choice placeholder as completed when a component number is in completed", () => {
    // e.g. student has 'CSC 1024' on transcript; tile is 'CSC/CPE 1024'
    const tile = makeCourse({ course_number: "CSC/CPE 1024", is_placeholder: true });
    const completed = toNormalizedSet(["CSC 1024"]);
    expect(getCourseStatus(tile, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("marks a slash-choice placeholder as completed via the second component", () => {
    const tile = makeCourse({ course_number: "CSC/CPE 1024", is_placeholder: true });
    const completed = toNormalizedSet(["CPE 1024"]);
    expect(getCourseStatus(tile, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
  });

  it("marks a slash-choice placeholder as in_progress when a component is in inProgress", () => {
    const tile = makeCourse({ course_number: "MATH 1261/1264", is_placeholder: true });
    const inProgress = toNormalizedSet(["MATH 1261"]);
    expect(getCourseStatus(tile, new Set(), inProgress, new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("in_progress");
  });

  it("does not mark a slash-choice placeholder as completed from the full slash string alone", () => {
    const tile = makeCourse({ course_number: "CSC/CPE 1024", is_placeholder: true });
    const completed = toNormalizedSet(["CSC/CPE 1024"]);
    expect(getCourseStatus(tile, completed, new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("completed");
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

  it("returns in_progress when a quarter course satisfies a semester GE approved course", () => {
    const ge = makeCourse({ course_number: "GE 1B", category: "ge", is_placeholder: true });
    const geAreaMap: GEAreaMap = { "GE 1B": ["COMS 1126"] };
    const inProgress = toNormalizedSet(["COMS 126"]);
    expect(getCourseStatus(ge, new Set(), inProgress, new Set(), new Set(), emptyLookup, geAreaMap)).toBe("in_progress");
  });

  it("returns incomplete when no approved course is known", () => {
    const ge = makeCourse({ course_number: "GE 3A", category: "ge", is_placeholder: true });
    expect(getCourseStatus(ge, new Set(), new Set(), new Set(), new Set(), emptyLookup, emptyGEMap)).toBe("incomplete");
  });
});
