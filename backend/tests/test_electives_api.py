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


def test_static_elective_endpoint_returns_ags_catalog_options():
    expectations = {
        "ags_life_science": ["BIO 1111", "BIO 1151", "BOT 1121", "MCRO 2221"],
        "ags_asci_pair": ["ASCI 1102", "ASCI 1103"],
        "ags_soil_science": ["SS 1120", "SS 1130"],
        "ags_dairy_food_safety": ["DSCI 2229", "FSN 2245"],
        "ags_aged_agc_choice": ["AGED 4410", "AGC 3314"],
        "ags_nr_choice": ["NR 3308", "NR 3323"],
        "ags_agc_ag_issues": ["AGC 4452", "AG 4452"],
        "ags_brae_aquaculture_irrigation": ["BRAE 4438", "MSCI 4438", "BRAE 4440"],
    }

    for key, course_numbers in expectations.items():
        response = client.get(f"/api/electives/{key}")

        assert response.status_code == 200
        assert [course["course_number"] for course in response.json()["courses"]] == course_numbers


def test_static_elective_endpoint_returns_asm_catalog_options():
    math_response = client.get("/api/electives/asm_math_elective")
    approved_response = client.get("/api/electives/asm_approved_elective")

    assert math_response.status_code == 200
    assert [course["course_number"] for course in math_response.json()["courses"]] == ["MATH 1007", "STAT 1110"]

    assert approved_response.status_code == 200
    approved_numbers = [course["course_number"] for course in approved_response.json()["courses"]]
    assert "BRAE 3344" in approved_numbers
    assert "CRP 4408" in approved_numbers
    assert "NR 4408" in approved_numbers
    assert "FDSC 1110" in approved_numbers
    assert "SS 2221" in approved_numbers


def test_static_elective_endpoint_returns_asci_catalog_options():
    expectations = {
        "asci_meat_science_pair": ["ASCI 2210", "ASCI 2211"],
        "asci_animal_management": ["ASCI 2230", "ASCI 2231", "ASCI 2232", "ASCI 2233"],
        "asci_nutrition_elective": ["ASCI 3346", "ASCI 3350", "ASCI 3355", "ASCI 4419"],
        "asci_physiology_elective": [
            "ASCI 4403",
            "ASCI 4405",
            "ASCI 4406",
            "ASCI 4438",
            "ASCI 4440",
            "ASCI 4455",
            "DSCI 3321",
            "DSCI 3330",
        ],
        "asci_senior_project": ["ASCI 4477", "ASCI 4478", "ASCI 4479"],
    }

    for key, course_numbers in expectations.items():
        response = client.get(f"/api/electives/{key}")

        assert response.status_code == 200
        assert [course["course_number"] for course in response.json()["courses"]] == course_numbers

    enterprise_response = client.get("/api/electives/asci_enterprise_elective")
    assert enterprise_response.status_code == 200
    enterprise_numbers = [course["course_number"] for course in enterprise_response.json()["courses"]]
    assert "ASCI 2001" in enterprise_numbers
    assert "ASCI 2017" in enterprise_numbers
    assert "ASCI 4015" in enterprise_numbers


def test_static_elective_endpoint_returns_antgeog_catalog_options():
    expectations = {
        "antgeog_physical_geography": ["GEOG 2250", "ERSC 2250"],
        "antgeog_professional_preparation": ["ANT 3384", "GEOG 3384"],
        "antgeog_methods_elective": ["ANT 3310", "ANT 3311", "ANT 3312", "ISLA 3393", "GEOG 3328", "GEOG 4441"],
        "antgeog_internship": ["ANT 4465", "GEOG 4465"],
        "antgeog_regional_geography": ["GEOG 3340", "GEOG 3370", "GEOG 3380"],
        "antgeog_research_design": ["ANT 4455", "GEOG 4455"],
        "antgeog_senior_project_i": ["ANT 4461", "GEOG 4461"],
        "antgeog_senior_project_ii": ["ANT 4462", "GEOG 4462"],
        "antgeog_human_ecology_foundation": ["ANT 3309", "ANT 3320"],
        "antgeog_human_ecology_geog": ["ERSC 3325", "GEOG 3308"],
    }

    for key, course_numbers in expectations.items():
        response = client.get(f"/api/electives/{key}")

        assert response.status_code == 200
        assert [course["course_number"] for course in response.json()["courses"]] == course_numbers


