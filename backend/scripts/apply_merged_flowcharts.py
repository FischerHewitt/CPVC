#!/usr/bin/env python3
"""
Apply merged concentration flowcharts to flowcharts.py and concentrations.py.

Reads FlowchartPdf/merged_concentration_entries.json and:
  1. Inserts new *_FLOWCHART variable declarations into flowcharts.py
  2. Inserts the new FLOWCHARTS dict entries
  3. Updates concentrations.py with full_flowchart_key for each new entry

Usage (from repo root):
    python3 backend/scripts/apply_merged_flowcharts.py [--dry-run]

    --dry-run: print what would be written, don't modify files

CAUTION: Creates backups at flowcharts.py.bak and concentrations.py.bak before modifying.
"""

import re
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "backend"))

from data.concentrations import CONCENTRATIONS  # noqa: E402

MERGED_PATH = REPO_ROOT / "FlowchartPdf" / "merged_concentration_entries.json"
FLOWCHARTS_PY = REPO_ROOT / "backend" / "data" / "flowcharts.py"
CONCENTRATIONS_PY = REPO_ROOT / "backend" / "data" / "concentrations.py"

DRY_RUN = "--dry-run" in sys.argv


# ---------------------------------------------------------------------------
# Python code generation
# ---------------------------------------------------------------------------

def py_repr(val) -> str:
    """Represent a Python value as a source-code literal."""
    if val is True:
        return "True"
    if val is False:
        return "False"
    if val is None:
        return "None"
    if isinstance(val, str):
        # Use double quotes, escape internal quotes
        escaped = val.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(val, int):
        return str(val)
    if isinstance(val, list):
        items = ", ".join(py_repr(i) for i in val)
        return f"[{items}]"
    if isinstance(val, dict):
        pairs = ", ".join(f"{py_repr(k)}: {py_repr(v)}" for k, v in val.items())
        return f"{{{pairs}}}"
    return repr(val)


def course_to_py_line(course: dict) -> str:
    """Render one course dict as a single Python line with consistent field ordering."""
    # Required fields in canonical order
    required_keys = [
        "id", "course_number", "title", "units",
        "category", "grid_col", "grid_row",
        "prerequisites", "quarter_equivalents", "is_placeholder",
    ]
    # Optional fields appended when present
    optional_keys = ["elective_key", "auto_satisfied_by", "lab_component", "units_display"]

    parts = []
    for k in required_keys:
        parts.append(f'"{k}": {py_repr(course[k])}')
    for k in optional_keys:
        if k in course and course[k] is not None:
            parts.append(f'"{k}": {py_repr(course[k])}')

    return "    {" + ", ".join(parts) + "},"


def generate_flowchart_block(entry: dict) -> str:
    """Generate the Python source for one concentration flowchart variable."""
    key = entry["key"]
    var_name = f"{key}_FLOWCHART"
    major = entry["major"]
    label = entry["concentration_label"]
    total_units = entry["total_units"]
    major_code = entry["major_code"]

    lines: list[str] = []
    lines.append("")
    lines.append("")
    lines.append(f"# {'─' * 73}")
    lines.append(f"# {major} — {label} ({total_units} units)")
    lines.append(f"# Source: FlowchartPdf/parsed_flowcharts.json (auto-generated)")
    lines.append(f"# {'─' * 73}")
    lines.append(f"{var_name}: list[Course] = [")

    # Group by grid_col for readability
    current_col = -1
    col_labels = [
        "FRESHMAN FALL", "FRESHMAN SPRING",
        "SOPHOMORE FALL", "SOPHOMORE SPRING",
        "JUNIOR FALL", "JUNIOR SPRING",
        "SENIOR FALL", "SENIOR SPRING",
    ]
    for course in entry["courses"]:
        col = course["grid_col"]
        if col != current_col:
            current_col = col
            col_label = col_labels[col] if col < len(col_labels) else f"TERM {col}"
            lines.append(f"    # ── {col_label} {'─' * (50 - len(col_label))}")
        lines.append(course_to_py_line(course))

    lines.append("]")
    return "\n".join(lines)


def generate_compact_call(entry: dict) -> str:
    key = entry["key"]
    var_name = f"{key}_FLOWCHART"
    return f"{var_name} = _compact_rows_by_category({var_name})"


