from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_majors_includes_available_flowcharts():
    response = client.get("/api/flowchart/majors")

    assert response.status_code == 200
    majors = response.json()["majors"]
    assert {"code": "CS", "name": "Computer Science"} in majors
    assert {"code": "AERO", "name": "Aerospace Engineering"} in majors


def test_get_flowchart_is_case_insensitive_and_has_expected_shape():
    response = client.get("/api/flowchart/cs")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == "CS"
    assert body["major"] == "Computer Science"
    assert body["total_units"] == 120
    assert body["courses"]
    assert {"year": "Freshman", "term": "Fall"} in body["columns"]


def test_get_flowchart_returns_404_for_unknown_major():
    response = client.get("/api/flowchart/not-a-major")

    assert response.status_code == 404
    assert response.json()["detail"] == "No flowchart for major: not-a-major"


def test_infer_flowchart_prerequisites_from_completed_course():
    response = client.post("/api/flowchart/CS/infer", json={"completed": ["CSC 3449"]})

    assert response.status_code == 200
    inferred = set(response.json()["inferred"])
    assert "CSC 2001" in inferred
    assert "CSC 202" in inferred
    assert "CSC 1001" in inferred
    assert "CSC 101" in inferred
    assert "MATH 2031" in inferred
    assert "MATH 1262" in inferred
    assert "MATH 142" in inferred
    assert "CSC 3449" not in inferred