def test_static_elective_endpoint_returns_arce_catalog_options():
    expectations = {
        "arce_hist_elective": ["ARCH 2221", "ARCH 2222", "ARCE 2280"],
        "arce_surveying_elective": ["BRAE 1239", "BRAE 2237", "CM 2239"],
        "arce_fe_technical_elective": ["GEOL 2240", "GEOL 3305", "IME 2315", "MATH 2263", "ME 2212"],
        "arce_caed_interdisciplinary_elective": ["ARCE 4484", "ARCE 4486"],
    }

    for key, course_numbers in expectations.items():
        response = client.get(f"/api/electives/{key}")

        assert response.status_code == 200
        assert [course["course_number"] for course in response.json()["courses"]] == course_numbers


def test_static_elective_endpoint_returns_me_catalog_options():
    expectations = {
        "me_ime_mfg_selective": ["IME 1141", "IME 1142", "IME 1149"],
        "me_life_science": ["BIO 1111", "BIO 2213", "BIO 2215", "BIO 2217"],
        "me_energy_technical_elective": ["EE 3255 & EE 3255L", "EE 4420", "ME 4437", "ME 4438", "ME 4439", "ME 4443", "ME 4444", "ME 4450", "ME 4455", "ME 4488", "ME 5541"],
        "me_mechatronics_technical_elective": ["ME 3313", "ME 4423", "ME 4452", "ME 5305", "ME 5506"],
        "me_manufacturing_elective": ["IME 3331", "IME 3336", "IME 3356", "IME 4418", "IME 4428", "IME 4432", "IME 4435", "IME 4450", "IME 5543", "MATE 4434 & MATE 4435", "ME 3305", "ME 4380", "ME 4480"],
    }

    for key, course_numbers in expectations.items():
        response = client.get(f"/api/electives/{key}")

        assert response.status_code == 200
        assert [course["course_number"] for course in response.json()["courses"]] == course_numbers


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


def test_elective_endpoint_returns_asci_dynamic_range(monkeypatch):
    def fake_dept_courses(dept):
        return {
            f"{dept.upper()} 2999": {"title": "Lower Course", "units": "3"},
            f"{dept.upper()} 3346": {"title": "Upper Course", "units": "3"},
            f"{dept.upper()} 5570": {"title": "Graduate Course", "units": "2"},
            f"{dept.upper()} 6000": {"title": "Too High Course", "units": "3"},
        }

    monkeypatch.setattr(electives_router, "get_dept_courses", fake_dept_courses)

    response = client.get("/api/electives/asci_approved_elective")

    assert response.status_code == 200
    assert [course["course_number"] for course in response.json()["courses"]] == [
        "ASCI 3346",
        "ASCI 5570",
        "DSCI 3346",
        "DSCI 5570",
    ]


def test_elective_endpoint_returns_antgeog_dynamic_ranges(monkeypatch):
    def fake_dept_courses(dept):
        return {
            f"{dept.upper()} 2201": {"title": "Lower Course", "units": "3"},
            f"{dept.upper()} 3308": {"title": "Upper Course", "units": "3"},
            f"{dept.upper()} 4455": {"title": "Senior Course", "units": "4"},
        }

    monkeypatch.setattr(electives_router, "get_dept_courses", fake_dept_courses)

    ant_response = client.get("/api/electives/antgeog_ant_elective")
    broad_response = client.get("/api/electives/antgeog_ant_geog_soc_elective")

    assert ant_response.status_code == 200
    assert [course["course_number"] for course in ant_response.json()["courses"]] == ["ANT 3308", "ANT 4455"]

    assert broad_response.status_code == 200
    assert [course["course_number"] for course in broad_response.json()["courses"]] == [
        "ANT 3308",
        "ANT 4455",
        "GEOG 3308",
        "GEOG 4455",
        "SOC 3308",
        "SOC 4455",
    ]


