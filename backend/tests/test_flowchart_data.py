from data.concentrations import CONCENTRATIONS
from data.flowcharts import FLOWCHARTS
from routers.flowchart import _ALIGNED_FLOWCHARTS
from services.layout import align_prereq_chains


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

LAYOUT_CATEGORY_ORDER = {
    "major": 0,
    "support": 1,
    "concentration": 3,
    "ge": 4,
}

DEFERRED_LAYOUT_TITLE_PARTS = (
    "orientation",
    "professional preparation",
)


def layout_bucket(course):
    title = course["title"].lower()
    if any(part in title for part in DEFERRED_LAYOUT_TITLE_PARTS):
        return 2
    return LAYOUT_CATEGORY_ORDER[course["category"]]


def _make_course(id, number, col, row, prereqs=None, placeholder=False):
    return {
        "id": id,
        "course_number": number,
        "grid_col": col,
        "grid_row": row,
        "prerequisites": prereqs or [],
        "is_placeholder": placeholder,
    }


def test_align_prereq_chains_direct_chain_lands_in_same_row():
    courses = [
        _make_course("c1", "MATH 1261", 0, 0),
        _make_course("c2", "MATH 1262", 1, 3, prereqs=["MATH 1261"]),
        _make_course("c3", "MATH 2263", 2, 5, prereqs=["MATH 1262"]),
    ]
    result = {c["id"]: c for c in align_prereq_chains(courses)}
    assert result["c1"]["grid_row"] == result["c2"]["grid_row"] == result["c3"]["grid_row"]


def test_align_prereq_chains_free_courses_compact_without_gaps():
    courses = [
        _make_course("a", "CSC 1024", 0, 0),
        _make_course("b", "MATH 1261", 0, 1),
        _make_course("c", "GE 1A", 0, 2),
    ]
    result_courses = align_prereq_chains(courses)
    rows = sorted(c["grid_row"] for c in result_courses)
    assert rows == list(range(len(rows)))


def test_align_prereq_chains_two_independent_chains_no_row_overlap():
    courses = [
        _make_course("a1", "CSC 1024", 0, 0),
        _make_course("b1", "MATH 1261", 0, 1),
        _make_course("a2", "CSC 1001", 1, 2, prereqs=["CSC 1024"]),
        _make_course("b2", "MATH 1262", 1, 3, prereqs=["MATH 1261"]),
    ]
    result = {c["id"]: c for c in align_prereq_chains(courses)}
    assert result["a2"]["grid_row"] == result["a1"]["grid_row"]
    assert result["b2"]["grid_row"] == result["b1"]["grid_row"]
    col1_rows = [result["a2"]["grid_row"], result["b2"]["grid_row"]]
    assert len(col1_rows) == len(set(col1_rows)), "Two chains in same column must not share a row"


def test_align_prereq_chains_unknown_prereq_treated_as_free():
    courses = [_make_course("c1", "CSC 2001", 0, 5, prereqs=["CSC 1001"])]
    result = align_prereq_chains(courses)
    assert result[0]["grid_row"] == 0, "Single free course should compact to row 0"


def test_align_prereq_chains_placeholder_course_participates_in_chain():
    courses = [
        _make_course("base", "MATH 1261", 0, 0),
        _make_course("ph",   "MATH 1262", 1, 4, prereqs=["MATH 1261"], placeholder=True),
    ]
    result = {c["id"]: c for c in align_prereq_chains(courses)}
    assert result["ph"]["grid_row"] == result["base"]["grid_row"]


def test_align_prereq_chains_does_not_move_support_into_major_band():
    courses = [
        {
            **_make_course("m1", "CPE 3160", 5, 0, prereqs=["CPE 2301"]),
            "title": "Microcontrollers and Embedded Applications",
            "category": "major",
        },
        {
            **_make_course("m2", "CPE 4464", 5, 1, prereqs=["CPE 3300"]),
            "title": "Introduction to Computer Networks",
            "category": "major",
        },
        {
            **_make_course("s1", "STAT 3210", 5, 2, prereqs=["MATH 1262"]),
            "title": "Engineering Statistics",
            "category": "support",
        },
        {
            **_make_course("p1", "CPE 2301", 4, 0),
            "title": "Computer Design and Assembly Language Programming",
            "category": "major",
        },
        {
            **_make_course("p2", "CPE 3300", 4, 0),
            "title": "Computer Architecture",
            "category": "major",
        },
        {
            **_make_course("p3", "MATH 1262", 1, 1),
            "title": "Calculus II",
            "category": "support",
        },
    ]

    result = {c["id"]: c for c in align_prereq_chains(courses)}

    assert result["m1"]["grid_row"] == 0
    assert result["m2"]["grid_row"] == 1
    assert result["s1"]["grid_row"] == 2


def test_align_prereq_chains_idempotent():
    courses = [
        _make_course("c1", "MATH 1261", 0, 0),
        _make_course("c2", "MATH 1262", 1, 0, prereqs=["MATH 1261"]),
        _make_course("c3", "MATH 2263", 2, 0, prereqs=["MATH 1262"]),
    ]
    once  = align_prereq_chains(courses)
    twice = align_prereq_chains(once)
    for a, b in zip(once, twice):
        assert a["grid_row"] == b["grid_row"], "align_prereq_chains should be idempotent"


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


