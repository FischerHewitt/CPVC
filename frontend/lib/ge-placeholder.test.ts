import { describe, expect, it } from "vitest";
import type { Course, GEAreaMap } from "./types";
import { getCourseStatus, toNormalizedSet } from "./course-status";
import { parseCalPolyCSV } from "./calpoly-csv";
import {
  gePlaceholderCandidates,
  gePlaceholderDisplayData,
  normalizePlannedGEPlaceholderStatuses,
  withPlannedGECourses,
} from "./ge-placeholder";

const FISCHER_COURSE_LIST_CSV = `Course,Description,Term,Grade,Units,Status,Status Note
"AUTO 1TR","Auto Transfer Lower Division","Fall Quarter 2025","A","3","Transferred (Course)",""
"B3GE 1TR","Laboratory Activity","Fall Quarter 2025","CR","1","Transferred (Test)",""
"BIO 111","General Biology","Winter Quarter 2026","A","4","Taken",""
"CHIN 1TR","Chin Transfer Lower Division","Fall Quarter 2025","A","4.5","Transferred (Course)",""
"COMS 101","Public Speaking","Fall Quarter 2025","A","4","Taken",""
"COMS 126","Argument and Advocacy","Spring Quarter 2026","-","4","In Progress",""
"CPE 225","Intro to Computer Organization","Spring Quarter 2026","-","4","In Progress",""
"CSC 101","Fundamentals of Computer Sci","Fall Quarter 2025","A","4","Taken",""
"CSC 202","Data Structures","Winter Quarter 2026","A","4","Taken",""
"CSC 203","Proj-Based OO Prog and Design","Spring Quarter 2026","-","4","In Progress",""
"CSC 3665","Intro to DataBse Mngmnt Systms","Fall Semester 2027","-","4","Planned",""
"CSC 490","Selected Advanced Topics","Fall Quarter 2025","A","1","Taken",""
"ENGL 134","Writing and Rhetoric","Winter Quarter 2026","A","4","Taken",""
"ES 1112","Race Culture & Politics in US","Fall Semester 2026","-","3","In Progress",""
"ES 253","Intro American Indian Studies","Spring Quarter 2026","-","4","In Progress",""
"HIST 2202","U.S. History Since 1877","Fall Semester 2026","-","3","In Progress",""
"MATH 141","Calculus I","Fall Quarter 2025","CR","4","Transferred (Test)",""
"MATH 142","Calculus II","Fall Quarter 2025","CR","4","Transferred (Test)",""
"MATH 143","Calculus III","Fall Quarter 2025","A","4","Taken",""
"MATH 1TR","Math Transfer Lower Division","Fall Quarter 2025","CR","1","Transferred (Test)",""
"MATH 2031","Transition to Advanced Math","Fall Semester 2026","-","3","In Progress",""
"MATH 244","Linear Analysis I","Winter Quarter 2026","A","4","Taken",""
"ME 470","Selected Advanced Topics","Spring Quarter 2026","-","3","In Progress",""
"ME 471","Selected Advanced Lab","Spring Quarter 2026","-","1","In Progress",""
"MU 101","Introduction to Music Theory","Fall Quarter 2025","CR","4","Transferred (Test)",""
"MU 1176","Mustang Band","Fall Semester 2026","-","1","In Progress",""
"MU 1178","Mustang Band Field Show","Fall Semester 2026","-","1","In Progress",""
"MU 173","Wind Ensemble","Spring Quarter 2026","-","1","In Progress",""
"MU 173","Wind Ensemble","Winter Quarter 2026","A","1","Taken",""
"MU 176","Mustang Band","Fall Quarter 2025","A","1","Taken",""
"MU 176","Mustang Band","Winter Quarter 2026","A","1","Taken",""
"MU 178","Field Show Marching Skills","Fall Quarter 2025","A","1","Taken",""
"MU 1TR","Mu   Transfer Lower Division","Fall Quarter 2025","CR","5","Transferred (Test)",""
"PHYS 141","General Physics I","Fall Quarter 2025","CR","4","Transferred (Test)",""
"PHYS 1TR","Phys Transfer Lower Division","Fall Quarter 2025","CR","4","Transferred (Test)",""
"STAT 3210","Engineering Statistics","Fall Semester 2026","-","3","In Progress",""`;

