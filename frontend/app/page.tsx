"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { getMajors, parseTranscript, parseCsvTranscript, getConcentrations, getFlowchart, syncSession } from "@/lib/api";
import { saveSession } from "@/lib/session";
import { parseMbpFile } from "@/lib/mbp";
import type { MajorOption, Concentration } from "@/lib/types";

function concs(...pairs: [string, string][]): Concentration[] {
  return pairs.map(([id, label]) => ({ id, label, slot_overrides: {} }));
}

const FALLBACK_CONCENTRATIONS: Record<string, Concentration[]> = {
  CS: concs(
    ["none", "General Curriculum"],
    ["ai_ml", "AI & Machine Learning"],
    ["data_eng", "Data Engineering"],
    ["game_dev", "Game Development"],
    ["graphics", "Graphics"],
    ["privacy_security", "Privacy & Security"],
  ),
  AERO: concs(
    ["none", "Concentration Not Yet Declared"],
    ["aeronautics", "Aeronautics"],
    ["astronautics", "Astronautics"],
  ),
  CPE: concs(
    ["none", "General Curriculum"],
    ["computer_architecture", "Computer Architecture"],
    ["computer_hardware", "Computer Hardware Engineering"],
    ["computer_systems", "Computer Systems"],
    ["embedded_systems", "Embedded Systems"],
    ["robotics", "Robotics and Autonomous Systems"],
    ["security", "Privacy and Security"],
  ),
  CE: concs(
    ["none", "General Civil Engineering"],
    ["construction", "Construction Engineering"],
    ["geotechnical", "Geotechnical Engineering"],
    ["structural", "Structural Engineering"],
    ["transportation", "Transportation Engineering"],
    ["water_resources", "Water Resources Engineering"],
  ),
  ME: concs(
    ["none", "General Curriculum"],
    ["energy_resources", "Energy Resources"],
    ["hvacr", "Sustainable Technology for the Built Environment (HVAC&R)"],
    ["mechatronics", "Mechatronics"],
    ["manufacturing", "Manufacturing"],
  ),
  AD: concs(
    ["none", "Concentration Not Yet Declared"],
    ["graphic_design", "Graphic Design"],
    ["photo_video", "Photography and Video"],
    ["studio_art", "Studio Art"],
  ),
  POLS: concs(
    ["none", "Concentration Not Yet Declared"],
    ["global_politics", "Global Politics"],
    ["pre_law", "Pre-Law"],
    ["us_politics", "U.S. Politics"],
    ["individualized", "Individualized Course of Study"],
  ),
  AGS: concs(
    ["none", "Emphasis Not Yet Declared"],
    ["ag_engineering_tech", "Agricultural Engineering Technology"],
    ["agribusiness", "Agribusiness"],
    ["animal_science", "Animal Science"],
    ["plant_crop_soil", "Plant, Crop, and Soil Science"],
    ["forestry_natural_resources", "Forestry and Natural Resources"],
    ["ornamental_horticulture", "Ornamental Horticulture"],
  ),
  ANTGEOG: concs(
    ["none", "Concentration Not Yet Declared"],
    ["environmental_sustainability", "Environmental Studies and Sustainability"],
    ["global_studies", "Global Studies and International Development"],
    ["human_ecology", "Human Ecology"],
    ["individualized", "Individualized Course of Study"],
  ),
  BIO: concs(
    ["none", "General Curriculum in Biology"],
    ["anatomy_physiology", "Anatomy and Physiology"],
    ["ecology_evolution_biodiversity_conservation", "Ecology, Evolution, Biodiversity, and Conservation"],
    ["molecular_cellular", "Molecular and Cellular Biology"],
  ),
  BMED: concs(
    ["none", "Concentration Not Yet Declared"],
    ["bioinstrumentation", "Bioinstrumentation"],
    ["cell_and_tissue_engineering", "Cell and Tissue Engineering"],
    ["mechanical_design", "Mechanical Design"],
    ["individualized", "Individualized Course of Study"],
  ),
  BIOC: concs(
    ["none", "General Biochemistry"],
    ["polymers_coatings", "Polymers and Coatings"],
  ),
};

