import { describe, expect, it } from "vitest";
import { parseUnitsRange } from "./units";

describe("parseUnitsRange", () => {
  it("parses a fixed integer string", () => {
    expect(parseUnitsRange("3")).toEqual({ units: 3 });
  });

  it("parses a fixed integer input", () => {
    expect(parseUnitsRange(3)).toEqual({ units: 3 });
  });

  it("parses a hyphen range", () => {
    expect(parseUnitsRange("1-3")).toEqual({ units: 1, units_min: 1, units_max: 3 });
  });

  it("parses an en-dash range", () => {
    expect(parseUnitsRange("1–3")).toEqual({ units: 1, units_min: 1, units_max: 3 });
  });

  it("returns default for empty string", () => {
    expect(parseUnitsRange("")).toEqual({ units: 3 });
  });

  it("returns default for null/undefined", () => {
    expect(parseUnitsRange(null)).toEqual({ units: 3 });
    expect(parseUnitsRange(undefined)).toEqual({ units: 3 });
  });

  it("respects custom default", () => {
    expect(parseUnitsRange("", 4)).toEqual({ units: 4 });
  });

  it("parses a wider range", () => {
    expect(parseUnitsRange("1-4")).toEqual({ units: 1, units_min: 1, units_max: 4 });
  });

  it("treats same-value range as fixed", () => {
    expect(parseUnitsRange("3-3")).toEqual({ units: 3 });
  });
});
