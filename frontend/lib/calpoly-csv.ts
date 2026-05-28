export interface CalPolyCSVResult {
  completed: string[];
  inProgress: string[];
}

const COMPLETED_STATUSES = new Set(["Taken", "Transferred (Course)", "Transferred (Test)"]);
const IN_PROGRESS_STATUSES = new Set(["In Progress"]);

function uniqueCourseNumbers(courseNumbers: string[]): string[] {
  const seen = new Set<string>();
  const result: string[] = [];
  for (const courseNumber of courseNumbers) {
    const normalized = courseNumber.toUpperCase().trim().replace(/\s+/g, " ");
    if (seen.has(normalized)) continue;
    seen.add(normalized);
    result.push(courseNumber);
  }
  return result;
}

export function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const next = line[i + 1];

    if (char === '"' && inQuotes && next === '"') {
      current += '"';
      i++;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      result.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }

  result.push(current.trim());
  return result;
}

export function parseCalPolyCSV(text: string): CalPolyCSVResult | null {
  const lines = text.replace(/^\uFEFF/, "").trim().split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return null;

  const header = parseCSVLine(lines[0]);
  const courseIdx = header.findIndex((h) => h.toLowerCase() === "course");
  const statusIdx = header.findIndex((h) => h.toLowerCase() === "status");
  if (courseIdx === -1 || statusIdx === -1) return null;

  const completed: string[] = [];
  const inProgress: string[] = [];

  for (let i = 1; i < lines.length; i++) {
    const cols = parseCSVLine(lines[i]);
    const course = cols[courseIdx]?.trim();
    const status = cols[statusIdx]?.trim();
    if (!course || !status) continue;

    if (COMPLETED_STATUSES.has(status)) {
      completed.push(course);
    } else if (IN_PROGRESS_STATUSES.has(status)) {
      inProgress.push(course);
    }
  }

  const uniqueCompleted = uniqueCourseNumbers(completed);
  const completedSet = new Set(uniqueCompleted.map((course) => course.toUpperCase()));
  return {
    completed: uniqueCompleted,
    inProgress: uniqueCourseNumbers(inProgress).filter((course) => !completedSet.has(course.toUpperCase())),
  };
}
