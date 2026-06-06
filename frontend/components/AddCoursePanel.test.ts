import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import React from "react";
import AddCoursePanel from "./AddCoursePanel";

const noop = () => {};
const noopRef = { current: null };

function renderPanel(col: number, termLabel: string) {
  return renderToStaticMarkup(
    React.createElement(AddCoursePanel, {
      col,
      termLabel,
      panelPos: { x: 100, y: 100 },
      panelDrag: noopRef,
      onSetPos: noop,
      onAdd: noop,
      onClose: noop,
    }),
  );
}

describe("AddCoursePanel", () => {
  it("shows the term label in the panel header", () => {
    const html = renderPanel(1, "Fr Spring");
    expect(html).toContain("Fr Spring");
  });

  it("shows 'Add Course' as the panel title", () => {
    const html = renderPanel(0, "Fr Fall");
    expect(html).toContain("Add Course");
  });

  it("renders the Add to Flowchart button as disabled when no course is selected", () => {
    const html = renderPanel(0, "Fr Fall");
    expect(html).toContain("Add to Flowchart");
    expect(html).toContain("disabled");
  });
});