def generate_flowcharts_dict_entry(entry: dict) -> str:
    """Generate the FLOWCHARTS dict entry for one concentration."""
    key = entry["key"]
    major = entry["major"]
    major_code = entry["major_code"]
    total_units = entry["total_units"]
    var_name = f"{key}_FLOWCHART"

    lines = [
        f'    "{key}": {{',
        f'        "major": {py_repr(major)},',
        f'        "code": {py_repr(major_code)},',
        f'        "total_units": {total_units},',
        f'        "courses": {var_name},',
        f'        "columns": COLUMN_LABELS,',
        f'    }},',
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Modify flowcharts.py
# ---------------------------------------------------------------------------

def update_flowcharts_py(entries: list[dict]) -> None:
    """Insert new flowchart variables and FLOWCHARTS dict entries into flowcharts.py."""
    text = FLOWCHARTS_PY.read_text(encoding="utf-8")

    # Find insertion point for variable declarations: just before "FLOWCHARTS = {"
    flowcharts_dict_start = text.find("\nFLOWCHARTS = {")
    if flowcharts_dict_start == -1:
        print("ERROR: Could not find 'FLOWCHARTS = {' in flowcharts.py", file=sys.stderr)
        sys.exit(1)

    # Filter to only entries that don't already have a variable in the file
    new_entries = [e for e in entries if f"{e['key']}_FLOWCHART" not in text]
    print(f"  {len(new_entries)} of {len(entries)} entries are new (not already in file)")

    if not new_entries:
        print("  Nothing to insert into flowcharts.py.")
        return

    # Build the block of new flowchart variable code
    var_blocks: list[str] = []
    compact_calls: list[str] = []
    dict_entries: list[str] = []

    for entry in new_entries:
        var_blocks.append(generate_flowchart_block(entry))
        compact_calls.append(generate_compact_call(entry))
        dict_entries.append(generate_flowcharts_dict_entry(entry))

    # Insert variable declarations + compact calls before FLOWCHARTS = {
    # Place them right before the FLOWCHARTS dict line
    insert_before = flowcharts_dict_start  # we insert at this position

    new_vars_section = "\n".join(var_blocks) + "\n\n" + "\n".join(compact_calls) + "\n"
    new_text = text[:insert_before] + "\n" + new_vars_section + text[insert_before:]

    # Now insert into the FLOWCHARTS dict (find the closing "}" of the dict)
    # After the insertion above, re-find FLOWCHARTS dict
    dict_close_marker = "\n}"  # the last "}" in the file closes FLOWCHARTS
    dict_close_pos = new_text.rfind(dict_close_marker)
    if dict_close_pos == -1:
        print("ERROR: Could not find closing '}' of FLOWCHARTS dict", file=sys.stderr)
        sys.exit(1)

    new_dict_entries_text = "\n" + "\n".join(dict_entries) + "\n"
    new_text = new_text[:dict_close_pos] + new_dict_entries_text + new_text[dict_close_pos:]

    if DRY_RUN:
        # Show a summary
        print(f"  [DRY-RUN] Would insert {len(new_entries)} entries into flowcharts.py")
        print(f"  New variables added (first 5): {[e['key'] for e in new_entries[:5]]}")
        return

    # Write backup then updated file
    FLOWCHARTS_PY.with_suffix(".py.bak").write_text(text, encoding="utf-8")
    FLOWCHARTS_PY.write_text(new_text, encoding="utf-8")
    print(f"  Updated flowcharts.py (backup at flowcharts.py.bak)")


# ---------------------------------------------------------------------------
# Modify concentrations.py
# ---------------------------------------------------------------------------

def find_major_section_bounds(text: str, major_code: str) -> tuple[int, int] | None:
    """
    Return (start, end) character positions of the concentration list for major_code.
    Handles both inline dict syntax ("CS": [...]) and assignment syntax (CONCENTRATIONS["CS"] = [...]).
    """
    # Pattern 1: inside CONCENTRATIONS dict: "MAJOR_CODE": [
    inline = f'"{major_code}": ['
    pos = text.find(inline)
    if pos != -1:
        list_start = text.index("[", pos)
        return list_start, _find_matching_bracket(text, list_start)

    # Pattern 2: CONCENTRATIONS["MAJOR_CODE"] = [
    assign = f'CONCENTRATIONS["{major_code}"] = ['
    pos = text.find(assign)
    if pos != -1:
        # Point directly at the trailing "[" of "= [", not the "[" in ["MAJOR_CODE"]
        list_start = pos + len(assign) - 1
        return list_start, _find_matching_bracket(text, list_start)

    return None


def _find_matching_brace(text: str, start: int) -> int:
    """Return position of the closing } of the first { found at or after start."""
    open_pos = text.find("{", start)
    if open_pos == -1:
        return len(text)
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return len(text)


def _find_matching_bracket(text: str, open_pos: int) -> int:
    """Return position of the closing ] matching the [ at open_pos."""
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return i
    return len(text)


def update_concentrations_py(entries: list[dict]) -> None:
    """Add full_flowchart_key to concentration entries in concentrations.py."""
    text = CONCENTRATIONS_PY.read_text(encoding="utf-8")
    updates_made = 0

    for entry in entries:
        key = entry["key"]
        major_code = entry["major_code"]
        conc_id = entry.get("concentration_id")

        if not conc_id:
            print(f"  SKIP {key}: no concentration_id, cannot update concentrations.py")
            continue

        if f'"full_flowchart_key": "{key}"' in text:
            print(f"  SKIP {key}: full_flowchart_key already present in concentrations.py")
            continue

        # Find the major's concentration list in the file
        bounds = find_major_section_bounds(text, major_code)
        if not bounds:
            print(f"  WARN {key}: could not find major section for {major_code} in concentrations.py")
            continue

        section_start, section_end = bounds
        section = text[section_start:section_end + 1]

        # Within the section, find the concentration entry by its id
        id_pattern = f'"id": "{conc_id}"'
        id_pos_in_section = section.find(id_pattern)
        if id_pos_in_section == -1:
            print(f"  WARN {key}: id={conc_id!r} not found in {major_code} section")
            continue

        id_pos = section_start + id_pos_in_section

        # Find end of this concentration's dict entry so we can search within it
        entry_end = _find_matching_brace(text, id_pos)

        # Find "slot_overrides" anywhere within this concentration's entry
        slot_pos = text.find('"slot_overrides"', id_pos, entry_end)
        if slot_pos == -1:
            print(f"  WARN {key}: slot_overrides not found after id={conc_id!r} in {major_code}")
            continue

        # Determine indentation from the slot_overrides line
        line_start = text.rfind("\n", 0, slot_pos) + 1
        line_prefix = text[line_start:slot_pos]

        if line_prefix.strip():
            # "slot_overrides" is inline with other fields on one line; insert inline
            insert_str = f'"full_flowchart_key": "{key}", '
        else:
            # "slot_overrides" is on its own line; use the leading whitespace as indent
            insert_str = f'{line_prefix}"full_flowchart_key": "{key}",\n'

        text = text[:slot_pos] + insert_str + text[slot_pos:]
        updates_made += 1

    if updates_made == 0:
        print("  No concentrations.py updates needed.")
        return

    if DRY_RUN:
        print(f"  [DRY-RUN] Would update {updates_made} entries in concentrations.py")
        return

    CONCENTRATIONS_PY.with_suffix(".py.bak").write_text(
        CONCENTRATIONS_PY.read_text(encoding="utf-8"), encoding="utf-8"
    )
    CONCENTRATIONS_PY.write_text(text, encoding="utf-8")
    print(f"  Updated {updates_made} entries in concentrations.py")


def normalize_label_for_match(label: str) -> str:
    return re.sub(r"\s+[Cc]oncentration$", "", label).strip().lower()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not MERGED_PATH.exists():
        print(f"ERROR: {MERGED_PATH} not found. Run merge_flowchart_json.py first.", file=sys.stderr)
        sys.exit(1)

    with open(MERGED_PATH) as f:
        entries: list[dict] = json.load(f)

    # Only process "create" entries (not "update" — those already exist in FLOWCHARTS)
    create_entries = [e for e in entries if e["action"] == "create"]
    print(f"Processing {len(create_entries)} 'create' entries (skipping {len(entries) - len(create_entries)} 'update')")

    print("\n--- flowcharts.py ---")
    update_flowcharts_py(create_entries)

    print("\n--- concentrations.py ---")
    update_concentrations_py(create_entries)

    print("\nDone." if not DRY_RUN else "\nDry-run complete.")


if __name__ == "__main__":
    main()
