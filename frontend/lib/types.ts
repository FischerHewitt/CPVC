export type Category = "major" | "support" | "concentration" | "ge";
export type CourseStatus = "completed" | "inferred" | "in_progress" | "incomplete" | "locked";

export interface Course {
  id: string;
  course_number: string;
  title: string;
  units: number;
  category: Category;
  grid_col: number;
  grid_row: number;
  prerequisites: string[];
  quarter_equivalents: string[];
  is_placeholder: boolean;
}

export interface ColumnLabel {
  year: string;
  term: string;
}

export interface Flowchart {
  major: string;
  code: string;
  total_units: number;
  courses: Course[];
  columns: ColumnLabel[];
}

export interface TranscriptSession {
  sessionId: string;
  studentName: string;
  major: string;
  completed: string[];
  inProgress: string[];
}

export interface Professor {
  name: string;
  overall_score: number;
  num_ratings: number;
  polyratings_url: string;
}
