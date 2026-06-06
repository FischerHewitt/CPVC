import { describe, expect, it } from "vitest";
import { applyAddCustomCourse, applyAssignCustomCourse, applyClearCustomAssignment, applyRemoveCustomCourse, applySetCustomCourseStatus, applyUpdateCustomCourse } from "./custom-courses";
import type { TranscriptSession } from "./types";

const BASE_SESSION: TranscriptSession = {
  sessionId: "sess-1",
  studentName: "Test Student",
  major: "MATH",
  completed: [],
  inProgress: [],
};

const ACCT: { course_number: string; title: string; units: number } = {
  course_number: "ACCT 221",
  title: "Accounting for Non-Business Majors",
  units: 4,
};

describe("applyAddCustomCourse", () => {
  it("adds a new entry to customCourses keyed by the provided id", () => {
    const next = applyAddCustomCourse(BASE_SESSION, 1, ACCT, "uuid-1");

    expect(next.customCourses?.["uuid-1"]).toBeDefined();
    expect(next.customCourses!["uuid-1"].course_number).toBe("ACCT 221");
  });

  it("stores the correct term column", () => {
    const next = applyAddCustomCourse(BASE_SESSION, 3, ACCT, "uuid-1");

    expect(next.customCourses!["uuid-1"].grid_col).toBe(3);
  });

  it("sets status to planned by default", () => {
    const next = applyAddCustomCourse(BASE_SESSION, 0, ACCT, "uuid-1");

    expect(next.customCourses!["uuid-1"].status).toBe("planned");
  });

  it("preserves existing custom courses when adding a new one", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "existing": { course_number: "MU 1010", title: "Music", units: 3, grid_col: 0, status: "planned" },
      },
    };

    const next = applyAddCustomCourse(session, 1, ACCT, "uuid-2");

    expect(next.customCourses!["existing"]).toBeDefined();
    expect(next.customCourses!["uuid-2"]).toBeDefined();
  });

  it("does not mutate the original session", () => {
    applyAddCustomCourse(BASE_SESSION, 0, ACCT, "uuid-1");

    expect(BASE_SESSION.customCourses).toBeUndefined();
  });

  it("sets assignedToSlotId when provided at add time", () => {
    const next = applyAddCustomCourse(BASE_SESSION, 1, ACCT, "uuid-1", "PHYS1420");

    expect(next.customCourses!["uuid-1"].assignedToSlotId).toBe("PHYS1420");
  });
});

describe("applyUpdateCustomCourse", () => {
  it("updates course_number, title, and units", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Old Title", units: 4, grid_col: 1, status: "planned" },
      },
    };

    const next = applyUpdateCustomCourse(session, "uuid-1", { course_number: "BUS 212", title: "New Title", units: 3 });

    expect(next.customCourses!["uuid-1"].course_number).toBe("BUS 212");
    expect(next.customCourses!["uuid-1"].title).toBe("New Title");
    expect(next.customCourses!["uuid-1"].units).toBe(3);
  });

  it("preserves grid_col and status when updating course", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Old", units: 4, grid_col: 2, status: "completed" },
      },
    };

    const next = applyUpdateCustomCourse(session, "uuid-1", { course_number: "BUS 212", title: "New", units: 3 });

    expect(next.customCourses!["uuid-1"].grid_col).toBe(2);
    expect(next.customCourses!["uuid-1"].status).toBe("completed");
  });

  it("updates assignedToSlotId when provided", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Old", units: 4, grid_col: 1, status: "planned", assignedToSlotId: "OLD_SLOT" },
      },
    };

    const next = applyUpdateCustomCourse(session, "uuid-1", { assignedToSlotId: "NEW_SLOT" });

    expect(next.customCourses!["uuid-1"].assignedToSlotId).toBe("NEW_SLOT");
  });

  it("clears assignedToSlotId when passed undefined", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Old", units: 4, grid_col: 1, status: "planned", assignedToSlotId: "SLOT" },
      },
    };

    const next = applyUpdateCustomCourse(session, "uuid-1", { assignedToSlotId: undefined });

    expect(next.customCourses!["uuid-1"].assignedToSlotId).toBeUndefined();
  });

  it("returns session unchanged when id does not exist", () => {
    const next = applyUpdateCustomCourse(BASE_SESSION, "nonexistent", { course_number: "BUS 212" });
    expect(next).toEqual(BASE_SESSION);
  });
});

