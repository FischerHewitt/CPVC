"""Tests for the ElectiveCatalog service (Stage 1: catalog loading and resolution)."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


def _reload_module():
    import importlib
    import services.elective_catalog as mod
    mod._loaded = False
    mod._catalog = {}
    return mod


def test_catalog_loads():
    mod = _reload_module()
    catalog = mod.get_catalog()
    assert len(catalog) > 500, f"Expected 500+ courses, got {len(catalog)}"


def test_known_cs_course_resolves():
    mod = _reload_module()
    result = mod.resolve_course("CSC 1001")
    assert result is not None
    assert result["course_number"] == "CSC 1001"
    assert result["title"] == "Fundamentals of Computer Science"
    assert result["units"] == 4


def test_known_math_course_resolves():
    mod = _reload_module()
    result = mod.resolve_course("MATH 1151")
    assert result is not None
    assert result["course_number"] == "MATH 1151"
    assert isinstance(result["units"], int)
    assert len(result["title"]) > 0


def test_unknown_course_returns_none():
    mod = _reload_module()
    assert mod.resolve_course("FAKE 9999") is None


def test_resolve_course_shape():
    mod = _reload_module()
    result = mod.resolve_course("MATH 1151")
    assert result is not None
    assert set(result.keys()) == {"course_number", "title", "units"}


def test_supplements_override_catalog(tmp_path):
    """Supplements file entries take precedence over the generated catalog."""
    supplements = {"CSC 1001": {"title": "Override Title", "units": 99}}
    sup_path = tmp_path / "course_supplements.json"
    sup_path.write_text(json.dumps(supplements))

    import services.elective_catalog as mod
    original_dir = mod._DATA_DIR
    try:
        mod._DATA_DIR = tmp_path
        # Copy catalog into tmp_path so it still loads
        catalog_path = Path(__file__).parent.parent / "data" / "course_catalog.json"
        (tmp_path / "course_catalog.json").write_text(catalog_path.read_text())
        mod._loaded = False
        mod._catalog = {}

        result = mod.resolve_course("CSC 1001")
        assert result is not None
        assert result["title"] == "Override Title"
        assert result["units"] == 99
    finally:
        mod._DATA_DIR = original_dir
        mod._loaded = False
        mod._catalog = {}


def test_multiple_majors_covered():
    """Spot-check that courses from diverse departments are in the catalog."""
    mod = _reload_module()
    courses_to_check = [
        "MATH 1261",   # Mathematics
        "PHYS 1141",   # Physics
        "CHEM 1120",   # Chemistry
        "BIO 1150",    # Biology
        "STAT 3210",   # Statistics
        "EE 2201",     # Electrical Engineering
        "ME 2212",     # Mechanical Engineering
    ]
    missing = [c for c in courses_to_check if mod.resolve_course(c) is None]
    assert not missing, f"Expected these courses in catalog but missing: {missing}"


# ── Stage 2: supplement coverage ─────────────────────────────────────────────

def test_supplements_loaded():
    """Supplements file is non-empty after seeding."""
    mod = _reload_module()
    catalog = mod.get_catalog()
    # These are CS elective-only courses that appear in no flowchart tile
    orphan_courses = ["CSC 5100", "CSC 4667", "CPE 4220", "DATA 4610", "ART 3332"]
    missing = [c for c in orphan_courses if c not in catalog]
    assert not missing, f"Expected seeded orphan courses in merged catalog but missing: {missing}"


def test_supplement_course_resolves_with_full_shape():
    """A supplement-only course resolves to the expected title and units."""
    mod = _reload_module()
    result = mod.resolve_course("CSC 5100")
    assert result is not None
    assert result["course_number"] == "CSC 5100"
    assert result["title"] == "Modern Software Engineering"
    assert result["units"] == 3
    assert set(result.keys()) == {"course_number", "title", "units"}


def test_supplement_cpe_course_resolves():
    mod = _reload_module()
    result = mod.resolve_course("CPE 4220")
    assert result is not None
    assert result["title"] == "Network Security"
    assert result["units"] == 3


def test_combined_catalog_size():
    """Merged catalog (flowchart + supplements) should exceed 900 entries after migration."""
    mod = _reload_module()
    assert len(mod.get_catalog()) > 900


# ── Stage 3: static elective definitions ─────────────────────────────────────

def test_static_elective_loads():
    mod = _reload_module()
    result = mod.get_static_elective("cs_calc_seq_1")
    assert result is not None
    assert result["key"] == "cs_calc_seq_1"
    assert result["title"] == "Calculus I or Calculus for Data Science I"
    assert len(result["courses"]) == 2


def test_static_elective_courses_fully_resolved():
    """Every course in a static elective has course_number, title, and units."""
    mod = _reload_module()
    result = mod.get_static_elective("cs_calc_seq_1")
    assert result is not None
    for course in result["courses"]:
        assert set(course.keys()) == {"course_number", "title", "units"}
        assert course["course_number"]
        assert course["title"]
        assert isinstance(course["units"], int)


def test_static_elective_unknown_key_returns_none():
    mod = _reload_module()
    assert mod.get_static_elective("nonexistent_key_xyz") is None


def test_static_elective_count():
    """Spot-check static and dynamic definitions across different majors."""
    mod = _reload_module()
    static_keys = [
        "cs_calc_seq_1", "cs_ethics_elective", "cs_tech_elective", "agc_chem_elective",
    ]
    for key in static_keys:
        assert mod.get_static_elective(key) is not None, f"Missing static elective: {key}"
    dynamic_keys = ["me_tech_elective", "se_tech_elective", "cpe_tech_elective"]
    for key in dynamic_keys:
        assert mod.get_dynamic_config(key) is not None, f"Missing dynamic config: {key}"


def test_all_static_courses_resolve():
    """No static elective should contain unresolvable course numbers."""
    import json
    from pathlib import Path
    data_dir = Path(__file__).parent.parent / "data"
    with open(data_dir / "electives_static.json") as f:
        raw = json.load(f)
    mod = _reload_module()
    catalog = mod.get_catalog()
    unresolvable = []
    for key, defn in raw.items():
        for num in defn.get("courses", []):
            if num not in catalog:
                unresolvable.append(f"{key}: {num}")
    assert not unresolvable, (
        f"{len(unresolvable)} course numbers in electives_static.json not in catalog:\n"
        + "\n".join(unresolvable[:20])
    )


def test_dynamic_config_loads():
    mod = _reload_module()
    cfg = mod.get_dynamic_config("se_tech_elective")
    assert cfg is not None
    assert cfg["depts"] == ["csc"]
    assert cfg["min_level"] == 4000
    assert cfg["max_level"] == 4999


def test_dynamic_config_with_extra_courses():
    mod = _reload_module()
    cfg = mod.get_dynamic_config("phys_tech_elective")
    assert cfg is not None
    assert "extra_courses" in cfg
    assert "CSC 2600" in cfg["extra_courses"]
    assert "CHEM 1122" in cfg["extra_courses"]


def test_placeholder_key_lookup():
    mod = _reload_module()
    assert mod.get_placeholder_key("LIFESCI") == "cs_life_science"
    assert mod.get_placeholder_key("AIML_ML_REQ") == "cs_aiml_ml_required"
    assert mod.get_placeholder_key("ME_TE_SRF1") == "me_tech_elective"


def test_placeholder_key_unknown_returns_none():
    mod = _reload_module()
    assert mod.get_placeholder_key("TOTALLY_UNKNOWN_XYZ") is None


def test_is_static_and_is_dynamic():
    mod = _reload_module()
    assert mod.is_static("cs_calc_seq_1")
    assert not mod.is_dynamic("cs_calc_seq_1")
    assert mod.is_dynamic("se_tech_elective")
    assert not mod.is_static("se_tech_elective")
