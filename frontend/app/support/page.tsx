"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { sendContactMessage } from "@/lib/api";

type Status = "idle" | "loading" | "success" | "error";

export default function SupportPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [category, setCategory] = useState("bug");
  const [customSubject, setCustomSubject] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const canSubmit = message.trim().length > 0 && status !== "loading";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    setStatus("loading");
    setErrorMsg("");
    try {
      await sendContactMessage({
        name,
        email,
        category,
        custom_subject: customSubject,
        message,
      });
      setStatus("success");
    } catch (err) {
      setStatus("error");
      setErrorMsg(err instanceof Error ? err.message : "Unknown error");
    }
  };

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
        <button onClick={() => router.push("/")} className="text-white/60 hover:text-white text-sm font-mono">← Back</button>
        <Image src="/mb-logo.png" alt="Mustang Blueprints" width={36} height={36} className="rounded flex-shrink-0 ml-1" style={{ border: "2px solid rgba(255,255,255,0.85)" }} />
        <div>
          <div className="text-white font-bold text-base tracking-widest uppercase font-mono leading-tight">Mustang Blueprints</div>
          <div className="text-white/45 text-[9px] tracking-widest uppercase font-mono">Cal Poly Course Planner</div>
        </div>
        <div className="ml-auto text-white/40 text-xs font-mono tracking-wide">Support</div>
      </header>

      <main className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="w-full max-w-md">
          <h1 className="text-3xl font-bold text-center mb-2" style={{ color: "var(--cp-green)" }}>
            Get Help
          </h1>
          <p className="text-center text-gray-500 mb-8 text-sm leading-relaxed">
            Found a bug? Have a feature idea? Just want to say hi? Fill out the form and we&apos;ll get your message.
          </p>

          {status === "success" ? (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 flex flex-col items-center gap-4 text-center">
              <div className="text-4xl">✓</div>
              <div className="text-lg font-semibold text-gray-800">Message sent!</div>
              <p className="text-sm text-gray-500">Thanks for reaching out. We&apos;ll get back to you soon.</p>
              <button
                onClick={() => { setStatus("idle"); setMessage(""); setCustomSubject(""); }}
                className="mt-2 text-sm font-medium underline"
                style={{ color: "var(--cp-green)" }}
              >
                Send another message
              </button>
            </div>
          ) : (
            <form
              onSubmit={handleSubmit}
              className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col gap-5"
            >
              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Your name <span className="text-gray-400 font-normal">(optional)</span></label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Cal Poly Student"
                  className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2"
                  style={{ "--tw-ring-color": "var(--cp-green)" } as React.CSSProperties}
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Your email <span className="text-gray-400 font-normal">(optional — for a reply)</span></label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@calpoly.edu"
                  className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2"
                  style={{ "--tw-ring-color": "var(--cp-green)" } as React.CSSProperties}
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Category</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none"
                >
                  <option value="bug">Bug report</option>
                  <option value="feature">Feature request</option>
                  <option value="question">Question</option>
                  <option value="other">Other</option>
                </select>
              </div>

              {category === "other" && (
                <div className="flex flex-col gap-1">
                  <label className="text-sm font-medium text-gray-700">Subject <span className="text-gray-400 font-normal">(optional)</span></label>
                  <input
                    type="text"
                    value={customSubject}
                    onChange={(e) => setCustomSubject(e.target.value)}
                    placeholder="Brief description of your topic"
                    className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2"
                    style={{ "--tw-ring-color": "var(--cp-green)" } as React.CSSProperties}
                  />
                </div>
              )}

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Message <span className="text-red-400">*</span></label>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Describe your issue or idea…"
                  rows={5}
                  className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none resize-none focus:ring-2"
                  style={{ "--tw-ring-color": "var(--cp-green)" } as React.CSSProperties}
                  required
                />
              </div>

              {status === "error" && (
                <p className="text-sm text-red-500 rounded-lg bg-red-50 border border-red-200 px-3 py-2">
                  {errorMsg || "Failed to send. Please try again."}
                </p>
              )}

              <button
                type="submit"
                disabled={!canSubmit}
                className="w-full py-3 rounded-xl font-semibold text-white text-sm transition-opacity disabled:opacity-50"
                style={{ background: "var(--cp-green)" }}
              >
                {status === "loading" ? "Sending…" : "Send Message →"}
              </button>
            </form>
          )}
        </div>
      </main>

      <footer className="px-6 py-4 text-center text-xs text-gray-400 border-t border-gray-100">
        Mustang Blueprints is an independent student project and is <strong>not affiliated with or endorsed by Cal Poly San Luis Obispo</strong>.
      </footer>
    </div>
  );
}
