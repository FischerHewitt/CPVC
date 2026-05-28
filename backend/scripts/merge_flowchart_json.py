#!/usr/bin/env python3
"""
Merge parsed_flowcharts.json onto existing FLOWCHARTS entries.

For each parsed concentration section:
  - Matches to an existing FLOWCHARTS entry by major code + concentration label
  - Preserves prerequisites, quarter_equivalents, elective_key from current entry
  - Generates IDs for concentration-unique courses (SLUG_COURSENUMBER)
  - For already-built concentrations: diffs parsed vs existing (validation)
  - For base sections (Concentration Not Yet Declared): diffs vs base FLOWCHARTS entry

Usage (from repo root):
    python3 backend/scripts/merge_flowchart_json.py

Outputs:
    FlowchartPdf/merged_concentration_entries.json  — new/updated entries to review
    FlowchartPdf/base_major_diffs.json              — diffs for base major updates
    FlowchartPdf/merge_report.txt                   — human-readable summary
"""

import re
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "backend"))

from data.flowcharts import FLOWCHARTS
from data.concentrations import CONCENTRATIONS

PARSED_PATH = REPO_ROOT / "FlowchartPdf" / "parsed_flowcharts.json"
MERGED_CONC_OUT = REPO_ROOT / "FlowchartPdf" / "merged_concentration_entries.json"
BASE_DIFFS_OUT = REPO_ROOT / "FlowchartPdf" / "base_major_diffs.json"
REPORT_OUT = REPO_ROOT / "FlowchartPdf" / "merge_report.txt"

# ---------------------------------------------------------------------------
# Major name → app code mappings
# ---------------------------------------------------------------------------

# PDF section major_name values that differ from FLOWCHARTS[code]["major"]
PDF_NAME_OVERRIDES: dict[str, str] = {
    "Mechanical Engineering (San Luis Obispo Campus)": "ME",
    "Food Science": "FSN",
    "Forest and Fire Sciences": "NR",
}

# PDF major names with no app entry — skip silently (documented in missing-majors.md)
SKIP_MAJOR_NAMES: set[str] = {
    "Facilities Engineering Technology",
    "Marine Engineering Technology",
    "Marine Transportation",
    "Plant Science",
}


def build_major_name_to_code() -> dict[str, str]:
    """Map PDF major_name → app FLOWCHARTS base code, excluding concentration keys."""
    conc_keys = {
        c["full_flowchart_key"]
        for concs in CONCENTRATIONS.values()
        for c in concs
        if "full_flowchart_key" in c
    }
    mapping: dict[str, str] = {}
    for code, fc in FLOWCHARTS.items():
        if code not in conc_keys:
            mapping[fc["major"]] = code
    for pdf_name, code in PDF_NAME_OVERRIDES.items():
        mapping[pdf_name] = code
    return mapping


# ---------------------------------------------------------------------------
# Base section detection
# ---------------------------------------------------------------------------

def is_base_label(label: str) -> bool:
    """True if this is the base/general curriculum section, not a specific concentration."""
    return (
        label == "Concentration Not Yet Declared"
        or label.startswith("General Curriculum")
    )


# ---------------------------------------------------------------------------
# Concentration label normalization and matching
# ---------------------------------------------------------------------------

def normalize_label(label: str) -> str:
    """Normalize a concentration label for fuzzy matching."""
    # Strip trailing " Concentration" (also handles "Concentration in")
    s = re.sub(r"\s+[Cc]oncentration(\s+in)?$", "", label).strip()
    # Strip any remaining trailing " in" artifact
    s = re.sub(r"\s+in$", "", s).strip()
    # Strip non-ASCII characters (®, ™, etc.)
    s = re.sub(r"[^\x00-\x7f]", "", s).strip()
    # Normalize all "&" variants (including "HVAC & R", "HVAC&R") to "and"
    s = re.sub(r"\s*&\s*", " and ", s)
    # Collapse multiple spaces
    s = re.sub(r"\s+", " ", s).strip()
    return s.lower()


