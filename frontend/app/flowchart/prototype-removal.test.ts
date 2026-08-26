import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const ROOT = resolve(__dirname, "../..");

describe("No prototype remnants", () => {
  it("prototype/MathCoPlan.tsx is deleted", () => {
    expect(existsSync(resolve(ROOT, "components/prototype/MathCoPlan.tsx"))).toBe(false);
  });

  it("flowchart page does not import from the prototype directory", () => {
    const src = readFileSync(resolve(ROOT, "app/flowchart/[sessionId]/page.tsx"), "utf8");
    expect(src).not.toMatch(/prototype/);
  });

  it("ElectiveDetailPanel does not have coPlanAfterCourse prop", () => {
    const src = readFileSync(resolve(ROOT, "components/ElectiveDetailPanel.tsx"), "utf8");
    expect(src).not.toMatch(/coPlanAfterCourse/);
  });
});
