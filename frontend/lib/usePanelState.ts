"use client";

import { useCallback, useRef, useState } from "react";
import type { Course, CourseStatus, CustomCourseEntry } from "@/lib/types";

function isFreeElective(course: Course) {
  return course.title.toLowerCase().includes("free elective") || course.course_number.toLowerCase().startsWith("free");
}

type DragState = { startX: number; startY: number; panelX: number; panelY: number };

export function usePanelState() {
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<CourseStatus | null>(null);
  const [selectedGECourse, setSelectedGECourse] = useState<Course | null>(null);
  const [selectedElectiveCourse, setSelectedElectiveCourse] = useState<Course | null>(null);
  const [selectedFreeElectiveCourse, setSelectedFreeElectiveCourse] = useState<Course | null>(null);

  const [checklistOpen, setChecklistOpen] = useState(false);
  const [tipsOpen, setTipsOpen] = useState(false);
  const [tipsPos, setTipsPos] = useState({ x: 32, y: 120 });
  const tipsDrag = useRef<DragState | null>(null);
  const [myNotesOpen, setMyNotesOpen] = useState(false);
  const [myNotesPos, setMyNotesPos] = useState({ x: 80, y: 160 });
  const myNotesDrag = useRef<DragState | null>(null);
  const [otherCreditsOpen, setOtherCreditsOpen] = useState(false);
  const [otherCreditsPos, setOtherCreditsPos] = useState({ x: 120, y: 180 });
  const otherCreditsDrag = useRef<DragState | null>(null);
  const [courseLookupOpen, setCourseLookupOpen] = useState(false);
  const [courseLookupPos, setCourseLookupPos] = useState({ x: 160, y: 140 });
  const courseLookupDrag = useRef<DragState | null>(null);
  const [courseSearch, setCourseSearch] = useState("");

  const [addCourseCol, setAddCourseCol] = useState<number | null>(null);
  const [addCoursePanelPos, setAddCoursePanelPos] = useState({ x: 60, y: 160 });
  const addCoursePanelDrag = useRef<DragState | null>(null);

  const [editCustomCourse, setEditCustomCourse] = useState<{ id: string; entry: CustomCourseEntry } | null>(null);
  const [editCustomPanelPos, setEditCustomPanelPos] = useState({ x: 60, y: 160 });
  const editCustomPanelDrag = useRef<DragState | null>(null);

  const openCoursePanel = useCallback((course: Course, status: CourseStatus) => {
    if (course.is_placeholder && (course.category === "ge" || course.course_number.startsWith("ART 3000+"))) {
      setSelectedGECourse(course);
      setSelectedCourse(null);
      setSelectedElectiveCourse(null);
      setSelectedFreeElectiveCourse(null);
    } else if (course.is_placeholder && isFreeElective(course)) {
      setSelectedFreeElectiveCourse(course);
      setSelectedCourse(null);
      setSelectedGECourse(null);
      setSelectedElectiveCourse(null);
    } else if (course.is_placeholder) {
      setSelectedElectiveCourse(course);
      setSelectedCourse(null);
      setSelectedGECourse(null);
      setSelectedFreeElectiveCourse(null);
    } else {
      setSelectedCourse(course);
      setSelectedStatus(status);
      setSelectedGECourse(null);
      setSelectedElectiveCourse(null);
      setSelectedFreeElectiveCourse(null);
    }
  }, []);

  return {
    selectedCourse, setSelectedCourse,
    selectedStatus, setSelectedStatus,
    selectedGECourse, setSelectedGECourse,
    selectedElectiveCourse, setSelectedElectiveCourse,
    selectedFreeElectiveCourse, setSelectedFreeElectiveCourse,
    openCoursePanel,
    checklistOpen, setChecklistOpen,
    tipsOpen, setTipsOpen, tipsPos, setTipsPos, tipsDrag,
    myNotesOpen, setMyNotesOpen, myNotesPos, setMyNotesPos, myNotesDrag,
    otherCreditsOpen, setOtherCreditsOpen, otherCreditsPos, setOtherCreditsPos, otherCreditsDrag,
    courseLookupOpen, setCourseLookupOpen, courseLookupPos, setCourseLookupPos, courseLookupDrag,
    courseSearch, setCourseSearch,
    addCourseCol, setAddCourseCol, addCoursePanelPos, setAddCoursePanelPos, addCoursePanelDrag,
    editCustomCourse, setEditCustomCourse, editCustomPanelPos, setEditCustomPanelPos, editCustomPanelDrag,
  };
}