const criticalThinking: Course = {
  id: "GE1B",
  course_number: "GE 1B",
  title: "Critical Thinking",
  units: 3,
  category: "ge",
  grid_col: 1,
  grid_row: 3,
  prerequisites: [],
  quarter_equivalents: [],
  is_placeholder: true,
};

describe("GE placeholder status/display", () => {
  it("marks GE 1B in-progress when an approved course is in-progress", () => {
    const geAreaMap: GEAreaMap = { "GE 1B": ["COMS 1126"] };
    const inProgress = toNormalizedSet(["COMS 1126"]);
    const status = getCourseStatus(
      criticalThinking,
      new Set(),
      inProgress,
      new Set(),
      inProgress,
      new Map(),
      geAreaMap,
    );
    const display = gePlaceholderDisplayData(criticalThinking, new Set(), inProgress, geAreaMap);

    expect(status).toBe("in_progress");
    expect(display.inProgressChecked).toBe(true);
    expect(display.activeCourseNumber).toBe("COMS 1126");
  });

  it("marks GE 1B in-progress from the uploaded quarter COMS 126 course", () => {
    const geAreaMap: GEAreaMap = { "GE 1B": ["COMS 1126"] };
    const parsed = parseCalPolyCSV(FISCHER_COURSE_LIST_CSV);
    expect(parsed?.inProgress).toContain("COMS 126");

    const inProgress = toNormalizedSet(parsed?.inProgress ?? []);
    const status = getCourseStatus(
      criticalThinking,
      toNormalizedSet(parsed?.completed ?? []),
      inProgress,
      new Set(),
      inProgress,
      new Map(),
      geAreaMap,
    );
    const display = gePlaceholderDisplayData(criticalThinking, new Set(), inProgress, geAreaMap);

    expect(status).toBe("in_progress");
    expect(display.inProgressChecked).toBe(true);
    expect(display.activeCourseNumber).toBe("COMS 126");
  });

  it("counts a selected GE course even if the loaded GE area map is missing it", () => {
    const geAreaMap: GEAreaMap = {};
    const plannedGECourses = { "GE 1B": "COMS 1126" };
    const effectiveMap = withPlannedGECourses(geAreaMap, plannedGECourses);
    const inProgress = toNormalizedSet(["COMS 1126"]);

    expect(gePlaceholderCandidates(criticalThinking, effectiveMap, plannedGECourses)).toContain("COMS 1126");
    expect(getCourseStatus(
      criticalThinking,
      new Set(),
      inProgress,
      new Set(),
      inProgress,
      new Map(),
      effectiveMap,
    )).toBe("in_progress");
    expect(gePlaceholderDisplayData(
      criticalThinking,
      new Set(),
      inProgress,
      effectiveMap,
      plannedGECourses,
    )).toMatchObject({
      inProgressChecked: true,
      plannedCourseNumber: "COMS 1126",
      activeCourseNumber: "COMS 1126",
    });
  });

  it("prefers the selected GE course over a legacy placeholder status", () => {
    const geAreaMap: GEAreaMap = { "GE 1B": ["COMS 1126"] };
    const plannedGECourses = { "GE 1B": "COMS 1126" };
    const inProgress = toNormalizedSet(["GE 1B", "COMS 1126"]);

    expect(gePlaceholderDisplayData(
      criticalThinking,
      new Set(),
      inProgress,
      geAreaMap,
      plannedGECourses,
    )).toMatchObject({
      inProgressChecked: true,
      plannedCourseNumber: "COMS 1126",
      activeCourseNumber: "COMS 1126",
    });
  });

  it("migrates planned GE placeholder statuses to the selected concrete course", () => {
    const { session, changed } = normalizePlannedGEPlaceholderStatuses({
      sessionId: "test",
      studentName: "Test Student",
      major: "CS",
      completed: [],
      inProgress: ["GE 1B", "COMS 1126"],
      plannedGECourses: { "GE 1B": "COMS 1126" },
    });

    expect(changed).toBe(true);
    expect(session.inProgress).toEqual(["COMS 1126"]);
  });
});
