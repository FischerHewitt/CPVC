import { describe, expect, it } from "vitest";
import { parseCalPolyCSV, parseCSVLine } from "./calpoly-csv";

const STUDENT_CENTER_CSV = `Course,Description,Term,Grade,Units,Status,Status Note
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

describe("parseCSVLine", () => {
  it("handles quoted commas and escaped quotes", () => {
    expect(parseCSVLine('"COMS 126","Argument, Advocacy, and ""Debate""","In Progress"')).toEqual([
      "COMS 126",
      "Argument, Advocacy, and \"Debate\"",
      "In Progress",
    ]);
  });
});

describe("parseCalPolyCSV", () => {
  it("parses the Student Center course list format", () => {
    const result = parseCalPolyCSV(`Course,Description,Term,Grade,Units,Status,Status Note
"COMS 126","Argument and Advocacy","Spring Quarter 2026","-","4","In Progress",""
"CSC 101","Fundamentals of Computer Sci","Fall Quarter 2025","A","4","Taken",""
"MATH 141","Calculus I","Fall Quarter 2025","CR","4","Transferred (Test)",""
"CSC 3665","Intro to DataBse Mngmnt Systms","Fall Semester 2027","-","4","Planned",""`);

    expect(result).toEqual({
      completed: ["CSC 101", "MATH 141"],
      inProgress: ["COMS 126"],
    });
  });

  it("returns null when required headers are missing", () => {
    expect(parseCalPolyCSV("Name,Status\nCOMS 126,In Progress")).toBeNull();
  });

  it("parses a representative Student Center export without dropping semester in-progress courses", () => {
    const result = parseCalPolyCSV(STUDENT_CENTER_CSV);

    expect(result?.completed).toEqual([
      "AUTO 1TR",
      "B3GE 1TR",
      "BIO 111",
      "CHIN 1TR",
      "COMS 101",
      "CSC 101",
      "CSC 202",
      "CSC 490",
      "ENGL 134",
      "MATH 141",
      "MATH 142",
      "MATH 143",
      "MATH 1TR",
      "MATH 244",
      "MU 101",
      "MU 173",
      "MU 176",
      "MU 178",
      "MU 1TR",
      "PHYS 141",
      "PHYS 1TR",
    ]);
    expect(result?.inProgress).toEqual([
      "COMS 126",
      "CPE 225",
      "CSC 203",
      "ES 1112",
      "ES 253",
      "HIST 2202",
      "MATH 2031",
      "ME 470",
      "ME 471",
      "MU 1176",
      "MU 1178",
      "STAT 3210",
    ]);
  });

  it("handles UTF-8 BOMs and CRLF line endings from spreadsheet downloads", () => {
    const text = `\uFEFFCourse,Description,Term,Grade,Units,Status,Status Note\r
"COMS 126","Argument and Advocacy","Spring Quarter 2026","-","4","In Progress",""\r
"CSC 101","Fundamentals of Computer Sci","Fall Quarter 2025","A","4","Taken",""`;

    expect(parseCalPolyCSV(text)).toEqual({
      completed: ["CSC 101"],
      inProgress: ["COMS 126"],
    });
  });

  it("does not keep an in-progress duplicate when the same course is already completed", () => {
    const result = parseCalPolyCSV(`Course,Description,Term,Grade,Units,Status,Status Note
"MU 173","Wind Ensemble","Spring Quarter 2026","-","1","In Progress",""
"MU 173","Wind Ensemble","Winter Quarter 2026","A","1","Taken",""`);

    expect(result).toEqual({
      completed: ["MU 173"],
      inProgress: [],
    });
  });
});
