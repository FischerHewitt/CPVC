"use client";

import { useEffect, useState } from "react";
import type { Course, CourseSearchResult, FreeElectiveSelection, FreeElectiveStatus, Professor } from "@/lib/types";
import { getProfessors } from "@/lib/api";
import {
  FREE_ELECTIVE_SEARCH_LIMIT,
  FREE_ELECTIVE_SEARCH_DEBOUNCE_MS,
  searchFreeElectiveCatalog,
  shouldSearchFreeElectiveCatalog,
} from "@/lib/free-elective-search";

const STATUS_LABELS: Record<FreeElectiveStatus, string> = {
  planned: "Plan",
  completed: "Done",
  in_progress: "IP",
};
const STATUS_ORDER = ["planned", "in_progress", "completed"] as const;

const STATUS_STYLES: Record<FreeElectiveStatus, {
  activeButton: string;
  inactiveButton: string;
  selectedCard: string;
  selectedRow: string;
  selectedTitle: string;
  selectedText: string;
  selectedSubtleText: string;
}> = {
  planned: {
    activeButton: "border-blue-600 bg-blue-600 text-white",
    inactiveButton: "border-blue-200 text-blue-700 hover:border-blue-400 hover:bg-blue-50",
    selectedCard: "border-blue-200 bg-blue-50",
    selectedRow: "border-blue-300 bg-blue-50/40",
    selectedTitle: "text-blue-900",
    selectedText: "text-blue-800/80",
    selectedSubtleText: "text-blue-800/70",
  },
  completed: {
    activeButton: "border-green-700 bg-green-700 text-white",
    inactiveButton: "border-green-200 text-green-800 hover:border-green-400 hover:bg-green-50",
    selectedCard: "border-green-200 bg-green-50",
    selectedRow: "border-green-300 bg-green-50/40",
    selectedTitle: "text-green-900",
    selectedText: "text-green-800/80",
    selectedSubtleText: "text-green-800/70",
  },
  in_progress: {
    activeButton: "border-orange-600 bg-orange-600 text-white",
    inactiveButton: "border-orange-200 text-orange-700 hover:border-orange-400 hover:bg-orange-50",
    selectedCard: "border-orange-200 bg-orange-50",
    selectedRow: "border-orange-300 bg-orange-50/40",
    selectedTitle: "text-orange-900",
    selectedText: "text-orange-800/80",
    selectedSubtleText: "text-orange-800/70",
  },
};

function ProfessorRow({ prof }: { prof: Professor }) {
  return (
    <div className="flex items-center justify-between border-b border-gray-100 py-1.5 last:border-0">
      <div>
        <div className="text-xs font-medium text-gray-800">{prof.name}</div>
        <div className="text-[10px] text-gray-400">{prof.num_ratings} ratings</div>
      </div>
      <div className="flex items-center gap-1.5">
        <span className="text-xs font-bold" style={{ color: "var(--cp-green)" }}>
          {prof.overall_score.toFixed(2)}
          <span className="text-[10px] font-normal text-gray-400">/4</span>
        </span>
        <a href={prof.polyratings_url} target="_blank" rel="noopener noreferrer" className="text-[10px] text-blue-500 hover:underline">
          ↗
        </a>
      </div>
    </div>
  );
}