def test_elective_endpoint_returns_arch_professional_elective_options(monkeypatch):
    monkeypatch.setattr(
        electives_router,
        "get_dept_courses",
        lambda dept: {
            f"{dept.upper()} 0999": {"title": "Too Low Course", "units": "3"},
            f"{dept.upper()} 1101": {"title": "Lower Course", "units": "4"},
            f"{dept.upper()} 3341": {"title": "Upper Course", "units": "3"},
            f"{dept.upper()} 5570": {"title": "Graduate Course", "units": "2"},
        },
    )

    response = client.get("/api/electives/arch_professional_elective")

    assert response.status_code == 200
    assert [course["course_number"] for course in response.json()["courses"]] == [
        "ARCH 1101",
        "ARCH 3341",
        "ARCE 1101",
        "ARCE 3341",
        "ART 1101",
        "ART 3341",
        "CM 1101",
        "CM 3341",
        "CRP 1101",
        "CRP 3341",
        "EDES 1101",
        "EDES 3341",
        "LA 1101",
        "LA 3341",
    ]


def test_elective_endpoint_returns_me_dynamic_range(monkeypatch):
    def fake_dept_courses(dept):
        return {
            f"{dept.upper()} 2201": {"title": "Lower Course", "units": "3"},
            f"{dept.upper()} 3305": {"title": "Upper Course", "units": "4"},
            f"{dept.upper()} 5570": {"title": "Graduate Course", "units": "3"},
            f"{dept.upper()} 6000": {"title": "Too High Course", "units": "3"},
        }

    monkeypatch.setattr(electives_router, "get_dept_courses", fake_dept_courses)

    response = client.get("/api/electives/me_tech_elective")

    assert response.status_code == 200
    course_numbers = [course["course_number"] for course in response.json()["courses"]]
    assert "ME 3305" in course_numbers
    assert "ME 5570" in course_numbers
    assert "AERO 3305" in course_numbers
    assert "MATE 5570" in course_numbers
    assert "ME 2201" not in course_numbers
    assert "ME 6000" not in course_numbers


def test_elective_endpoint_returns_arce_dynamic_range(monkeypatch):
    monkeypatch.setattr(
        electives_router,
        "get_dept_courses",
        lambda dept: {
            f"{dept.upper()} 2280": {"title": "Lower Course", "units": "3"},
            f"{dept.upper()} 3311": {"title": "Upper Course", "units": "3"},
            f"{dept.upper()} 5570": {"title": "Graduate Course", "units": "2"},
            f"{dept.upper()} 6000": {"title": "Too High Course", "units": "3"},
        },
    )

    response = client.get("/api/electives/arce_upper_division_elective")

    assert response.status_code == 200
    assert [course["course_number"] for course in response.json()["courses"]] == ["ARCE 3311", "ARCE 5570"]


def test_elective_endpoint_returns_404_for_unknown_key():
    response = client.get("/api/electives/not-real")

    assert response.status_code == 404


def test_elective_endpoint_returns_chem_catalog_options():
    response = client.get("/api/electives/chem_research_or_methods")
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "chem_research_or_methods"
    course_numbers = [c["course_number"] for c in data["courses"]]
    assert "CHEM 2201" in course_numbers
    assert "CHEM 2203" in course_numbers

    response2 = client.get("/api/electives/chem_subdiscipline_elective")
    assert response2.status_code == 200
    data2 = response2.json()
    subdiscipline_numbers = [c["course_number"] for c in data2["courses"]]
    assert "CHEM 4430" in subdiscipline_numbers
    assert "CHEM 2244" in subdiscipline_numbers
    assert "CHEM 4480" in subdiscipline_numbers


def test_elective_endpoint_returns_cd_catalog_options():
    # Static: foundational course options
    response = client.get("/api/electives/cd_foundational_course")
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "cd_foundational_course"
    course_numbers = [c["course_number"] for c in data["courses"]]
    assert "CD 1131" in course_numbers
    assert "CD 2202" in course_numbers
    assert "CD 2254" in course_numbers

    # Static: life stage development options
    response2 = client.get("/api/electives/cd_lifestage_elective")
    assert response2.status_code == 200
    data2 = response2.json()
    ls_numbers = [c["course_number"] for c in data2["courses"]]
    assert "CD 3304" in ls_numbers
    assert "CD 3305" in ls_numbers
    assert "CD 3306" in ls_numbers

    # Dynamic: upper-div CD electives
    response3 = client.get("/api/electives/cd_upper_div_elective")
    assert response3.status_code == 200
    data3 = response3.json()
    upper_numbers = [c["course_number"] for c in data3["courses"]]
    assert any(n.startswith("CD ") for n in upper_numbers)

    # Static: DEI and professional skills
    response4 = client.get("/api/electives/cd_dei_elective")
    assert response4.status_code == 200
    dei_numbers = [c["course_number"] for c in response4.json()["courses"]]
    assert "ES 3380" in dei_numbers
    assert "WGQS 3351" in dei_numbers

    response5 = client.get("/api/electives/cd_professional_skills")
    assert response5.status_code == 200
    prof_numbers = [c["course_number"] for c in response5.json()["courses"]]
    assert "COMS 3316" in prof_numbers
    assert "PSY 3304" in prof_numbers

    # Static: internship options
    response6 = client.get("/api/electives/cd_internship_i")
    assert response6.status_code == 200
    intern_numbers = [c["course_number"] for c in response6.json()["courses"]]
    assert "CD 4448" in intern_numbers
    assert "CD 4453" in intern_numbers


