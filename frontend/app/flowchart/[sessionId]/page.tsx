"use client";

import { useCallback, useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import type { Course, CourseStatus, FreeElectiveStatus } from "@/lib/types";
import { expandSlashCourseNumber } from "@/lib/course-status";
import { useFlowchartSession } from "@/lib/useFlowchartSession";
import { usePanelState } from "@/lib/usePanelState";
import FlowchartGrid from "@/components/FlowchartGrid";
import CourseDetailPanel from "@/components/CourseDetailPanel";
import GEDetailPanel from "@/components/GEDetailPanel";
import ElectiveDetailPanel from "@/components/ElectiveDetailPanel";
import FreeElectivePickerPanel from "@/components/FreeElectivePickerPanel";
import ManualCourseChecklist from "@/components/ManualCourseChecklist";

export default function FlowchartPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();
  const fs = useFlowchartSession(sessionId);
  const panel = usePanelState();

  // Wire session mutations that require panel side-effects
  const toggleCourseCompleted = useCallback((course: Course) => {
    const { newStatus, openPicker } = fs.toggleCourseCompleted(course, panel.selectedCourse?.id);
    if (openPicker) panel.setSelectedFreeElectiveCourse(course);
    if (newStatus) panel.setSelectedStatus(newStatus);
  }, [fs, panel]);

  const toggleCourseInProgress = useCallback((course: Course) => {
    const { newStatus, openPicker } = fs.toggleCourseInProgress(course, panel.selectedCourse?.id);
    if (openPicker) panel.setSelectedFreeElectiveCourse(course);
    if (newStatus) panel.setSelectedStatus(newStatus);
  }, [fs, panel]);

  const setFreeElectiveStatus = useCallback((placeholder: Course, status: FreeElectiveStatus) => {
    const { openPicker } = fs.setFreeElectiveStatus(placeholder, status);
    if (openPicker) panel.setSelectedFreeElectiveCourse(placeholder);
  }, [fs, panel]);

  // Course search — depends on both resolvedFlowchart (session hook) and courseSearch (panel hook)
  const { searchTerms, courseSearchMatches, allMatchCount, highlightedCourseIds } = useMemo(() => {
    const terms = panel.courseSearch.trim().toLowerCase().split(/\s+/).filter(Boolean);
    if (!fs.resolvedFlowchart || terms.length === 0) {
      return { searchTerms: terms, courseSearchMatches: [], allMatchCount: 0, highlightedCourseIds: new Set<string>() };
    }
    const compact = (v: string) => v.toLowerCase().replace(/[^a-z0-9]/g, "");
    const all = fs.resolvedFlowchart.courses.filter((course) => {
      const col = fs.resolvedFlowchart!.columns[course.grid_col];
      const vals = [
        course.id, course.course_number, course.title, course.category,
        col?.year, col?.term, ...course.quarter_equivalents,
        ...expandSlashCourseNumber(course.course_number),
      ].filter(Boolean) as string[];
      const hay = vals.join(" ").toLowerCase();
      const compactHay = vals.map(compact).join(" ");
      return terms.every((t) => hay.includes(t) || compactHay.includes(compact(t)));
    });
    return {
      searchTerms: terms,
      courseSearchMatches: all.slice(0, 8),
      allMatchCount: all.length,
      highlightedCourseIds: panel.courseLookupOpen ? new Set(all.map((c) => c.id)) : new Set<string>(),
    };
  }, [panel.courseSearch, panel.courseLookupOpen, fs.resolvedFlowchart]);

  if (fs.error) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--cp-bg)" }}>
        <div className="text-center">
          <div className="text-red-500 font-semibold mb-2">{fs.error}</div>
          <button onClick={() => router.push("/")} className="text-sm text-gray-500 underline">← Start over</button>
        </div>
      </div>
    );
  }

  if (!fs.session || !fs.flowchart || !fs.resolvedFlowchart) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--cp-bg)" }}>
        <div className="text-gray-400 text-sm">Loading flowchart…</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--cp-bg)" }}>
      {/* Header */}
      <header
        className="px-6 py-3 flex items-center gap-4 flex-wrap relative"
        style={{
          background: "#002D72",
          backgroundImage: [
            "linear-gradient(rgba(255,255,255,0.06) 1px, transparent 1px)",
            "linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px)",
          ].join(", "),
          backgroundSize: "22px 22px",
          borderBottom: "2px solid rgba(255,255,255,0.18)",
        }}
      >
        <button onClick={() => router.push("/upload")} className="text-white/60 hover:text-white text-sm font-mono flex-shrink-0">← Back</button>
        <div className="text-white font-bold text-sm font-mono truncate">{fs.flowchart.major}</div>
        {fs.concentrations.length > 0 && (
          <>
            <div className="text-white/35 text-sm flex-shrink-0">·</div>
            <select
              value={fs.session.concentration ?? "none"}
              onChange={(e) => fs.changeConcentration(e.target.value)}
              className="text-sm rounded px-2 py-0.5 font-mono min-w-0 max-w-[180px] sm:max-w-none"
              style={{ background: "rgba(255,255,255,0.12)", color: "white", border: "1px solid rgba(255,255,255,0.25)" }}
            >
              {fs.concentrations.map((c) => (
                <option key={c.id} value={c.id} style={{ background: "#002D72", color: "white" }}>{c.label}</option>
              ))}
            </select>
          </>
        )}
        <div className="ml-auto flex items-center gap-3 flex-shrink-0">
          <Link href="/support" className="text-white/60 hover:text-white text-sm transition-colors font-mono hidden sm:inline">Support</Link>
          <div className="flex items-center gap-2">
            <Image src="/mb-logo.png" alt="Mustang Blueprints" width={28} height={28} className="rounded flex-shrink-0" style={{ border: "2px solid rgba(255,255,255,0.85)" }} />
            <span className="text-white font-bold text-xs font-mono tracking-widest uppercase hidden md:inline">Mustang Blueprints</span>
          </div>
        </div>
      </header>

      <main className="flex-1 p-2 sm:p-6">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-3 sm:p-5">
          <div className="mb-4 flex flex-wrap items-center gap-2">
            <div className="flex items-baseline gap-2 mr-auto">
              <h1 className="text-base sm:text-lg font-bold" style={{ color: "var(--cp-green)" }}>
                {fs.flowchart.major}
              </h1>
              <span className="text-gray-400 text-xs hidden sm:inline">4-Year Semester Flowchart</span>
            </div>
            <div className="flex gap-1.5 sm:gap-2">
              <button
                onClick={() => panel.setChecklistOpen(true)}
                className="rounded-lg px-3 sm:px-5 py-1.5 sm:py-2 text-xs sm:text-sm font-bold text-white shadow-sm transition-colors hover:opacity-90 active:scale-[0.98]"
                style={{ background: "var(--cp-green)" }}
              >
                Course Checklist
              </button>
              <button
                onClick={() => panel.setTipsOpen((o) => !o)}
                className="rounded-lg px-3 sm:px-5 py-1.5 sm:py-2 text-xs sm:text-sm font-bold shadow-sm transition-colors hover:opacity-90 active:scale-[0.98]"
                style={{ background: panel.tipsOpen ? "#005fa3" : "var(--cp-green)", color: "white" }}
              >
                Tips
              </button>
              <button
                onClick={() => panel.setMyNotesOpen((o) => !o)}
                className="rounded-lg px-3 sm:px-5 py-1.5 sm:py-2 text-xs sm:text-sm font-bold shadow-sm transition-colors hover:opacity-90 active:scale-[0.98]"
                style={{ background: panel.myNotesOpen ? "#005fa3" : "var(--cp-green)", color: "white" }}
              >
                My Notes
              </button>
              <button
                onClick={() => panel.setOtherCreditsOpen((o) => !o)}
                className="rounded-lg px-3 sm:px-5 py-1.5 sm:py-2 text-xs sm:text-sm font-bold shadow-sm transition-colors hover:opacity-90 active:scale-[0.98]"
                style={{ background: panel.otherCreditsOpen ? "#005fa3" : "var(--cp-green)", color: "white" }}
              >
                Other Credits
              </button>
              <button
                onClick={() => panel.setCourseLookupOpen((o) => !o)}
                className="rounded-lg px-3 sm:px-5 py-1.5 sm:py-2 text-xs sm:text-sm font-bold shadow-sm transition-colors hover:opacity-90 active:scale-[0.98]"
                style={{ background: panel.courseLookupOpen ? "#005fa3" : "var(--cp-green)", color: "white" }}
              >
                Course Lookup
              </button>
            </div>
            <div className="flex gap-1.5 sm:gap-2">
              <button
                onClick={fs.downloadSession}
                className="rounded border border-gray-200 px-2 sm:px-2.5 py-1 text-xs text-gray-400 transition-colors hover:border-gray-300 hover:text-gray-600"
              >
                Download
              </button>
              <button
                onClick={fs.resetCourseLayout}
                className="rounded border border-gray-200 px-2 sm:px-2.5 py-1 text-xs text-gray-400 transition-colors hover:border-gray-300 hover:text-gray-600 hidden sm:inline"
              >
                Reset Layout
              </button>
            </div>
          </div>

          <FlowchartGrid
            flowchart={fs.resolvedFlowchart}
            session={fs.session}
            inferred={fs.inferred}
            geAreaMap={fs.geAreaMap}
            highlightedCourseIds={highlightedCourseIds}
            onToggleCourseCompleted={toggleCourseCompleted}
            onToggleCourseInProgress={toggleCourseInProgress}
            onMoveCourse={fs.moveCourse}
            onCourseClick={panel.openCoursePanel}
          />
        </div>
      </main>

      <CourseDetailPanel
        course={panel.selectedCourse}
        status={panel.selectedStatus}
        allCourses={fs.resolvedFlowchart.courses}
        completed={fs.session.completed}
        inProgress={fs.session.inProgress}
        inferred={fs.inferred}
        onClose={() => { panel.setSelectedCourse(null); panel.setSelectedStatus(null); }}
      />

      <GEDetailPanel
        course={panel.selectedGECourse}
        completedSet={new Set(fs.session.completed)}
        inProgressSet={new Set(fs.session.inProgress)}
        plannedGECourses={fs.session.plannedGECourses ?? {}}
        onToggleGECourse={fs.toggleGECourse}
        onToggleGECourseInProgress={fs.toggleGECourseInProgress}
        onPlanGECourse={fs.planGECourse}
        onAreaLoaded={fs.rememberGEAreaCourses}
        onClose={() => panel.setSelectedGECourse(null)}
      />

      <ElectiveDetailPanel
        course={panel.selectedElectiveCourse}
        completedSet={new Set(fs.session.completed)}
        inProgressSet={new Set(fs.session.inProgress)}
        plannedElectiveCourses={fs.session.plannedGECourses ?? {}}
        currentSlotId={panel.selectedElectiveCourse?.id}
        plannedSlotUnits={panel.selectedElectiveCourse ? (fs.session.plannedCourseUnits ?? {})[panel.selectedElectiveCourse.id] : undefined}
        cappedCourseConfig={fs.getCappedCourseConfig(panel.selectedElectiveCourse)}
        onToggleElectiveCourse={fs.toggleElectiveCourse}
        onToggleElectiveCourseInProgress={fs.toggleElectiveCourseInProgress}
        onPlanElectiveCourse={fs.planElectiveCourse}
        onSetSlotUnits={fs.setSlotUnits}
        onClose={() => panel.setSelectedElectiveCourse(null)}
      />

      <FreeElectivePickerPanel
        course={panel.selectedFreeElectiveCourse}
        selection={panel.selectedFreeElectiveCourse ? (fs.session.plannedFreeElectiveCourses ?? {})[panel.selectedFreeElectiveCourse.id] : undefined}
        onChoose={fs.chooseFreeElectiveCourse}
        onSetStatus={setFreeElectiveStatus}
        onClear={fs.clearFreeElectiveCourse}
        onClose={() => panel.setSelectedFreeElectiveCourse(null)}
      />

      {/* Disclaimer */}
      <footer className="px-6 py-3 text-center text-xs text-gray-400 border-t border-gray-100 bg-white">
        Mustang Blueprints is an independent student project — <strong>not affiliated with Cal Poly</strong>. Always verify your plan with your academic advisor.
      </footer>

      {panel.tipsOpen && (
        <div
          className="fixed z-50 flex flex-col rounded-lg border border-gray-200 bg-white shadow-2xl"
          style={{ left: panel.tipsPos.x, top: panel.tipsPos.y, width: "min(400px, calc(100vw - 2rem))", height: "min(70vh, 480px)", minWidth: "240px", minHeight: "120px", resize: "both", overflow: "hidden" }}
        >
          <div
            className="flex flex-shrink-0 items-center justify-between border-b border-gray-100 px-4 py-3 cursor-grab select-none"
            onMouseDown={(e) => {
              panel.tipsDrag.current = { startX: e.clientX, startY: e.clientY, panelX: panel.tipsPos.x, panelY: panel.tipsPos.y };
              const onMove = (ev: MouseEvent) => {
                if (!panel.tipsDrag.current) return;
                panel.setTipsPos({ x: panel.tipsDrag.current.panelX + ev.clientX - panel.tipsDrag.current.startX, y: panel.tipsDrag.current.panelY + ev.clientY - panel.tipsDrag.current.startY });
              };
              const onUp = () => { panel.tipsDrag.current = null; window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseup", onUp); };
              window.addEventListener("mousemove", onMove);
              window.addEventListener("mouseup", onUp);
            }}
          >
            <h2 className="text-sm font-bold" style={{ color: "var(--cp-green)" }}>Flowchart Tips</h2>
            <button onClick={() => panel.setTipsOpen(false)} className="text-gray-400 hover:text-gray-600 leading-none ml-4">✕</button>
          </div>
          <div className="flex-1 overflow-y-auto px-5 py-4 space-y-5">
            {(!fs.resolvedFlowchart.notes || fs.resolvedFlowchart.notes.length === 0) && !fs.activeConcentration?.tips?.length ? (
              <p className="text-sm text-gray-400 italic">No catalog tips available yet.</p>
            ) : (
              <>
                {(fs.resolvedFlowchart.notes ?? []).filter((s) => s.title !== "GE Tips").map((section, si) => (
                  <div key={si}>
                    <h3 className="text-xs font-semibold uppercase tracking-wide mb-2" style={{ color: "var(--cp-green)" }}>{section.title}</h3>
                    <ol className="space-y-2 list-decimal list-outside pl-4">
                      {section.items.map((item, i) => <li key={i} className="text-sm text-gray-700 leading-relaxed">{item}</li>)}
                    </ol>
                  </div>
                ))}
                {fs.activeConcentration?.tips && fs.activeConcentration.tips.length > 0 && (
                  <div>
                    <h3 className="text-xs font-semibold uppercase tracking-wide mb-2" style={{ color: "var(--cp-green)" }}>{fs.activeConcentration.label} Tips</h3>
                    <ol className="space-y-2 list-decimal list-outside pl-4">
                      {fs.activeConcentration.tips.map((item, i) => <li key={i} className="text-sm text-gray-700 leading-relaxed">{item}</li>)}
                    </ol>
                  </div>
                )}
                {(fs.resolvedFlowchart.notes ?? []).filter((s) => s.title === "GE Tips").map((section, si) => (
                  <div key={si}>
                    <h3 className="text-xs font-semibold uppercase tracking-wide mb-2" style={{ color: "var(--cp-green)" }}>{section.title}</h3>
                    <ol className="space-y-2 list-decimal list-outside pl-4">
                      {section.items.map((item, i) => <li key={i} className="text-sm text-gray-700 leading-relaxed">{item}</li>)}
                    </ol>
                  </div>
                ))}
              </>
            )}
          </div>
        </div>
      )}

      {panel.myNotesOpen && (
        <div
          className="fixed z-50 flex flex-col rounded-lg border border-gray-200 bg-white shadow-2xl"
          style={{ left: panel.myNotesPos.x, top: panel.myNotesPos.y, width: "min(380px, calc(100vw - 2rem))", height: "min(60vh, 440px)", minWidth: "240px", minHeight: "160px", resize: "both", overflow: "hidden" }}
        >
          <div
            className="flex flex-shrink-0 items-center justify-between border-b border-gray-100 px-4 py-3 cursor-grab select-none"
            onMouseDown={(e) => {
              panel.myNotesDrag.current = { startX: e.clientX, startY: e.clientY, panelX: panel.myNotesPos.x, panelY: panel.myNotesPos.y };
              const onMove = (ev: MouseEvent) => {
                if (!panel.myNotesDrag.current) return;
                panel.setMyNotesPos({ x: panel.myNotesDrag.current.panelX + ev.clientX - panel.myNotesDrag.current.startX, y: panel.myNotesDrag.current.panelY + ev.clientY - panel.myNotesDrag.current.startY });
              };
              const onUp = () => { panel.myNotesDrag.current = null; window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseup", onUp); };
              window.addEventListener("mousemove", onMove);
              window.addEventListener("mouseup", onUp);
            }}
          >
            <h2 className="text-sm font-bold" style={{ color: "var(--cp-green)" }}>My Notes</h2>
            <button onClick={() => panel.setMyNotesOpen(false)} className="text-gray-400 hover:text-gray-600 leading-none ml-4">✕</button>
          </div>
          <textarea
            className="flex-1 w-full resize-none px-4 py-3 text-sm text-gray-700 placeholder-gray-300 focus:outline-none"
            placeholder="Write anything here — course notes, reminders, questions for your advisor…"
            value={fs.myNotesText}
            onChange={(e) => fs.updateMyNotes(e.target.value)}
          />
        </div>
      )}

      {panel.otherCreditsOpen && (
        <div
          className="fixed z-50 flex flex-col rounded-lg border border-gray-200 bg-white shadow-2xl"
          style={{ left: panel.otherCreditsPos.x, top: panel.otherCreditsPos.y, width: "min(380px, calc(100vw - 2rem))", maxHeight: "min(60vh, 440px)", minWidth: "260px", overflow: "hidden" }}
        >
          <div
            className="flex flex-shrink-0 items-center justify-between border-b border-gray-100 px-4 py-3 cursor-grab select-none"
            onMouseDown={(e) => {
              panel.otherCreditsDrag.current = { startX: e.clientX, startY: e.clientY, panelX: panel.otherCreditsPos.x, panelY: panel.otherCreditsPos.y };
              const onMove = (ev: MouseEvent) => {
                if (!panel.otherCreditsDrag.current) return;
                panel.setOtherCreditsPos({ x: panel.otherCreditsDrag.current.panelX + ev.clientX - panel.otherCreditsDrag.current.startX, y: panel.otherCreditsDrag.current.panelY + ev.clientY - panel.otherCreditsDrag.current.startY });
              };
              const onUp = () => { panel.otherCreditsDrag.current = null; window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseup", onUp); };
              window.addEventListener("mousemove", onMove);
              window.addEventListener("mouseup", onUp);
            }}
          >
            <div>
              <h2 className="text-sm font-bold" style={{ color: "var(--cp-green)" }}>Other Credits</h2>
              <div className="mt-0.5 text-[11px] text-gray-400">{fs.otherCredits.length} imported</div>
            </div>
            <button onClick={() => panel.setOtherCreditsOpen(false)} className="text-gray-400 hover:text-gray-600 leading-none ml-4">✕</button>
          </div>
          <div className="overflow-y-auto px-4 py-3">
            {fs.otherCredits.length === 0 ? (
              <div className="py-6 text-center text-sm text-gray-400">No other credits found.</div>
            ) : (
              <div className="divide-y divide-gray-100">
                {fs.otherCredits.map((credit) => (
                  <div key={`${credit.status}-${credit.courseNumber}`} className="flex items-center justify-between gap-3 py-2.5">
                    <span className="font-mono text-sm font-semibold text-gray-800">{credit.courseNumber}</span>
                    <span className={`rounded px-2 py-0.5 text-[10px] font-bold uppercase ${credit.status === "completed" ? "bg-green-50 text-green-700" : "bg-amber-50 text-amber-700"}`}>
                      {credit.status === "completed" ? "Done" : "IP"}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {panel.courseLookupOpen && (
        <div
          className="fixed z-50 flex flex-col rounded-lg border border-gray-200 bg-white shadow-2xl"
          style={{ left: panel.courseLookupPos.x, top: panel.courseLookupPos.y, width: "min(520px, calc(100vw - 2rem))", maxHeight: "min(70vh, 520px)", minWidth: "280px", overflow: "hidden" }}
        >
          <div
            className="flex flex-shrink-0 items-center justify-between border-b border-gray-100 px-4 py-3 cursor-grab select-none"
            onMouseDown={(e) => {
              panel.courseLookupDrag.current = { startX: e.clientX, startY: e.clientY, panelX: panel.courseLookupPos.x, panelY: panel.courseLookupPos.y };
              const onMove = (ev: MouseEvent) => {
                if (!panel.courseLookupDrag.current) return;
                panel.setCourseLookupPos({ x: panel.courseLookupDrag.current.panelX + ev.clientX - panel.courseLookupDrag.current.startX, y: panel.courseLookupDrag.current.panelY + ev.clientY - panel.courseLookupDrag.current.startY });
              };
              const onUp = () => { panel.courseLookupDrag.current = null; window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseup", onUp); };
              window.addEventListener("mousemove", onMove);
              window.addEventListener("mouseup", onUp);
            }}
          >
            <div>
              <h2 className="text-sm font-bold" style={{ color: "var(--cp-green)" }}>Course Lookup</h2>
              <div className="mt-0.5 text-[11px] text-gray-400">
                {searchTerms.length === 0 ? "Search this flowchart" : `${allMatchCount} matches`}
              </div>
            </div>
            <button onClick={() => panel.setCourseLookupOpen(false)} className="text-gray-400 hover:text-gray-600 leading-none ml-4">✕</button>
          </div>
          <div className="overflow-y-auto px-4 py-3">
            <div className="flex gap-2">
              <input
                value={panel.courseSearch}
                onChange={(e) => panel.setCourseSearch(e.target.value)}
                placeholder="Course number, title, keyword, or term"
                className="min-w-0 flex-1 rounded border border-gray-300 bg-white px-3 py-2 text-sm outline-none transition-colors focus:border-blue-700"
                autoFocus
              />
              {panel.courseSearch && (
                <button onClick={() => panel.setCourseSearch("")} className="rounded border border-gray-200 px-2.5 py-2 text-xs font-semibold text-gray-500 hover:bg-gray-50">
                  Clear
                </button>
              )}
            </div>
            {searchTerms.length > 0 && (
              <div className="mt-3">
                {courseSearchMatches.length === 0 ? (
                  <div className="py-6 text-center text-sm text-gray-400">No matching courses in this flowchart.</div>
                ) : (
                  <div className="flex flex-col divide-y divide-gray-100">
                    {courseSearchMatches.map((course) => {
                      const col = fs.resolvedFlowchart!.columns[course.grid_col];
                      const status = fs.statusForCourse(course);
                      return (
                        <button
                          key={course.id}
                          onClick={() => panel.openCoursePanel(course, status)}
                          className="flex items-start justify-between gap-3 py-2.5 text-left text-sm hover:bg-yellow-50"
                        >
                          <div>
                            <div className="font-mono font-bold text-gray-900">{course.course_number}</div>
                            <div className="text-xs text-gray-600">{course.title}</div>
                          </div>
                          {col && <span className="mt-0.5 whitespace-nowrap text-[11px] font-semibold text-gray-400">{col.year} {col.term}</span>}
                        </button>
                      );
                    })}
                    {allMatchCount > courseSearchMatches.length && (
                      <div className="py-2 text-xs text-gray-400">
                        +{allMatchCount - courseSearchMatches.length} more highlighted on the flowchart.
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      <ManualCourseChecklist
        open={panel.checklistOpen}
        courses={fs.resolvedFlowchart.courses}
        completed={fs.session.completed}
        inProgress={fs.session.inProgress}
        geAreaMap={fs.statusGEAreaMap}
        plannedGECourses={fs.session.plannedGECourses ?? {}}
        plannedFreeElectiveCourses={fs.session.plannedFreeElectiveCourses ?? {}}
        onToggleCourse={toggleCourseCompleted}
        onToggleCourseInProgress={toggleCourseInProgress}
        onToggleGEArea={fs.toggleGEArea}
        onToggleGEAreaInProgress={fs.toggleGEAreaInProgress}
        onTogglePickedCourse={fs.togglePickedCourse}
        onTogglePickedCourseInProgress={fs.togglePickedCourseInProgress}
        onToggleFreeElectiveStatus={setFreeElectiveStatus}
        onOpenFreeElectivePicker={panel.setSelectedFreeElectiveCourse}
        onImportCSV={fs.importCSV}
        onClose={() => panel.setChecklistOpen(false)}
      />
    </div>
  );
}
