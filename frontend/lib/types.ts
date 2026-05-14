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

export interface MajorOption {
  code: string;
  name: string;
}

export interface TranscriptSession {
  sessionId: string;
  studentName: string;
  major: string;
  completed: string[];
  inProgress: string[];
  coursePositions?: Record<string, CoursePosition>;
  plannedGECourses?: Record<string, string>;
  plannedGEUnits?: Record<string, number>;
}

export interface Professor {
  name: string;
  overall_score: number;
  num_ratings: number;
  polyratings_url: string;
}

export interface GECourse {
  course_number: string;
  title: string;
  units: number;
}

/** Maps GE area ID (e.g. "GE 1A") to list of approved semester course numbers */
export type GEAreaMap = Record<string, string[]>;

export interface CourseInfo {
  course_number: string;
  title: string;
  units: string;
  description: string;
  prerequisites_text?: string;
}

export interface GEArea {
  area_id: string;
  title: string;
  description: string;
  courses: GECourse[];
}

export interface CoursePosition {
  grid_col: number;
  grid_row: number;
}