function SearchResultRow({
  result,
  selection,
  onChoose,
}: {
  result: CourseSearchResult;
  selection?: FreeElectiveSelection;
  onChoose: (result: CourseSearchResult, status: FreeElectiveStatus) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [professors, setProfessors] = useState<Professor[]>([]);
  const selected = selection?.course_number === result.course_number;
  const selectedStyles = selection ? STATUS_STYLES[selection.status] : null;

  function toggleProfessors() {
    if (expanded) {
      setExpanded(false);
      return;
    }
    setExpanded(true);
    if (professors.length > 0) return;
    setLoading(true);
    getProfessors(result.course_number).then(setProfessors).finally(() => setLoading(false));
  }

  return (
    <div className={`mb-1.5 overflow-hidden rounded-lg border ${selected && selectedStyles ? selectedStyles.selectedRow : "border-gray-100"}`}>
      <div className="flex items-center gap-2 px-3 py-2.5">
        <button className="min-w-0 flex-1 text-left">
          <div className={`text-sm font-semibold leading-tight ${selected && selectedStyles ? selectedStyles.selectedTitle : "text-gray-800"}`}>
            {result.course_number}
          </div>
          <div className="line-clamp-2 text-xs leading-tight text-gray-500">{result.title}</div>
        </button>
        <div className="flex flex-shrink-0 items-center gap-1.5">
          {STATUS_ORDER.map((status) => {
            const style = STATUS_STYLES[status];
            return (
              <button
                key={status}
                onClick={() => onChoose(result, status)}
                className={`rounded border px-1.5 py-0.5 text-[10px] font-semibold transition-colors ${
                  selected && selection?.status === status
                    ? style.activeButton
                    : style.inactiveButton
                }`}
              >
                {STATUS_LABELS[status]}
              </button>
            );
          })}
          <span className="text-xs text-gray-400">{result.units}u</span>
          <button
            onClick={toggleProfessors}
            className="rounded border border-gray-200 px-1.5 py-0.5 text-[10px] text-gray-400 transition-colors hover:border-gray-300 hover:text-gray-600"
            title="Show professors"
          >
            {expanded ? "▲" : "▼"}
          </button>
        </div>
      </div>
      {expanded && (
        <div className="border-t border-gray-100 bg-gray-50/60 px-3 pb-2">
          {loading && <div className="py-2 text-xs text-gray-400">Loading professors…</div>}
          {!loading && professors.length === 0 && <div className="py-2 text-xs text-gray-400">No professor data available yet.</div>}
          {professors.map((prof) => <ProfessorRow key={prof.name} prof={prof} />)}
        </div>
      )}
    </div>
  );
}

interface Props {
  course: Course | null;
  selection?: FreeElectiveSelection;
  onChoose: (course: Course, result: CourseSearchResult, status: FreeElectiveStatus) => void;
  onSetStatus: (course: Course, status: FreeElectiveStatus) => void;
  onClear: (course: Course) => void;
  onClose: () => void;
}

export default function FreeElectivePickerPanel({
  course,
  selection,
  onChoose,
  onSetStatus,
  onClear,
  onClose,
}: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<CourseSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const trimmed = query.trim();
    if (trimmed && !shouldSearchFreeElectiveCatalog(trimmed)) {
      const handle = window.setTimeout(() => {
        if (cancelled) return;
        setResults([]);
        setLoading(false);
        setLoadingMore(false);
        setHasMore(false);
      }, 0);

      return () => {
        cancelled = true;
        window.clearTimeout(handle);
      };
    }

    const stateHandle = window.setTimeout(() => {
      if (cancelled) return;
      setLoading(true);
      setLoadingMore(false);
      setHasMore(false);
    }, 0);
    const delay = trimmed ? FREE_ELECTIVE_SEARCH_DEBOUNCE_MS : 0;
    const handle = window.setTimeout(() => {
      searchFreeElectiveCatalog(trimmed, undefined, 0)
        .then((courses) => {
          if (cancelled) return;
          setResults(courses);
          setHasMore(courses.length === FREE_ELECTIVE_SEARCH_LIMIT);
        })
        .finally(() => {
          if (cancelled) return;
          setLoading(false);
        });
    }, delay);

    return () => {
      cancelled = true;
      window.clearTimeout(stateHandle);
      window.clearTimeout(handle);
    };
  }, [query]);

  if (!course) return null;
  const selectionStyles = selection ? STATUS_STYLES[selection.status] : null;

  async function loadMoreCourses() {
    if (loading || loadingMore || !hasMore) return;
    setLoadingMore(true);
    const nextCourses = await searchFreeElectiveCatalog(query.trim(), undefined, results.length);
    setResults((current) => {
      const seen = new Set(current.map((item) => item.course_number));
      return [...current, ...nextCourses.filter((item) => !seen.has(item.course_number))];
    });
    setHasMore(nextCourses.length === FREE_ELECTIVE_SEARCH_LIMIT);
    setLoadingMore(false);
  }

  return (
    <>
      <div className="fixed inset-0 z-40 bg-black/20 transition-opacity" onClick={onClose} />

      <div className="fixed right-0 top-0 z-50 flex h-full w-[min(560px,100vw)] flex-col bg-white shadow-2xl">
        <div className="flex flex-shrink-0 items-start justify-between border-b border-white/20 px-5 py-4" style={{ background: "var(--cp-green)" }}>
          <div>
            <div className="text-xs font-medium text-white/70">{course.course_number}</div>
            <div className="mt-0.5 text-base font-bold leading-tight text-white">{course.title}</div>
            <div className="mt-1 text-xs text-white/70">Free Elective Requirement</div>
          </div>
          <button onClick={onClose} className="ml-3 mt-0.5 text-xl leading-none text-white/70 hover:text-white">×</button>
        </div>

        <div
          className="flex-1 overflow-y-auto px-5 py-4"
          onScroll={(event) => {
            const target = event.currentTarget;
            if (target.scrollHeight - target.scrollTop - target.clientHeight < 240) {
              void loadMoreCourses();
            }
          }}
        >
          {selection && (
            <div className={`mb-4 rounded-lg border px-3 py-3 ${selectionStyles?.selectedCard ?? "border-green-200 bg-green-50"}`}>
              <div className="flex items-start gap-2">
                <div className="min-w-0 flex-1">
                  <div className={`text-sm font-bold ${selectionStyles?.selectedTitle ?? "text-green-900"}`}>{selection.course_number}</div>
                  <div className={`text-xs ${selectionStyles?.selectedText ?? "text-green-800/80"}`}>{selection.title}</div>
                  <div className={`mt-1 text-[11px] ${selectionStyles?.selectedSubtleText ?? "text-green-800/70"}`}>{selection.units} units selected</div>
                </div>
                <button onClick={() => onClear(course)} className="rounded border border-gray-200 bg-white px-2 py-1 text-[10px] font-semibold text-gray-700 hover:border-gray-300">
                  Clear
                </button>
              </div>
              <div className="mt-3 flex gap-1.5">
                {STATUS_ORDER.map((status) => {
                  const style = STATUS_STYLES[status];
                  return (
                    <button
                      key={status}
                      onClick={() => onSetStatus(course, status)}
                      className={`rounded border px-2 py-1 text-xs font-semibold transition-colors ${
                        selection.status === status
                          ? style.activeButton
                          : `bg-white ${style.inactiveButton}`
                      }`}
                    >
                      {STATUS_LABELS[status]}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          <input
            value={query}
            onChange={(event) => {
              const nextQuery = event.target.value;
              setQuery(nextQuery);
              if (nextQuery.trim() && !shouldSearchFreeElectiveCatalog(nextQuery)) {
                setResults([]);
                setLoading(false);
                setLoadingMore(false);
                setHasMore(false);
              } else {
                setLoading(true);
              }
            }}
            placeholder="Search or browse catalog courses"
            className="mb-3 w-full rounded border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-700"
          />

          <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">Catalog Courses</div>
          {query.trim() && !shouldSearchFreeElectiveCatalog(query) && <div className="text-xs text-gray-400">Type at least 2 characters to search.</div>}
          {loading && <div className="text-xs text-gray-400">{query.trim() ? "Searching…" : "Loading catalog…"}</div>}
          {!loading && results.length === 0 && (!query.trim() || shouldSearchFreeElectiveCatalog(query)) && (
            <div className="text-xs text-gray-400">{query.trim() ? "No matching courses." : "No catalog courses loaded."}</div>
          )}
          {results.map((result) => (
            <SearchResultRow
              key={result.course_number}
              result={result}
              selection={selection}
              onChoose={(selected, status) => onChoose(course, selected, status)}
            />
          ))}
          {loadingMore && <div className="py-2 text-xs text-gray-400">Loading more…</div>}
        </div>
      </div>
    </>
  );
}
