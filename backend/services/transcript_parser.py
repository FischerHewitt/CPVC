import csv
import io
import re
import pdfplumber
from dataclasses import dataclass, field
from typing import IO


@dataclass
class ParsedCourse:
    course_number: str
    title: str
    attempted: float
    earned: float
    grade: str | None
    term: str
    year: int
    is_quarter: bool


@dataclass
class TranscriptResult:
    student_name: str
    student_id: str
    major: str
    courses: list[ParsedCourse] = field(default_factory=list)


TERM_RE = re.compile(r"(Fall|Winter|Spring|Summer)\s+(Quarter|Semester)\s+(\d{4})")

# Matches: DEPT NUM Title... attempted earned grade? points?
# Works even when the line starts mid-sentence (e.g. left-col text prepended)
COURSE_RE = re.compile(
    r"\b([A-Z]{2,8})\s+(\d{3,4}[A-Z]?)\s+((?:[A-Za-z&/,.\-'() ]+?))\s+"
    r"([\d]+\.[\d]+)\s+([\d]+\.[\d]+)\s*([A-Z][A-Z+\-]*)?\s*([\d]+\.[\d]+)?"
)


def _reconstruct_column_lines(page) -> list[str]:
    """Split a two-column page into two independent line streams."""
    words = page.extract_words(x_tolerance=3, y_tolerance=3)
    if not words:
        return []

    page_mid = page.width / 2

    # Separate words into left and right columns
    left_words  = [w for w in words if w["x0"] < page_mid]
    right_words = [w for w in words if w["x0"] >= page_mid]

    def words_to_lines(wds: list) -> list[str]:
        if not wds:
            return []
        # Group by approximate top (y0), tolerance 3pt
        rows: dict[int, list] = {}
        for w in wds:
            bucket = round(w["top"] / 3) * 3
            rows.setdefault(bucket, []).append(w)
        lines = []
        for _, row_words in sorted(rows.items()):
            row_words.sort(key=lambda w: w["x0"])
            lines.append(" ".join(w["text"] for w in row_words))
        return lines

    return words_to_lines(left_words) + words_to_lines(right_words)


def _parse_lines(lines: list[str]) -> tuple[str, str, str, list[ParsedCourse]]:
    student_name = ""
    student_id = ""
    major = ""
    courses: list[ParsedCourse] = []
    current_term = ""
    current_year = 0
    current_is_quarter = True

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Student name — appears once near top
        if line.startswith("Name:") and not student_name:
            student_name = line.replace("Name:", "").strip()

        # Student ID
        if line.startswith("Student ID:") and not student_id:
            parts = line.split()
            if len(parts) >= 3:
                student_id = parts[2]

        # Major / Plan — first "Plan:" we see
        if line.startswith("Plan:") and not major:
            raw = line.replace("Plan:", "").strip()
            # strip trailing garbage like "Fall 2026 reflect semester..."
            raw = re.split(r"\s{2,}|\d{4}\s+reflect", raw)[0].strip()
            major = raw

        # Term header (may appear anywhere in a line for two-col PDFs)
        for m in TERM_RE.finditer(line):
            season, system, yr = m.groups()
            current_term = f"{season} {system}"
            current_year = int(yr)
            current_is_quarter = system == "Quarter"

        if not current_term:
            continue

        # Find all course patterns in this line
        for m in COURSE_RE.finditer(line):
            dept, num, title, attempted, earned, grade, _points = m.groups()
            # Skip obvious non-course matches (GPA lines, totals)
            if dept in ("GPA", "CPSLO", "QTR", "SEM", "Term", "Cum"):
                continue
            title_clean = title.strip()
            if not title_clean:
                continue
            courses.append(ParsedCourse(
                course_number=f"{dept} {num}",
                title=title_clean,
                attempted=float(attempted),
                earned=float(earned),
                grade=grade.strip() if grade else None,
                term=current_term,
                year=current_year,
                is_quarter=current_is_quarter,
            ))

    return student_name, student_id, major, courses


def parse_transcript(file: IO[bytes]) -> TranscriptResult:
    with pdfplumber.open(file) as pdf:
        all_lines: list[str] = []
        for page in pdf.pages:
            all_lines.extend(_reconstruct_column_lines(page))

    name, sid, major, courses = _parse_lines(all_lines)

    # Deduplicate — same course can appear in both columns on merged lines
    seen: set[tuple] = set()
    unique: list[ParsedCourse] = []
    for c in courses:
        key = (c.course_number, c.term, c.year, c.attempted, c.earned)
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return TranscriptResult(
        student_name=name,
        student_id=sid,
        major=major,
        courses=unique,
    )


_CSV_COMPLETED_STATUSES = {"Taken", "Transferred (Course)", "Transferred (Test)"}
_CSV_IN_PROGRESS_STATUSES = {"In Progress"}


def parse_csv_transcript(file: IO[bytes]) -> TranscriptResult:
    """Parse a Cal Poly course list CSV (Student Center → Academic Process → Course List)."""
    content = file.read().decode("utf-8-sig")  # handle BOM from Excel/browser exports
    reader = csv.DictReader(io.StringIO(content))

    courses: list[ParsedCourse] = []
    for row in reader:
        course_number = row.get("Course", "").strip()
        status = row.get("Status", "").strip()
        term = row.get("Term", "").strip()
        grade = row.get("Grade", "").strip() or None
        try:
            units = float(row.get("Units", "0").strip())
        except ValueError:
            units = 0.0

        if not course_number or status not in (_CSV_COMPLETED_STATUSES | _CSV_IN_PROGRESS_STATUSES):
            continue

        m = TERM_RE.search(term)
        if m:
            season, system, yr = m.groups()
            parsed_term = f"{season} {system}"
            year = int(yr)
            is_quarter = system == "Quarter"
        else:
            parsed_term = term
            year = 0
            is_quarter = True

        earned = units if status in _CSV_COMPLETED_STATUSES else 0.0
        courses.append(ParsedCourse(
            course_number=course_number,
            title=row.get("Description", "").strip(),
            attempted=units,
            earned=earned,
            grade=grade,
            term=parsed_term,
            year=year,
            is_quarter=is_quarter,
        ))

    return TranscriptResult(student_name="", student_id="", major="", courses=courses)


def completed_course_numbers(result: TranscriptResult) -> set[str]:
    return {
        c.course_number
        for c in result.courses
        if c.earned > 0 and c.grade not in ("W", "F", "NC", "U")
    }


def in_progress_course_numbers(result: TranscriptResult) -> set[str]:
    completed = completed_course_numbers(result)
    return {
        c.course_number
        for c in result.courses
        if c.earned == 0 and c.attempted > 0 and c.course_number not in completed
    }
