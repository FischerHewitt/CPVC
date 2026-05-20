"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { getMajors, parseTranscript, parseCsvTranscript, getConcentrations, getFlowchart, syncSession } from "@/lib/api";
import { saveSession } from "@/lib/session";
import { parseMbpFile } from "@/lib/mbp";
import { validateFile, getFileType, getProgressLabel } from "@/lib/upload-utils";
import type { MajorOption, Concentration } from "@/lib/types";

const css = `
*{box-sizing:border-box}
.bp-upload{
  --bp-bg:#0E3A8A;
  --bp-bg-deep:#0A2C6B;
  --bp-line:rgba(255,255,255,0.16);
  --bp-line-faint:rgba(255,255,255,0.08);
  --bp-line-strong:rgba(255,255,255,0.55);
  --bp-ink:#F1F6FF;
  --bp-ink-dim:rgba(241,246,255,0.6);
  --bp-ink-faint:rgba(241,246,255,0.35);
  --bp-amber:#F6C667;
  font-family:var(--font-mono-bp,'JetBrains Mono',ui-monospace,Menlo,monospace);
  color:var(--bp-ink);
  background:
    radial-gradient(120% 80% at 50% -10%,rgba(255,255,255,0.07),transparent 60%),
    radial-gradient(100% 60% at 50% 110%,rgba(0,0,0,0.25),transparent 60%),
    linear-gradient(var(--bp-line) 1px,transparent 1px) 50% 0/120px 120px,
    linear-gradient(90deg,var(--bp-line) 1px,transparent 1px) 50% 0/120px 120px,
    linear-gradient(var(--bp-line-faint) 1px,transparent 1px) 50% 0/24px 24px,
    linear-gradient(90deg,var(--bp-line-faint) 1px,transparent 1px) 50% 0/24px 24px,
    var(--bp-bg);
  font-size:14px;
  line-height:1.5;
  overflow-x:hidden;
  min-height:100vh;
}
.bp-upload .sheet{position:relative;max-width:1320px;margin:0 auto;padding:12px 48px 48px}
.bp-upload .mono{font-family:var(--font-mono-bp,'JetBrains Mono',monospace)}

/* topbar */
.bp-upload .topbar{display:flex;align-items:center;gap:24px;border-bottom:1px solid var(--bp-line);padding:8px 0;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-upload .topbar .dot{width:8px;height:8px;border-radius:50%;background:var(--bp-amber);box-shadow:0 0 0 3px rgba(246,198,103,0.18)}
.bp-upload .topbar .nav{margin-left:auto;display:flex;gap:24px}
.bp-upload .topbar a{color:var(--bp-ink-dim);text-decoration:none;transition:.15s}
.bp-upload .topbar a:hover{color:var(--bp-ink)}

/* title block */
.bp-upload .titleblock{margin-top:12px;display:grid;grid-template-columns:96px 1fr auto;align-items:center;gap:24px;padding:8px 0 14px;border-bottom:1px dashed var(--bp-line-strong)}
.bp-upload .logo-box{width:96px;height:96px;border:1px solid var(--bp-line-strong);display:grid;place-items:center;position:relative;background:rgba(255,255,255,0.03)}
.bp-upload .logo-box::before,.bp-upload .logo-box::after{content:"";position:absolute;width:10px;height:10px;border:1px solid var(--bp-line-strong);background:var(--bp-bg)}
.bp-upload .logo-box::before{top:-5px;left:-5px}
.bp-upload .logo-box::after{bottom:-5px;right:-5px}
.bp-upload .titleblock .name{font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-weight:700;font-size:24px;letter-spacing:0.22em;text-transform:uppercase;color:var(--bp-ink);white-space:nowrap}
.bp-upload .titleblock .sub{font-size:10px;letter-spacing:0.32em;text-transform:uppercase;color:var(--bp-ink-dim);margin-top:-3px}
.bp-upload .titleblock .meta{display:grid;grid-template-columns:repeat(3,minmax(0,auto));gap:0;border:1px solid var(--bp-line-strong);font-size:10px;letter-spacing:0.18em;text-transform:uppercase}
.bp-upload .titleblock .meta>div{padding:8px 14px;border-right:1px solid var(--bp-line)}
.bp-upload .titleblock .meta>div:last-child{border-right:0}
.bp-upload .titleblock .meta b{display:block;color:var(--bp-ink);font-weight:600;margin-top:2px;letter-spacing:0.18em}
.bp-upload .titleblock .meta span{color:var(--bp-ink-faint)}

/* form stage */
.bp-upload .form-stage{padding:48px 0;display:grid;grid-template-columns:1fr;place-items:center}
.bp-upload .form-sheet{position:relative;width:100%;max-width:720px;border:1px solid var(--bp-line-strong);background:rgba(10,44,107,0.55);padding:36px 40px 32px}
.bp-upload .form-sheet>.corner-tl,.bp-upload .form-sheet>.corner-tr,.bp-upload .form-sheet>.corner-bl,.bp-upload .form-sheet>.corner-br{position:absolute;width:12px;height:12px;border:1px solid var(--bp-amber);background:var(--bp-bg-deep)}
.bp-upload .form-sheet>.corner-tl{top:-6px;left:-6px}
.bp-upload .form-sheet>.corner-tr{top:-6px;right:-6px}
.bp-upload .form-sheet>.corner-bl{bottom:-6px;left:-6px}
.bp-upload .form-sheet>.corner-br{bottom:-6px;right:-6px}

/* sheet header */
.bp-upload .sheet-head{display:flex;align-items:center;justify-content:space-between;border-bottom:1px dashed var(--bp-line);padding-bottom:14px;margin-bottom:18px;font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-upload .sheet-head b{color:var(--bp-amber);font-weight:700}

/* form lede */
.bp-upload .form-lede{font-size:13px;line-height:1.6;color:var(--bp-ink);margin:0 0 32px;max-width:520px}

/* step labels */
.bp-upload .step-label{display:flex;align-items:center;gap:10px;font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:var(--bp-ink-dim);margin-bottom:10px}
.bp-upload .step-label b{color:var(--bp-amber);font-weight:700;border:1px solid var(--bp-amber);padding:2px 7px;letter-spacing:0.18em}
.bp-upload .step-label .rule{flex:1;height:1px;background:var(--bp-line)}

/* dropzone */
.bp-upload .dropzone{display:block;width:100%;position:relative;border:1.5px dashed var(--bp-line-strong);background:rgba(255,255,255,0.03);padding:40px 24px;text-align:center;cursor:pointer;transition:background 0.15s,border-color 0.15s;margin-bottom:28px}
.bp-upload .dropzone:hover,.bp-upload .dropzone.drag{border-color:var(--bp-amber);background:rgba(246,198,103,0.06)}
.bp-upload .dropzone .glyph{display:block;margin:0 auto 16px;width:36px;height:36px;color:var(--bp-ink);opacity:0.7}
.bp-upload .dropzone:hover .glyph,.bp-upload .dropzone.drag .glyph,.bp-upload .dropzone.has-file .glyph{color:var(--bp-amber);opacity:1}
.bp-upload .dropzone .dz-title{font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-size:13px;font-weight:500;letter-spacing:0.04em;color:var(--bp-ink);margin-bottom:6px}
.bp-upload .dropzone .dz-title u{text-underline-offset:3px}
.bp-upload .dropzone .dz-sub{font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-upload .dropzone.has-file{border-style:solid;border-color:var(--bp-amber);background:rgba(246,198,103,0.06)}
.bp-upload .dropzone.has-file .dz-title{color:var(--bp-amber);font-weight:600}

/* help accordion */
.bp-upload .help{margin-top:-12px;margin-bottom:28px;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-upload .help summary{cursor:pointer;user-select:none;display:flex;align-items:center;gap:8px;list-style:none;text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--bp-line-strong)}
.bp-upload .help summary::-webkit-details-marker{display:none}
.bp-upload .help summary:hover{color:var(--bp-ink);text-decoration-color:var(--bp-amber)}
.bp-upload .help .body{margin-top:14px;border-left:1px dashed var(--bp-line-strong);padding:6px 0 6px 16px;font-size:12px;line-height:1.7;letter-spacing:0;text-transform:none;color:var(--bp-ink)}
.bp-upload .help .body b{color:var(--bp-amber);display:block;margin-top:10px;font-weight:600}
.bp-upload .help .body b:first-child{margin-top:0}
.bp-upload .help .body .note{color:var(--bp-ink-dim);font-size:11px;margin-top:2px}

/* field / select */
.bp-upload .field{margin-bottom:24px}
.bp-upload .field select{width:100%;appearance:none;-webkit-appearance:none;background:linear-gradient(45deg,transparent 50%,var(--bp-amber) 50%) calc(100% - 18px) 50%/6px 6px no-repeat,linear-gradient(135deg,var(--bp-amber) 50%,transparent 50%) calc(100% - 12px) 50%/6px 6px no-repeat,rgba(10,44,107,0.6);color:var(--bp-ink);border:1px solid var(--bp-line-strong);padding:12px 36px 12px 14px;font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-size:14px;letter-spacing:0.04em;cursor:pointer}
.bp-upload .field select:hover,.bp-upload .field select:focus{outline:none;border-color:var(--bp-amber)}
.bp-upload .field select option{background:var(--bp-bg-deep);color:var(--bp-ink)}

/* buttons */
.bp-upload .btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-weight:600;font-size:13px;letter-spacing:0.22em;text-transform:uppercase;padding:16px 22px;width:100%;cursor:pointer;background:var(--bp-amber);color:#1a1a1a;border:1px solid var(--bp-amber);text-decoration:none;transition:background 0.12s,transform 0.05s}
.bp-upload .btn:hover{background:#f9d486;transform:translateY(-1px)}
.bp-upload .btn:active{transform:translateY(0)}
.bp-upload .btn:disabled{opacity:0.5;cursor:not-allowed;transform:none}
.bp-upload .btn.ghost{background:transparent;color:var(--bp-ink);border:1px solid var(--bp-line-strong)}
.bp-upload .btn.ghost:hover{background:rgba(255,255,255,0.06);border-color:var(--bp-ink)}

/* divider */
.bp-upload .divider{display:flex;align-items:center;gap:14px;margin:24px 0 14px;font-size:10px;letter-spacing:0.32em;text-transform:uppercase;color:var(--bp-ink-faint)}
.bp-upload .divider::before,.bp-upload .divider::after{content:"";flex:1;height:1px;background:var(--bp-line)}

/* progress bar */
.bp-upload .progress-wrap{border:1px solid rgba(246,198,103,0.3);background:rgba(246,198,103,0.06);padding:12px 16px;margin-bottom:20px}
.bp-upload .progress-top{display:flex;justify-content:space-between;font-size:10px;letter-spacing:0.18em;text-transform:uppercase;margin-bottom:8px;color:var(--bp-ink-dim)}
.bp-upload .progress-top b{color:var(--bp-amber)}
.bp-upload .progress-bar{height:3px;background:rgba(255,255,255,0.1);position:relative}
.bp-upload .progress-bar-fill{position:absolute;left:0;top:0;bottom:0;background:var(--bp-amber);transition:width 0.3s ease-out}

/* error */
.bp-upload .error-box{border:1px solid rgba(246,198,103,0.5);background:rgba(246,198,103,0.08);padding:10px 14px;margin-bottom:20px;font-size:12px;color:var(--bp-amber);letter-spacing:0.04em}

/* footnote */
.bp-upload .footnote{margin-top:24px;padding-top:18px;border-top:1px dashed var(--bp-line);text-align:center;font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:var(--bp-ink-faint)}
.bp-upload .footnote .dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--bp-amber);margin-right:6px;vertical-align:middle}

/* responsive */
@media(max-width:720px){
  .bp-upload .sheet{padding:12px 22px 32px}
  .bp-upload .form-sheet{padding:28px 22px 24px}
  .bp-upload .titleblock{grid-template-columns:56px 1fr}
  .bp-upload .titleblock .meta{display:none}
  .bp-upload .topbar .nav{display:none}
}
`;

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