# Manual overrides for label mismatches that can't be resolved by normalization alone.
# (major_code, normalized_pdf_label) → final FLOWCHARTS key to use
LABEL_KEY_OVERRIDES: dict[tuple[str, str], str] = {
    # "AI & Machine Learning" (app) vs "Artificial Intelligence and Machine Learning" (PDF)
    ("CS", "artificial intelligence and machine learning"): "CS_AIML",
    # ME: "HVAC & R" (PDF, all & normalized to " and ") vs "HVAC&R" (app)
    ("ME", "sustainable technology for the built environment (hvac and r)"): "ME_HVACR",
    # BMED: "Cell Therapy" (PDF, old name) → "Cell and Tissue Engineering" (app, new name)
    ("BMED", "cell therapy"): "BMED_CELL_AND_TISSUE_ENGINEERING",
    # ECON: PDF typo "Consumer Packing" → app "Consumer Packaging"
    ("ECON", "consumer packing"): "ECON_CONSUMER_PACKAGING",
    # LAES: "Computer Science Concentration" (PDF) → "Computer Science (Engineering)" (app)
    ("LAES", "computer science"): "LAES_COMPUTER_SCIENCE",
    ("LAES", "electrical engineering"): "LAES_ELECTRICAL_ENGINEERING",
    ("LAES", "industrial engineering"): "LAES_INDUSTRIAL_ENGINEERING",
    ("LAES", "engineering individualized course of study"): "LAES_ENGINEERING_INDIVIDUALIZED_COURSE_OF_STUDY",
}

# (major_code, normalized_pdf_label) → app concentration_id to find the entry in CONCENTRATIONS
# Required when the app's concentration label doesn't fuzzy-match the PDF label.
LABEL_CONC_ID_OVERRIDES: dict[tuple[str, str], str] = {
    ("CS", "artificial intelligence and machine learning"): "ai_ml",
    ("ME", "sustainable technology for the built environment (hvac and r)"): "hvacr",
    ("BMED", "cell therapy"): "cell_and_tissue_engineering",
    ("ECON", "consumer packing"): "consumer_packaging",
    ("LAES", "computer science"): "computer_science",
    ("LAES", "electrical engineering"): "electrical_engineering",
    ("LAES", "industrial engineering"): "industrial_engineering",
    ("LAES", "engineering individualized course of study"): "engineering_ics",
}


def find_concentration_entry(major_code: str, parsed_label: str) -> dict | None:
    """Find the matching entry in CONCENTRATIONS[major_code] for a parsed label."""
    concs = CONCENTRATIONS.get(major_code, [])
    parsed_norm = normalize_label(parsed_label)

    # 0a. Manual override: look up the concentration by its known id
    override_conc_id = LABEL_CONC_ID_OVERRIDES.get((major_code, parsed_norm))
    if override_conc_id:
        for c in concs:
            if c.get("id") == override_conc_id:
                return c

    # 0b. Manual override: look up by existing full_flowchart_key (for already-built entries)
    override_key = LABEL_KEY_OVERRIDES.get((major_code, parsed_norm))
    if override_key:
        for c in concs:
            if c.get("full_flowchart_key") == override_key:
                return c

    # 1. Exact label match
    for c in concs:
        if c["label"].lower() == parsed_label.lower():
            return c

    # 2. Normalized match (strip " Concentration", unify &/and, strip non-ASCII)
    for c in concs:
        if normalize_label(c["label"]) == parsed_norm:
            return c

    # 3. Substring match (parsed normalized label contained in app label)
    for c in concs:
        if parsed_norm in normalize_label(c["label"]):
            return c

    # 4. App label contained in parsed normalized label
    for c in concs:
        app_norm = normalize_label(c["label"])
        if app_norm and app_norm in parsed_norm:
            return c

    return None


# ---------------------------------------------------------------------------
# Slug and ID generation
# ---------------------------------------------------------------------------

def build_slug(concentration_label: str) -> str:
    """Convert concentration label to uppercase slug for use in flowchart keys and IDs."""
    # Strip trailing " Concentration"
    slug = re.sub(r"\s+[Cc]oncentration$", "", concentration_label).strip()
    # Uppercase, replace non-alphanumeric runs with underscores
    slug = re.sub(r"[^A-Z0-9]+", "_", slug.upper()).strip("_")
    return slug


def clean_id_part(course_number: str) -> str:
    """Convert a course number to a safe ID suffix (no spaces/slashes/special chars)."""
    return re.sub(r"[^A-Z0-9]+", "_", course_number.upper()).strip("_")


def make_flowchart_key(major_code: str, concentration_label: str, existing_key: str | None) -> str:
    if existing_key:
        return existing_key
    slug = build_slug(concentration_label)
    return f"{major_code}_{slug}"


# ---------------------------------------------------------------------------
# Course lookup helpers
# ---------------------------------------------------------------------------