def test_elective_endpoint_returns_crp_catalog_options():
    # Stat/Data support
    response = client.get("/api/electives/crp_stat_data_support")
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "crp_stat_data_support"
    course_numbers = [c["course_number"] for c in data["courses"]]
    assert "DATA 1000" in course_numbers
    assert "STAT 1110" in course_numbers

    # Senior project options
    response2 = client.get("/api/electives/crp_senior_project")
    assert response2.status_code == 200
    senior_numbers = [c["course_number"] for c in response2.json()["courses"]]
    assert "CRP 4461" in senior_numbers
    assert "CRP 4463" in senior_numbers

    # CAED designated electives
    response3 = client.get("/api/electives/crp_caed_elective")
    assert response3.status_code == 200
    caed_numbers = [c["course_number"] for c in response3.json()["courses"]]
    assert "CRP 3303" in caed_numbers
    assert "CRP 4448" in caed_numbers
    assert "LA 4410" in caed_numbers
    assert "CM 3317" in caed_numbers
    assert "EDES 3350" in caed_numbers


def test_elective_endpoint_returns_ee_options():
    # Senior project lab I choices
    r1 = client.get("/api/electives/ee_senior_proj_lab_i")
    assert r1.status_code == 200
    lab_i = [c["course_number"] for c in r1.json()["courses"]]
    assert "EE 4463" in lab_i
    assert "EE 4465" in lab_i

    # Senior project lab II choices
    r2 = client.get("/api/electives/ee_senior_proj_lab_ii")
    assert r2.status_code == 200
    lab_ii = [c["course_number"] for c in r2.json()["courses"]]
    assert "EE 4464" in lab_ii
    assert "EE 4466" in lab_ii

    # Dynamic technical elective (EE 4000+ level courses)
    r3 = client.get("/api/electives/ee_technical_elective")
    assert r3.status_code == 200
    tech = r3.json()
    assert len(tech["courses"]) > 0
    assert all(c["course_number"].startswith("EE ") for c in tech["courses"])


def test_elective_endpoint_returns_ie_options():
    # Intro lab choices
    r1 = client.get("/api/electives/ie_intro_lab")
    assert r1.status_code == 200
    labs = [c["course_number"] for c in r1.json()["courses"]]
    assert "IME 1141" in labs
    assert "IME 1142" in labs

    # Linear math choices
    r2 = client.get("/api/electives/ie_linear_math")
    assert r2.status_code == 200
    math_opts = [c["course_number"] for c in r2.json()["courses"]]
    assert "MATH 1151" in math_opts
    assert "MATH 2341" in math_opts

    # Support elective
    r3 = client.get("/api/electives/ie_support_elective")
    assert r3.status_code == 200
    support = [c["course_number"] for c in r3.json()["courses"]]
    assert "ENGR 2211" in support

    # Technical elective (dynamic)
    r4 = client.get("/api/electives/ie_technical_elective")
    assert r4.status_code == 200
    assert len(r4.json()["courses"]) > 0


def test_elective_endpoint_returns_mate_options():
    # Chemistry choice
    r1 = client.get("/api/electives/mate_chem_elective")
    assert r1.status_code == 200
    chem = [c["course_number"] for c in r1.json()["courses"]]
    assert "CHEM 1122" in chem
    assert "CHEM 2240" in chem

    # Design elective
    r2 = client.get("/api/electives/mate_design_elective")
    assert r2.status_code == 200
    design = [c["course_number"] for c in r2.json()["courses"]]
    assert "IME 3326" in design
    assert "ME 3234" in design

    # Technical elective (dynamic MATE 4000+)
    r3 = client.get("/api/electives/mate_technical_elective")
    assert r3.status_code == 200
    assert len(r3.json()["courses"]) > 0
    assert all(c["course_number"].startswith("MATE ") for c in r3.json()["courses"])


