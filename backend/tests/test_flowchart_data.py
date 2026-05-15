from data.concentrations import CONCENTRATIONS
from data.flowcharts import FLOWCHARTS


REQUIRED_COURSE_KEYS = {
    "id",
    "course_number",
    "title",
    "units",
    "category",
    "grid_col",
    "grid_row",
    "prerequisites",
    "quarter_equivalents",
    "is_placeholder",
}

VALID_CATEGORIES = {"major", "support", "concentration", "ge"}


def test_flowcharts_have_valid_course_shape_and_unique_ids():
    for major_code, flowchart in FLOWCHARTS.items():
        course_ids = [course["id"] for course in flowchart["courses"]]

        assert len(course_ids) == len(set(course_ids)), f"{major_code} has duplicate course ids"

        for course in flowchart["courses"]:
            assert REQUIRED_COURSE_KEYS <= course.keys(), f"{major_code} {course.get('id')} is missing keys"
            assert course["course_number"]
            assert course["title"]
            assert course["units"] > 0
            assert course["category"] in VALID_CATEGORIES
            assert 0 <= course["grid_col"] <= 7
            assert course["grid_row"] >= 0
            assert isinstance(course["prerequisites"], list)
            assert isinstance(course["quarter_equivalents"], list)
            assert isinstance(course["is_placeholder"], bool)


def test_flowchart_prerequisites_reference_courses_in_same_major():
    for major_code, flowchart in FLOWCHARTS.items():
        course_numbers = {course["course_number"] for course in flowchart["courses"]}

        for course in flowchart["courses"]:
            missing = [prereq for prereq in course["prerequisites"] if prereq not in course_numbers]
            assert missing == [], f"{major_code} {course['course_number']} has unknown prereqs: {missing}"


def test_aerospace_engineering_concentrations_cover_catalog_options():
    aero_concentrations = CONCENTRATIONS["AERO"]
    concentration_ids = {concentration["id"] for concentration in aero_concentrations}

    assert {"none", "aeronautics", "astronautics"} <= concentration_ids

    aeronautics = next(c for c in aero_concentrations if c["id"] == "aeronautics")
    assert aeronautics["slot_overrides"]["CON_JRS1"]["course_number"] == "AERO 3305"
    assert aeronautics["slot_overrides"]["CON_SRF1"]["units"] == 3
    assert aeronautics["slot_overrides"]["CON_SRS1"]["course_number"] == "AERO 4462"

    astronautics = next(c for c in aero_concentrations if c["id"] == "astronautics")
    assert astronautics["slot_overrides"]["CON_JRS1"]["course_number"] == "AERO 3351"
    assert astronautics["slot_overrides"]["CON_SRF4"]["course_number"] == "AERO 4455/4456"
    assert astronautics["slot_overrides"]["CON_SRS1"]["course_number"] == "AERO 4464"


def test_civil_engineering_flowchart_contains_expected_core_sequence():
    ce_courses = {course["course_number"]: course for course in FLOWCHARTS["CE"]["courses"]}

    assert FLOWCHARTS["CE"]["total_units"] == 132
    assert ce_courses["CE 1111"]["title"] == "Introduction to Civil Engineering"
    assert ce_courses["CE 4467"]["prerequisites"] == ["CE 4466"]
    assert ce_courses["CE 3337"]["prerequisites"] == ["CE 3336"]
    assert ce_courses["GE UD-4"]["category"] == "ge"


def test_civil_engineering_concentrations_replace_only_technical_electives():
    ce_concentrations = CONCENTRATIONS["CE"]
    focus_area_ids = {concentration["id"] for concentration in ce_concentrations}

    assert {
        "none",
        "construction",
        "geotechnical",
        "structural",
        "transportation",
        "water_resources",
    } <= focus_area_ids

    for concentration in ce_concentrations:
        for slot_id in concentration["slot_overrides"]:
            assert slot_id.startswith("CE_TE_")

    structural = next(c for c in ce_concentrations if c["id"] == "structural")
    assert structural["slot_overrides"]["CE_TE_SRF1"]["course_number"] == "CE 4356"

    water_resources = next(c for c in ce_concentrations if c["id"] == "water_resources")
    assert water_resources["slot_overrides"]["CE_TE_SRF2"]["prerequisites"] == ["CE 3337"]


def test_mechanical_engineering_flowchart_contains_core_and_double_counted_ge():
    me_courses = {course["course_number"]: course for course in FLOWCHARTS["ME"]["courses"]}

    assert FLOWCHARTS["ME"]["total_units"] == 129
    assert me_courses["ME 1125"]["title"] == "Introduction to Mechanical Engineering"
    assert me_courses["MATH 1261"]["category"] == "support"
    assert me_courses["CHEM 1120"]["category"] == "support"
    assert me_courses["ME 3234"]["category"] == "major"
    assert me_courses["ME 3236"]["category"] == "major"
    assert me_courses["GE 5B"]["category"] == "ge"
    assert me_courses["GE UD-3"]["category"] == "ge"


def test_mechanical_engineering_concentrations_cover_catalog_options():
    me_concentrations = CONCENTRATIONS["ME"]
    concentration_ids = {concentration["id"] for concentration in me_concentrations}

    assert {
        "none",
        "energy_resources",
        "hvacr",
        "mechatronics",
        "manufacturing",
    } <= concentration_ids

    hvac = next(c for c in me_concentrations if c["id"] == "hvacr")
    assert hvac["slot_overrides"]["ME4460"]["course_number"] == "ME 4465"

    mechatronics = next(c for c in me_concentrations if c["id"] == "mechatronics")
    assert mechatronics["slot_overrides"]["ME3317"]["course_number"] == "ME 3305"

    manufacturing = next(c for c in me_concentrations if c["id"] == "manufacturing")
    assert manufacturing["slot_overrides"]["ME_TE_SRF1"]["course_number"] == "IME 3327"


def test_art_and_design_flowchart_contains_expected_core_and_ge_sequence():
    ad_courses = {course["course_number"]: course for course in FLOWCHARTS["AD"]["courses"]}

    assert FLOWCHARTS["AD"]["total_units"] == 120
    assert ad_courses["ART 1101"]["title"] == "Fundamentals of Drawing"
    assert ad_courses["ART 2201"]["category"] == "major"
    assert ad_courses["GE 2"]["category"] == "ge"
    assert ad_courses["GE 5A"]["category"] == "ge"
    assert ad_courses["GE 5C"]["units"] == 1
    assert ad_courses["GE UD-2/5"]["category"] == "ge"


def test_concentration_overrides_target_existing_slots_and_keep_course_shape():
    for major_code, concentrations in CONCENTRATIONS.items():
        flowchart_ids = {course["id"] for course in FLOWCHARTS[major_code]["courses"]}

        for concentration in concentrations:
            assert concentration["id"]
            assert concentration["label"]
            assert isinstance(concentration["slot_overrides"], dict)

            for slot_id, override in concentration["slot_overrides"].items():
                assert slot_id in flowchart_ids
                assert {"course_number", "title", "units", "prerequisites", "quarter_equivalents", "is_placeholder"} <= override.keys()
                assert override["course_number"]
                assert override["title"]
                assert override["units"] > 0
                assert isinstance(override["prerequisites"], list)
                assert isinstance(override["quarter_equivalents"], list)
                assert isinstance(override["is_placeholder"], bool)
