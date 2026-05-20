export type FileType = "pdf" | "csv" | "mbp";

export function getFileType(filename: string): FileType | null {
  if (filename.endsWith(".pdf")) return "pdf";
  if (filename.endsWith(".csv")) return "csv";
  if (filename.endsWith(".mbp")) return "mbp";
  return null;
}

export function validateFile(filename: string): string | null {
  if (getFileType(filename) === null)
    return "Please upload a PDF transcript, CSV course list, or .mbp flowchart file.";
  return null;
}

export function getProgressLabel(progress: number): string {
  if (progress >= 95) return "Opening flowchart";
  if (progress >= 70) return "Creating flowchart";
  if (progress >= 35) return "Matching completed courses";
  return "Reading transcript";
}
