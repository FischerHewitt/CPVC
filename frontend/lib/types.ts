export type Category = "major" | "support" | "concentration" | "ge";
export type CustomCourseStatus = "planned" | "completed" | "in_progress";

export interface CustomCourseEntry {
  course_number: string;
  title: string;
  units: number;
  grid_col: number;
  status: CustomCourseStatus;
  assignedToSlotId?: string;
}
export type CourseStatus = "completed" | "inferred" | "in_progress" | "incomplete" | "locked";
export type FreeElectiveStatus = "planned" | "completed" | "in_progress";

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
  is_required?: boolean;
  auto_satisfied_by?: string[];
  elective_key?: string;
  is_placeholder: boolean;
  lab_component?: { course_number: string; lecture_units: number; lab_units: number };
}

export interface ColumnLabel {
  year: string;
  term: string;
}

export interface FlowchartTipSection {
  title: string;
  items: string[];
}

export interface Flowchart {
  major: string;
  code: string;
  total_units: number;
  courses: Course[];
  columns: ColumnLabel[];
  notes?: FlowchartTipSection[];
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
  plannedCourseUnits?: Record<string, number>;
  plannedFreeElectiveCourses?: Record<string, FreeElectiveSelection>;
  customCourses?: Record<string, CustomCourseEntry>;
  concentration?: string;
  notes?: string;
}

export interface FreeElectiveSelection {
  course_number: string;
  title: string;
  units: number;
  status: FreeElectiveStatus;
}

export interface ConcentrationSlotOverride {
  course_number: string;
  title: string;
  units: number;
  prerequisites: string[];
  quarter_equivalents: string[];
  is_placeholder: boolean;
}

export interface Concentration {
  id: string;
  label: string;
  slot_overrides: Record<string, ConcentrationSlotOverride>;
  extra_courses?: Course[];
  tips?: string[];
  full_flowchart_key?: string;
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

export type CourseSearchResult = GECourse;

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

export interface ElectiveArea {
  key: string;
  title: string;
  description: string;
  courses: GECourse[];
}

export interface CoursePosition {
  grid_col: number;
  grid_row: number;
}