const FALLBACK_MAJORS: MajorOption[] = [
  { code: "CS", name: "Computer Science" },
  { code: "AERO", name: "Aerospace Engineering" },
  { code: "SE", name: "Software Engineering" },
  { code: "CPE", name: "Computer Engineering" },
  { code: "CE", name: "Civil Engineering" },
  { code: "ME", name: "Mechanical Engineering" },
  { code: "AD", name: "Art and Design" },
  { code: "POLS", name: "Political Science" },
  { code: "PSY", name: "Psychology" },
  { code: "ENGL", name: "English" },
  { code: "MU", name: "Music" },
  { code: "AGC", name: "Agricultural Communication" },
  { code: "AGS", name: "Agricultural Science" },
  { code: "ASCI", name: "Animal Science" },
  { code: "ANTGEOG", name: "Anthropology and Geography" },
  { code: "ARCH", name: "Architecture" },
  { code: "BIO", name: "Biological Sciences" },
  { code: "BMED", name: "Biomedical Engineering" },
];

export default function HomePage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [majorCode, setMajorCode] = useState("CS");
  const [majors, setMajors] = useState<MajorOption[]>(FALLBACK_MAJORS);
  const [concentrations, setConcentrations] = useState<Concentration[]>(
    () => FALLBACK_CONCENTRATIONS["CS"] ?? [],
  );
  const [concentration, setConcentration] = useState<string>("none");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [showInstructions, setShowInstructions] = useState(false);
  const [isMbpFile, setIsMbpFile] = useState(false);

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

  useEffect(() => {
    const fallback = FALLBACK_CONCENTRATIONS[majorCode] ?? [];
    setConcentrations(fallback);
    if (fallback.length === 0) setConcentration("none");

    let cancelled = false;
    getConcentrations(majorCode)
      .then((list) => {
        if (!cancelled && list.length > 0) setConcentrations(list);
      })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [majorCode]);

  useEffect(() => {
    if (!loading) return;

    const interval = window.setInterval(() => {
      setProgress((current) => {
        if (current < 45) return current + 6;
        if (current < 75) return current + 3;
        if (current < 90) return current + 1;
        return current;
      });
    }, 350);

    return () => window.clearInterval(interval);
  }, [loading]);

  const handleFile = (f: File) => {
    const isMbp = f.name.endsWith(".mbp");
    if (!f.name.endsWith(".pdf") && !f.name.endsWith(".csv") && !isMbp) {
      setError("Please upload a PDF transcript, CSV course list, or .mbp flowchart file.");
      return;
    }
    setFile(f);
    setIsMbpFile(isMbp);
    setProgress(0);
    setError(null);
  };

  const progressLabel =
    progress >= 95
      ? "Opening flowchart"
      : progress >= 70
        ? "Creating flowchart"
        : progress >= 35
          ? "Matching completed courses"
          : "Reading transcript";

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }, []);

  const onSubmit = async () => {
    if (!file) { setError("Please upload your transcript or course list first."); return; }
    if (loading) return;

    if (isMbpFile) {
      try {
        const text = await file.text();
        const data = parseMbpFile(text);
        const newSessionId = crypto.randomUUID();
        saveSession({ ...data, sessionId: newSessionId });
        router.push(`/flowchart/${newSessionId}`);
      } catch {
        setError("Could not read the flowchart file. Make sure it's a valid .mbp file.");
      }
      return;
    }

    setLoading(true);
    setProgress(12);
    setError(null);
    let createdFlowchart = false;
    const isCsv = file.name.endsWith(".csv");
    try {
      const result = isCsv
        ? await parseCsvTranscript(file, majorCode)
        : await parseTranscript(file, majorCode);
      setProgress(95);
      const majorName = majors.find((m) => m.code === majorCode)?.name ?? majorCode;
      saveSession({
        sessionId:   result.session_id,
        studentName: result.student_name || majorName,
        major:       majorCode,
        completed:   result.completed,
        inProgress:  result.in_progress,
        coursePositions: {},
        plannedGECourses: {},
        concentration: concentration !== "none" ? concentration : undefined,
      });
      if (concentration !== "none") {
        void syncSession(result.session_id, { concentration });
      }
      createdFlowchart = true;
      setProgress(100);
      router.push(`/flowchart/${result.session_id}`);
    } catch (e) {
      setError(
        isCsv
          ? "Failed to parse course list. Make sure it's the CSV downloaded from Student Center."
          : "Failed to parse transcript. Make sure it's a Cal Poly unofficial transcript PDF."
      );
      console.error(e);
    } finally {
      if (!createdFlowchart) {
        setProgress(0);
        setLoading(false);
      }
    }
  };

  const onBrowse = async () => {
    if (loading) return;
    setLoading(true);
    setError(null);
    setProgress(35);
    try {
      await getFlowchart(majorCode);
    } catch (e) {
      console.error(e);
      setError("Could not reach the deployed backend for this major. Check the API deployment and NEXT_PUBLIC_API_URL.");
      setProgress(0);
      setLoading(false);
      return;
    }

    const sessionId = crypto.randomUUID();
    const majorName = majors.find((m) => m.code === majorCode)?.name ?? majorCode;
    saveSession({
      sessionId,
      studentName: majorName,
      major: majorCode,
      completed: [],
      inProgress: [],
      coursePositions: {},
      plannedGECourses: {},
      concentration: concentration !== "none" ? concentration : undefined,
    });
    setProgress(100);
    router.push(`/flowchart/${sessionId}`);
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--cp-bg)" }}>
      {/* Header */}
      <header
        className="px-6 py-3 flex items-center gap-3 relative"
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
        <Image src="/mb-logo.png" alt="Mustang Blueprints" width={42} height={42} className="rounded flex-shrink-0" style={{ border: "2px solid rgba(255,255,255,0.85)" }} />
        <div>
          <div className="text-white font-bold text-base tracking-widest uppercase font-mono leading-tight">Mustang Blueprints</div>
          <div className="text-white/45 text-[9px] tracking-widest uppercase font-mono">Cal Poly Course Planner</div>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <Link href="/support" className="text-white/60 hover:text-white text-xs transition-colors font-mono tracking-wide">Support</Link>
          <span className="text-white/40 text-xs font-mono tracking-wide">Unofficial Tool</span>
        </div>
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
                file ? "bg-blue-50" : dragging ? "bg-blue-50" : "hover:bg-gray-50"
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
                accept=".pdf,.csv,.mbp"
                className="hidden"
                onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }}
              />
              {file ? (
                <div>
                  <div className="text-2xl mb-1">{isMbpFile ? "🗺️" : "✅"}</div>
                  <div className="font-medium text-blue-700 text-sm">{file.name}</div>
                  <div className="text-xs text-gray-400 mt-1">Click to change</div>
                </div>
              ) : (
                <div>
                  <div className="text-3xl mb-2">📄</div>
                  <div className="font-medium text-gray-600 text-sm">Drop your transcript, course list, or flowchart</div>
                  <div className="text-xs text-gray-400 mt-1">or click to upload (.pdf, .csv, or .mbp)</div>
                </div>
              )}
            </div>

            {/* Instructions toggle */}
            <div>
              <button
                type="button"
                onClick={() => setShowInstructions((v) => !v)}
                className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
              >
                <span>{showInstructions ? "▲" : "▼"}</span>
                How to download your file from my.calpoly.edu
              </button>
              {showInstructions && (
                <div className="mt-3 flex flex-col gap-3 text-xs text-gray-600 bg-gray-50 rounded-xl p-4 border border-gray-100">
                  <div>
                    <div className="font-semibold text-gray-700 mb-1">
                      📊 CSV — Course List <span className="text-green-600 font-semibold">(Recommended)</span>
                    </div>
                    <div className="text-gray-500 leading-relaxed">
                      my.calpoly.edu → Student Center → <span className="font-medium">Academic Process</span> → Course List → download arrow (top right corner)
                    </div>
                    <div className="mt-1 text-gray-400">
                      Includes transfer credit and test scores — most accurate option.
                    </div>
                  </div>
                  <div className="border-t border-gray-200" />
                  <div>
                    <div className="font-semibold text-gray-700 mb-1">📄 PDF — Unofficial Transcript</div>
                    <div className="text-gray-500 leading-relaxed">
                      my.calpoly.edu → Student Center → <span className="font-medium">Student Records</span> → View Unofficial Transcript → Download PDF
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Major selector (hidden when restoring from .mbp — major is embedded in file) */}
            {!isMbpFile && <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Major</label>
              <select
                value={majorCode}
                onChange={(e) => {
                  setMajorCode(e.target.value);
                  setConcentration("none");
                }}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none"
              >
                {[...majors].sort((a, b) => a.name.localeCompare(b.name)).map((m) => (
                  <option key={m.code} value={m.code}>{m.name}</option>
                ))}
              </select>
            </div>}

            {/* Concentration selector (only shown when available and not restoring from .mbp) */}
            {!isMbpFile && concentrations.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Concentration</label>
                <select
                  value={concentration}
                  onChange={(e) => setConcentration(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none"
                >
                  {[
                    ...concentrations.filter((c) => c.id === "none"),
                    ...[...concentrations.filter((c) => c.id !== "none")].sort((a, b) =>
                      a.label.localeCompare(b.label)
                    ),
                  ].map((c) => (
                    <option key={c.id} value={c.id}>{c.label}</option>
                  ))}
                </select>
              </div>
            )}

            {error && (
              <div className="text-red-600 text-xs bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                {error}
              </div>
            )}

            {loading && (
              <div className="rounded-xl border border-blue-100 bg-blue-50 px-4 py-3">
                <div className="mb-2 flex items-center justify-between gap-3 text-xs font-medium">
                  <span className="text-blue-900">{progressLabel}</span>
                  <span className="tabular-nums text-blue-700">{Math.round(progress)}%</span>
                </div>
                <div
                  className="h-2 overflow-hidden rounded-full bg-white"
                  role="progressbar"
                  aria-label={progressLabel}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={Math.round(progress)}
                >
                  <div
                    className="h-full rounded-full transition-all duration-300 ease-out"
                    style={{ width: `${progress}%`, background: "var(--cp-green)" }}
                  />
                </div>
              </div>
            )}

            <button
              onClick={onSubmit}
              disabled={loading || !file}
              className="w-full py-3 rounded-xl font-semibold text-white text-sm transition-opacity disabled:opacity-50"
              style={{ background: "var(--cp-green)" }}
            >
              {loading ? (isMbpFile ? "Restoring flowchart…" : "Creating flowchart…") : isMbpFile ? "Restore My Flowchart →" : "View My Flowchart →"}
            </button>

            <div className="relative flex items-center gap-3">
              <div className="flex-1 h-px bg-gray-200" />
              <span className="text-xs text-gray-400">or</span>
              <div className="flex-1 h-px bg-gray-200" />
            </div>

            <button
              onClick={onBrowse}
              disabled={loading}
              className="w-full py-2.5 rounded-xl font-semibold text-sm border transition-colors disabled:opacity-50 hover:bg-gray-50"
              style={{ borderColor: "var(--cp-green)", color: "var(--cp-green)" }}
            >
              Browse without transcript →
            </button>

            <p className="text-center text-xs text-gray-400">
              Your file is only used to extract course data and is never stored.
            </p>
          </div>
        </div>
      </main>

      {/* Disclaimer */}
      <footer className="px-6 py-4 text-center text-xs text-gray-400 border-t border-gray-100">
        Mustang Blueprints is an independent student project and is <strong>not affiliated with or endorsed by Cal Poly San Luis Obispo</strong>.
        Course requirements change — always verify your plan with your academic advisor.
      </footer>
    </div>
  );
}
