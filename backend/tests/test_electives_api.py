from fastapi.testclient import TestClient

import routers.electives as electives_router
from main import app


client = TestClient(app)


def test_static_elective_endpoint_returns_options_for_slash_placeholder():
    response = client.get("/api/electives/arch_precalc_or_calculus")

    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "arch_precalc_or_calculus"
    assert data["title"] == "Precalculus or Calculus I"
    assert [course["course_number"] for course in data["courses"]] == ["MATH 1007", "MATH 1261"]


def test_static_elective_endpoint_returns_agb_agricultural_options():
    response = client.get("/api/electives/agb_agricultural_elective")

    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "agb_agricultural_elective"
    assert data["title"] == "Agricultural Elective"
    assert [course["course_number"] for course in data["courses"]] == [
        "ASCI 1112",
        "ASCI 2215",
        "ASCI 2239",
        "DSCI 2229",
        "FSN 2245",
        "PLSC 1120",
        "PLSC 1120L",
        "SS 1120",
    ]


def test_static_elective_endpoint_returns_agc_support_options():
    stat_response = client.get("/api/electives/agc_stat_data_1000")
    plant_response = client.get("/api/electives/agc_plsc_pair")

    assert stat_response.status_code == 200
    assert [course["course_number"] for course in stat_response.json()["courses"]] == ["STAT 1000", "DATA 1000"]
    assert plant_response.status_code == 200
    assert [course["course_number"] for course in plant_response.json()["courses"]] == ["PLSC 1120", "PLSC 1120L"]


def test_auto_placeholder_endpoint_returns_direct_course_options(monkeypatch):
    monkeypatch.setattr(
        electives_router,
        "get_course_info",
        lambda course_number: {"title": f"{course_number} title", "units": "3"},
    )

    response = client.get(
        "/api/electives/auto/placeholder",
        params={
            "course_id": "AGS_DSCI_FSN",
            "course_number": "DSCI 2229/FSN 2245",
            "title": "Safe Practices in Handling Food Products",
            "quarter_equivalents": "DSCI 229,FSN 245",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "auto:AGS_DSCI_FSN"
    assert [course["course_number"] for course in data["courses"]][:2] == ["DSCI 2229", "FSN 2245"]


def test_auto_placeholder_endpoint_returns_dynamic_courses_for_broad_bucket(monkeypatch):
    monkeypatch.setattr(
        electives_router,
        "get_dept_courses",
        lambda dept: {
            f"{dept.upper()} 2999": {"title": "Lower Course", "units": "3"},
            f"{dept.upper()} 3301": {"title": "Upper Course", "units": "4"},
        },
    )

    response = client.get(
        "/api/electives/auto/placeholder",
        params={
            "course_id": "POLS_UD1",
            "course_number": "POLS UD",
            "title": "3000-4000 Level POLS Elective",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["courses"] == [{"course_number": "POLS 3301", "title": "Upper Course", "units": 4}]


def test_elective_endpoint_returns_agb_dynamic_ranges(monkeypatch):
    monkeypatch.setattr(
        electives_router,
        "get_dept_courses",
        lambda dept: {
            f"{dept.upper()} 2212": {"title": "Lower Course", "units": "3"},
            f"{dept.upper()} 3301": {"title": "Upper Course", "units": "3"},
            f"{dept.upper()} 4462": {"title": "Senior Course", "units": "3"},
        },
    )

    general_response = client.get("/api/electives/agb_general_elective")
    senior_response = client.get("/api/electives/agb_4000_elective")

    assert general_response.status_code == 200
    assert [course["course_number"] for course in general_response.json()["courses"]] == ["AGB 3301", "AGB 4462"]
    assert senior_response.status_code == 200
    assert [course["course_number"] for course in senior_response.json()["courses"]] == ["AGB 4462"]


def test_elective_endpoint_returns_404_for_unknown_key():
    response = client.get("/api/electives/not-real")

    assert response.status_code == 404
