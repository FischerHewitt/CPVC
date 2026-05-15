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
    assert {"code": "SE", "name": "Software Engineering"} in majors
    assert {"code": "CPE", "name": "Computer Engineering"} in majors
    assert {"code": "CE", "name": "Civil Engineering"} in majors
    assert {"code": "ME", "name": "Mechanical Engineering"} in majors
    assert {"code": "AD", "name": "Art and Design"} in majors


def test_get_flowchart_is_case_insensitive_and_has_expected_shape():
    response = client.get("/api/flowchart/cs")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == "CS"
    assert body["major"] == "Computer Science"
    assert body["total_units"] == 120
    assert body["courses"]
    assert {"year": "Freshman", "term": "Fall"} in body["columns"]


def test_new_engineering_flowcharts_are_available():
    se_response = client.get("/api/flowchart/SE")
    cpe_response = client.get("/api/flowchart/CPE")
    ce_response = client.get("/api/flowchart/CE")
    me_response = client.get("/api/flowchart/ME")
    ad_response = client.get("/api/flowchart/AD")

    assert se_response.status_code == 200
    assert se_response.json()["major"] == "Software Engineering"
    assert se_response.json()["courses"]

    assert cpe_response.status_code == 200
    assert cpe_response.json()["major"] == "Computer Engineering"
    assert cpe_response.json()["courses"]

    assert ce_response.status_code == 200
    assert ce_response.json()["major"] == "Civil Engineering"
    assert ce_response.json()["total_units"] == 132
    assert ce_response.json()["courses"]

    assert me_response.status_code == 200
    assert me_response.json()["major"] == "Mechanical Engineering"
    assert me_response.json()["total_units"] == 129
    assert me_response.json()["courses"]

    assert ad_response.status_code == 200
    assert ad_response.json()["major"] == "Art and Design"
    assert ad_response.json()["total_units"] == 120
    assert ad_response.json()["courses"]


def test_get_concentrations_for_major():
    response = client.get("/api/flowchart/CS/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert concentrations[0]["label"] == "General Curriculum"
    assert any(c["id"] == "ai_ml" for c in concentrations)
    assert any(c["id"] == "privacy_security" for c in concentrations)


def test_get_art_and_design_concentrations_for_major():
    response = client.get("/api/flowchart/AD/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "graphic_design" for c in concentrations)
    assert any(c["id"] == "photo_video" for c in concentrations)
    assert any(c["id"] == "studio_art" for c in concentrations)


def test_get_civil_engineering_concentrations_for_major():
    response = client.get("/api/flowchart/CE/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "construction" for c in concentrations)
    assert any(c["id"] == "geotechnical" for c in concentrations)
    assert any(c["id"] == "structural" for c in concentrations)
    assert any(c["id"] == "transportation" for c in concentrations)
    assert any(c["id"] == "water_resources" for c in concentrations)


def test_get_mechanical_engineering_concentrations_for_major():
    response = client.get("/api/flowchart/ME/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "energy_resources" for c in concentrations)
    assert any(c["id"] == "hvacr" for c in concentrations)
    assert any(c["id"] == "mechatronics" for c in concentrations)
    assert any(c["id"] == "manufacturing" for c in concentrations)


def test_get_concentrations_returns_empty_list_for_major_without_overrides():
    response = client.get("/api/flowchart/AERO/concentrations")

    assert response.status_code == 200
    assert response.json() == {"concentrations": []}


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
