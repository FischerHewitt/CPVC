#!/usr/bin/env python3
"""
Parse FlowchartPdf/General Curriculum in Computer Science.txt into an
intermediate JSON for the flowchart migration.

Usage (from repo root):
    python3 backend/scripts/parse_flowchart_txt.py

Output:
    FlowchartPdf/parsed_flowcharts.json  — one entry per concentration grid
    FlowchartPdf/parse_warnings.txt      — anything that looked ambiguous
"""

import re
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TXT_PATH = REPO_ROOT / "FlowchartPdf" / "General Curriculum in Computer Science.txt"
OUTPUT_PATH = REPO_ROOT / "FlowchartPdf" / "parsed_flowcharts.json"
WARNINGS_PATH = REPO_ROOT / "FlowchartPdf" / "parse_warnings.txt"

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Matches full section-header lines: "Accounting Concentration - BS in Business Administration"
SECTION_HEADER_RE = re.compile(r"^(.+) - (BS|BA|BFA) in (.+)$")

YEAR_NAMES = {"First": 1, "Second": 2, "Third": 3, "Fourth": 4, "Fifth": 5}
YEAR_RE = re.compile(r"^(First|Second|Third|Fourth|Fifth) Year$")

TERM_RE = re.compile(r"^Term (\d+)$")
TOTAL_UNITS_RE = re.compile(r"^Total Units$")
UNITS_HEADER_RE = re.compile(r"^Units$")

# A units value: standalone integer or range like "3-4", "0-3", "2-8"
UNITS_VALUE_RE = re.compile(r"^(\d+)(-\d+)?$")

# Course-number line: dept prefix(es) + 4-digit number, e.g. "CSC 1000", "CSC/CPE 1000",
# "BIO/ASCI 1101", "CSC 1001 & 1001L" (lab suffix handled separately)
COURSE_NUM_RE = re.compile(
    r"^([A-Z]{2,6}(?:/[A-Z]{2,6})?\s+\d{4}[A-Z]?)"  # primary
    r"(\s+&\s+\d+[A-Z]+)?$"                            # optional inline lab suffix
)

# Footnote reference numbers embedded in a title: trailing " 1" or " 1, 2" etc.
# We strip them but record them.
FOOTNOTE_REFS_RE = re.compile(r"\s+(\d+(?:,\s*\d+)*)$")

# Boilerplate lines to skip
BOILERPLATE_PREFIXES = (
    "Suggested Four-Year",
    "Courses may be completed",
)


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def strip_tab(line: str) -> str:
    return line[1:] if line.startswith("\t") else line


def is_tabbed(line: str) -> bool:
    return line.startswith("\t")


def is_blank_separator(line: str) -> bool:
    return line.rstrip("\n") in ("\t ", "\t", "")


def is_boilerplate(line: str) -> bool:
    s = line.strip()
    return any(s.startswith(p) for p in BOILERPLATE_PREFIXES)


def extract_footnote_refs(text: str) -> tuple[str, list[str]]:
    """Strip trailing footnote numbers from a title and return (clean_title, refs)."""
    m = FOOTNOTE_REFS_RE.search(text)
    if m:
        refs = [r.strip() for r in m.group(1).split(",")]
        return text[: m.start()].strip(), refs
    return text, []


def parse_units(raw: str) -> tuple[int, str]:
    """Return (min_units: int, display: str) from '3' or '3-4'."""
    m = UNITS_VALUE_RE.match(raw)
    if not m:
        raise ValueError(f"Not a units value: {raw!r}")
    display = raw
    min_units = int(m.group(1))
    return min_units, display


def is_course_number(text: str) -> bool:
    return bool(COURSE_NUM_RE.match(text))


def is_ge_placeholder(text: str) -> bool:
    return text.startswith("General Education Requirement")


def is_placeholder_description(text: str) -> bool:
    """Lines that serve as both course_number and title (no separate title line follows)."""
    keywords = (
        "General Education Requirement",
        "Elective",
        "Course",          # "Technology Management Course", "Senior Project Course"
        "Senior Project",
        "Free Elective",
        "Concentration",
        "Internship",
    )
    return any(text.startswith(k) for k in keywords) and not is_course_number(text)


# ---------------------------------------------------------------------------
# Entry-level parser: turn a list of raw content strings into a course dict
# ---------------------------------------------------------------------------

