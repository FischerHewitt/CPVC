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


def test_elective_endpoint_returns_mfge_options():
    # Linear math choice
    r1 = client.get("/api/electives/mfge_linear_math")
    assert r1.status_code == 200
    lin = [c["course_number"] for c in r1.json()["courses"]]
    assert "MATH 1151" in lin
    assert "MATH 2341" in lin


def test_elective_endpoint_returns_phys_options():
    # Lab elective (static)
    r1 = client.get("/api/electives/phys_lab_elective")
    assert r1.status_code == 200
    lab = [c["course_number"] for c in r1.json()["courses"]]
    assert "PHYS 3323" in lab
    assert "PHYS 4425" in lab
    assert "ASTR 4444" in lab


def test_elective_endpoint_returns_jour_options():
    # Stats choice
    r1 = client.get("/api/electives/jour_stat_choice")
    assert r1.status_code == 200
    stats = [c["course_number"] for c in r1.json()["courses"]]
    assert "STAT 1000" in stats
    assert "STAT 1110" in stats
    assert "STAT 1210" in stats

    # Cross-cultural slash choice
    r2 = client.get("/api/electives/jour_crosscultural")
    assert r2.status_code == 200
    cross = [c["course_number"] for c in r2.json()["courses"]]
    assert "JOUR 2219" in cross
    assert "JOUR 3319" in cross

    # MI method choice
    r3 = client.get("/api/electives/jour_mi_method")
    assert r3.status_code == 200
    mi = [c["course_number"] for c in r3.json()["courses"]]
    assert "JOUR 3345" in mi
    assert "JOUR 3310" in mi

    # News elective
    r4 = client.get("/api/electives/jour_news_elective")
    assert r4.status_code == 200
    news = [c["course_number"] for c in r4.json()["courses"]]
    assert "JOUR 3307" in news
    assert "JOUR 3350" in news
    assert "JOUR 3353" in news

    # PR or-choice
    r5 = client.get("/api/electives/jour_pr_or_choice")
    assert r5.status_code == 200
    pr = [c["course_number"] for c in r5.json()["courses"]]
    assert "JOUR 3314" in pr
    assert "JOUR 3345" in pr


def test_elective_endpoint_returns_cm_options():
    # Accounting slash choice
    r1 = client.get("/api/electives/cm_accounting_choice")
    assert r1.status_code == 200
    acct = [c["course_number"] for c in r1.json()["courses"]]
    assert "BUS 2212" in acct
    assert "BUS 2214" in acct

    # Major elective list
    r2 = client.get("/api/electives/cm_major_elective")
    assert r2.status_code == 200
    elec = [c["course_number"] for c in r2.json()["courses"]]
    assert "CM 4421" in elec
    assert "CM 4475" in elec
    assert "CRP 4442" in elec
    assert "LA 4410" in elec

    # Business elective (dynamic)
    r3 = client.get("/api/electives/cm_bus_elective")
    assert r3.status_code == 200
    bus = r3.json()["courses"]
    assert len(bus) > 0


def test_elective_endpoint_returns_soc_options():
    # WI elective (static)
    r1 = client.get("/api/electives/soc_wi_elective")
    assert r1.status_code == 200
    wi = [c["course_number"] for c in r1.json()["courses"]]
    assert "SOC 3315" in wi
    assert "SOC 3321" in wi
    assert "SOC 3326" in wi
    assert "SOC 3343" in wi

    # Generic SOC upper-div elective (dynamic)
    r2 = client.get("/api/electives/soc_elective")
    assert r2.status_code == 200
    elec = [c["course_number"] for c in r2.json()["courses"]]
    assert "SOC 3353" in elec or "SOC 3302" in elec  # at least one 3000-level SOC course

    # Lower-division social sciences support elective (dynamic, multi-dept)
    r3 = client.get("/api/electives/soc_ld_support")
    assert r3.status_code == 200
    ld = r3.json()["courses"]
    assert len(ld) > 0

    # CJ required choice
    r4 = client.get("/api/electives/soc_cj_req_choice")
    assert r4.status_code == 200
    cj_req = [c["course_number"] for c in r4.json()["courses"]]
    assert "SOC 4402" in cj_req
    assert "SOC 4412" in cj_req

    # CJ elective
    r5 = client.get("/api/electives/soc_cj_elective")
    assert r5.status_code == 200
    cj = [c["course_number"] for c in r5.json()["courses"]]
    assert "SOC 3303" in cj
    assert "SOC 4406" in cj
    assert "SOC 4414" in cj

    # Organizations core choice
    r6 = client.get("/api/electives/soc_org_core")
    assert r6.status_code == 200
    org = [c["course_number"] for c in r6.json()["courses"]]
    assert "SOC 3395" in org
    assert "SOC 4423" in org

    # Social Justice required
    r7 = client.get("/api/electives/soc_sj_req")
    assert r7.status_code == 200
    sj = [c["course_number"] for c in r7.json()["courses"]]
    assert "SOC 3305" in sj
    assert "SOC 4402" in sj
    assert "SOC 4444" in sj

    # Social Services elective
    r8 = client.get("/api/electives/soc_ss_elective")
    assert r8.status_code == 200
    ss = [c["course_number"] for c in r8.json()["courses"]]
    assert "SOC 3303" not in ss  # fixed course, not in elective pool
    assert "SOC 3395" in ss
    assert "SOC 4435" in ss