export default function UploadPage() {
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
  const [isMbpFile, setIsMbpFile] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getMajors()
      .then((nextMajors) => { if (!cancelled && nextMajors.length > 0) setMajors(nextMajors); })
      .catch(() => { if (!cancelled) setMajors(FALLBACK_MAJORS); });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    const fallback = FALLBACK_CONCENTRATIONS[majorCode] ?? [];
    setConcentrations(fallback);
    if (fallback.length === 0) setConcentration("none");
    let cancelled = false;
    getConcentrations(majorCode)
      .then((list) => { if (!cancelled && list.length > 0) setConcentrations(list); })
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
    const err = validateFile(f.name);
    if (err) { setError(err); return; }
    setFile(f);
    setIsMbpFile(getFileType(f.name) === "mbp");
    setProgress(0);
    setError(null);
  };

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
        sessionId: result.session_id,
        studentName: result.student_name || majorName,
        major: majorCode,
        completed: result.completed,
        inProgress: result.in_progress,
        coursePositions: {},
        plannedGECourses: {},
        concentration: concentration !== "none" ? concentration : undefined,
      });
      if (concentration !== "none") void syncSession(result.session_id, { concentration });
      createdFlowchart = true;
      setProgress(100);
      router.push(`/flowchart/${result.session_id}`);
    } catch (e) {
      setError(
        isCsv
          ? "Failed to parse course list. Make sure it's the CSV downloaded from Student Center."
          : "Failed to parse transcript. Make sure it's a Cal Poly unofficial transcript PDF.",
      );
      console.error(e);
    } finally {
      if (!createdFlowchart) { setProgress(0); setLoading(false); }
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
      setError("Could not reach the backend for this major. Check the API deployment and NEXT_PUBLIC_API_URL.");
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

  const statusLabel = loading
    ? "Parsing…"
    : file
      ? "File Ready"
      : "Awaiting File";

  const dzClass = `dropzone${dragging ? " drag" : ""}${file ? " has-file" : ""}`;
  const dzTitle = file ? file.name : "Drop your file here, or  click to browse";
  const dzSub = file
    ? `${Math.round(file.size / 1024)} KB · ready to parse`
    : "PDF · CSV · MBP — up to 10 MB";

  return (
    <>
      <style>{css}</style>
      <div className="bp-upload">
        <div className="sheet">

          {/* ── TOPBAR ── */}
          <div className="topbar">
            <span className="dot" />
            <span>Sheet 02 / 03</span>
            <span>Rev. A · 2026.05</span>
            <span>Scale 1 : 1</span>
            <span>Step · Input</span>
            <span className="nav">
              <Link href="/">← Back to Home</Link>
              <Link href="/support">Support</Link>
            </span>
          </div>

          {/* ── TITLE BLOCK ── */}
          <div className="titleblock">
            <div className="logo-box">
              <Image src="/mb-logo.png" alt="Mustang Blueprints" width={84} height={84} style={{ objectFit: "contain" }} />
            </div>
            <div>
              <div className="name">Mustang Blueprints</div>
              <div className="sub">Cal Poly · Four-Year Course Planner · Student-Built</div>
            </div>
            <div className="meta">
              <div><span>Sheet</span><b>02</b></div>
              <div><span>Step</span><b>Input</b></div>
              <div><span>Status</span><b>{statusLabel}</b></div>
            </div>
          </div>

          {/* ── FORM STAGE ── */}
          <main className="form-stage">
            <div className="form-sheet">
              <i className="corner-tl" /><i className="corner-tr" />
              <i className="corner-bl" /><i className="corner-br" />

              <div className="sheet-head">
                <span>Input Your Record</span>
                <span>Detail · D</span>
              </div>

              <p className="form-lede">
                Drop in your transcript, course list, or saved{" "}
                <span className="mono" style={{ color: "var(--bp-amber)" }}>.mbp</span> file.
              </p>

              {/* Step 01: Upload File */}
              <div className="step-label">
                <b>01</b><span>Upload File</span><span className="rule" />
              </div>

              <label
                className={dzClass}
                onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                onDragLeave={() => setDragging(false)}
                onDrop={onDrop}
              >
                <svg
                  className="glyph"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={1.5}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M12 3v12" />
                  <path d="M7 8l5-5 5 5" />
                  <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
                </svg>
                <div className="dz-title">
                  {file ? dzTitle : <>Drop your file here, or <u>click to browse</u></>}
                </div>
                <div className="dz-sub">{dzSub}</div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.csv,.mbp"
                  style={{ display: "none" }}
                  onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }}
                />
              </label>

              {/* Help accordion */}
              <details className="help">
                <summary>How to download your file from my.calpoly.edu</summary>
                <div className="body">
                  <b>📊 CSV — Course List (Recommended)</b>
                  my.calpoly.edu → Student Center → Academic Process → Course List → download arrow (top-right corner)
                  <div className="note">Includes transfer credit and test scores — most accurate option.</div>
                  <b>📄 PDF — Unofficial Transcript</b>
                  my.calpoly.edu → Student Center → Student Records → View Unofficial Transcript → Download PDF
                  <b>🗺️ MBP — Saved Flowchart</b>
                  A <span className="mono">.mbp</span> file you previously exported from Mustang Blueprints.
                </div>
              </details>

              {/* Step 02: Major (hidden for .mbp) */}
              {!isMbpFile && (
                <>
                  <div className="step-label">
                    <b>02</b><span>Major</span><span className="rule" />
                  </div>
                  <div className="field">
                    <select
                      value={majorCode}
                      onChange={(e) => { setMajorCode(e.target.value); setConcentration("none"); }}
                    >
                      {[...majors].sort((a, b) => a.name.localeCompare(b.name)).map((m) => (
                        <option key={m.code} value={m.code}>{m.name}</option>
                      ))}
                    </select>
                  </div>
                </>
              )}

              {/* Step 03: Concentration (hidden for .mbp or when none available) */}
              {!isMbpFile && concentrations.length > 0 && (
                <>
                  <div className="step-label">
                    <b>03</b><span>Concentration</span><span className="rule" />
                  </div>
                  <div className="field">
                    <select
                      value={concentration}
                      onChange={(e) => setConcentration(e.target.value)}
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
                </>
              )}

              {/* Error */}
              {error && <div className="error-box">⚠ {error}</div>}

              {/* Progress */}
              {loading && (
                <div className="progress-wrap">
                  <div className="progress-top">
                    <span>{getProgressLabel(progress)}</span>
                    <b>{Math.round(progress)}%</b>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
                  </div>
                </div>
              )}

              {/* Primary CTA */}
              <button
                className="btn"
                onClick={onSubmit}
                disabled={loading || !file}
              >
                {loading
                  ? (isMbpFile ? "Restoring flowchart…" : "Creating flowchart…")
                  : (isMbpFile ? "Restore My Flowchart →" : "View My Flowchart →")}
              </button>

              <div className="divider">— or —</div>

              {/* Secondary CTA */}
              <button className="btn ghost" onClick={onBrowse} disabled={loading}>
                Browse without a transcript →
              </button>

              {/* Footnote */}
              <div className="footnote">
                <span className="dot" />Parsed locally · nothing leaves your browser
              </div>
            </div>
          </main>
        </div>
      </div>
    </>
  );
}