# GE placeholder course_number patterns from the PDF → app course_number format
# e.g. "General Education Requirement (1A)" → "GE 1A"
GE_AREA_RE = re.compile(r"^General Education Requirement\s*\(([^)]+)\)$")
GE_UPPER_DIV_RE = re.compile(r"^General Education Requirement\s*\(Upper-?Division\s+([^)]+)\)$", re.IGNORECASE)


def normalize_pdf_course_number(cn: str) -> str:
    """
    Normalize a PDF-parsed course_number to the format used in our FLOWCHARTS entries.

    Key transforms:
    - "General Education Requirement (1A)" → "GE 1A"
    - "General Education Requirement (Upper-Division 4)" → "GE UD-4"
    - "CSC 1001 & 1001L" → "CSC 1001"  (strip inline lab suffix)
    - "MATH 1261/MATH 1264" → "MATH 1261/1264"  (remove repeated dept prefix)
    - "CPE/CSC 1000" → sorted dept order to match existing flowchart convention
    """
    # GE upper-division placeholder
    m = GE_UPPER_DIV_RE.match(cn)
    if m:
        return f"GE UD-{m.group(1)}"

    # GE area placeholder
    m = GE_AREA_RE.match(cn)
    if m:
        return f"GE {m.group(1)}"

    # Strip inline lab suffix: "CSC 1001 & 1001L" → "CSC 1001"
    cn = re.sub(r"\s+&\s+\d+[A-Z]+$", "", cn).strip()

    # Normalize repeated-dept slash choices: "MATH 1261/MATH 1264" → "MATH 1261/1264"
    # Pattern: "DEPT NNNN/DEPT NNNN" or "DEPT/DEPT NNNN/DEPT NNNN"
    def _collapse_slash(s: str) -> str:
        parts = s.split("/")
        if len(parts) < 2:
            return s
        # Extract leading dept from first part
        m0 = re.match(r"^([A-Z]{2,6}(?:/[A-Z]{2,6})?)\s+(\d{4}[A-Z]?)$", parts[0])
        if not m0:
            return s
        lead_dept, first_num = m0.group(1), m0.group(2)
        condensed = [f"{lead_dept} {first_num}"]
        for part in parts[1:]:
            mp = re.match(r"^([A-Z]{2,6})\s+(\d{4}[A-Z]?)$", part)
            if mp:
                dept2, num2 = mp.group(1), mp.group(2)
                if dept2 == lead_dept:
                    condensed.append(num2)  # drop dept, keep number only
                else:
                    condensed.append(f"{dept2} {num2}")
            else:
                condensed.append(part)
        return "/".join(condensed)

    cn = _collapse_slash(cn)
    return cn


def course_lookup(courses: list[dict]) -> dict[str, dict]:
    """Build {course_number: course_dict} from a list of course dicts."""
    return {c["course_number"]: c for c in courses}


def course_lookup_with_normalized_keys(courses: list[dict]) -> dict[str, dict]:
    """
    Build lookup keyed by BOTH original course_number AND normalized PDF form.
    This allows matching PDF-parsed course numbers against our stored formats.
    """
    lkp: dict[str, dict] = {}
    for c in courses:
        lkp[c["course_number"]] = c
    return lkp


def infer_category(course_number: str, title: str, is_placeholder: bool, base_lkp: dict[str, dict]) -> str:
    """Infer category for a course not found in the base lookup."""
    # GE placeholders (course_number is already normalized at this point)
    if course_number.startswith("GE ") or course_number == "GE":
        return "ge"
    if "General Education Requirement" in title or title.startswith("GE "):
        return "ge"
    # Elective-like placeholders
    if is_placeholder and any(
        kw in title for kw in ("Elective", "elective", "Concentration", "Internship")
    ):
        return "concentration"
    if any(kw in course_number for kw in ("Elective", "elective", "Concentration", "Senior Project", "Free")):
        return "concentration"
    return "major"


# ---------------------------------------------------------------------------
# Core merge: build one merged concentration entry
# ---------------------------------------------------------------------------