def test_elective_endpoint_returns_math_options():
    # Programming elective
    r1 = client.get("/api/electives/math_programming_elective")
    assert r1.status_code == 200
    prog = [c["course_number"] for c in r1.json()["courses"]]
    assert "CSC 2001" in prog
    assert "MATH 3681" in prog
    assert "STAT 2610" in prog

    # Senior project
    r2 = client.get("/api/electives/math_senior_project")
    assert r2.status_code == 200
    senior = [c["course_number"] for c in r2.json()["courses"]]
    assert "MATH 4463" in senior
    assert "MATH 4464" in senior

    # Upper-division GE choice
    r3 = client.get("/api/electives/math_upper_div_choice")
    assert r3.status_code == 200
    ud = [c["course_number"] for c in r3.json()["courses"]]
    assert "MATH 3051" in ud
    assert "MATH 3111" in ud
    assert "MATH 3301" in ud

    # Track elective (general/applied)
    r4 = client.get("/api/electives/math_track_elective")
    assert r4.status_code == 200
    track = [c["course_number"] for c in r4.json()["courses"]]
    assert "MATH 4265" in track
    assert "MATH 4911" in track
    assert len(track) >= 15

    # Teaching track elective (adds MATH 3971, 4972)
    r5 = client.get("/api/electives/math_track_teaching")
    assert r5.status_code == 200
    teaching = [c["course_number"] for c in r5.json()["courses"]]
    assert "MATH 3971" in teaching
    assert "MATH 4972" in teaching


def test_elective_endpoint_returns_kine_options():
    # HLTH choice
    r1 = client.get("/api/electives/kine_hlth_choice")
    assert r1.status_code == 200
    hlth = [c["course_number"] for c in r1.json()["courses"]]
    assert "HLTH 1155" in hlth
    assert "HLTH 1160" in hlth

    # Cultural course
    r2 = client.get("/api/electives/kine_cultural_course")
    assert r2.status_code == 200
    cultural = [c["course_number"] for c in r2.json()["courses"]]
    assert "KINE 3323" in cultural
    assert "KINE 3325" in cultural

    # Senior project
    r3 = client.get("/api/electives/kine_senior_project")
    assert r3.status_code == 200
    senior = [c["course_number"] for c in r3.json()["courses"]]
    assert "KINE 4461" in senior

    # ES elective
    r4 = client.get("/api/electives/kine_es_elective")
    assert r4.status_code == 200
    es = [c["course_number"] for c in r4.json()["courses"]]
    assert "KINE 2278" in es
    assert "KINE 4408" in es

    # HP elective
    r5 = client.get("/api/electives/kine_hp_elective")
    assert r5.status_code == 200
    hp = [c["course_number"] for c in r5.json()["courses"]]
    assert "HLTH 4435" in hp
    assert "KINE 3349" in hp

    # SS elective
    r6 = client.get("/api/electives/kine_ss_elective")
    assert r6.status_code == 200
    ss = [c["course_number"] for c in r6.json()["courses"]]
    assert "COMS 3387" in ss
    assert "EIM 2260" in ss


def test_elective_endpoint_returns_fsn_options():
    # Senior project
    r1 = client.get("/api/electives/fsn_senior_project")
    assert r1.status_code == 200
    senior = [c["course_number"] for c in r1.json()["courses"]]
    assert "FDSC 4461" in senior
    assert "FDSC 4462" in senior

    # Food safety elective
    r2 = client.get("/api/electives/fsn_fs_elective")
    assert r2.status_code == 200
    fs = [c["course_number"] for c in r2.json()["courses"]]
    assert "FDSC 5545" in fs
    assert "MCRO 3342" in fs

    # SFT elective
    r3 = client.get("/api/electives/fsn_sft_elective")
    assert r3.status_code == 200
    sft = [c["course_number"] for c in r3.json()["courses"]]
    assert "BRAE 3348" in sft
    assert "NR 3324" in sft
