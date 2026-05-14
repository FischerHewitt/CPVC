import type { TranscriptSession } from "./types";

export function saveSession(session: TranscriptSession): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(`cpvc_session_${session.sessionId}`, JSON.stringify(session));
}

export function loadSession(sessionId: string): TranscriptSession | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(`cpvc_session_${sessionId}`);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as TranscriptSession;
  } catch {
    return null;
  }
}

export function generateSessionId(): string {
  return Math.random().toString(36).slice(2, 10);
}
