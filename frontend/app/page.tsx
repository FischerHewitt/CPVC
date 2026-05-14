"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getMajors, parseTranscript } from "@/lib/api";
import { saveSession } from "@/lib/session";
import type { MajorOption } from "@/lib/types";

const FALLBACK_MAJORS: MajorOption[] = [
  { code: "CS", name: "Computer Science" },
  { code: "AERO", name: "Aerospace Engineering" },
];

export default function HomePage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [majorCode, setMajorCode] = useState("CS");
  const [majors, setMajors] = useState<MajorOption[]>(FALLBACK_MAJORS);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    getMajors()
      .then((nextMajors) => {
        if (!cancelled && nextMajors.length > 0) setMajors(nextMajors);
      })
      .catch(() => {
        if (!cancelled) setMajors(FALLBACK_MAJORS);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const handleFile = (f: File) => {
    if (!f.name.endsWith(".pdf")) {
      setError("Please upload a PDF file.");
      return;
    }
    setFile(f);
    setError(null);
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }, []);

  const onSubmit = async () => {
    if (!file) { setError("Please upload your transcript first."); return; }
    setLoading(true);
    setError(null);
    try {
      const result = await parseTranscript(file, majorCode);
      // Backend created the DB session and returned its UUID
      saveSession({
        sessionId:  result.session_id,
        studentName: result.student_name,
        major:      majorCode,
        completed:  result.completed,
        inProgress: result.in_progress,
        coursePositions: {},
        plannedGECourses: {},
      });
      router.push(`/flowchart/${result.session_id}`);
    } catch (e) {
      setError("Failed to parse transcript. Make sure it's a Cal Poly unofficial transcript PDF.");
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--cp-bg)" }}>
      {/* Header */}
      <header style={{ background: "var(--cp-green)" }} className="px-6 py-4 flex items-center gap-3">
        <div className="text-white font-bold text-xl tracking-wide">CAL POLY</div>
        <div className="text-white/60 text-sm font-medium">SAN LUIS OBISPO</div>
        <div className="ml-auto text-white/80 text-sm">Semester Conversion Tracker</div>
      </header>

      {/* Hero */}
      <main className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="w-full max-w-md">
          <h1 className="text-3xl font-bold text-center mb-2" style={{ color: "var(--cp-green)" }}>
            See where you stand.
          </h1>
          <p className="text-center text-gray-500 mb-8 text-sm leading-relaxed">
            Upload your unofficial transcript and we&apos;ll show you which semester
            requirements you&apos;ve already satisfied — and who&apos;s teaching what&apos;s left.
          </p>

          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col gap-5">
            {/* Drop zone */}
            <div
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
                file ? "bg-green-50" : dragging ? "bg-green-50" : "hover:bg-gray-50"
              }`}
              style={{ borderColor: dragging || file ? "var(--cp-green)" : "#d1d5db" }}
              onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
              onDragLeave={() => setDragging(false)}
              onDrop={onDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }}
              />
              {file ? (
                <div>
                  <div className="text-2xl mb-1">✅</div>
                  <div className="font-medium text-green-700 text-sm">{file.name}</div>
                  <div className="text-xs text-gray-400 mt-1">Click to change</div>
                </div>
              ) : (
                <div>
                  <div className="text-3xl mb-2">📄</div>
                  <div className="font-medium text-gray-600 text-sm">Drop your unofficial transcript</div>
                  <div className="text-xs text-gray-400 mt-1">or click to upload (.pdf)</div>
                </div>
              )}
            </div>

            {/* Major selector */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Major</label>
              <select
                value={majorCode}
                onChange={(e) => setMajorCode(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none"
              >
                {majors.map((m) => (
                  <option key={m.code} value={m.code}>{m.name}</option>
                ))}
              </select>
            </div>

            {error && (
              <div className="text-red-600 text-xs bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                {error}
              </div>
            )}

            <button
              onClick={onSubmit}
              disabled={loading || !file}
              className="w-full py-3 rounded-xl font-semibold text-white text-sm transition-opacity disabled:opacity-50"
              style={{ background: "var(--cp-green)" }}
            >
              {loading ? "Parsing transcript…" : "View My Flowchart →"}
            </button>

            <p className="text-center text-xs text-gray-400">
              Your PDF is only used to extract course data and is never stored.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