def test_flowchart_columns_are_compacted_after_default_layout_pass():
    for major_code, flowchart in FLOWCHARTS.items():
        for grid_col in range(len(flowchart["columns"])):
            rows = sorted(
                course["grid_row"]
                for course in flowchart["courses"]
                if course["grid_col"] == grid_col
            )
            assert rows == list(range(len(rows))), f"{major_code} column {grid_col} has row gaps: {rows}"


def test_flowchart_api_initial_layout_groups_categories_for_every_major():
    for major_code, flowchart in _ALIGNED_FLOWCHARTS.items():
        for grid_col in range(len(flowchart["columns"])):
            column_courses = sorted(
                (course for course in flowchart["courses"] if course["grid_col"] == grid_col),
                key=lambda course: course["grid_row"],
            )
            rows = [course["grid_row"] for course in column_courses]
            buckets = [layout_bucket(course) for course in column_courses]

            assert rows == list(range(len(rows))), f"{major_code} column {grid_col} has row gaps: {rows}"
            assert buckets == sorted(buckets), f"{major_code} column {grid_col} is not category grouped: {buckets}"


def test_concentration_overlays_keep_initial_layout_grouped():
    for major_code, concentrations in CONCENTRATIONS.items():
        flowchart = _ALIGNED_FLOWCHARTS[major_code]

        for concentration in concentrations:
            resolved_courses = []
            for course in flowchart["courses"]:
                override = concentration["slot_overrides"].get(course["id"])
                resolved_courses.append({**course, **override} if override else course)

            for grid_col in range(len(flowchart["columns"])):
                buckets = [
                    layout_bucket(course)
                    for course in sorted(
                        (course for course in resolved_courses if course["grid_col"] == grid_col),
                        key=lambda course: course["grid_row"],
                    )
                ]

                assert buckets == sorted(buckets), (
                    f"{major_code} {concentration['id']} column {grid_col} is not category grouped: {buckets}"
                )


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


def test_computer_science_layout_groups_early_major_and_support_rows():
    cs_courses = {course["course_number"]: course for course in FLOWCHARTS["CS"]["courses"]}

    assert cs_courses["CSC 1024"]["grid_row"] == 0
    assert cs_courses["CSC 1001"]["grid_row"] == 0
    assert cs_courses["CSC 2001"]["grid_row"] == 0

    assert cs_courses["MATH 1261"]["grid_row"] == 1
    assert cs_courses["MATH 1262"]["grid_row"] == 1
    assert cs_courses["MATH 1151"]["grid_row"] == 1

    assert cs_courses["CSC 1000"]["grid_row"] == 3
    assert cs_courses["PHYS 1141"]["grid_row"] == 2
    assert cs_courses["GE 1C"]["grid_row"] == 2
    assert cs_courses["BIO/BOT"]["grid_row"] == 2
    assert cs_courses["GE 1A"]["grid_row"] > cs_courses["CSC 1000"]["grid_row"]
    assert cs_courses["GE 1B"]["grid_row"] > cs_courses["PHYS 1141"]["grid_row"]


def test_civil_engineering_flowchart_contains_expected_core_sequence():
    ce_courses = {course["course_number"]: course for course in FLOWCHARTS["CE"]["courses"]}

    assert FLOWCHARTS["CE"]["total_units"] == 132
    assert ce_courses["CE 1111"]["title"] == "Introduction to Civil Engineering"
    assert ce_courses["CE 4467"]["prerequisites"] == ["CE 4466"]
    assert ce_courses["CE 3337"]["prerequisites"] == ["CE 3336"]
    assert ce_courses["GE UD-4"]["category"] == "ge"


def test_civil_engineering_layout_prioritizes_calculus_row_and_category_bands():
    ce_courses = {course["course_number"]: course for course in FLOWCHARTS["CE"]["courses"]}

    calc_row = ce_courses["MATH 1261"]["grid_row"]
    assert calc_row == ce_courses["MATH 1262"]["grid_row"] == ce_courses["MATH 2263"]["grid_row"]

    assert ce_courses["CE 1111"]["grid_row"] < calc_row
    assert ce_courses["CE 1112"]["grid_row"] < calc_row
    assert ce_courses["CE 2251"]["grid_row"] < calc_row
    assert ce_courses["CHEM 1120"]["grid_row"] == 1
    assert ce_courses["PHYS 1141"]["grid_row"] > calc_row
    assert ce_courses["GE 1A"]["grid_row"] > ce_courses["PHYS 1141"]["grid_row"]
    assert ce_courses["GE 1B"]["grid_row"] > ce_courses["PHYS 1143"]["grid_row"]
    assert ce_courses["GE 3A"]["grid_row"] > ce_courses["ENGR 2211"]["grid_row"]


