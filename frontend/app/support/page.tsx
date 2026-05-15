"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const SUPPORT_EMAIL = "fischerhewittdeveloper@gmail.com";

export default function SupportPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [category, setCategory] = useState("bug");
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const subject = encodeURIComponent(
      `[Mustang Blueprints] ${category === "bug" ? "Bug Report" : category === "feature" ? "Feature Request" : "Question"} from ${name || "a user"}`
    );
    const body = encodeURIComponent(
      `Name: ${name}\nEmail: ${email}\n\n${message}`
    );
    window.location.href = `mailto:${SUPPORT_EMAIL}?subject=${subject}&body=${body}`;
  };

  const canSubmit = message.trim().length > 0;

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--cp-bg)" }}>
      <header style={{ background: "var(--cp-green)" }} className="px-6 py-4 flex items-center gap-3">
        <button onClick={() => router.push("/")} className="text-white/70 hover:text-white text-sm">← Back</button>
        <div className="text-white font-bold text-xl tracking-wide ml-2">Mustang Blueprints</div>
        <div className="ml-auto text-white/70 text-xs">Support</div>
      </header>

      <main className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="w-full max-w-md">
          <h1 className="text-3xl font-bold text-center mb-2" style={{ color: "var(--cp-green)" }}>
            Get Help
          </h1>
          <p className="text-center text-gray-500 mb-8 text-sm leading-relaxed">
            Found a bug? Have a feature idea? Just want to say hi? Fill out the form
            and your email client will open with the message ready to send.
          </p>

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

            <button
              type="submit"
              disabled={!canSubmit}
              className="w-full py-3 rounded-xl font-semibold text-white text-sm transition-opacity disabled:opacity-50"
              style={{ background: "var(--cp-green)" }}
            >
              Open in email client →
            </button>

            <p className="text-center text-xs text-gray-400">
              Sends to <span className="font-mono">{SUPPORT_EMAIL}</span>
            </p>
          </form>
        </div>
      </main>

      <footer className="px-6 py-4 text-center text-xs text-gray-400 border-t border-gray-100">
        Mustang Blueprints is an independent student project and is <strong>not affiliated with or endorsed by Cal Poly San Luis Obispo</strong>.
      </footer>
    </div>
  );
}