def test_elective_endpoint_returns_la_options():
    # Plant biology choice
    r1 = client.get("/api/electives/la_bio_choice")
    assert r1.status_code == 200
    bio = [c["course_number"] for c in r1.json()["courses"]]
    assert "BIO 1114" in bio
    assert "BOT 1121" in bio

    # Designated Elective Group 1
    r2 = client.get("/api/electives/la_des_elec1")
    assert r2.status_code == 200
    de1 = [c["course_number"] for c in r2.json()["courses"]]
    assert "STAT 1110" in de1
    assert "SS 1120" in de1

    # Designated Elective Group 2
    r3 = client.get("/api/electives/la_des_elec2")
    assert r3.status_code == 200
    de2 = [c["course_number"] for c in r3.json()["courses"]]
    assert "BIO 2215" in de2
    assert "GEOL 2240" in de2

    # Designated Elective Group 3
    r4 = client.get("/api/electives/la_des_elec3")
    assert r4.status_code == 200
    de3 = [c["course_number"] for c in r4.json()["courses"]]
    assert "BOT 3326" in de3
    assert "NR 3310" in de3
    assert "PLSC 3334" in de3

    # CAED Theory elective
    r5 = client.get("/api/electives/la_caed_theory")
    assert r5.status_code == 200
    theory = [c["course_number"] for c in r5.json()["courses"]]
    assert "ARCE 2280" in theory
    assert "CRP 4448" in theory

    # CAED Finance elective
    r6 = client.get("/api/electives/la_caed_finance")
    assert r6.status_code == 200
    finance = [c["course_number"] for c in r6.json()["courses"]]
    assert "CM 4475" in finance
    assert "CRP 4420" in finance
    assert "LA 5531" in finance

    # CAED Sustainability elective
    r7 = client.get("/api/electives/la_caed_sustain")
    assert r7.status_code == 200
    sustain = [c["course_number"] for c in r7.json()["courses"]]
    assert "CM 3317" in sustain
    assert "LA 5520" in sustain

    # Professional Topics elective
    r8 = client.get("/api/electives/la_pro_topics")
    assert r8.status_code == 200
    topics = [c["course_number"] for c in r8.json()["courses"]]
    assert "LA 4414" in topics
    assert "LA 4418" in topics

    # Design Studio choice
    r9 = client.get("/api/electives/la_studio_choice")
    assert r9.status_code == 200
    studio = [c["course_number"] for c in r9.json()["courses"]]
    assert "LA 4422" in studio
    assert "LA 4424" in studio


def test_elective_endpoint_returns_wvit_options():
    # Math choice
    r1 = client.get("/api/electives/wvit_math_choice")
    assert r1.status_code == 200
    math_courses = [c["course_number"] for c in r1.json()["courses"]]
    assert "MATH 1261" in math_courses
    assert "MATH 1267" in math_courses

    # Accounting choice
    r2 = client.get("/api/electives/wvit_accounting_choice")
    assert r2.status_code == 200
    acct = [c["course_number"] for c in r2.json()["courses"]]
    assert "AGB 2214" in acct
    assert "BUS 2214" in acct

    # Wine Business micro/econ choice
    r3 = client.get("/api/electives/wvit_wb_micro_choice")
    assert r3.status_code == 200
    micro = [c["course_number"] for c in r3.json()["courses"]]
    assert "AGB 2212" in micro
    assert "ECON 2030" in micro

    # Wine Business HR choice
    r4 = client.get("/api/electives/wvit_wb_hr_choice")
    assert r4.status_code == 200
    hr = [c["course_number"] for c in r4.json()["courses"]]
    assert "AGB 3369" in hr
    assert "BUS 3384" in hr

    # Senior project choice
    r5 = client.get("/api/electives/wvit_senior_project")
    assert r5.status_code == 200
    sp = [c["course_number"] for c in r5.json()["courses"]]
    assert "WVIT 4464" in sp
    assert "WVIT 4465" in sp


