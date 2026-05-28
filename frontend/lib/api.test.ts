import { afterEach, describe, expect, it, vi } from "vitest";
import {
  getConcentrations,
  getElectiveCourses,
  getFlowchart,
  getGEAreaMap,
  getGECourses,
  getMajors,
  getPlaceholderElectiveCourses,
  getProfessors,
  inferPrerequisites,
  searchCatalogCourses,
} from "./api";
import { resetPolyRatingsCacheForTests } from "./polyratings";

describe("API static fallback", () => {
  afterEach(() => {
    resetPolyRatingsCacheForTests();
    vi.unstubAllGlobals();
  });

  it("loads a bundled flowchart when the backend is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    const flowchart = await getFlowchart("CS");

    expect(flowchart.code).toBe("CS");
    expect(flowchart.major).toBe("Computer Science");
    expect(flowchart.courses.length).toBeGreaterThan(0);
  });

  it("inherits bundled base notes for full-flowchart concentrations", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    const flowchart = await getFlowchart("CS_DATA_ENG");
    const notesByTitle = Object.fromEntries(
      (flowchart.notes ?? []).map((section) => [section.title, section.items]),
    );

    expect(notesByTitle["Flowchart Tips"]).toEqual([
      "No Major or Support courses may be selected as credit/no credit. In addition, no more than 12 units of cooperative or internship courses can count towards your degree requirements.",
    ]);
    expect(notesByTitle["GE Tips"]).toEqual([
      "Required in Major or Support; also satisfies General Education (GE) requirement.",
    ]);
  });

  it("loads bundled majors when the backend majors endpoint is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    await expect(getMajors()).resolves.toContainEqual({
      code: "CS",
      name: "Computer Science",
    });
  });

  it("loads bundled concentrations when the backend concentrations endpoint is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    const concentrations = await getConcentrations("CS");

    expect(concentrations.some((c) => c.id === "ai_ml")).toBe(true);
  });

  it("still throws for unknown flowchart codes when backend and fallback both miss", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("nope", { status: 404 })));

    await expect(getFlowchart("NOT_A_MAJOR")).rejects.toThrow(/NOT_A_MAJOR|flowchart/i);
  });

  it("treats prerequisite inference as best-effort when the backend is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    await expect(inferPrerequisites("CS", ["CSC 101"])).resolves.toEqual([]);
  });

  it("treats optional detail endpoints as best-effort when the backend is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    await expect(getProfessors("COMS 126")).resolves.toEqual([]);
    await expect(getElectiveCourses("cs_ai_ml_elective")).resolves.toBeNull();
    await expect(getPlaceholderElectiveCourses({
      id: "slot",
      course_number: "Elective",
      title: "Elective",
      quarter_equivalents: [],
    })).resolves.toBeNull();
  });

  it("loads the bundled Privacy/Security elective list when the backend is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    const area = await getElectiveCourses("cs_privacy_security_elective");
    const numbers = area?.courses.map((course) => course.course_number) ?? [];

    expect(area?.title).toBe("Privacy & Security Concentration Elective");
    expect(numbers).toContain("CSC 4210");
    expect(numbers).toContain("CPE 4280");
    expect(numbers).not.toContain("CSC 3710");
  });

  it("loads GE professors from PolyRatings when the backend professor endpoint is unavailable", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("professors.all")) {
        return new Response(JSON.stringify({
          result: {
            data: [
              {
                id: "mehl",
                firstName: "Martin",
                lastName: "Mehl",
                courses: ["COMS126 - Argument and Advocacy"],
                overallRating: 3.7,
                numEvals: 298,
              },
              {
                id: "unrelated",
                firstName: "Ada",
                lastName: "Lovelace",
                courses: ["CSC 101"],
                overallRating: 4,
                numEvals: 30,
              },
            ],
          },
        }));
      }
      return new Response("missing backend route", { status: 404 });
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(getProfessors("COMS 1126")).resolves.toEqual([
      {
        name: "Martin Mehl",
        overall_score: 3.7,
        num_ratings: 298,
        polyratings_url: "https://polyratings.dev/professor/mehl",
      },
    ]);
    expect(fetchMock).toHaveBeenCalledWith("/api/professors/COMS%201126");
    expect(fetchMock).toHaveBeenCalledWith("https://api-prod.polyratings.org/professors.all");
  });

  it("loads GE professors from PolyRatings when the backend returns an empty professor list", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("professors.all")) {
        return new Response(JSON.stringify({
          result: {
            data: [
              {
                id: "speech",
                firstName: "Lisa",
                lastName: "Kawamura",
                courses: ["COMS 101"],
                overallRating: 3.8,
                numEvals: 338,
              },
            ],
          },
        }));
      }
      return new Response(JSON.stringify({ professors: [] }));
    }));

    await expect(getProfessors("COMS 1101")).resolves.toMatchObject([
      {
        name: "Lisa Kawamura",
        num_ratings: 338,
      },
    ]);
  });

  it("loads bundled GE approved courses when the backend is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    const area = await getGECourses("GE 1B");

    expect(area?.title).toBe("Critical Thinking");
    expect(area?.courses).toContainEqual({
      course_number: "COMS 1126",
      title: "Argument and Advocacy",
      units: 3,
    });
  });

  it("loads bundled GE approved courses when the backend returns an HTTP error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("nope", { status: 404 })));

    const areaMap = await getGEAreaMap();
    const area = await getGECourses("GE 1B");

    expect(areaMap["GE 1B"]).toContain("COMS 1126");
    expect(area?.courses.some((course) => course.course_number === "COMS 1126")).toBe(true);
  });

  it("searches catalog courses through the backend", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      courses: [{ course_number: "COMS 1126", title: "Argument and Advocacy", units: 3 }],
    })));
    vi.stubGlobal("fetch", fetchMock);

    await expect(searchCatalogCourses("coms1126", 7, 14)).resolves.toEqual([
      { course_number: "COMS 1126", title: "Argument and Advocacy", units: 3 },
    ]);
    expect(String(fetchMock.mock.calls[0][0])).toContain("/api/courses/search?");
    expect(String(fetchMock.mock.calls[0][0])).toContain("q=coms1126");
    expect(String(fetchMock.mock.calls[0][0])).toContain("limit=7");
    expect(String(fetchMock.mock.calls[0][0])).toContain("offset=14");
  });

  it("returns an empty catalog search result when the backend search fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend down")));

    await expect(searchCatalogCourses("coms1126")).resolves.toEqual([]);
  });
});
