import Link from "next/link";
import Image from "next/image";

const css = `
*{box-sizing:border-box}
.bp-page{
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
.bp-page .sheet{position:relative;max-width:1320px;margin:0 auto;padding:12px 48px 0}
.bp-page .mono{font-family:var(--font-mono-bp,'JetBrains Mono',monospace)}
.bp-page .label-strong{font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:var(--bp-ink)}

/* topbar */
.bp-page .topbar{display:flex;align-items:center;gap:24px;border-bottom:1px solid var(--bp-line);padding:8px 0;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-page .topbar .dot{width:8px;height:8px;border-radius:50%;background:var(--bp-amber);box-shadow:0 0 8px var(--bp-amber)}
.bp-page .topbar .spacer{flex:1}
.bp-page .topbar a{color:var(--bp-ink-dim);text-decoration:none;border-bottom:1px solid transparent;padding-bottom:2px;transition:.15s}
.bp-page .topbar a:hover{color:var(--bp-ink);border-color:var(--bp-amber)}

/* title block */
.bp-page .titleblock{margin-top:12px;display:grid;grid-template-columns:72px 1fr auto;align-items:center;gap:20px;padding:8px 0 14px;border-bottom:1px dashed var(--bp-line-strong)}
.bp-page .logo-box{width:72px;height:72px;border:1px solid var(--bp-line-strong);display:grid;place-items:center;position:relative;background:rgba(255,255,255,0.03)}
.bp-page .logo-box::before,.bp-page .logo-box::after{content:"";position:absolute;width:8px;height:8px;border:1px solid var(--bp-line-strong);border-radius:50%}
.bp-page .logo-box::before{top:-4px;left:-4px;background:var(--bp-bg)}
.bp-page .logo-box::after{bottom:-4px;right:-4px;background:var(--bp-bg)}
.bp-page .titleblock .name{font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-weight:700;font-size:38px;letter-spacing:0.28em;text-transform:uppercase;color:var(--bp-ink)}
.bp-page .titleblock .sub{font-size:10px;letter-spacing:0.32em;text-transform:uppercase;color:var(--bp-ink-dim);margin-top:-3px}
.bp-page .titleblock .meta{display:grid;grid-template-columns:repeat(3,minmax(0,auto));gap:0;border:1px solid var(--bp-line-strong);font-size:10px;letter-spacing:0.18em;text-transform:uppercase}
.bp-page .titleblock .meta>div{padding:8px 14px;border-right:1px solid var(--bp-line)}
.bp-page .titleblock .meta>div:last-child{border-right:0}
.bp-page .titleblock .meta b{display:block;color:var(--bp-ink);font-weight:600;margin-top:2px;letter-spacing:0.18em}
.bp-page .titleblock .meta span{color:var(--bp-ink-faint)}

/* hero */
.bp-page .hero{position:relative;padding:24px 0 48px;display:grid;grid-template-columns:1fr 1.15fr;gap:48px;align-items:start}
.bp-page .hero-left{display:flex;flex-direction:column;min-height:100%}
.bp-page .hero .kicker{display:inline-flex;align-items:center;gap:10px;border:1px solid var(--bp-line-strong);padding:6px 12px;font-size:10px;letter-spacing:0.32em;text-transform:uppercase;color:var(--bp-ink);background:rgba(255,255,255,0.03)}
.bp-page .hero .kicker .pip{width:6px;height:6px;background:var(--bp-amber);border-radius:50%}
.bp-page .hero h1{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-weight:800;font-size:clamp(64px,9.2vw,160px);line-height:0.84;letter-spacing:0.005em;text-transform:uppercase;margin:16px 0 0;color:var(--bp-ink)}
.bp-page .hero h1 .stroke{-webkit-text-stroke:1.5px var(--bp-ink);color:transparent}
.bp-page .hero h1 .amber{color:var(--bp-amber);-webkit-text-stroke:0}
.bp-page .hero .ctas{display:flex;align-items:center;gap:14px;margin-top:20px;flex-wrap:nowrap}

/* buttons */
.bp-page .btn{font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-size:13px;letter-spacing:0.28em;text-transform:uppercase;padding:18px 32px;border:1px solid var(--bp-ink);color:var(--bp-bg-deep);background:var(--bp-ink);text-decoration:none;cursor:pointer;display:inline-flex;align-items:center;gap:14px;transition:.15s;white-space:nowrap}
.bp-page .btn:hover{background:var(--bp-amber);border-color:var(--bp-amber);color:#1c1404}
.bp-page .btn.ghost{background:transparent;color:var(--bp-ink);border-color:var(--bp-line-strong)}
.bp-page .btn.ghost:hover{background:rgba(255,255,255,0.06);color:var(--bp-ink);border-color:var(--bp-ink)}

/* hero right */
.bp-page .hero-right{position:relative;border:1px solid var(--bp-line-strong);background:linear-gradient(var(--bp-line-faint) 1px,transparent 1px) 0 0/24px 24px,linear-gradient(90deg,var(--bp-line-faint) 1px,transparent 1px) 0 0/24px 24px,var(--bp-bg-deep);padding:20px}
.bp-page .hero-right .panel-head{display:flex;justify-content:space-between;align-items:center;font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:var(--bp-ink-dim);padding-bottom:10px;border-bottom:1px dashed var(--bp-line)}
.bp-page .hero-right .panel-head b{color:var(--bp-ink);font-weight:600}
.bp-page .detail-callout{position:absolute;border:1px solid var(--bp-ink);border-radius:50%;width:64px;height:64px;display:grid;place-items:center;font-size:9px;letter-spacing:0.22em;text-transform:uppercase;color:var(--bp-ink);text-align:center;background:var(--bp-bg-deep)}
.bp-page .detail-callout.tl{top:-14px;left:-14px}
.bp-page .detail-callout b{display:block;font-size:14px;letter-spacing:0.04em;margin-top:2px}

/* mini chart */
.bp-page .mini-chart{margin-top:18px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.bp-page .mini-chart .col-head{font-size:9px;letter-spacing:0.24em;text-transform:uppercase;color:var(--bp-ink);padding:6px 4px;border:1px solid var(--bp-ink);text-align:center;background:rgba(255,255,255,0.06)}
.bp-page .mini-chart .tile{border:1px solid var(--bp-line-strong);padding:8px 8px 9px;font-size:10px;background:rgba(255,255,255,0.04);position:relative;min-height:54px}
.bp-page .mini-chart .tile .code{font-size:9px;letter-spacing:0.18em;color:var(--bp-ink-dim)}
.bp-page .mini-chart .tile .name{font-size:11px;color:var(--bp-ink);font-weight:600;line-height:1.2;margin-top:4px}
.bp-page .mini-chart .tile.cat-major{background:rgba(125,211,252,0.18);border-color:#7dd3fc}
.bp-page .mini-chart .tile.cat-major .code{color:#bae6fd}
.bp-page .mini-chart .tile.cat-major .name{color:#e0f2fe}
.bp-page .mini-chart .tile.cat-support{background:rgba(167,139,250,0.20);border-color:#a78bfa}
.bp-page .mini-chart .tile.cat-support .code{color:#ddd6fe}
.bp-page .mini-chart .tile.cat-support .name{color:#ede9fe}
.bp-page .mini-chart .tile.cat-ge{background:rgba(74,222,128,0.16);border-color:#4ade80}
.bp-page .mini-chart .tile.cat-ge .code{color:#bbf7d0}
.bp-page .mini-chart .tile.cat-ge .name{color:#dcfce7}
.bp-page .mini-chart .tile.done{box-shadow:inset 0 0 0 9999px rgba(246,198,103,0.22);border-color:var(--bp-amber)}
.bp-page .mini-chart .tile.done .code{color:var(--bp-amber)}
.bp-page .mini-chart .tile.done .name{color:var(--bp-amber)}
.bp-page .mini-chart .tile.done::after{content:"✓";position:absolute;top:4px;right:7px;font-weight:700;font-size:12px;color:var(--bp-amber)}
.bp-page .mini-chart .tile.now{border-style:dashed}
.bp-page .mini-chart .tile.now::after{content:"IP";position:absolute;top:6px;right:8px;font-size:8px;letter-spacing:0.1em;color:var(--bp-ink);font-weight:700}
.bp-page .mini-chart .tile.placeholder{background-image:repeating-linear-gradient(45deg,transparent 0 6px,rgba(255,255,255,0.06) 6px 12px);border-style:dashed}
.bp-page .mini-chart .tile.placeholder .name{font-style:italic;opacity:0.9}

/* progress row */
.bp-page .progress-row{margin-top:18px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.bp-page .progress-cell{border:1px solid var(--bp-line);padding:10px 12px}
.bp-page .progress-cell .lbl{display:flex;justify-content:space-between;font-size:9px;letter-spacing:0.24em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-page .progress-cell .lbl b{color:var(--bp-ink);font-weight:600}
.bp-page .progress-cell .bar{margin-top:8px;height:4px;background:rgba(255,255,255,0.1);position:relative}
.bp-page .progress-cell .bar::after{content:"";position:absolute;left:0;top:0;bottom:0}
.bp-page .progress-cell.major .bar::after{width:62%;background:#7dd3fc}
.bp-page .progress-cell.support .bar::after{width:33%;background:#a78bfa}
.bp-page .progress-cell.ge .bar::after{width:45%;background:#4ade80}

/* legend */
.bp-page .legend{margin-top:14px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.bp-page .legend .item{display:flex;align-items:center;gap:10px;font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:var(--bp-ink);border:1px solid var(--bp-line);padding:8px 10px}
.bp-page .legend .sw{width:18px;height:14px;border:1px solid var(--bp-ink)}
.bp-page .legend .sw.major{background:rgba(125,211,252,0.45);border-color:#7dd3fc}
.bp-page .legend .sw.support{background:rgba(167,139,250,0.45);border-color:#a78bfa}
.bp-page .legend .sw.conc{background:rgba(244,114,182,0.45);border-color:#f472b6}
.bp-page .legend .sw.ge{background:rgba(74,222,128,0.45);border-color:#4ade80}

/* section */
.bp-page .section{position:relative;padding:72px 0}
.bp-page .section-head{display:grid;grid-template-columns:144px 1fr auto;align-items:end;gap:24px;border-top:1px solid var(--bp-line-strong);border-bottom:1px dashed var(--bp-line-strong);padding:24px 0;margin-bottom:48px}
.bp-page .section-head .bignum{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-weight:800;font-size:120px;line-height:0.85;letter-spacing:0.005em;color:var(--bp-amber);margin:0}
.bp-page .section-head .head-body{padding-bottom:6px}
.bp-page .section-head .num{font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-size:12px;letter-spacing:0.32em;text-transform:uppercase;color:var(--bp-ink-dim);display:inline-flex;align-items:center;gap:8px}
.bp-page .section-head .num::before{content:"";width:24px;height:1px;background:var(--bp-amber)}
.bp-page .section-head h2{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-weight:800;font-size:clamp(56px,6.4vw,96px);line-height:0.88;letter-spacing:0.005em;text-transform:uppercase;margin:14px 0 0;color:var(--bp-ink)}
.bp-page .section-head .scale{font-family:var(--font-mono-bp,'JetBrains Mono',monospace);font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:var(--bp-ink-dim);border:1px solid var(--bp-line-strong);padding:8px 12px;align-self:end;margin-bottom:6px}

/* steps */
.bp-page .steps{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid var(--bp-line-strong)}
.bp-page .step{padding:24px;border-right:1px solid var(--bp-line);position:relative;display:flex;flex-direction:column}
.bp-page .step:last-child{border-right:0}
.bp-page .step .step-num{display:flex;align-items:baseline;gap:10px;font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-page .step .step-num b{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-size:64px;font-weight:800;line-height:1;color:var(--bp-amber);letter-spacing:0.01em}
.bp-page .step h3{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-size:32px;font-weight:700;letter-spacing:0.01em;text-transform:uppercase;margin:16px 0 10px;color:var(--bp-ink)}
.bp-page .step p{font-size:13px;line-height:1.65;color:var(--bp-ink);margin:0 0 24px}
.bp-page .step .icon{margin-top:auto;height:144px;border:1px dashed var(--bp-line-strong);display:grid;place-items:center;color:var(--bp-ink-dim);font-size:10px;letter-spacing:0.22em;text-transform:uppercase;background:repeating-linear-gradient(45deg,transparent 0 8px,rgba(255,255,255,0.03) 8px 16px)}
.bp-page .step .icon svg{width:100%;height:100%;padding:18px}

/* features */
.bp-page .features{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
.bp-page .feat{border:1px solid var(--bp-line-strong);padding:24px;position:relative;background:rgba(255,255,255,0.02)}
.bp-page .feat::before{content:"";position:absolute;top:-5px;left:-5px;width:10px;height:10px;border:1px solid var(--bp-line-strong);background:var(--bp-bg)}
.bp-page .feat::after{content:"";position:absolute;bottom:-5px;right:-5px;width:10px;height:10px;border:1px solid var(--bp-line-strong);background:var(--bp-bg)}
.bp-page .feat .feat-label{display:flex;justify-content:space-between;font-size:9px;letter-spacing:0.28em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-page .feat h3{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-size:36px;font-weight:700;letter-spacing:0.01em;text-transform:uppercase;margin:12px 0 10px;color:var(--bp-ink);line-height:1}
.bp-page .feat p{font-size:13px;line-height:1.65;color:var(--bp-ink);margin:0}
.bp-page .feat.size-lg{grid-column:span 6}
.bp-page .feat.size-md{grid-column:span 4}
.bp-page .feat.size-half{grid-column:span 6}
.bp-page .feat.size-full{grid-column:span 12;padding:24px}
.bp-page .feat .stat{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-size:108px;font-weight:800;letter-spacing:0.005em;line-height:0.9;color:var(--bp-amber);margin:14px 0 4px}
.bp-page .feat .stat-sub{font-size:10px;letter-spacing:0.24em;text-transform:uppercase;color:var(--bp-ink-dim)}
.bp-page .feat .screenshot-frame{margin-top:18px;border:1px solid var(--bp-line-strong);background:rgba(255,255,255,0.04);padding:8px;position:relative}

/* cta block */
.bp-page .cta-block{position:relative;border:1.5px solid var(--bp-ink);padding:48px;margin:48px 0;background:repeating-linear-gradient(45deg,transparent 0 22px,rgba(255,255,255,0.03) 22px 44px)}
.bp-page .cta-block::before,.bp-page .cta-block::after,.bp-page .cta-block>i:nth-child(1),.bp-page .cta-block>i:nth-child(2){content:"";position:absolute;width:14px;height:14px;border:1px solid var(--bp-ink);border-radius:50%;background:var(--bp-bg)}
.bp-page .cta-block::before{top:-8px;left:-8px}
.bp-page .cta-block::after{top:-8px;right:-8px}
.bp-page .cta-block>i:nth-child(1){bottom:-8px;left:-8px}
.bp-page .cta-block>i:nth-child(2){bottom:-8px;right:-8px}
.bp-page .cta-block .tag{display:inline-block;font-size:10px;letter-spacing:0.32em;text-transform:uppercase;color:var(--bp-amber)}
.bp-page .cta-block h2{font-family:var(--font-display,'Big Shoulders Display',sans-serif);font-weight:800;font-size:clamp(56px,7vw,104px);line-height:0.9;letter-spacing:0.01em;text-transform:uppercase;margin:10px 0 18px;color:var(--bp-ink);max-width:980px}
.bp-page .cta-block p{max-width:560px;font-size:14px;line-height:1.65;color:var(--bp-ink);margin:0 0 28px}
.bp-page .cta-block .ctas{display:flex;align-items:center;gap:14px;flex-wrap:wrap}

/* footer */
.bp-page footer{border-top:1px dashed var(--bp-line-strong);padding:24px 0 48px;color:var(--bp-ink-dim);font-size:10px;letter-spacing:0.18em;text-transform:uppercase;display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}
.bp-page footer p{margin:0;line-height:1.8}
.bp-page footer .disclaimer{max-width:640px;text-transform:none;letter-spacing:0.04em;font-size:11px;color:var(--bp-ink)}
.bp-page footer .disclaimer strong{color:var(--bp-amber);font-weight:700}
.bp-page footer .footnote{font-size:9px;color:var(--bp-ink-faint)}
.bp-page footer .right{text-align:right}
.bp-page footer a{color:var(--bp-ink);text-decoration:none;border-bottom:1px solid var(--bp-line-strong);padding-bottom:1px}
.bp-page footer a:hover{border-color:var(--bp-amber);color:var(--bp-amber)}

/* responsive */
@media(max-width:900px){
  .bp-page .sheet{padding:20px 22px 0}
  .bp-page .hero{grid-template-columns:1fr;padding:40px 0 56px}
  .bp-page .titleblock{grid-template-columns:64px 1fr}
  .bp-page .titleblock .meta{grid-column:span 2;margin-top:8px}
  .bp-page .steps{grid-template-columns:1fr}
  .bp-page .step{border-right:0;border-bottom:1px solid var(--bp-line)}
  .bp-page .step:last-child{border-bottom:0}
  .bp-page .section-head{grid-template-columns:1fr}
  .bp-page .section-head .bignum{font-size:84px}
  .bp-page .section-head .scale{justify-self:start}
  .bp-page .features .feat.size-lg,.bp-page .features .feat.size-md,.bp-page .features .feat.size-half{grid-column:span 12}
  .bp-page .legend{grid-template-columns:repeat(2,1fr)}
  .bp-page footer{grid-template-columns:1fr}
  .bp-page footer .right{text-align:left}
  .bp-page .cta-block{padding:36px 24px 40px}
}
`;