def test_elective_endpoint_returns_econ_options():
    client = TestClient(app)

    # Intro micro/survey choice
    r1 = client.get("/api/electives/econ_intro_choice")
    assert r1.status_code == 200
    intro = [c["course_number"] for c in r1.json()["courses"]]
    assert "ECON 2030" in intro
    assert "ECON 2001" in intro

    # Macro choice
    r2 = client.get("/api/electives/econ_macro_choice")
    assert r2.status_code == 200
    macro = [c["course_number"] for c in r2.json()["courses"]]
    assert "ECON 2040" in macro
    assert "ECON 2021" in macro

    # BUS intro choice
    r3 = client.get("/api/electives/econ_bus_choice")
    assert r3.status_code == 200
    bus = [c["course_number"] for c in r3.json()["courses"]]
    assert "BUS 2207" in bus
    assert "BUS 2214" in bus

    # Accounting concentration electives
    r4 = client.get("/api/electives/econ_accounting_elective")
    assert r4.status_code == 200
    acct = [c["course_number"] for c in r4.json()["courses"]]
    assert "BUS 4424" in acct
    assert "BUS 4428" in acct

    # Project elective (dynamic — should return ECON courses)
    r5 = client.get("/api/electives/econ_project_elective")
    assert r5.status_code == 200
    proj = r5.json()["courses"]
    assert len(proj) > 0
    assert all(c["course_number"].startswith("ECON") for c in proj)

    # Info systems project picker
    r6 = client.get("/api/electives/econ_info_sys_project")
    assert r6.status_code == 200
    isp = [c["course_number"] for c in r6.json()["courses"]]
    assert "BUS 4497" in isp

    # Management HR project picker
    r7 = client.get("/api/electives/econ_mgmt_hr_project")
    assert r7.status_code == 200
    mhr = [c["course_number"] for c in r7.json()["courses"]]
    assert "BUS 4477" in mhr



def test_elective_endpoint_returns_coms_options():
    client = TestClient(app)

    # Public speaking choice
    r1 = client.get("/api/electives/coms_public_speaking")
    assert r1.status_code == 200
    ps = [c["course_number"] for c in r1.json()["courses"]]
    assert "COMS 1101" in ps
    assert "COMS 1102" in ps

    # Interpersonal/org/media/group choice
    r2 = client.get("/api/electives/coms_interp_choice")
    assert r2.status_code == 200
    interp = [c["course_number"] for c in r2.json()["courses"]]
    assert "COMS 2211" in interp
    assert "COMS 2213" in interp
    assert "COMS 2215" in interp
    assert "COMS 2217" in interp

    # Advocacy choice
    r3 = client.get("/api/electives/coms_advocacy_choice")
    assert r3.status_code == 200
    adv = [c["course_number"] for c in r3.json()["courses"]]
    assert "COMS 2250" in adv
    assert "COMS 2208" in adv

    # Research methods choice
    r4 = client.get("/api/electives/coms_research_methods")
    assert r4.status_code == 200
    res = [c["course_number"] for c in r4.json()["courses"]]
    assert "COMS 3312" in res
    assert "COMS 3313" in res

    # Criticism choice
    r5 = client.get("/api/electives/coms_criticism_choice")
    assert r5.status_code == 200
    crit = [c["course_number"] for c in r5.json()["courses"]]
    assert "COMS 3332" in crit
    assert "COMS 3385" in crit

    # Upper-div elective (dynamic)
    r6 = client.get("/api/electives/coms_upper_div_elective")
    assert r6.status_code == 200
    ud = r6.json()["courses"]
    assert len(ud) > 0
    assert all(c["course_number"].startswith("COMS") for c in ud)

    # Focus area base elective (dynamic)
    r7 = client.get("/api/electives/coms_focus_elective")
    assert r7.status_code == 200
    focus = r7.json()["courses"]
    assert len(focus) > 0

    # Culture, Identity, and Power focus area (static)
    r8 = client.get("/api/electives/coms_focus_culture")
    assert r8.status_code == 200
    culture = [c["course_number"] for c in r8.json()["courses"]]
    assert "COMS 3319" in culture
    assert "COMS 4421" in culture

    # Media and Technology focus area (static)
    r9 = client.get("/api/electives/coms_focus_media")
    assert r9.status_code == 200
    media = [c["course_number"] for c in r9.json()["courses"]]
    assert "COMS 3317" in media
    assert "COMS 3384" in media

    # Persuasion focus area (static)
    r10 = client.get("/api/electives/coms_focus_persuasion")
    assert r10.status_code == 200
    persuasion = [c["course_number"] for c in r10.json()["courses"]]
    assert "COMS 3305" in persuasion
    assert "COMS 4435" in persuasion

    # Politics focus area (static)
    r11 = client.get("/api/electives/coms_focus_politics")
    assert r11.status_code == 200
    politics = [c["course_number"] for c in r11.json()["courses"]]
    assert "COMS 3390" in politics
    assert "COMS 4435" in politics

    # Relationships focus area (static)
    r12 = client.get("/api/electives/coms_focus_relationships")
    assert r12.status_code == 200
    rels = [c["course_number"] for c in r12.json()["courses"]]
    assert "COMS 4413" in rels
    assert "COMS 4428" in rels