def parse_entry(raw_lines: list[str], section_title: str, warnings: list[str]) -> dict:
    """
    raw_lines: content lines for one course entry, WITHOUT the leading tab
               and WITHOUT the units-value line (that was already consumed).
               Continuation lines ("or X", "& X", "and X") are included as-is.
    Returns a course dict.
    """
    # Separate tabbed lines vs. continuation lines
    primary_lines = []   # lines that originally had a leading tab
    cont_lines = []      # "or X", "& X", "and X" style lines

    for line in raw_lines:
        s = line.strip()
        if s.startswith("or ") or s.startswith("& ") or s.startswith("and "):
            cont_lines.append(s)
        else:
            primary_lines.append(s)

    course_number = ""
    title = ""
    footnote_refs: list[str] = []
    or_alternatives: list[str] = []  # alternative course numbers
    is_placeholder = False

    if not primary_lines:
        warnings.append(f"[{section_title}] Entry with no primary lines: {raw_lines!r}")
        return {}

    first = primary_lines[0]

    if is_course_number(first):
        course_number = first
        # Gather "or" and "&" continuations on the course-number
        for c in cont_lines:
            if c.startswith("or "):
                alt = c[3:].strip()
                if is_course_number(alt):
                    or_alternatives.append(alt)
            elif c.startswith("& "):
                # Lab companion: fold into course_number
                course_number = f"{course_number} & {c[2:].strip()}"
        # Title is the second primary line (if present)
        if len(primary_lines) >= 2:
            raw_title = primary_lines[1]
            # Gather "and" continuations into title
            for c in cont_lines:
                if c.startswith("and "):
                    raw_title = f"{raw_title} and {c[4:].strip()}"
                elif c.startswith("or ") and not is_course_number(c[3:].strip()):
                    raw_title = f"{raw_title} or {c[3:].strip()}"
            title, footnote_refs = extract_footnote_refs(raw_title)
        elif primary_lines:
            title = first  # fallback: use course number as title
    else:
        # Placeholder: first line is both the description and the course_number placeholder
        is_placeholder = True
        raw_description = first
        for c in cont_lines:
            if c.startswith("or "):
                raw_description = f"{raw_description} or {c[3:].strip()}"
        title, footnote_refs = extract_footnote_refs(raw_description)
        course_number = title  # will be overridden in the merge step

    # Build combined course_number for slash-choices
    if or_alternatives:
        # e.g. "MATH 1261" + ["MATH 1264"] → "MATH 1261/MATH 1264"
        course_number = "/".join([course_number] + or_alternatives)
        is_placeholder = True  # slash-choice = user picks one

    return {
        "course_number": course_number,
        "title": title,
        "is_placeholder": is_placeholder,
        "footnote_refs": footnote_refs,
    }


# ---------------------------------------------------------------------------
# Term-level parser
# ---------------------------------------------------------------------------

def parse_term_courses(
    term_lines: list[str],
    section_title: str,
    warnings: list[str],
) -> list[dict]:
    """
    term_lines: raw lines belonging to one term block (still with leading tabs
                where present), EXCLUDING the "Term N" header line itself.
    Returns a list of course entry dicts, each with an added 'units' / 'units_display'.
    """
    courses = []
    current_entry_lines: list[str] = []
    skip_next_number = False  # True right after we see a bare "Units" header line

    i = 0
    while i < len(term_lines):
        raw = term_lines[i]
        stripped = raw.rstrip("\n")

        if is_blank_separator(stripped):
            i += 1
            continue

        content = strip_tab(stripped).strip()

        # "Units" appears twice per term:
        #   1. Column header at the start (next non-blank line is a course, not a number)
        #   2. Term-total marker at the end (next non-blank line IS a number)
        # Only skip the following line when it is actually a number (case 2).
        if UNITS_HEADER_RE.match(content):
            # Peek ahead to the next non-blank line
            j = i
            while j < len(term_lines):
                peek = strip_tab(term_lines[j].rstrip("\n")).strip()
                if peek and not is_blank_separator(term_lines[j].rstrip("\n")):
                    break
                j += 1
            if j < len(term_lines) and UNITS_VALUE_RE.match(peek):
                skip_next_number = True
            i += 1
            continue

        if skip_next_number and UNITS_VALUE_RE.match(content):
            skip_next_number = False
            i += 1
            continue

        # Year sub-header inside a term block (shouldn't happen, but guard)
        if YEAR_RE.match(content):
            i += 1
            continue

        # Units value — ends the current entry
        if UNITS_VALUE_RE.match(content):
            if current_entry_lines:
                entry = parse_entry(current_entry_lines, section_title, warnings)
                if entry:
                    min_u, disp = parse_units(content)
                    entry["units"] = min_u
                    entry["units_display"] = disp
                    courses.append(entry)
            current_entry_lines = []
            i += 1
            continue

        # Everything else belongs to the current entry
        current_entry_lines.append(stripped)
        i += 1

    if current_entry_lines:
        warnings.append(
            f"[{section_title}] Leftover entry lines with no units: {current_entry_lines!r}"
        )

    return courses