describe("applyAssignCustomCourse", () => {
  it("sets assignedToSlotId on the matching custom entry", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 1, status: "planned" },
      },
    };

    const next = applyAssignCustomCourse(session, "uuid-1", "PHYS1420");

    expect(next.customCourses!["uuid-1"].assignedToSlotId).toBe("PHYS1420");
  });

  it("preserves all other fields when assigning", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 1, status: "planned" },
      },
    };

    const next = applyAssignCustomCourse(session, "uuid-1", "PHYS1420");

    expect(next.customCourses!["uuid-1"].course_number).toBe("ACCT 221");
    expect(next.customCourses!["uuid-1"].grid_col).toBe(1);
  });

  it("returns session unchanged when customId does not exist", () => {
    const next = applyAssignCustomCourse(BASE_SESSION, "nonexistent", "PHYS1420");
    expect(next).toEqual(BASE_SESSION);
  });
});

describe("applyClearCustomAssignment", () => {
  it("removes assignedToSlotId from the matching custom entry", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 1, status: "planned", assignedToSlotId: "PHYS1420" },
      },
    };

    const next = applyClearCustomAssignment(session, "uuid-1");

    expect(next.customCourses!["uuid-1"].assignedToSlotId).toBeUndefined();
  });

  it("returns session unchanged when customId does not exist", () => {
    const next = applyClearCustomAssignment(BASE_SESSION, "nonexistent");
    expect(next.customCourses).toEqual({});
  });
});

describe("applySetCustomCourseStatus", () => {
  it("updates status on the matching custom entry", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 1, status: "planned" },
      },
    };

    const next = applySetCustomCourseStatus(session, "uuid-1", "completed");

    expect(next.customCourses!["uuid-1"].status).toBe("completed");
  });

  it("preserves all other fields when setting status", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 1, status: "planned", assignedToSlotId: "PHYS1420" },
      },
    };

    const next = applySetCustomCourseStatus(session, "uuid-1", "in_progress");

    expect(next.customCourses!["uuid-1"].assignedToSlotId).toBe("PHYS1420");
    expect(next.customCourses!["uuid-1"].course_number).toBe("ACCT 221");
  });

  it("returns session unchanged when id does not exist", () => {
    const next = applySetCustomCourseStatus(BASE_SESSION, "nonexistent", "completed");
    expect(next).toEqual(BASE_SESSION);
  });
});

describe("applyRemoveCustomCourse", () => {
  it("removes the entry with the given id", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: {
        "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 1, status: "planned" },
        "uuid-2": { course_number: "MU 1010", title: "Music", units: 3, grid_col: 0, status: "planned" },
      },
    };

    const next = applyRemoveCustomCourse(session, "uuid-1");

    expect(next.customCourses?.["uuid-1"]).toBeUndefined();
    expect(next.customCourses?.["uuid-2"]).toBeDefined();
  });

  it("returns session unchanged when id does not exist", () => {
    const next = applyRemoveCustomCourse(BASE_SESSION, "nonexistent");

    expect(next.customCourses).toEqual({});
  });

  it("does not mutate the original session", () => {
    const session: TranscriptSession = {
      ...BASE_SESSION,
      customCourses: { "uuid-1": { course_number: "ACCT 221", title: "Accounting", units: 4, grid_col: 1, status: "planned" } },
    };

    applyRemoveCustomCourse(session, "uuid-1");

    expect(session.customCourses?.["uuid-1"]).toBeDefined();
  });
});
