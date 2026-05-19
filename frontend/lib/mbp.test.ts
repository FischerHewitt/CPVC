import { describe, it, expect } from "vitest";
import { parseMbpFile, mbpFilename } from "./mbp";
import type { TranscriptSession } from "./types";

const BASE_SESSION: TranscriptSession = {
  sessionId: "abc-123",
  studentName: "Jane Doe",
  major: "CS",
  completed: ["CSC 1024", "MATH 1261"],
  inProgress: ["CSC 2000"],
  coursePositions: {},
  plannedGECourses: {},
  plannedGEUnits: {},
  concentration: "ai_ml",
};

// ── parseMbpFile ──────────────────────────────────────────────────────────────

describe("parseMbpFile", () => {
  it("round-trips a full session", () => {
    const result = parseMbpFile(JSON.stringify(BASE_SESSION));
    expect(result.major).toBe("CS");
    expect(result.completed).toEqual(["CSC 1024", "MATH 1261"]);
    expect(result.inProgress).toEqual(["CSC 2000"]);
    expect(result.concentration).toBe("ai_ml");
  });

  it("preserves optional fields", () => {
    const result = parseMbpFile(JSON.stringify(BASE_SESSION));
    expect(result.coursePositions).toEqual({});
    expect(result.plannedGECourses).toEqual({});
    expect(result.sessionId).toBe("abc-123");
  });

  it("accepts a session with only the required fields", () => {
    const minimal = { major: "ME", completed: [] };
    const result = parseMbpFile(JSON.stringify(minimal));
    expect(result.major).toBe("ME");
    expect(result.completed).toEqual([]);
  });

  it("preserves coursePositions with data", () => {
    const session = {
      ...BASE_SESSION,
      coursePositions: { "CS_csc1024": { grid_col: 2, grid_row: 1 } },
    };
    const result = parseMbpFile(JSON.stringify(session));
    expect(result.coursePositions).toEqual({ "CS_csc1024": { grid_col: 2, grid_row: 1 } });
  });

  it("preserves plannedGECourses", () => {
    const session = {
      ...BASE_SESSION,
      plannedGECourses: { "GE 1A": "ENGL 1500" },
    };
    const result = parseMbpFile(JSON.stringify(session));
    expect(result.plannedGECourses).toEqual({ "GE 1A": "ENGL 1500" });
  });

  it("throws on malformed JSON", () => {
    expect(() => parseMbpFile("{not: valid json}")).toThrow();
  });

  it("throws when major is missing", () => {
    const data = { completed: ["CSC 1024"] };
    expect(() => parseMbpFile(JSON.stringify(data))).toThrow("Invalid Mustang Blueprints file");
  });

  it("throws when completed is missing", () => {
    const data = { major: "CS" };
    expect(() => parseMbpFile(JSON.stringify(data))).toThrow("Invalid Mustang Blueprints file");
  });

  it("throws when completed is not an array", () => {
    const data = { major: "CS", completed: "CSC 1024" };
    expect(() => parseMbpFile(JSON.stringify(data))).toThrow("Invalid Mustang Blueprints file");
  });

  it("throws when major is a number instead of string", () => {
    const data = { major: 42, completed: [] };
    expect(() => parseMbpFile(JSON.stringify(data))).toThrow("Invalid Mustang Blueprints file");
  });

  it("throws on empty string input", () => {
    expect(() => parseMbpFile("")).toThrow();
  });

  it("throws on null JSON", () => {
    expect(() => parseMbpFile("null")).toThrow("Invalid Mustang Blueprints file");
  });
});

// ── mbpFilename ───────────────────────────────────────────────────────────────

describe("mbpFilename", () => {
  it("builds filename from name and major", () => {
    expect(mbpFilename({ studentName: "Jane Doe", major: "CS" })).toBe("jane_doe-cs-flowchart.mbp");
  });

  it("lowercases the major code", () => {
    expect(mbpFilename({ studentName: "Alex", major: "AERO" })).toBe("alex-aero-flowchart.mbp");
  });

  it("replaces spaces in name with underscores", () => {
    expect(mbpFilename({ studentName: "Pat Smith", major: "ME" })).toBe("pat_smith-me-flowchart.mbp");
  });

  it("replaces special characters in name with underscores", () => {
    expect(mbpFilename({ studentName: "O'Brien", major: "CPE" })).toBe("o_brien-cpe-flowchart.mbp");
  });

  it("preserves digits in student name", () => {
    expect(mbpFilename({ studentName: "Student2024", major: "CPE" })).toBe("student2024-cpe-flowchart.mbp");
  });

  it("handles a name that is already a major code (Browse mode)", () => {
    expect(mbpFilename({ studentName: "Computer Science", major: "CS" })).toBe("computer_science-cs-flowchart.mbp");
  });

  it("produces valid filename for all-special-char name", () => {
    const filename = mbpFilename({ studentName: "---", major: "BIO" });
    expect(filename).toBe("___-bio-flowchart.mbp");
  });

  it("always ends with .mbp", () => {
    const filename = mbpFilename({ studentName: "Any Name", major: "SE" });
    expect(filename.endsWith(".mbp")).toBe(true);
  });
});