def merge_concentration_section(
    section: dict,
    major_code: str,
    base_entry: dict,
    existing_conc_key: str | None,
) -> dict:
    """
    Build a merged flowchart entry for one concentration section.
    Preserves id/prerequisites/quarter_equivalents/elective_key from existing entries.
    """
    concentration_label = section["concentration_label"]
    slug = build_slug(concentration_label)
    key = make_flowchart_key(major_code, concentration_label, existing_conc_key)

    base_lkp = course_lookup(base_entry.get("courses", []))
    existing_conc_lkp: dict[str, dict] = {}
    if existing_conc_key and existing_conc_key in FLOWCHARTS:
        existing_conc_lkp = course_lookup(FLOWCHARTS[existing_conc_key].get("courses", []))

    merged_courses: list[dict] = []
    new_course_ids: list[str] = []
    warnings: list[str] = []
    used_ids: dict[str, int] = {}  # base_id → count, for deduplication

    def unique_id(base_id: str) -> str:
        count = used_ids.get(base_id, 0)
        used_ids[base_id] = count + 1
        return base_id if count == 0 else f"{base_id}_{count + 1}"

    for term in section["terms"]:
        grid_col = term["grid_col"]
        for parsed_course in term["courses"]:
            cn_raw = parsed_course["course_number"]
            cn_norm = normalize_pdf_course_number(cn_raw)
            title = parsed_course["title"]
            units = parsed_course["units"]
            units_display = parsed_course["units_display"]
            is_placeholder = parsed_course["is_placeholder"]

            # Look up in base first (try normalized, then raw), then existing concentration
            existing = (
                base_lkp.get(cn_norm)
                or base_lkp.get(cn_raw)
                or existing_conc_lkp.get(cn_norm)
                or existing_conc_lkp.get(cn_raw)
            )
            # Use normalized course_number for the stored entry
            cn = cn_norm

            if existing:
                course_id = unique_id(existing["id"])
                prerequisites = existing.get("prerequisites", [])
                quarter_equivalents = existing.get("quarter_equivalents", [])
                elective_key = existing.get("elective_key")
                category = existing.get("category", "major")
                auto_satisfied_by = existing.get("auto_satisfied_by")
                lab_component = existing.get("lab_component")
            else:
                # Concentration-unique course: generate new ID
                base_id = f"{slug}_{clean_id_part(cn)}"
                course_id = unique_id(base_id)
                prerequisites = []
                quarter_equivalents = []
                elective_key = None
                auto_satisfied_by = None
                lab_component = None
                category = infer_category(cn, title, is_placeholder, base_lkp)
                new_course_ids.append(course_id)
                warnings.append(f"New course (manual prereqs needed): {cn} ({title}) → id={course_id}")

            entry: dict = {
                "id": course_id,
                "course_number": cn,
                "title": title,
                "units": units,
                "units_display": units_display,
                "category": category,
                "grid_col": grid_col,
                "grid_row": 0,
                "prerequisites": prerequisites,
                "quarter_equivalents": quarter_equivalents,
                "is_placeholder": is_placeholder,
            }
            if elective_key is not None:
                entry["elective_key"] = elective_key
            if auto_satisfied_by is not None:
                entry["auto_satisfied_by"] = auto_satisfied_by
            if lab_component is not None:
                entry["lab_component"] = lab_component

            merged_courses.append(entry)

    action = "update" if (existing_conc_key and existing_conc_key in FLOWCHARTS) else "create"

    return {
        "key": key,
        "action": action,
        "major_code": major_code,
        "concentration_label": concentration_label,
        "total_units": section["total_units"],
        "major": base_entry["major"],
        "courses": merged_courses,
        "notes": base_entry.get("notes"),
        "new_course_ids": new_course_ids,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Base section diff
# ---------------------------------------------------------------------------

def diff_base_section(section: dict, major_code: str, base_entry: dict) -> dict:
    """Compare a parsed base section against the existing FLOWCHARTS[major_code] entry."""
    base_lkp = course_lookup(base_entry.get("courses", []))

    parsed_courses = {
        normalize_pdf_course_number(c["course_number"]): c
        for term in section["terms"]
        for c in term["courses"]
    }

    added = sorted(parsed_courses.keys() - base_lkp.keys())
    removed = sorted(base_lkp.keys() - parsed_courses.keys())
    changed: list[dict] = []

    for cn, pc in parsed_courses.items():
        if cn in base_lkp:
            bc = base_lkp[cn]
            changes: dict[str, dict] = {}
            if pc["units"] != bc.get("units"):
                changes["units"] = {"old": bc.get("units"), "new": pc["units"]}
            if pc["title"] != bc.get("title"):
                changes["title"] = {"old": bc.get("title"), "new": pc["title"]}
            if changes:
                changed.append({"course_number": cn, "changes": changes})

    return {
        "major_code": major_code,
        "section_title": section["section_title"],
        "total_units_parsed": section["total_units"],
        "total_units_existing": base_entry.get("total_units"),
        "courses_in_parsed": len(parsed_courses),
        "courses_in_existing": len(base_lkp),
        "added_courses": [
            {"course_number": cn, **parsed_courses[cn]} for cn in added
        ],
        "removed_courses": [
            {"course_number": cn, **base_lkp[cn]} for cn in removed
        ],
        "changed_courses": changed,
    }


# ---------------------------------------------------------------------------
# Validate existing concentration entry against parsed
# ---------------------------------------------------------------------------

def validate_existing_concentration(
    section: dict,
    major_code: str,
    existing_key: str,
    base_entry: dict,
) -> dict:
    """Diff a parsed section against an already-built FLOWCHARTS concentration entry."""
    if existing_key not in FLOWCHARTS:
        return {"existing_key": existing_key, "error": "Key not in FLOWCHARTS"}

    existing_entry = FLOWCHARTS[existing_key]
    existing_lkp = course_lookup(existing_entry.get("courses", []))

    parsed_courses = {
        normalize_pdf_course_number(c["course_number"]): c
        for term in section["terms"]
        for c in term["courses"]
    }

    added = sorted(parsed_courses.keys() - existing_lkp.keys())
    removed = sorted(existing_lkp.keys() - parsed_courses.keys())
    changed: list[dict] = []

    for cn, pc in parsed_courses.items():
        if cn in existing_lkp:
            ec = existing_lkp[cn]
            changes: dict[str, dict] = {}
            if pc["units"] != ec.get("units"):
                changes["units"] = {"old": ec.get("units"), "new": pc["units"]}
            if pc["title"] != ec.get("title"):
                changes["title"] = {"old": ec.get("title"), "new": pc["title"]}
            if changes:
                changed.append({"course_number": cn, "changes": changes})

    return {
        "existing_key": existing_key,
        "section_title": section["section_title"],
        "total_units_parsed": section["total_units"],
        "total_units_existing": existing_entry.get("total_units"),
        "in_parsed_not_existing": added,
        "in_existing_not_parsed": removed,
        "changed_courses": changed,
        "clean": not (added or removed or changed),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not PARSED_PATH.exists():
        print(f"ERROR: {PARSED_PATH} not found. Run parse_flowchart_txt.py first.", file=sys.stderr)
        sys.exit(1)

    with open(PARSED_PATH) as f:
        parsed: list[dict] = json.load(f)

    name_to_code = build_major_name_to_code()

    merged_concentration_entries: list[dict] = []
    base_diffs: list[dict] = []
    validation_results: list[dict] = []
    skipped: list[str] = []
    unmatched_concentrations: list[dict] = []

    for section in parsed:
        major_name = section["major_name"]

        if major_name in SKIP_MAJOR_NAMES:
            skipped.append(section["section_title"])
            continue

        major_code = name_to_code.get(major_name)
        if not major_code:
            skipped.append(f"UNMAPPED: {section['section_title']}")
            continue

        if major_code not in FLOWCHARTS:
            skipped.append(f"NO_FLOWCHART: {section['section_title']}")
            continue

        base_entry = FLOWCHARTS[major_code]
        label = section["concentration_label"]

        # Base section → diff only
        if is_base_label(label):
            diff = diff_base_section(section, major_code, base_entry)
            base_diffs.append(diff)
            continue

        # Find matching concentration entry
        conc_entry = find_concentration_entry(major_code, label)
        parsed_norm = normalize_label(label)

        # Determine the flowchart key: prefer explicit override, then existing full_flowchart_key
        override_key = LABEL_KEY_OVERRIDES.get((major_code, parsed_norm))
        existing_key = override_key or (conc_entry.get("full_flowchart_key") if conc_entry else None)

        if existing_key and existing_key in FLOWCHARTS:
            # Already built — validate against parsed
            result = validate_existing_concentration(section, major_code, existing_key, base_entry)
            validation_results.append(result)
            continue

        # Build new concentration flowchart
        merged = merge_concentration_section(section, major_code, base_entry, existing_key)

        if conc_entry:
            merged["concentration_id"] = conc_entry.get("id")
        else:
            merged["concentration_id"] = None
            unmatched_concentrations.append({
                "major_code": major_code,
                "parsed_label": label,
                "section_title": section["section_title"],
            })

        merged_concentration_entries.append(merged)

    # Write outputs
    with open(MERGED_CONC_OUT, "w") as f:
        json.dump(merged_concentration_entries, f, indent=2)
    print(f"Wrote {len(merged_concentration_entries)} concentration entries → {MERGED_CONC_OUT}")

    with open(BASE_DIFFS_OUT, "w") as f:
        json.dump({
            "base_diffs": base_diffs,
            "validation_results": validation_results,
        }, f, indent=2)
    print(f"Wrote {len(base_diffs)} base diffs, {len(validation_results)} validations → {BASE_DIFFS_OUT}")

    # Report
    report_lines: list[str] = []
    report_lines.append("=" * 80)
    report_lines.append("FLOWCHART MERGE REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")

    report_lines.append(f"New concentration entries to create/update: {len(merged_concentration_entries)}")
    report_lines.append(f"Existing concentration entries validated:    {len(validation_results)}")
    report_lines.append(f"Base major sections diffed:                 {len(base_diffs)}")
    report_lines.append(f"Skipped (unmapped/out-of-scope):            {len(skipped)}")
    report_lines.append("")

    # New concentration entries
    report_lines.append("-" * 60)
    report_lines.append("NEW/UPDATED CONCENTRATION ENTRIES")
    report_lines.append("-" * 60)
    for entry in merged_concentration_entries:
        action = entry["action"].upper()
        key = entry["key"]
        label = entry["concentration_label"]
        n_courses = len(entry["courses"])
        n_new = len(entry["new_course_ids"])
        report_lines.append(f"  [{action}] {key}  ({label})")
        report_lines.append(f"    {n_courses} courses total, {n_new} concentration-unique")
        if entry.get("concentration_id") is None:
            report_lines.append("    WARNING: No matching CONCENTRATIONS entry found")
        if entry["warnings"]:
            for w in entry["warnings"]:
                report_lines.append(f"    ! {w}")
        report_lines.append("")

    # Validation results
    report_lines.append("-" * 60)
    report_lines.append("EXISTING CONCENTRATION VALIDATION")
    report_lines.append("-" * 60)
    for v in validation_results:
        status = "CLEAN" if v.get("clean") else "DIFFS"
        report_lines.append(f"  [{status}] {v['existing_key']}")
        if not v.get("clean"):
            if v.get("in_parsed_not_existing"):
                report_lines.append(f"    In PDF not in app: {v['in_parsed_not_existing']}")
            if v.get("in_existing_not_parsed"):
                report_lines.append(f"    In app not in PDF: {v['in_existing_not_parsed']}")
            for cc in v.get("changed_courses", []):
                report_lines.append(f"    Changed: {cc['course_number']} {cc['changes']}")
    report_lines.append("")

    # Base diffs
    report_lines.append("-" * 60)
    report_lines.append("BASE MAJOR DIFFS")
    report_lines.append("-" * 60)
    for diff in base_diffs:
        mc = diff["major_code"]
        has_changes = diff["added_courses"] or diff["removed_courses"] or diff["changed_courses"]
        tu_match = diff["total_units_parsed"] == diff["total_units_existing"]
        status = "CLEAN" if (not has_changes and tu_match) else "DIFFS"
        report_lines.append(f"  [{status}] {mc}  (parsed {diff['total_units_parsed']} units vs existing {diff['total_units_existing']})")
        if not tu_match:
            report_lines.append(f"    Total units mismatch!")
        if diff["added_courses"]:
            report_lines.append(f"    Added in PDF ({len(diff['added_courses'])}): {[c['course_number'] for c in diff['added_courses']]}")
        if diff["removed_courses"]:
            report_lines.append(f"    Removed from PDF ({len(diff['removed_courses'])}): {[c['course_number'] for c in diff['removed_courses']]}")
        for cc in diff["changed_courses"]:
            report_lines.append(f"    Changed: {cc['course_number']} {cc['changes']}")
    report_lines.append("")

    # Unmatched concentrations
    if unmatched_concentrations:
        report_lines.append("-" * 60)
        report_lines.append("UNMATCHED CONCENTRATIONS (no CONCENTRATIONS entry found)")
        report_lines.append("-" * 60)
        for u in unmatched_concentrations:
            report_lines.append(f"  {u['major_code']}: {u['parsed_label']!r}")
        report_lines.append("")

    # Skipped
    if skipped:
        report_lines.append("-" * 60)
        report_lines.append("SKIPPED SECTIONS")
        report_lines.append("-" * 60)
        for s in skipped:
            report_lines.append(f"  {s}")

    report_text = "\n".join(report_lines)
    with open(REPORT_OUT, "w") as f:
        f.write(report_text + "\n")
    print(f"Wrote report → {REPORT_OUT}")
    print()
    print(report_text)


if __name__ == "__main__":
    main()