export default function HomePage() {
  return (
    <>
      <style>{css}</style>
      <div className="bp-page">
        <div className="sheet">

          {/* ── TOPBAR ── */}
          <div className="topbar">
            <span className="dot" />
            <span>Sheet 01 / 01</span>
            <span>Rev. A · 2026.05</span>
            <span>Scale 1 : 1</span>
            <span className="spacer" />
            <a href="#how">How It Works</a>
            <Link href="/">Planner</Link>
            <a href="#about">About</a>
            <Link href="/support">Support</Link>
          </div>

          {/* ── TITLE BLOCK ── */}
          <div className="titleblock">
            <div className="logo-box">
              <Image src="/mb-logo.png" alt="Mustang Blueprints" width={62} height={62} style={{ objectFit: "contain" }} />
            </div>
            <div>
              <div className="name">Mustang Blueprints</div>
              <div className="sub">Cal Poly · Four-Year Course Planner · Student-Built</div>
            </div>
            <div className="meta">
              <div><span>Project</span><b>MB-001</b></div>
              <div><span>Majors</span><b>65 Total</b></div>
              <div><span>Status</span><b>Live</b></div>
            </div>
          </div>

          {/* ── HERO ── */}
          <section className="hero">
            <div className="hero-left">
              <span className="kicker"><span className="pip" />A Blueprint for Your Degree</span>
              <h1>
                Draft your<br />
                <span className="stroke">
                  <span className="amber">four</span> years.
                </span>
              </h1>
              <div className="ctas">
                <Link href="/" className="btn">Open the Planner <span>→</span></Link>
                <a href="#how" className="btn ghost">See how it works</a>
              </div>
              <div style={{ marginTop: "24px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px 28px", maxWidth: "560px" }}>
                <div className="label-strong">✓ No account · No storage</div>
                <div className="label-strong">✓ Works for all 65 majors</div>
                <div className="label-strong">✓ PDF or CSV upload</div>
                <div className="label-strong">✓ Tracks GE + concentrations</div>
              </div>
            </div>

            {/* Hero right: mini flowchart preview */}
            <div className="hero-right">
              <div className="detail-callout tl">Detail<b>A</b></div>
              <div className="panel-head">
                <span>SAM · COMPUTER SCIENCE · BS</span>
                <span><b>52</b> / 120 units</span>
              </div>
              <div className="mini-chart">
                <div className="col-head">Fr · Fall</div>
                <div className="col-head">Fr · Spr</div>
                <div className="col-head">So · Fall</div>
                <div className="col-head">So · Spr</div>
                {/* major row */}
                <div className="tile cat-major done"><div className="code">CSC 1024</div><div className="name">Intro to Computing</div></div>
                <div className="tile cat-major done"><div className="code">CSC 1001</div><div className="name">Fund. of CS</div></div>
                <div className="tile cat-major done"><div className="code">CSC 2001</div><div className="name">Data Structures</div></div>
                <div className="tile cat-major now"><div className="code">CSC 2050</div><div className="name">Sys. Software</div></div>
                {/* support row */}
                <div className="tile cat-support done"><div className="code">MATH 1261</div><div className="name">Calculus I</div></div>
                <div className="tile cat-support done"><div className="code">MATH 1262</div><div className="name">Calculus II</div></div>
                <div className="tile cat-support now"><div className="code">MATH 1151</div><div className="name">Linear Algebra</div></div>
                <div className="tile cat-support"><div className="code">MATH 2031</div><div className="name">Adv. Math</div></div>
                {/* GE row */}
                <div className="tile cat-ge done"><div className="code">GE 1A</div><div className="name">Written Comm.</div></div>
                <div className="tile cat-ge done"><div className="code">GE 1B</div><div className="name">Critical Think.</div></div>
                <div className="tile cat-ge placeholder"><div className="code">GE 3A · Arts</div><div className="name">Choose 1</div></div>
                <div className="tile cat-ge placeholder"><div className="code">GE 3B · Hum.</div><div className="name">Choose 1</div></div>
              </div>
              <div className="progress-row">
                <div className="progress-cell major">
                  <div className="lbl"><span>Major</span><b>9 / 14</b></div>
                  <div className="bar" />
                </div>
                <div className="progress-cell support">
                  <div className="lbl"><span>Support</span><b>1 / 3</b></div>
                  <div className="bar" />
                </div>
                <div className="progress-cell ge">
                  <div className="lbl"><span>Gen. Ed.</span><b>5 / 11</b></div>
                  <div className="bar" />
                </div>
              </div>
              <div className="legend">
                <div className="item"><span className="sw major" />Major</div>
                <div className="item"><span className="sw support" />Support</div>
                <div className="item"><span className="sw conc" />Concentration</div>
                <div className="item"><span className="sw ge" />Gen Ed</div>
              </div>
            </div>
          </section>

          {/* ── SECTION 01: HOW IT WORKS ── */}
          <section className="section" id="how">
            <div className="section-head">
              <div className="bignum">01</div>
              <div className="head-body">
                <div className="num" style={{ color: "rgb(246,198,103)" }}>Section · Procedure</div>
                <h2>From transcript<br />to flowchart in <span style={{ color: "var(--bp-amber)" }}>~10 seconds</span>.</h2>
              </div>
              <div className="scale">Scale · 1:1 · Sheet 01</div>
            </div>

            <div className="steps">
              {/* Step 01 */}
              <div className="step">
                <div className="step-num"><b>01</b><span>Upload</span></div>
                <h3>Drop in your transcript.</h3>
                <p style={{ fontSize: "14px", lineHeight: "1.75" }}>
                  PDF unofficial transcript, CSV course list from Student Center, or a saved{" "}
                  <span className="mono">.mbp</span> file — whichever you have. Nothing leaves your browser.
                </p>
                <div className="icon">
                  <svg viewBox="0 0 160 100" fill="none" stroke="currentColor" strokeWidth={1.2} preserveAspectRatio="xMidYMid meet">
                    <rect x="30" y="10" width="54" height="68" stroke="#F1F6FF" />
                    <path d="M38 22 H76 M38 30 H76 M38 38 H68 M38 46 H72 M38 54 H62 M38 62 H70" stroke="#F1F6FF" strokeDasharray="3 3" opacity={0.6} />
                    <text x="38" y="18" fontFamily="JetBrains Mono" fontSize="5" fill="#F6C667" stroke="none" letterSpacing="1">TRANSCRIPT</text>
                    <path d="M100 22 H132 M124 14 L132 22 L124 30" stroke="#F6C667" strokeWidth={1.4} />
                    <text x="104" y="38" fontFamily="JetBrains Mono" fontSize="5" fill="#F6C667" stroke="none" letterSpacing="1">PARSE</text>
                    <rect x="100" y="50" width="40" height="28" stroke="#F1F6FF" strokeDasharray="3 3" />
                    <path d="M114 60 H126 M114 66 H126 M114 72 H122" stroke="#F1F6FF" opacity={0.7} />
                    <path d="M30 86 H84 M30 84 V88 M84 84 V88" stroke="#F1F6FF" opacity={0.4} />
                    <path d="M100 86 H140 M100 84 V88 M140 84 V88" stroke="#F1F6FF" opacity={0.4} />
                  </svg>
                </div>
              </div>
              {/* Step 02 */}
              <div className="step">
                <div className="step-num"><b>02</b><span>Match</span></div>
                <h3>Courses light up.</h3>
                <p style={{ lineHeight: "1.75", fontSize: "14px" }}>
                  Every completed class is auto-mapped to its slot — quarter equivalents included. Prereqs unlock,
                  in-progress classes mark themselves, transfer credit lands where it belongs.
                </p>
                <div className="icon">
                  <svg viewBox="0 0 160 100" fill="none" stroke="currentColor" strokeWidth={1.2} preserveAspectRatio="xMidYMid meet">
                    <g stroke="#F1F6FF" strokeWidth={1.1}>
                      <rect x="18" y="22" width="28" height="22" fill="rgba(246,198,103,0.18)" stroke="#F6C667" />
                      <rect x="54" y="22" width="28" height="22" fill="rgba(246,198,103,0.18)" stroke="#F6C667" />
                      <rect x="90" y="22" width="28" height="22" strokeDasharray="3 3" />
                      <rect x="126" y="22" width="28" height="22" strokeDasharray="3 3" />
                      <rect x="18" y="54" width="28" height="22" fill="rgba(246,198,103,0.18)" stroke="#F6C667" />
                      <rect x="54" y="54" width="28" height="22" strokeDasharray="3 3" />
                      <rect x="90" y="54" width="28" height="22" strokeDasharray="3 3" />
                      <rect x="126" y="54" width="28" height="22" strokeDasharray="3 3" />
                    </g>
                    <g stroke="#F6C667" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" fill="none">
                      <path d="M28 33 L31 36 L37 30" />
                      <path d="M64 33 L67 36 L73 30" />
                      <path d="M28 65 L31 68 L37 62" />
                    </g>
                    <g fontFamily="JetBrains Mono" fontSize={4.5} fill="#F1F6FF" stroke="none" opacity={0.55} letterSpacing="0.8">
                      <text x="22" y="16">FR·F</text>
                      <text x="58" y="16">FR·S</text>
                      <text x="94" y="16">SO·F</text>
                      <text x="130" y="16">SO·S</text>
                    </g>
                    <path d="M18 86 H154" stroke="#F1F6FF" opacity={0.3} strokeDasharray="2 4" />
                  </svg>
                </div>
              </div>
              {/* Step 03 */}
              <div className="step">
                <div className="step-num"><b>03</b><span>Plan</span></div>
                <h3>Map out the rest.</h3>
                <p style={{ fontSize: "14px", lineHeight: "1.75" }}>
                  Pick a concentration, drag electives around, plan GEs by area. Save your blueprint as a{" "}
                  <span className="mono">.mbp</span> and pick it back up next quarter.
                </p>
                <div className="icon">
                  <svg viewBox="0 0 160 100" fill="none" stroke="currentColor" strokeWidth={1.2} preserveAspectRatio="xMidYMid meet">
                    <circle cx="16" cy="50" r="5" fill="#F6C667" stroke="#F6C667" />
                    <text x="6" y="68" fontFamily="JetBrains Mono" fontSize="5" fill="#F1F6FF" stroke="none" opacity={0.7} letterSpacing="1">NOW</text>
                    <path d="M22 50 Q42 50 50 32 T84 28 Q102 28 110 50 T144 50" stroke="#F6C667" strokeWidth={1.4} strokeDasharray="4 3" />
                    <circle cx="50" cy="32" r="3" stroke="#F1F6FF" />
                    <circle cx="84" cy="28" r="3" stroke="#F1F6FF" />
                    <circle cx="110" cy="50" r="3" stroke="#F1F6FF" />
                    <line x1="144" y1="50" x2="144" y2="22" stroke="#F1F6FF" strokeWidth={1.4} />
                    <path d="M144 22 L156 26 L144 30 Z" fill="#F6C667" stroke="#F6C667" />
                    <text x="130" y="68" fontFamily="JetBrains Mono" fontSize="5" fill="#F6C667" stroke="none" letterSpacing="1">DIPLOMA</text>
                    <path d="M8 84 H152" stroke="#F1F6FF" opacity={0.3} strokeDasharray="2 4" />
                  </svg>
                </div>
              </div>
            </div>
          </section>

          {/* ── SECTION 02: SPECIFICATIONS ── */}
          <section className="section" id="about">
            <div className="section-head">
              <div className="bignum">02</div>
              <div className="head-body">
                <div className="num" style={{ color: "rgb(246,198,103)" }}>Section · Specifications</div>
                <h2>Built for the way<br />Cal Poly actually works.</h2>
              </div>
              <div className="scale">Detail · B · Sheet 02</div>
            </div>

            <div className="features">
              <div className="feat size-lg">
                <div className="feat-label"><span>01 · Catalog Accuracy</span><span>Verified</span></div>
                <h3>Every course pulled straight from the Cal Poly catalog.</h3>
                <p style={{ lineHeight: "1.75" }}>
                  Units, titles, prerequisites and term placement match the published flowchart for each major.
                  Footnotes from the catalog are surfaced as &ldquo;Tips&rdquo; right next to the relevant tile
                  — including those weird overlap rules nobody reads.
                </p>
              </div>

              <div className="feat size-md">
                <div className="feat-label"><span>02 · Coverage</span><span>Scope</span></div>
                <div className="stat">65</div>
                <div className="stat-sub">Majors supported</div>
                <p style={{ marginTop: "18px" }}>
                  From Aerospace to Wine &amp; Viticulture. Concentrations, emphases, and tracks all included.
                </p>
              </div>

              <div className="feat size-half">
                <div className="feat-label"><span>03 · Q→S Mapping</span><span>Built-in</span></div>
                <h3 style={{ fontSize: "22px" }}>Quarter to semester, handled.</h3>
                <p>
                  Transcripts from the quarter system are mapped automatically. CSC 101 becomes CSC 1001.
                  CHEM 124 becomes CHEM 1241. You don&apos;t do the math.
                </p>
              </div>

              <div className="feat size-half">
                <div className="feat-label"><span>04 · Privacy</span><span>Local-only</span></div>
                <h3 style={{ fontSize: "22px" }}>Your transcript never leaves your browser.</h3>
                <p>
                  Parsing happens locally. We don&apos;t store transcripts, names, or PolyPass IDs.
                  Save to a <span className="mono">.mbp</span> file you control.
                </p>
              </div>

              <div className="feat size-full">
                <div className="feat-label"><span>Detail · C · In Use</span><span>Computer Science · BS</span></div>
                <h3 style={{ fontSize: "22px" }}>What you&apos;ll see inside.</h3>
                <p style={{ maxWidth: "780px" }}>
                  Every requirement, every prereq lock, every GE bucket — laid out the way Cal Poly publishes them.
                  Check off classes as you go, plan electives, and watch the progress bars move.
                </p>
                <div className="screenshot-frame">
                  <div style={{ height: "280px", display: "grid", placeItems: "center", background: "rgba(10,44,107,0.7)" }}>
                    <div style={{ textAlign: "center" }}>
                      <div style={{ fontSize: "10px", letterSpacing: "0.28em", textTransform: "uppercase", color: "rgba(241,246,255,0.35)", marginBottom: "16px" }}>
                        Flowchart Preview
                      </div>
                      <Link href="/" className="btn" style={{ fontSize: "10px" }}>
                        Open the Planner →
                      </Link>
                    </div>
                  </div>
                </div>
              </div>

              <div className="feat size-half">
                <div className="feat-label"><span>05 · Planning Tools</span><span>Interactive</span></div>
                <h3>Notes, electives, GE planner, in-progress tracking.</h3>
                <p style={{ lineHeight: "1.75" }}>
                  Add personal notes per term. Pick which courses you&apos;ll use to satisfy each GE area.
                  Mark classes in-progress so your projected progress bar moves with you.
                </p>
              </div>

              <div className="feat size-half">
                <div className="feat-label"><span>06 · Free &amp; Open</span><span>By a student</span></div>
                <h3>Made by a Cal Poly student, free for every Cal Poly student.</h3>
                <p style={{ lineHeight: "1.75" }}>
                  No subscription. No sign-up. No nonsense. Mustang Blueprints exists because building a
                  four-year plan in Excel is a rite of passage that nobody asked for.
                </p>
              </div>
            </div>
          </section>

          {/* ── CTA BLOCK ── */}
          <section className="section" id="cta">
            <div className="cta-block">
              <i /><i />
              <span className="tag">— Ready to draft?</span>
              <h2>Bring a transcript.<br />Leave with a plan.</h2>
              <p>Most students finish in under 30 seconds. No account required. Works on any browser, any device, any major.</p>
              <div className="ctas">
                <Link href="/" className="btn">Start Your Blueprint <span>→</span></Link>
                <Link href="/" className="btn ghost">Browse without a transcript</Link>
              </div>
            </div>
          </section>

          {/* ── FOOTER ── */}
          <footer>
            <div>
              <p className="disclaimer">
                Mustang Blueprints is an independent student project and is{" "}
                <strong>not affiliated with or endorsed by Cal&nbsp;Poly San Luis Obispo</strong>.
                Course requirements change every catalog year — always verify your plan with your academic advisor before registering.
              </p>
              <p className="footnote" style={{ marginTop: "14px" }}>
                © 2026 Mustang Blueprints · MB-001 · Rev. A
              </p>
            </div>
            <div className="right">
              <p>
                <Link href="/legal">Privacy &amp; Legal</Link>
                {" "}&nbsp;·&nbsp;{" "}
                <Link href="/support">Support</Link>
                {" "}&nbsp;·&nbsp;{" "}
                <Link href="/">Open the Planner</Link>
              </p>
              <p className="footnote" style={{ marginTop: "14px" }}>
                Drawn &amp; drafted in San Luis Obispo, CA
              </p>
            </div>
          </footer>

        </div>
      </div>
    </>
  );
}