def test_elective_endpoint_returns_grc_options():
    client = TestClient(app)

    # Senior project choice
    r1 = client.get("/api/electives/grc_senior_project")
    assert r1.status_code == 200
    sp = [c["course_number"] for c in r1.json()["courses"]]
    assert "GRC 4461" in sp
    assert "GRC 4462" in sp
    assert "GRC 4463" in sp

    # Concentration elective (dynamic)
    r2 = client.get("/api/electives/grc_concentration_elective")
    assert r2.status_code == 200
    conc = r2.json()["courses"]
    assert len(conc) > 0
    assert all(c["course_number"].startswith("GRC") for c in conc)

    # Design Reproduction Technology elective
    r3 = client.get("/api/electives/grc_design_elective")
    assert r3.status_code == 200
    drt = [c["course_number"] for c in r3.json()["courses"]]
    assert "GRC 4550" in drt
    assert "ART 1103" in drt

    # Management concentration elective
    r4 = client.get("/api/electives/grc_mgmt_elective")
    assert r4.status_code == 200
    mgmt = [c["course_number"] for c in r4.json()["courses"]]
    assert "BUS 3310" in mgmt
    assert "GRC 3270" in mgmt

    # Packaging concentration elective
    r5 = client.get("/api/electives/grc_packaging_elective")
    assert r5.status_code == 200
    pkg = [c["course_number"] for c in r5.json()["courses"]]
    assert "ITP 3334" in pkg

    # Immersive Experience Design elective
    r6 = client.get("/api/electives/grc_immersive_elective")
    assert r6.status_code == 200
    ied = [c["course_number"] for c in r6.json()["courses"]]
    assert "GRC 3990" in ied
    assert "GRC 4900" in ied

    # UX/UI elective
    r7 = client.get("/api/electives/grc_uxui_elective")
    assert r7.status_code == 200
    uxui = [c["course_number"] for c in r7.json()["courses"]]
    assert "GRC 4290" in uxui
    assert "COMS 3317" in uxui


def test_elective_endpoint_returns_grc_options():
    client = TestClient(app)

    # Senior project (static)
    r1 = client.get("/api/electives/grc_senior_project")
    assert r1.status_code == 200
    sp = [c["course_number"] for c in r1.json()["courses"]]
    assert "GRC 4461" in sp
    assert "GRC 4462" in sp
    assert "GRC 4463" in sp

    # Concentration elective (dynamic)
    r2 = client.get("/api/electives/grc_concentration_elective")
    assert r2.status_code == 200
    ce = r2.json()["courses"]
    assert len(ce) > 0
    assert all(c["course_number"].startswith("GRC") for c in ce)

    # Design Reproduction Technology elective
    r3 = client.get("/api/electives/grc_design_elective")
    assert r3.status_code == 200
    de = [c["course_number"] for c in r3.json()["courses"]]
    assert "GRC 4550" in de
    assert "ART 1103" in de

    # GRC Management elective
    r4 = client.get("/api/electives/grc_mgmt_elective")
    assert r4.status_code == 200
    me = [c["course_number"] for c in r4.json()["courses"]]
    assert "BUS 3310" in me
    assert "GRC 4600" not in me  # fixed, not an elective

    # Graphics for Packaging elective
    r5 = client.get("/api/electives/grc_packaging_elective")
    assert r5.status_code == 200
    pe = [c["course_number"] for c in r5.json()["courses"]]
    assert "ITP 3334" in pe

    # Immersive Experience Design elective
    r6 = client.get("/api/electives/grc_immersive_elective")
    assert r6.status_code == 200
    ie = [c["course_number"] for c in r6.json()["courses"]]
    assert "GRC 3990" in ie

    # UX/UI elective
    r7 = client.get("/api/electives/grc_uxui_elective")
    assert r7.status_code == 200
    ue = [c["course_number"] for c in r7.json()["courses"]]
    assert "COMS 3317" in ue
    assert "GRC 4290" in ue


def test_elective_endpoint_returns_enve_options():
    client = TestClient(app)

    # CE technical elective (static)
    r1 = client.get("/api/electives/enve_ce_elective")
    assert r1.status_code == 200
    ce = [c["course_number"] for c in r1.json()["courses"]]
    assert "CE 3321" in ce
    assert "CE 5537" in ce

    # ENVE technical elective (dynamic)
    r2 = client.get("/api/electives/enve_tech_elective")
    assert r2.status_code == 200
    te = r2.json()["courses"]
    assert len(te) > 0
    assert all(c["course_number"].startswith("ENVE") for c in te)