def test_civil_engineering_technical_elective_placeholders_are_unique():
    ce_te_courses = [
        course["course_number"]
        for course in FLOWCHARTS["CE"]["courses"]
        if course["id"].startswith("CE_TE_")
    ]

    assert len(ce_te_courses) == 6
    assert len(ce_te_courses) == len(set(ce_te_courses))


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


def test_political_science_flowchart_contains_expected_core_and_concentrations():
    pols_courses = {course["course_number"]: course for course in FLOWCHARTS["POLS"]["courses"]}
    pols_concentrations = CONCENTRATIONS["POLS"]
    concentration_ids = {concentration["id"] for concentration in pols_concentrations}

    assert FLOWCHARTS["POLS"]["total_units"] == 120
    assert pols_courses["POLS 1112"]["title"] == "U.S. and California Government"
    assert pols_courses["POLS 3359"]["title"] == "Research Design"
    assert pols_courses["POLS 3361"]["prerequisites"] == ["POLS 3359"]
    assert pols_courses["POLS 4462"]["prerequisites"] == ["POLS 4461"]
    assert pols_courses["STAT 1110"]["category"] == "support"
    assert pols_courses["GE UD-3"]["category"] == "ge"
    assert {"none", "global_politics", "pre_law", "us_politics", "individualized"} <= concentration_ids

    pre_law = next(c for c in pols_concentrations if c["id"] == "pre_law")
    assert pre_law["slot_overrides"]["POLS_CON_JRF1"]["course_number"] == "POLS 2245"


def test_english_flowchart_contains_expected_core_and_catalog_buckets():
    english_courses = {course["course_number"]: course for course in FLOWCHARTS["ENGL"]["courses"]}

    assert FLOWCHARTS["ENGL"]["total_units"] == 120
    assert english_courses["ENGL 1101"]["title"] == "Introduction to English Studies"
    assert english_courses["ENGL GE 3B"]["title"] == "Literature Elective"
    assert english_courses["Language 1101"]["category"] == "support"
    assert english_courses["ENGL UD GWR"]["title"] == "Upper-Division English GWR Elective"
    assert english_courses["ENGL Diversity"]["title"] == "4000-Level Diversity Elective"
    assert english_courses["ENGL 4461"]["title"] == "Senior Project"
    assert english_courses["GE UD-3"]["category"] == "ge"
    assert "ENGL" not in CONCENTRATIONS


def test_psychology_flowchart_contains_expected_core_sequence():
    psy_courses = {course["course_number"]: course for course in FLOWCHARTS["PSY"]["courses"]}

    assert FLOWCHARTS["PSY"]["total_units"] == 120
    assert psy_courses["PSY 1102"]["title"] == "Orientation to the Psychology Major"
    assert psy_courses["PSY 2201"]["category"] == "major"
    assert psy_courses["STAT 1110"]["category"] == "support"
    assert psy_courses["PSY 2229"]["prerequisites"] == ["PSY 2201", "STAT 1110"]
    assert psy_courses["PSY 3333"]["prerequisites"] == ["PSY 2229", "STAT 1110"]
    assert psy_courses["PSY 4461"]["prerequisites"] == ["PSY 2229"]
    assert psy_courses["PSY 4462"]["prerequisites"] == ["PSY 4461"]
    assert psy_courses["PSY 4449/4454"]["prerequisites"] == ["PSY 4448/4453"]


def test_psychology_research_methods_chain_spans_correct_semesters():
    psy_courses = {course["course_number"]: course for course in FLOWCHARTS["PSY"]["courses"]}

    assert psy_courses["PSY 2229"]["grid_col"] == 1   # Freshman Spring
    assert psy_courses["PSY 3333"]["grid_col"] == 3   # Sophomore Spring
    assert psy_courses["PSY 4461"]["grid_col"] == 6   # Senior Fall
    assert psy_courses["PSY 4462"]["grid_col"] == 7   # Senior Spring


def test_psychology_elective_placeholders_are_present():
    psy_by_id = {course["id"]: course for course in FLOWCHARTS["PSY"]["courses"]}

    assert "PSY_FOUND" in psy_by_id
    assert "PSY_SOC_PERS" in psy_by_id
    assert "PSY_MENTH" in psy_by_id
    assert "PSY_COGN" in psy_by_id
    assert "PSY_INTERN1" in psy_by_id
    assert "PSY_INTERN2" in psy_by_id

    assert psy_by_id["PSY_FOUND"]["is_placeholder"] is True
    assert psy_by_id["PSY_INTERN1"]["is_placeholder"] is True


def test_psychology_quarter_equivalents_are_mapped():
    psy_courses = {course["course_number"]: course for course in FLOWCHARTS["PSY"]["courses"]}

    assert "PSY 201" in psy_courses["PSY 2201"]["quarter_equivalents"]
    assert "PSY 329" in psy_courses["PSY 2229"]["quarter_equivalents"]
    assert "PSY 340" in psy_courses["PSY 2240"]["quarter_equivalents"]
    assert "PSY 333" in psy_courses["PSY 3333"]["quarter_equivalents"]
    assert "PSY 461" in psy_courses["PSY 4461"]["quarter_equivalents"]
    assert "PSY 462" in psy_courses["PSY 4462"]["quarter_equivalents"]


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
