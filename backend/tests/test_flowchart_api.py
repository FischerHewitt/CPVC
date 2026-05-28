from fastapi.testclient import TestClient

from main import _allowed_frontend_origins, app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_allowed_frontend_origins_support_comma_separated_env(monkeypatch):
    monkeypatch.setenv(
        "FRONTEND_URLS",
        "https://mustang-blueprints.vercel.app, https://blueprints.example.edu/",
    )

    assert _allowed_frontend_origins() == [
        "https://mustang-blueprints.vercel.app",
        "https://blueprints.example.edu",
    ]


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
    assert {"code": "POLS", "name": "Political Science"} in majors
    assert {"code": "ENGL", "name": "English"} in majors
    assert {"code": "MU", "name": "Music"} in majors
    assert {"code": "AGC", "name": "Agricultural Communication"} in majors
    assert {"code": "AGS", "name": "Agricultural Science"} in majors
    assert {"code": "ASCI", "name": "Animal Science"} in majors
    assert {"code": "ANTGEOG", "name": "Anthropology and Geography"} in majors
    assert {"code": "ARCH", "name": "Architecture"} in majors
    assert {"code": "BIO", "name": "Biological Sciences"} in majors
    assert {"code": "BMED", "name": "Biomedical Engineering"} in majors


def test_get_flowchart_is_case_insensitive_and_has_expected_shape():
    response = client.get("/api/flowchart/cs")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == "CS"
    assert body["major"] == "Computer Science"
    assert body["total_units"] == 120
    assert body["courses"]
    assert {"year": "Freshman", "term": "Fall"} in body["columns"]


def test_full_flowchart_concentration_inherits_base_major_notes():
    response = client.get("/api/flowchart/CS_DATA_ENG")

    assert response.status_code == 200
    notes_by_title = {
        section["title"]: section["items"]
        for section in response.json()["notes"]
    }
    assert notes_by_title["Flowchart Tips"] == [
        "No Major or Support courses may be selected as credit/no credit. In addition, no more than 12 units of cooperative or internship courses can count towards your degree requirements.",
    ]
    assert notes_by_title["GE Tips"] == [
        "Required in Major or Support; also satisfies General Education (GE) requirement.",
    ]


def test_all_full_flowchart_concentrations_inherit_base_notes_when_available():
    from data.concentrations import CONCENTRATIONS
    from data.flowcharts import FLOWCHARTS

    for base_major, concentrations in CONCENTRATIONS.items():
        base_notes = FLOWCHARTS.get(base_major, {}).get("notes")
        if not base_notes:
            continue

        for concentration in concentrations:
            full_key = concentration.get("full_flowchart_key")
            if not full_key:
                continue

            response = client.get(f"/api/flowchart/{full_key}")
            assert response.status_code == 200
            assert response.json().get("notes") == base_notes


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


def test_get_english_flowchart_is_available():
    response = client.get("/api/flowchart/ENGL")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "English"
    assert body["total_units"] == 120
    assert body["courses"]


def test_get_music_flowchart_is_available():
    response = client.get("/api/flowchart/MU")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Music"
    assert body["total_units"] == 120
    assert body["courses"]


def test_get_agricultural_communication_flowchart_is_available():
    response = client.get("/api/flowchart/AGC")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Agricultural Communication"
    assert body["total_units"] == 120
    assert body["courses"]


def test_get_agricultural_science_flowchart_is_available():
    response = client.get("/api/flowchart/AGS")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Agricultural Science"
    assert body["total_units"] == 120
    assert body["courses"]


def test_get_animal_science_flowchart_is_available():
    response = client.get("/api/flowchart/ASCI")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Animal Science"
    assert body["total_units"] == 120
    assert body["courses"]


def test_get_anthropology_geography_flowchart_is_available():
    response = client.get("/api/flowchart/ANTGEOG")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Anthropology and Geography"
    assert body["total_units"] == 120
    assert body["courses"]


def test_get_architecture_flowchart_is_available():
    response = client.get("/api/flowchart/ARCH")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Architecture"
    assert body["total_units"] == 150
    assert {"year": "Fifth Year", "term": "Spring"} in body["columns"]
    assert body["courses"]


def test_get_biological_sciences_flowchart_is_available():
    response = client.get("/api/flowchart/BIO")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Biological Sciences"
    assert body["total_units"] == 120
    assert body["courses"]


def test_get_biomedical_engineering_flowchart_is_available():
    response = client.get("/api/flowchart/BMED")

    assert response.status_code == 200
    body = response.json()
    assert body["major"] == "Biomedical Engineering"
    assert body["total_units"] == 130
    assert body["courses"]