def test_elective_endpoint_returns_enve_options():
    client = TestClient(app)

    # ENVE tech elective (dynamic)
    r1 = client.get("/api/electives/enve_tech_elective")
    assert r1.status_code == 200
    enve = r1.json()["courses"]
    assert len(enve) > 0
    assert all(c["course_number"].startswith("ENVE") for c in enve)

    # CE tech elective (static)
    r2 = client.get("/api/electives/enve_ce_elective")
    assert r2.status_code == 200
    ce = [c["course_number"] for c in r2.json()["courses"]]
    assert "CE 3381" in ce
    assert "CE 4434" in ce
    assert "CE 5537" in ce
    assert "CE 4474" in ce


def test_elective_endpoint_returns_eim_options():
    client = TestClient(app)

    # Math choice
    r1 = client.get("/api/electives/eim_math_elective")
    assert r1.status_code == 200
    math = [c["course_number"] for c in r1.json()["courses"]]
    assert "MATH 1004" in math
    assert "MATH 1267" in math

    # Financial accounting choice
    r2 = client.get("/api/electives/eim_acct_choice")
    assert r2.status_code == 200
    acct = [c["course_number"] for c in r2.json()["courses"]]
    assert "BUS 2212" in acct
    assert "AGB 2214" in acct

    # Statistics choice
    r3 = client.get("/api/electives/eim_stat_choice")
    assert r3.status_code == 200
    stat = [c["course_number"] for c in r3.json()["courses"]]
    assert "STAT 1110" in stat
    assert "STAT 1210" in stat

    # Managerial accounting choice
    r4 = client.get("/api/electives/eim_mgmt_acct_choice")
    assert r4.status_code == 200
    mgmt = [c["course_number"] for c in r4.json()["courses"]]
    assert "BUS 2215" in mgmt
    assert "AGB 3323" in mgmt

    # Senior project choice
    r5 = client.get("/api/electives/eim_senior_project")
    assert r5.status_code == 200
    sp = [c["course_number"] for c in r5.json()["courses"]]
    assert "EIM 4460" in sp
    assert "EIM 4461" in sp

    # Concentration elective (dynamic)
    r6 = client.get("/api/electives/eim_concentration_elective")
    assert r6.status_code == 200
    conc = r6.json()["courses"]
    assert len(conc) > 0

    # Event planning elective
    r7 = client.get("/api/electives/eim_event_elective")
    assert r7.status_code == 200
    event = [c["course_number"] for c in r7.json()["courses"]]
    assert "EIM 3321" in event
    assert "EIM 3323" in event

    # Sport intro slash choice
    r8 = client.get("/api/electives/eim_sport_intro_choice")
    assert r8.status_code == 200
    intro = [c["course_number"] for c in r8.json()["courses"]]
    assert "EIM 1112" in intro
    assert "EIM 1160" in intro

    # Tourism elective
    r9 = client.get("/api/electives/eim_tourism_elective")
    assert r9.status_code == 200
    tourism = [c["course_number"] for c in r9.json()["courses"]]
    assert "EIM 3321" in tourism
    assert "EIM 4450" in tourism


def test_elective_endpoint_returns_hist_options():
    # LD elective (dynamic — HIST 2000-2999)
    r1 = client.get("/api/electives/hist_ld_elective")
    assert r1.status_code == 200
    ld = r1.json()["courses"]
    assert len(ld) > 0

    # UD elective (dynamic — HIST 3000-4999)
    r2 = client.get("/api/electives/hist_ud_elective")
    assert r2.status_code == 200
    ud = r2.json()["courses"]
    assert len(ud) > 0

    # Global history elective (dynamic — HIST 3000-4999)
    r3 = client.get("/api/electives/hist_global_elective")
    assert r3.status_code == 200
    glob = r3.json()["courses"]
    assert len(glob) > 0

    # World language requirement (static — 7 options at 4 units each)
    r4 = client.get("/api/electives/hist_lang_elective")
    assert r4.status_code == 200
    lang_nums = [c["course_number"] for c in r4.json()["courses"]]
    assert "CHIN 2201" in lang_nums
    assert "FR 2201"   in lang_nums
    assert "GER 2201"  in lang_nums
    assert "ITAL 2201" in lang_nums
    assert "JPNS 2201" in lang_nums
    assert "SPAN 2201" in lang_nums
    assert "WLC 2201"  in lang_nums
    assert all(c["units"] == 4 for c in r4.json()["courses"])


