"use client";

import { useEffect, useRef, useState } from "react";
import type { CourseSearchResult } from "@/lib/types";
import {
  searchFreeElectiveCatalog,
  shouldSearchFreeElectiveCatalog,
  FREE_ELECTIVE_SEARCH_DEBOUNCE_MS,
} from "@/lib/free-elective-search";

type DragState = { startX: number; startY: number; panelX: number; panelY: number };

export interface AssignableSlot {
  id: string;
  course_number: string;
  title: string;
}

interface Props {
  col: number;
  termLabel: string;
  assignableSlots?: AssignableSlot[];
  panelPos: { x: number; y: number };
  panelDrag: React.MutableRefObject<DragState | null>;
  onSetPos: (pos: { x: number; y: number }) => void;
  onAdd: (course: CourseSearchResult, slotId?: string) => void;
  onClose: () => void;
}

export default function AddCoursePanel({
  col: _col,
  termLabel,
  assignableSlots = [],
  panelPos,
  panelDrag,
  onSetPos,
  onAdd,
  onClose,
}: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<CourseSearchResult[]>([]);
  const [picked, setPicked] = useState<CourseSearchResult | null>(null);
  const [selectedSlotId, setSelectedSlotId] = useState("");
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Debounced catalog search
  useEffect(() => {
    if (picked) return;
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (!shouldSearchFreeElectiveCatalog(query)) { setResults([]); return; }

    debounceRef.current = setTimeout(async () => {
      const found = await searchFreeElectiveCatalog(query);
      setResults(found);
    }, FREE_ELECTIVE_SEARCH_DEBOUNCE_MS);

    return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
  }, [query, picked]);

  const handleAdd = () => {
    if (!picked) return;
    onAdd(picked, selectedSlotId || undefined);
    onClose();
  };

  return (
    <div
      className="fixed z-50 flex flex-col rounded-lg border border-gray-200 bg-white shadow-2xl"
      style={{ left: panelPos.x, top: panelPos.y, width: "min(340px, calc(100vw - 2rem))", maxHeight: "min(460px, 80vh)", overflow: "hidden" }}
    >
      {/* Drag handle / header */}
      <div
        className="flex flex-shrink-0 items-center justify-between border-b border-gray-100 px-4 py-3 cursor-grab select-none"
        onMouseDown={(e) => {
          panelDrag.current = { startX: e.clientX, startY: e.clientY, panelX: panelPos.x, panelY: panelPos.y };
          const onMove = (ev: MouseEvent) => {
            if (!panelDrag.current) return;
            onSetPos({
              x: panelDrag.current.panelX + ev.clientX - panelDrag.current.startX,
              y: panelDrag.current.panelY + ev.clientY - panelDrag.current.startY,
            });
          };
          const onUp = () => {
            panelDrag.current = null;
            window.removeEventListener("mousemove", onMove);
            window.removeEventListener("mouseup", onUp);
          };
          window.addEventListener("mousemove", onMove);
          window.addEventListener("mouseup", onUp);
        }}
      >
        <div>
          <h2 className="text-sm font-bold" style={{ color: "var(--cp-green)" }}>Add Course</h2>
          <div className="mt-0.5 text-[11px] text-gray-400">{termLabel}</div>
        </div>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600 leading-none ml-4">✕</button>
      </div>

      <div className="overflow-y-auto px-4 py-3 flex flex-col gap-3">
        {/* Course search */}
        <div>
          <label className="block text-xs font-semibold text-gray-500 mb-1">Course</label>
          {picked ? (
            <div className="flex items-center justify-between rounded border border-blue-200 bg-blue-50 px-3 py-2">
              <div>
                <div className="text-xs font-bold text-blue-900 font-mono">{picked.course_number}</div>
                <div className="text-[10px] text-blue-700">{picked.title} · {picked.units}u</div>
              </div>
              <button
                onClick={() => { setPicked(null); setQuery(""); setResults([]); }}
                className="text-blue-400 hover:text-blue-600 text-xs ml-2"
              >
                change
              </button>
            </div>
          ) : (
            <div className="relative">
              <input
                autoFocus
                placeholder="Search course number or title…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full rounded border border-gray-200 px-3 py-1.5 text-xs"
              />
              {results.length > 0 && (
                <div className="absolute top-full left-0 right-0 z-10 rounded border border-gray-200 bg-white shadow-lg mt-0.5 max-h-48 overflow-y-auto">
                  {results.map((r) => (
                    <button
                      key={r.course_number}
                      onClick={() => { setPicked(r); setQuery(""); setResults([]); }}
                      className="block w-full text-left px-3 py-2 hover:bg-gray-50 text-xs border-b border-gray-50 last:border-0"
                    >
                      <span className="font-bold font-mono">{r.course_number}</span>
                      <span className="ml-1.5 text-gray-500">{r.title}</span>
                      <span className="ml-1 text-gray-400">· {r.units}u</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Count toward requirement (optional) */}
        {assignableSlots.length > 0 && (
          <div>
            <label className="block text-xs font-semibold text-gray-500 mb-1">
              Count toward requirement? <span className="font-normal text-gray-400">(optional)</span>
            </label>
            <select
              value={selectedSlotId}
              onChange={(e) => setSelectedSlotId(e.target.value)}
              className="w-full rounded border border-gray-200 px-2 py-1.5 text-xs"
            >
              <option value="">— leave unassigned —</option>
              {assignableSlots.map((s) => (
                <option key={s.id} value={s.id}>{s.course_number} — {s.title}</option>
              ))}
            </select>
            {selectedSlotId && (
              <p className="mt-1 text-[10px] text-orange-600">
                The {assignableSlots.find((s) => s.id === selectedSlotId)?.course_number} tile will show "covered by" this course.
              </p>
            )}
          </div>
        )}

        <button
          onClick={handleAdd}
          disabled={!picked}
          className="w-full rounded-lg py-2 text-xs font-bold text-white disabled:opacity-40 hover:opacity-90 active:scale-[0.98] transition-all"
          style={{ background: "var(--cp-green)" }}
        >
          Add to Flowchart
        </button>
      </div>
    </div>
  );
}