def test_get_concentrations_for_major():
    response = client.get("/api/flowchart/CS/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert concentrations[0]["label"] == "General Curriculum"
    assert any(c["id"] == "ai_ml" for c in concentrations)
    assert any(c["id"] == "privacy_security" for c in concentrations)


def test_get_aerospace_engineering_concentrations_for_major():
    response = client.get("/api/flowchart/AERO/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "aeronautics" for c in concentrations)
    assert any(c["id"] == "astronautics" for c in concentrations)


def test_get_art_and_design_concentrations_for_major():
    response = client.get("/api/flowchart/AD/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "graphic_design" for c in concentrations)
    assert any(c["id"] == "photo_video" for c in concentrations)
    assert any(c["id"] == "studio_art" for c in concentrations)



def test_get_mechanical_engineering_concentrations_for_major():
    response = client.get("/api/flowchart/ME/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "energy_resources" for c in concentrations)
    assert any(c["id"] == "hvacr" for c in concentrations)
    assert any(c["id"] == "mechatronics" for c in concentrations)
    assert any(c["id"] == "manufacturing" for c in concentrations)


def test_get_political_science_concentrations_for_major():
    response = client.get("/api/flowchart/POLS/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "global_politics" for c in concentrations)
    assert any(c["id"] == "pre_law" for c in concentrations)
    assert any(c["id"] == "us_politics" for c in concentrations)
    assert any(c["id"] == "individualized" for c in concentrations)


def test_get_agricultural_science_emphasis_areas_for_major():
    response = client.get("/api/flowchart/AGS/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "ag_engineering_tech" for c in concentrations)
    assert any(c["id"] == "agribusiness" for c in concentrations)
    assert any(c["id"] == "animal_science" for c in concentrations)
    assert any(c["id"] == "plant_crop_soil" for c in concentrations)
    assert any(c["id"] == "forestry_natural_resources" for c in concentrations)
    assert any(c["id"] == "ornamental_horticulture" for c in concentrations)


def test_get_anthropology_geography_concentrations_for_major():
    response = client.get("/api/flowchart/ANTGEOG/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "environmental_sustainability" for c in concentrations)
    assert any(c["id"] == "global_studies" for c in concentrations)
    assert any(c["id"] == "human_ecology" for c in concentrations)
    assert any(c["id"] == "individualized" for c in concentrations)


def test_get_biological_sciences_concentrations_for_major():
    response = client.get("/api/flowchart/BIO/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "anatomy_physiology" for c in concentrations)
    assert any(c["id"] == "ecology_evolution_biodiversity_conservation" for c in concentrations)
    assert any(c["id"] == "molecular_cellular" for c in concentrations)


def test_get_biomedical_engineering_concentrations_for_major():
    response = client.get("/api/flowchart/BMED/concentrations")

    assert response.status_code == 200
    concentrations = response.json()["concentrations"]
    assert concentrations[0]["id"] == "none"
    assert any(c["id"] == "bioinstrumentation" for c in concentrations)
    assert any(c["id"] == "cell_and_tissue_engineering" for c in concentrations)
    assert any(c["id"] == "mechanical_design" for c in concentrations)
    assert any(c["id"] == "individualized" for c in concentrations)


def test_get_concentrations_returns_empty_list_for_major_without_overrides():
    response = client.get("/api/flowchart/SE/concentrations")
    english_response = client.get("/api/flowchart/ENGL/concentrations")
    music_response = client.get("/api/flowchart/MU/concentrations")
    agc_response = client.get("/api/flowchart/AGC/concentrations")
    animal_science_response = client.get("/api/flowchart/ASCI/concentrations")
    architecture_response = client.get("/api/flowchart/ARCH/concentrations")
    ce_response = client.get("/api/flowchart/CE/concentrations")
    math_response = client.get("/api/flowchart/MATH/concentrations")

    assert response.status_code == 200
    assert response.json() == {"concentrations": []}
    assert english_response.status_code == 200
    assert english_response.json() == {"concentrations": []}
    assert music_response.status_code == 200
    assert music_response.json() == {"concentrations": []}
    assert agc_response.status_code == 200
    assert agc_response.json() == {"concentrations": []}
    assert animal_science_response.status_code == 200
    assert animal_science_response.json() == {"concentrations": []}
    assert architecture_response.status_code == 200
    assert architecture_response.json() == {"concentrations": []}
    assert ce_response.status_code == 200
    assert ce_response.json() == {"concentrations": []}
    assert math_response.status_code == 200
    assert math_response.json() == {"concentrations": []}


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
    assert "MATH 1262/1265" in inferred  # CS uses slash-choice, not bare MATH 1262
    assert "MATH 142" in inferred
    assert "CSC 3449" not in inferred


def test_infer_uses_pre_built_lookup():
    """infer_from_lookup with the module-level pre-built lookup must produce
    the same result as infer_completed, which builds the lookup on each call."""
    from services.inference import build_lookup, infer_completed, infer_from_lookup
    from routers.flowchart import _ALL_COURSES, _ALL_COURSES_LOOKUP

    completed = {"CSC 3449"}
    via_list = infer_completed(completed, _ALL_COURSES)
    via_lookup = infer_from_lookup(completed, _ALL_COURSES_LOOKUP)
    assert via_list == via_lookup


def test_all_courses_lookup_covers_quarter_equivalents():
    """Every quarter equivalent listed on a tile must appear as a key in the
    pre-built lookup so transcript course numbers resolve correctly."""
    from routers.flowchart import _ALL_COURSES, _ALL_COURSES_LOOKUP

    for course in _ALL_COURSES:
        assert course["course_number"] in _ALL_COURSES_LOOKUP
        for q in course["quarter_equivalents"]:
            assert q in _ALL_COURSES_LOOKUP


def test_build_courses_cache_is_populated_on_first_call_and_returns_same_object():
    import services.elective_catalog as ec
    from routers.electives import _build_courses, _build_courses_cache

    key = next(iter(ec.get_dynamic_configs()))
    cfg = ec.get_dynamic_config(key)
    cache_key = (tuple(cfg["depts"]), cfg["min_level"], cfg["max_level"])

    # Ensure cache is warm from previous test module import; result should be cached
    first = _build_courses(cfg["depts"], cfg["min_level"], cfg["max_level"])
    second = _build_courses(cfg["depts"], cfg["min_level"], cfg["max_level"])

    assert first is second  # same list object — cache hit, not rebuilt
    assert cache_key in _build_courses_cache