def test_elective_endpoint_returns_mcro_options():
    # Organic chemistry choice (static)
    r1 = client.get("/api/electives/mcro_orga_choice")
    assert r1.status_code == 200
    orga = [c["course_number"] for c in r1.json()["courses"]]
    assert "CHEM 2240" in orga
    assert "CHEM 2242" in orga

    # Biochemistry choice (static)
    r2 = client.get("/api/electives/mcro_bioc_choice")
    assert r2.status_code == 200
    bioc = [c["course_number"] for c in r2.json()["courses"]]
    assert "CHEM 3350" in bioc
    assert "CHEM 3352" in bioc

    # Restricted elective (static)
    r3 = client.get("/api/electives/mcro_restricted_elective")
    assert r3.status_code == 200
    rest = [c["course_number"] for c in r3.json()["courses"]]
    assert "MCRO 4402" in rest
    assert "MCRO 4423" in rest
    assert "BIO 4452" in rest
    assert "BIO 4456" in rest

    # Senior project (static)
    r4 = client.get("/api/electives/mcro_senior_project")
    assert r4.status_code == 200
    sp = [c["course_number"] for c in r4.json()["courses"]]
    assert "BIO 4461" in sp
    assert "BIO 4462" in sp
    assert "BIO 4463" in sp


def test_elective_endpoint_returns_plsc_options():
    # Base concentration elective (dynamic)
    r1 = client.get("/api/electives/plsc_concentration_elective")
    assert r1.status_code == 200
    assert len(r1.json()["courses"]) > 0

    # Fruit and Crop Science static list
    r2 = client.get("/api/electives/plsc_fruit_crop_elective")
    assert r2.status_code == 200
    fruit = [c["course_number"] for c in r2.json()["courses"]]
    assert "PLSC 1132" in fruit
    assert "PLSC 3360" in fruit
    assert "PLSC 4420" in fruit

    # Environmental Horticultural Science static list
    r3 = client.get("/api/electives/plsc_environ_hort_elective")
    assert r3.status_code == 200
    env = [c["course_number"] for c in r3.json()["courses"]]
    assert "PLSC 1123" in env
    assert "PLSC 3332" in env
    assert "PLSC 4427" in env

    # Plant Protection Science static list
    r4 = client.get("/api/electives/plsc_plant_protection_elective")
    assert r4.status_code == 200
    pp = [c["course_number"] for c in r4.json()["courses"]]
    assert "PLSC 4406" in pp
    assert "PLSC 4431" in pp
    assert "PLSC 4441" in pp


