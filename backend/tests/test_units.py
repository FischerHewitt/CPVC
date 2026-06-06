from services.units import parse_units_range


def test_fixed_integer_string():
    result = parse_units_range("3")
    assert result == {"units": 3}


def test_fixed_integer_input():
    result = parse_units_range(3)
    assert result == {"units": 3}


def test_hyphen_range():
    result = parse_units_range("1-3")
    assert result == {"units": 1, "units_min": 1, "units_max": 3}


def test_en_dash_range():
    result = parse_units_range("1–3")
    assert result == {"units": 1, "units_min": 1, "units_max": 3}


def test_empty_string_returns_default():
    result = parse_units_range("")
    assert result == {"units": 3}


def test_none_returns_default():
    result = parse_units_range(None)
    assert result == {"units": 3}


def test_custom_default():
    result = parse_units_range("", default=4)
    assert result == {"units": 4}


def test_wider_range():
    result = parse_units_range("1-4")
    assert result == {"units": 1, "units_min": 1, "units_max": 4}


def test_same_value_range_treated_as_fixed():
    result = parse_units_range("3-3")
    assert result == {"units": 3}


# ── Integration: elective route emits range fields ────────────────────────────

from fastapi.testclient import TestClient
from main import app

_client = TestClient(app)


def test_variable_unit_course_emits_units_min_max():
    """TH 2285 (1-3u) must appear in th_ld_elective with units_min and units_max."""
    import services.elective_catalog as ec
    ec.reload()
    response = _client.get("/api/electives/th_ld_elective")
    assert response.status_code == 200
    courses = {c["course_number"]: c for c in response.json()["courses"]}
    th2285 = courses.get("TH 2285")
    assert th2285 is not None, "TH 2285 missing from th_ld_elective"
    assert th2285["units"] == 1
    assert th2285["units_min"] == 1
    assert th2285["units_max"] == 3


def test_fixed_unit_course_omits_units_min_max():
    """Fixed-unit courses must not have units_min / units_max."""
    import services.elective_catalog as ec
    ec.reload()
    response = _client.get("/api/electives/th_ld_elective")
    assert response.status_code == 200
    courses = {c["course_number"]: c for c in response.json()["courses"]}
    th2240 = courses.get("TH 2240")
    assert th2240 is not None, "TH 2240 missing from th_ld_elective"
    assert "units_min" not in th2240
    assert "units_max" not in th2240
