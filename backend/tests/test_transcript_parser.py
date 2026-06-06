import io

from services.transcript_parser import (
    _parse_lines,
    completed_course_numbers,
    in_progress_course_numbers,
    parse_csv_transcript,
    TranscriptResult,
)


STUDENT_CENTER_CSV = """Course,Description,Term,Grade,Units,Status,Status Note
"AUTO 1TR","Auto Transfer Lower Division","Fall Quarter 2025","A","3","Transferred (Course)",""
"B3GE 1TR","Laboratory Activity","Fall Quarter 2025","CR","1","Transferred (Test)",""
"BIO 111","General Biology","Winter Quarter 2026","A","4","Taken",""
"COMS 101","Public Speaking","Fall Quarter 2025","A","4","Taken",""
"COMS 126","Argument and Advocacy","Spring Quarter 2026","-","4","In Progress",""
"CPE 225","Intro to Computer Organization","Spring Quarter 2026","-","4","In Progress",""
"CSC 101","Fundamentals of Computer Sci","Fall Quarter 2025","A","4","Taken",""
"CSC 203","Proj-Based OO Prog and Design","Spring Quarter 2026","-","4","In Progress",""
"CSC 3665","Intro to DataBse Mngmnt Systms","Fall Semester 2027","-","4","Planned",""
"ES 1112","Race Culture & Politics in US","Fall Semester 2026","-","3","In Progress",""
"HIST 2202","U.S. History Since 1877","Fall Semester 2026","-","3","In Progress",""
"MATH 141","Calculus I","Fall Quarter 2025","CR","4","Transferred (Test)",""
"MATH 2031","Transition to Advanced Math","Fall Semester 2026","-","3","In Progress",""
"MU 173","Wind Ensemble","Spring Quarter 2026","-","1","In Progress",""
"MU 173","Wind Ensemble","Winter Quarter 2026","A","1","Taken",""
"STAT 3210","Engineering Statistics","Fall Semester 2026","-","3","In Progress",""
"""


def test_parse_lines_extracts_student_metadata_and_courses():
    lines = [
        "Name: Ada Lovelace",
        "Student ID: 123456789",
        "Plan: Computer Science BS",
        "Fall Quarter 2025",
        "CSC 101 Fundamentals of Computer Science 4.00 4.00 A 16.00",
        "MATH 141 Calculus I 4.00 4.00 B+ 13.20",
        "Winter Quarter 2026",
        "CSC 202 Data Structures 4.00 0.00 IP",
    ]

    name, student_id, major, courses = _parse_lines(lines)

    assert name == "Ada Lovelace"
    assert student_id == "123456789"
    assert major == "Computer Science BS"
    assert [course.course_number for course in courses] == ["CSC 101", "MATH 141", "CSC 202"]
    assert courses[0].term == "Fall Quarter"
    assert courses[0].year == 2025
    assert courses[2].grade == "IP"
    assert courses[2].earned == 0


def test_completed_and_in_progress_course_numbers_filter_grades():
    _, _, _, courses = _parse_lines(
        [
            "Name: Ada Lovelace",
            "Student ID: 123456789",
            "Plan: Computer Science BS",
            "Fall Quarter 2025",
            "CSC 101 Fundamentals of Computer Science 4.00 4.00 A 16.00",
            "MATH 141 Calculus I 4.00 0.00 IP",
            "ENGL 134 Writing and Rhetoric 4.00 0.00 W",
            "PHYS 141 General Physics 4.00 0.00 F",
        ]
    )
    result = TranscriptResult(
        student_name="Ada Lovelace",
        student_id="123456789",
        major="Computer Science BS",
        courses=courses,
    )

    assert completed_course_numbers(result) == {"CSC 101"}
    assert in_progress_course_numbers(result) == {"MATH 141", "ENGL 134", "PHYS 141"}


def test_completed_course_with_no_grade_is_not_dropped():
    """A PDF line where the grade token is missing but units were earned (e.g. grade=None)
    must land in completed, not be silently dropped."""
    _, _, _, courses = _parse_lines(
        [
            "Name: Ada Lovelace",
            "Student ID: 123456789",
            "Plan: Computer Science BS",
            "Fall Quarter 2025",
            # Grade column absent — regex captures grade=None, but earned=4.0
            "MATH 141 Calculus I 4.00 4.00 16.00",
            # Normal case for comparison
            "CSC 101 Fundamentals of Computer Science 4.00 4.00 A 16.00",
        ]
    )
    result = TranscriptResult(
        student_name="Ada Lovelace",
        student_id="123456789",
        major="Computer Science BS",
        courses=courses,
    )

    math_course = next(c for c in courses if c.course_number == "MATH 141")
    assert math_course.grade is None
    assert math_course.earned == 4.0

    assert "MATH 141" in completed_course_numbers(result)
    assert "MATH 141" not in in_progress_course_numbers(result)


def test_in_progress_course_with_no_grade_stays_in_progress():
    """A course with grade=None and earned=0 must land in in_progress, not be dropped."""
    _, _, _, courses = _parse_lines(
        [
            "Name: Ada Lovelace",
            "Student ID: 123456789",
            "Plan: Computer Science BS",
            "Spring Semester 2026",
            # In-progress: attempted=4, earned=0, no grade captured
            "CSC 203 Proj-Based OO Prog and Design 4.00 0.00",
        ]
    )
    result = TranscriptResult(
        student_name="Ada Lovelace",
        student_id="123456789",
        major="Computer Science BS",
        courses=courses,
    )

    csc_course = next(c for c in courses if c.course_number == "CSC 203")
    assert csc_course.grade is None
    assert csc_course.earned == 0.0

    assert "CSC 203" not in completed_course_numbers(result)
    assert "CSC 203" in in_progress_course_numbers(result)


def test_parse_csv_transcript_reads_student_center_course_list():
    result = parse_csv_transcript(io.BytesIO(STUDENT_CENTER_CSV.encode("utf-8")))

    assert [course.course_number for course in result.courses] == [
        "AUTO 1TR",
        "B3GE 1TR",
        "BIO 111",
        "COMS 101",
        "COMS 126",
        "CPE 225",
        "CSC 101",
        "CSC 203",
        "ES 1112",
        "HIST 2202",
        "MATH 141",
        "MATH 2031",
        "MU 173",
        "MU 173",
        "STAT 3210",
    ]
    assert {course.course_number for course in result.courses if course.term == "Fall Semester"} == {
        "ES 1112",
        "HIST 2202",
        "MATH 2031",
        "STAT 3210",
    }
    assert completed_course_numbers(result) == {
        "AUTO 1TR",
        "B3GE 1TR",
        "BIO 111",
        "COMS 101",
        "CSC 101",
        "MATH 141",
        "MU 173",
    }
    assert in_progress_course_numbers(result) == {
        "COMS 126",
        "CPE 225",
        "CSC 203",
        "ES 1112",
        "HIST 2202",
        "MATH 2031",
        "STAT 3210",
    }


def test_parse_csv_transcript_handles_bom_and_crlf_exports():
    csv_text = (
        "\ufeffCourse,Description,Term,Grade,Units,Status,Status Note\r\n"
        '"COMS 126","Argument and Advocacy","Spring Quarter 2026","-","4","In Progress",""\r\n'
        '"CSC 101","Fundamentals of Computer Sci","Fall Quarter 2025","A","4","Taken",""\r\n'
    )
    result = parse_csv_transcript(io.BytesIO(csv_text.encode("utf-8")))

    assert completed_course_numbers(result) == {"CSC 101"}
    assert in_progress_course_numbers(result) == {"COMS 126"}