def test_elective_endpoint_returns_envm_options():
    # Static pickers
    for key, expected in [
        ("envm_bio_plant_choice",   "BOT 1121"),
        ("envm_math_choice",        "MATH 1267"),
        ("envm_bio_ecology_choice", "BIO 2215"),
        ("envm_chem_choice",        "CHEM 1122"),
        ("envm_bio_life_choice",    "BIO 1150"),
        ("envm_soc_choice",         "NR 3323"),
        ("envm_enviro_choice",      "BRAE 3348"),
        ("envm_ecology_choice",     "NR 3305"),
        ("envm_water_choice",       "SS 3321"),
        ("envm_quant_choice",       "NR 4418"),
        ("envm_policy_choice",      "NR 4408"),
        ("envm_senior_project",     "NR 4462"),
        ("envm_conservation_elective", "BIO 3327"),
        ("envm_corporate_elective",    "NR 4442"),
        ("envm_data_science_elective", "STAT 3430"),
        ("envm_law_justice_elective",  "POLS 3351"),
        ("envm_sust_ag_elective",      "PLSC 3315"),
        ("envm_sust_urban_elective",   "CRP 3336"),
        ("envm_water_mgmt_elective",   "NR 4422"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"

    # Dynamic concentration fallback
    r = client.get("/api/electives/envm_concentration_elective")
    assert r.status_code == 200
    nums = [c["course_number"] for c in r.json()["courses"]]
    assert any(n.startswith("NR ") for n in nums)


def test_elective_endpoint_returns_phil_options():
    for key, expected in [
        ("phil_hist_group1",          "PHIL 3310"),
        ("phil_hist_group2",          "PHIL 3314"),
        ("phil_hist_group3",          "PHIL 3318"),
        ("phil_ethics_elective",      "PHIL 3337"),
        ("phil_tech_ethics_elective", "PHIL 3339"),
        ("phil_sci_tech_elective",    "PHIL 3327"),
        ("phil_senior_sem_elective",  "PHIL 4422"),
        ("phil_asian_rel_elective",   "RELS 3301"),
        ("phil_religion_elective",    "RELS 3311"),
        ("phil_senior_phil_elective", "PHIL 4449"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"

    for key, dept_prefix in [
        ("phil_gen_elective",      "PHIL "),
        ("phil_arts_hum_support",  "ENGL "),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert any(n.startswith(dept_prefix) for n in nums), f"No {dept_prefix} course in {key}"


def test_elective_endpoint_returns_nut_options():
    for key, expected in [
        ("nut_mcro_choice",    "MCRO 2221"),
        ("nut_senior_project", "NUTR 4461"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"

    # Dynamic pickers
    for key, dept_prefix in [
        ("nut_dietetics_elective", "PSY "),
        ("nut_prehealth_elective", "BIO "),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert any(n.startswith(dept_prefix) for n in nums), f"No {dept_prefix} course in {key}"


def test_elective_endpoint_returns_ph_options():
    for key, expected in [
        ("ph_hlth_freshman_elective", "HLTH 1160"),
        ("ph_ant_soc_elective",       "SOC 1110"),
        ("ph_senior_project",         "HLTH 4462"),
        ("ph_com_health_elective",    "KINE 4412"),
        ("ph_equity_global_elective", "SOC 4435"),
        ("ph_bus_econ_elective",      "ECON 2001"),
        ("ph_mgmt_admin_elective",    "PSY 3302"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"


def test_elective_endpoint_returns_span_options():
    for key, expected in [
        ("span_2202_2206",   "SPAN 2202"),
        ("span_3k_elective", "SPAN 3303"),
        ("span_4k_elective", "SPAN 4402"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        data = r.json()
        nums = [c["course_number"] for c in data["courses"]]
        assert expected in nums, f"{expected} not in {key} results"

    # Dynamic picker: span_lang_cult_elective should return SPAN and other language courses
    r = client.get("/api/electives/span_lang_cult_elective")
    assert r.status_code == 200
    nums = [c["course_number"] for c in r.json()["courses"]]
    assert any(n.startswith("SPAN ") for n in nums), "No SPAN course in span_lang_cult_elective"


def test_elective_endpoint_returns_thea_options():
    for key, expected in [
        ("th_mainstage_choice",    "TH 1145"),
        ("th_history_choice",      "TH 2227"),
        ("th_construction_choice", "TH 3325"),
        ("th_design_choice",       "TH 4430"),
        ("th_ld_elective",         "TH 2240"),
        ("th_ud_elective",         "TH 3320"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"


def test_elective_endpoint_returns_libs_options():
    for key, expected in [
        ("libs_stat_choice",         "STAT 1000"),
        ("libs_phil_choice",         "PHIL 2230"),
        ("libs_advanced_integration","LS 4411"),
        ("libs_senior_project",      "LS 4461"),
        ("libs_math_upper_div",      "MATH 3511"),
        ("libs_engl_3393_choice",    "ENGL 3393"),
        ("libs_am_lit_elective",     "ENGL 3340"),
        ("libs_engl_ling_choice",    "ENGL 2290"),
        ("libs_pols_elective",       "POLS 1112"),
        ("libs_geog_elective",       "GEOG 1150"),
        ("libs_soc_hist_elective",   "HIST 3322"),
        ("libs_env_cultural",        "PHIL 3340"),
        ("libs_env_ecological",      "NR 3310"),
        ("libs_env_education",       "COMS 3390"),
        ("libs_env_capstone",        "SCM 3360"),
        ("libs_hd_apps_ed",          "CD 3350"),
        ("libs_hd_child_dev",        "CD 3304"),
        ("libs_hd_social_context",   "LS 3350"),
        ("libs_sci_core",            "CHEM 1110"),
        ("libs_sci_approved",        "ASTR 1101"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"

    # Dynamic picker: libs_hd_cd_course should return CD courses
    r = client.get("/api/electives/libs_hd_cd_course")
    assert r.status_code == 200
    nums = [c["course_number"] for c in r.json()["courses"]]
    assert any(n.startswith("CD ") for n in nums), "No CD course in libs_hd_cd_course"


def test_elective_endpoint_returns_dsci_options():
    # Static pickers
    for key, expected in [
        ("dsci_senior_project", "ASCI 4477"),
        ("dsci_ud_elective",    "DSCI 4401"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"

    # Dynamic picker: dsci_approved_elective should return ASCI and DSCI courses
    r = client.get("/api/electives/dsci_approved_elective")
    assert r.status_code == 200
    nums = [c["course_number"] for c in r.json()["courses"]]
    assert any(n.startswith("ASCI ") or n.startswith("DSCI ") for n in nums), \
        "No ASCI/DSCI course in dsci_approved_elective"


def test_elective_endpoint_returns_itp_options():
    # Static pickers
    for key, expected in [
        ("itp_math_choice",           "MATH 1261"),
        ("itp_math_choice",           "MATH 1267"),
        ("itp_stat_choice",           "STAT 1110"),
        ("itp_stat_choice",           "STAT 1210"),
        ("itp_it_approved_elective",  "ITP 4404"),
        ("itp_it_approved_elective",  "BUS 3310"),
        ("itp_pkg_approved_elective", "ITP 4410"),
        ("itp_pkg_approved_elective", "FSN 3319"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"

    # Dynamic picker: itp_concentration_elective should return ITP courses
    r = client.get("/api/electives/itp_concentration_elective")
    assert r.status_code == 200
    nums = [c["course_number"] for c in r.json()["courses"]]
    assert any(n.startswith("ITP ") for n in nums), "No ITP course in itp_concentration_elective"


def test_elective_endpoint_returns_nr_options():
    # Static pickers
    for key, expected in [
        ("nr_bio_bot_choice",         "BIO 1114"),
        ("nr_bio_bot_choice",         "BOT 1121"),
        ("nr_senior_project",         "NR 4460"),
        ("nr_senior_project",         "NR 4466"),
        ("nr_senior_project",         "NR 4475"),
        ("nr_ws_soil_choice",         "SS 3321"),
        ("nr_ws_soil_choice",         "SS 4431"),
        ("nr_fr_approved_elective",   "NR 3306"),
        ("nr_fr_approved_elective",   "SS 4440"),
        ("nr_ws_approved_elective",   "NR 4422"),
        ("nr_ws_approved_elective",   "STAT 3520"),
        ("nr_wf_approved_elective",   "NR 3312"),
        ("nr_wf_approved_elective",   "CRP 4458"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key} results"


def test_ces_elective_keys():
    # CES theory courses (static)
    r = client.get("/api/electives/ces_theory")
    assert r.status_code == 200
    nums = [c["course_number"] for c in r.json()["courses"]]
    assert "ES 4401" in nums
    assert "ES 4402" in nums
    assert "ES 4403" in nums

    # CES dynamic buckets return results
    for key in ["ces_area6_course", "ces_popular_culture", "ces_lit_ud3", "ces_ud_elective"]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        assert len(r.json()["courses"]) > 0, f"No courses for {key}"


def test_gen_elective_keys():
    r = client.get("/api/electives/gen_gender_sci_choice")
    assert r.status_code == 200
    nums = [c["course_number"] for c in r.json()["courses"]]
    assert "WGQS 3350" in nums
    assert "WGQS 3351" in nums


def test_msci_elective_keys():
    for key, expected in [
        ("msci_phys1_choice",     "PHYS 1121"),
        ("msci_phys1_choice",     "PHYS 1141"),
        ("msci_phys2_choice",     "PHYS 1123"),
        ("msci_phys2_choice",     "PHYS 1143"),
        ("msci_math_choice",      "MATH 1261"),
        ("msci_math_choice",      "MATH 1264"),
        ("msci_chem_choice",      "CHEM 2240"),
        ("msci_chem_choice",      "CHEM 2242"),
        ("msci_marine_elective",  "MSCI 4403"),
        ("msci_marine_elective",  "BIO 3322"),
        ("msci_senior_project",   "BIO 4461"),
        ("msci_senior_project",   "BIO 4463"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key}"

    r = client.get("/api/electives/msci_approved_elective")
    assert r.status_code == 200
    assert len(r.json()["courses"]) > 0


def test_eess_elective_keys():
    for key, expected in [
        ("eess_math_choice",          "MATH 1261"),
        ("eess_math_choice",          "MATH 1264"),
        ("eess_phys_choice",          "PHYS 1121"),
        ("eess_phys_choice",          "PHYS 1141"),
        ("eess_strat_or_soil",        "GEOL 3330"),
        ("eess_strat_or_soil",        "SS 2221"),
        ("eess_strat_or_soil",        "SS 3444"),
        ("eess_soil_or_geomorph",     "SS 4422"),
        ("eess_soil_or_geomorph",     "ERSC 4450"),
        ("eess_gis_choice",           "BRAE 3345"),
        ("eess_gis_choice",           "NR 4418"),
        ("eess_env_physics_choice",   "SS 4424"),
        ("eess_env_physics_choice",   "ERSC 4442"),
        ("eess_env_physics_choice",   "ERSC 4443"),
        ("eess_senior_project",       "ERSC 4478"),
        ("eess_senior_project",       "ERSC 4479"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key}"

    for key in ["eess_approved_elective", "eess_nr_elective"]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        assert len(r.json()["courses"]) > 0, f"No courses for {key}"


def test_ints_elective_keys():
    for key, expected in [
        ("ints_intro_course",       "ES 1112"),
        ("ints_intro_course",       "HIST 2206"),
        ("ints_intro_course",       "ISLA 1123"),
        ("ints_intro_course",       "WGQS 2301"),
        ("ints_ud_isla_elective",   "ISLA 3303"),
        ("ints_ud_isla_elective",   "ISLA 4440"),
        ("ints_ud_isla_elective",   "COMS 3395"),
    ]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        nums = [c["course_number"] for c in r.json()["courses"]]
        assert expected in nums, f"{expected} not in {key}"

    for key in ["ints_eljs_concentration", "ints_gcss_concentration",
                "ints_hs_concentration", "ints_sts_concentration",
                "ints_vmcs_concentration"]:
        r = client.get(f"/api/electives/{key}")
        assert r.status_code == 200, f"Failed for {key}"
        assert len(r.json()["courses"]) > 0, f"No courses for {key}"


def test_laes_elective_keys():
    r = client.get("/api/electives/laes_eng_elective")
    assert r.status_code == 200
    assert len(r.json()["courses"]) > 0
