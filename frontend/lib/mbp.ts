import type { TranscriptSession } from "./types";

/** Parse and validate the contents of a `.mbp` file. Throws on invalid input. */
export function parseMbpFile(text: string): TranscriptSession {
  const data = JSON.parse(text) as Record<string, unknown> | null;
  if (!data || typeof data.major !== "string" || !Array.isArray(data.completed)) {
    throw new Error("Invalid Mustang Blueprints file: missing major or completed fields.");
  }
  return data as unknown as TranscriptSession;
}

/** Build the download filename for a session's `.mbp` file. */
export function mbpFilename(session: Pick<TranscriptSession, "studentName" | "major">): string {
  const safeName = session.studentName.replace(/[^a-z0-9]/gi, "_").toLowerCase();
  return `${safeName}-${session.major.toLowerCase()}-flowchart.mbp`;
}
