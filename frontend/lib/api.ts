import type { Flowchart, Professor } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function parseTranscript(file: File): Promise<{
  student_name: string;
  student_id: string;
  major: string;
  completed: string[];
  in_progress: string[];
}> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API}/api/transcript/parse`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getFlowchart(majorCode: string): Promise<Flowchart> {
  const res = await fetch(`${API}/api/flowchart/${majorCode}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function inferPrerequisites(
  majorCode: string,
  completed: string[],
): Promise<string[]> {
  const res = await fetch(`${API}/api/flowchart/${majorCode}/infer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) return [];
  const data = await res.json();
  return data.inferred ?? [];
}

export async function getProfessors(courseNumber: string): Promise<Professor[]> {
  const res = await fetch(`${API}/api/professors/${encodeURIComponent(courseNumber)}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.professors ?? [];
}
