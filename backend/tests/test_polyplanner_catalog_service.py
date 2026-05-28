from services.polyplanner_catalog import catalog_summaries, degree_summaries, get_degree
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_imported_polyplanner_catalogs_include_semester_catalog():
    summaries = catalog_summaries()
    semester = next(catalog for catalog in summaries if catalog["name"] == "2026-2028")

    assert semester["termType"] == "semester"
    assert semester["courseCount"] > 4000
    assert semester["degreeCount"] >= 14


def test_imported_polyplanner_degree_can_be_found_by_name_or_id():
    degrees = degree_summaries("2026-2028")
    assert degrees is not None

    computer_science = next(degree for degree in degrees if degree["name"] == "Computer Science")
    by_name = get_degree("2026-2028", "Computer Science")
    by_id = get_degree("302", str(computer_science["id"]))

    assert by_name is not None
    assert by_id is not None
    assert by_name["id"] == by_id["id"]
    assert by_name["flowchartTemplates"]


def test_imported_polyplanner_catalog_api_exposes_summaries():
    response = client.get("/api/polyplanner-catalogs")

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "https://api.polyplanner.pro/catalogs"
    assert any(catalog["name"] == "2026-2028" for catalog in body["catalogs"])


def test_imported_polyplanner_degree_api_returns_degree_payload():
    response = client.get("/api/polyplanner-catalogs/2026-2028/degrees/Computer%20Science")

    assert response.status_code == 200
    body = response.json()
    assert body["catalog"]["termType"] == "semester"
    assert body["degree"]["name"] == "Computer Science"
    assert body["degree"]["requirements"]
