from services.transcript_parser import (
    _parse_lines,
    completed_course_numbers,
    in_progress_course_numbers,
    TranscriptResult,
)


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
