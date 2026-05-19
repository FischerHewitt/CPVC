import Link from "next/link";
import Image from "next/image";

export default function LegalPage() {
  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--cp-bg)" }}>
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
        <Link href="/" className="text-white/60 hover:text-white text-sm font-mono">← Back</Link>
        <Image src="/mb-logo.png" alt="Mustang Blueprints" width={36} height={36} className="rounded flex-shrink-0 ml-1" style={{ border: "2px solid rgba(255,255,255,0.85)" }} />
        <div>
          <div className="text-white font-bold text-base tracking-widest uppercase font-mono leading-tight">Mustang Blueprints</div>
          <div className="text-white/45 text-[9px] tracking-widest uppercase font-mono">Cal Poly Course Planner</div>
        </div>
      </header>

      <main className="flex-1 px-4 py-12">
        <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-200 p-8 flex flex-col gap-8">
          <div>
            <h1 className="text-2xl font-bold mb-1" style={{ color: "var(--cp-green)" }}>Privacy &amp; Legal</h1>
            <p className="text-xs text-gray-400">Independent student project — not affiliated with Cal Poly SLO</p>
          </div>

          <section className="flex flex-col gap-2">
            <h2 className="text-base font-semibold text-gray-800">Affiliation Disclaimer</h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              Mustang Blueprints is an independent student project and is <strong>not affiliated with, endorsed by,
              or sponsored by California Polytechnic State University, San Luis Obispo</strong>. Cal Poly&apos;s name,
              logo, and course data are referenced solely for informational purposes.
            </p>
          </section>

          <section className="flex flex-col gap-2">
            <h2 className="text-base font-semibold text-gray-800">Data Accuracy</h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              Flowchart data is sourced from the Cal Poly catalog but may be incomplete or out of date.
              Course requirements, unit counts, and prerequisite rules change from year to year.{" "}
              <strong>Always verify your degree plan with your academic advisor and the official Cal Poly catalog.</strong>{" "}
              Mustang Blueprints is a planning aid, not an official degree audit tool.
            </p>
          </section>

          <section className="flex flex-col gap-2">
            <h2 className="text-base font-semibold text-gray-800">Your Transcript &amp; Privacy</h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              When you upload a transcript or CSV course list, it is processed locally in your browser and on our
              server only long enough to extract your completed course numbers. <strong>Your transcript file is never
              stored.</strong> The course numbers extracted from it are saved to your session so the flowchart can
              show your progress — this data is tied to your session ID and is not linked to your identity.
            </p>
            <p className="text-sm text-gray-600 leading-relaxed">
              Session data (completed courses, notes, course positions) is stored in our database to let you
              restore your flowchart from any device. You can delete your session at any time by contacting us
              via the <Link href="/support" className="underline hover:text-gray-800">Support</Link> page.
            </p>
          </section>

          <section className="flex flex-col gap-2">
            <h2 className="text-base font-semibold text-gray-800">No Warranty</h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              This tool is provided as-is without any warranty. We make no guarantees about the accuracy,
              completeness, or fitness for any particular purpose of the information shown. Use it at your
              own discretion.
            </p>
          </section>

          <section className="flex flex-col gap-2">
            <h2 className="text-base font-semibold text-gray-800">Contact</h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              Questions, corrections, or data deletion requests?{" "}
              <Link href="/support" className="underline hover:text-gray-800">Reach out via the Support page.</Link>
            </p>
          </section>
        </div>
      </main>

      <footer className="px-6 py-4 text-center text-xs text-gray-400 border-t border-gray-100">
        Mustang Blueprints — Cal Poly SLO Course Planner
      </footer>
    </div>
  );
}
