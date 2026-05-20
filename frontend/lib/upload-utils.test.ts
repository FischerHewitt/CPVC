import { describe, it, expect } from "vitest";
import { getFileType, validateFile, getProgressLabel } from "./upload-utils";

describe("getFileType", () => {
  it("returns pdf for .pdf files", () => {
    expect(getFileType("transcript.pdf")).toBe("pdf");
  });
  it("returns csv for .csv files", () => {
    expect(getFileType("courses.csv")).toBe("csv");
  });
  it("returns mbp for .mbp files", () => {
    expect(getFileType("plan.mbp")).toBe("mbp");
  });
  it("returns null for unknown extensions", () => {
    expect(getFileType("resume.docx")).toBeNull();
  });
  it("returns null for empty filename", () => {
    expect(getFileType("")).toBeNull();
  });
  it("is case-sensitive — uppercase extension returns null", () => {
    expect(getFileType("TRANSCRIPT.PDF")).toBeNull();
  });
  it("handles dotted filenames correctly", () => {
    expect(getFileType("my.file.name.pdf")).toBe("pdf");
  });
});

describe("validateFile", () => {
  it("returns null for valid pdf", () => {
    expect(validateFile("transcript.pdf")).toBeNull();
  });
  it("returns null for valid csv", () => {
    expect(validateFile("courses.csv")).toBeNull();
  });
  it("returns null for valid mbp", () => {
    expect(validateFile("plan.mbp")).toBeNull();
  });
  it("returns an error string for invalid file type", () => {
    const result = validateFile("resume.docx");
    expect(typeof result).toBe("string");
    expect(result).not.toBeNull();
  });
  it("error string mentions valid file types", () => {
    const result = validateFile("notes.txt") as string;
    expect(result.toLowerCase()).toMatch(/pdf|csv|mbp/);
  });
});

describe("getProgressLabel", () => {
  it("returns Reading transcript at 0%", () => {
    expect(getProgressLabel(0)).toBe("Reading transcript");
  });
  it("returns Reading transcript at 34%", () => {
    expect(getProgressLabel(34)).toBe("Reading transcript");
  });
  it("returns Matching completed courses at 35%", () => {
    expect(getProgressLabel(35)).toBe("Matching completed courses");
  });
  it("returns Creating flowchart at 70%", () => {
    expect(getProgressLabel(70)).toBe("Creating flowchart");
  });
  it("returns Opening flowchart at 95%", () => {
    expect(getProgressLabel(95)).toBe("Opening flowchart");
  });
  it("returns Opening flowchart at 100%", () => {
    expect(getProgressLabel(100)).toBe("Opening flowchart");
  });
});