# ---------------------------------------------------------------------------
# Section parser
# ---------------------------------------------------------------------------

def parse_section(section_lines: list[str], warnings: list[str]) -> dict | None:
    """
    section_lines: all raw lines belonging to one flowchart grid section,
                   starting with the section header line.
    """
    # First line is always the section header
    header_line = section_lines[0].strip()
    m = SECTION_HEADER_RE.match(header_line)
    if not m:
        warnings.append(f"Could not parse section header: {header_line!r}")
        return None

    concentration_label = m.group(1).strip()
    degree = m.group(2).strip()
    major_name = m.group(3).strip()

    terms: list[dict] = []
    footnotes: dict[str, str] = {}
    total_units: int = 0

    current_year = 0
    current_term_num = 0
    current_term_lines: list[str] = []
    in_footnotes = False
    pending_footnote_key: str | None = None

    def flush_term():
        nonlocal current_term_lines
        if current_term_lines and current_year > 0 and current_term_num > 0:
            grid_col = (current_year - 1) * 2 + (current_term_num - 1)
            courses = parse_term_courses(current_term_lines, header_line, warnings)
            terms.append({
                "year": current_year,
                "term": current_term_num,
                "grid_col": grid_col,
                "courses": courses,
            })
        current_term_lines = []

    i = 1  # skip header line
    while i < len(section_lines):
        raw = section_lines[i]
        stripped_raw = raw.rstrip("\n")
        content = stripped_raw.strip()
        tabbed = stripped_raw.startswith("\t")
        i += 1

        if not content:
            continue

        if is_boilerplate(content):
            continue

        # Once we've seen "Total Units", everything is footnotes
        if TOTAL_UNITS_RE.match(content):
            flush_term()
            in_footnotes = True
            # Next non-blank tabbed line is the total units number
            continue

        if in_footnotes:
            # Total-units number (first thing after "Total Units")
            if UNITS_VALUE_RE.match(content) and total_units == 0:
                total_units = int(content.split("-")[0])
                continue
            # Footnote key: a standalone digit (with or without leading tab)
            if re.match(r"^\d+$", content):
                pending_footnote_key = content
                continue
            # Footnote text follows
            if pending_footnote_key:
                existing = footnotes.get(pending_footnote_key, "")
                footnotes[pending_footnote_key] = (existing + " " + content).strip()
                pending_footnote_key = None
            continue

        # Year header (with or without leading tab)
        if YEAR_RE.match(content):
            flush_term()
            current_year = YEAR_NAMES[content.split()[0]]
            current_term_num = 0
            continue

        # Term header
        if TERM_RE.match(content):
            flush_term()
            current_term_num = int(TERM_RE.match(content).group(1))
            continue

        # Anything else belongs to the current term
        current_term_lines.append(stripped_raw)

    flush_term()

    return {
        "section_title": header_line,
        "concentration_label": concentration_label,
        "degree": degree,
        "major_name": major_name,
        "total_units": total_units,
        "terms": terms,
        "footnotes": footnotes,
    }


# ---------------------------------------------------------------------------
# Top-level: split file into sections and parse each
# ---------------------------------------------------------------------------

def split_into_sections(lines: list[str]) -> list[list[str]]:
    """Split file lines into per-section groups by section header lines."""
    section_starts: list[int] = []
    for idx, line in enumerate(lines):
        s = line.strip()
        if (
            SECTION_HEADER_RE.match(s)
            and not s.startswith("or ")
            and not s.startswith("and ")
            and not line.startswith("\t")
        ):
            section_starts.append(idx)

    sections = []
    for j, start in enumerate(section_starts):
        end = section_starts[j + 1] if j + 1 < len(section_starts) else len(lines)
        sections.append(lines[start:end])
    return sections


def main() -> None:
    if not TXT_PATH.exists():
        print(f"ERROR: {TXT_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(TXT_PATH, encoding="utf-8-sig") as f:
        lines = f.readlines()

    print(f"Read {len(lines)} lines from {TXT_PATH.name}")

    sections = split_into_sections(lines)
    print(f"Found {len(sections)} sections")

    warnings: list[str] = []
    results: list[dict] = []

    for section_lines in sections:
        result = parse_section(section_lines, warnings)
        if result:
            results.append(result)

    # Summary stats
    total_courses = sum(
        len(t["courses"]) for r in results for t in r["terms"]
    )
    print(f"Parsed {len(results)} flowcharts, {total_courses} course entries total")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")

    if warnings:
        with open(WARNINGS_PATH, "w") as f:
            f.write("\n".join(warnings) + "\n")
        print(f"Wrote {len(warnings)} warnings to {WARNINGS_PATH}")
    else:
        print("No warnings.")


if __name__ == "__main__":
    main()
