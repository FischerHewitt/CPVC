import { describe, expect, it, vi } from "vitest";
import {
  FREE_ELECTIVE_SEARCH_LIMIT,
  normalizeFreeElectiveSearchQuery,
  searchFreeElectiveCatalog,
  shouldSearchFreeElectiveCatalog,
} from "./free-elective-search";

describe("free elective catalog search", () => {
  it("normalizes whitespace and waits until the query is searchable", () => {
    expect(normalizeFreeElectiveSearchQuery("  coms1126  ")).toBe("coms1126");
    expect(shouldSearchFreeElectiveCatalog("c")).toBe(false);
    expect(shouldSearchFreeElectiveCatalog("  c  ")).toBe(false);
    expect(shouldSearchFreeElectiveCatalog("cs")).toBe(true);
  });

  it("searches catalog courses with the picker limit and trimmed query", async () => {
    const search = vi.fn().mockResolvedValue([
      { course_number: "COMS 1126", title: "Argument and Advocacy", units: 3 },
    ]);

    await expect(searchFreeElectiveCatalog("  coms1126  ", search)).resolves.toEqual([
      { course_number: "COMS 1126", title: "Argument and Advocacy", units: 3 },
    ]);
    expect(search).toHaveBeenCalledWith("coms1126", FREE_ELECTIVE_SEARCH_LIMIT, 0);
  });

  it("browses catalog courses for an empty query", async () => {
    const search = vi.fn().mockResolvedValue([
      { course_number: "AERO 1200", title: "Introduction to Aerospace Engineering", units: 1 },
    ]);

    await expect(searchFreeElectiveCatalog("", search, 50)).resolves.toEqual([
      { course_number: "AERO 1200", title: "Introduction to Aerospace Engineering", units: 1 },
    ]);
    expect(search).toHaveBeenCalledWith("", FREE_ELECTIVE_SEARCH_LIMIT, 50);
  });

  it("does not call the backend for too-short queries", async () => {
    const search = vi.fn();

    await expect(searchFreeElectiveCatalog("x", search)).resolves.toEqual([]);
    expect(search).not.toHaveBeenCalled();
  });

  it("keeps the picker stable if catalog search fails", async () => {
    const search = vi.fn().mockRejectedValue(new Error("backend down"));

    await expect(searchFreeElectiveCatalog("coms1126", search)).resolves.toEqual([]);
  });
});
