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
            assert 0 <= course["grid_col"] < len(flowchart["columns"])
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
    assert ad_courses["ART 1184 / ART 2282"]["is_placeholder"] is True
    assert "ART 1184" in ad_courses["ART 1184 / ART 2282"]["quarter_equivalents"]
    assert "ART 2282" in ad_courses["ART 1184 / ART 2282"]["quarter_equivalents"]
    assert ad_courses["ART 3359 / ART 3379 / ART 3399"]["is_placeholder"] is True
    assert "ART 3359" in ad_courses["ART 3359 / ART 3379 / ART 3399"]["quarter_equivalents"]
    assert "ART 3379" in ad_courses["ART 3359 / ART 3379 / ART 3399"]["quarter_equivalents"]
    assert "ART 3399" in ad_courses["ART 3359 / ART 3379 / ART 3399"]["quarter_equivalents"]


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
    assert pols_courses["ANT 2201 / GEOG 1150 / HIST 2222 / HIST 2223 / SOC 1110"]["is_placeholder"] is True
    assert "ANT 2201" in pols_courses["ANT 2201 / GEOG 1150 / HIST 2222 / HIST 2223 / SOC 1110"]["quarter_equivalents"]
    assert "HIST 2222" in pols_courses["ANT 2201 / GEOG 1150 / HIST 2222 / HIST 2223 / SOC 1110"]["quarter_equivalents"]
    assert "SOC 1110" in pols_courses["ANT 2201 / GEOG 1150 / HIST 2222 / HIST 2223 / SOC 1110"]["quarter_equivalents"]
    assert pols_courses["GE UD-3"]["category"] == "ge"
    assert {"none", "global_politics", "pre_law", "us_politics", "individualized"} <= concentration_ids

    pre_law = next(c for c in pols_concentrations if c["id"] == "pre_law")
    assert pre_law["slot_overrides"]["POLS_CON_JRF1"]["course_number"] == "POLS 2245"


def test_english_flowchart_contains_expected_core_and_catalog_buckets():
    english_courses = {course["course_number"]: course for course in FLOWCHARTS["ENGL"]["courses"]}

    assert FLOWCHARTS["ENGL"]["total_units"] == 120
    assert english_courses["ENGL 1101"]["title"] == "Introduction to English Studies"
    assert english_courses["ENGL GE 3B"]["title"] == "Literature Elective"
    language = english_courses["CHIN 1101 / FR 1101 / GER 1101 / ITAL 1101 / JPNS 1101 / SPAN 1101 / WLC 1101"]
    assert language["category"] == "support"
    assert language["is_placeholder"] is True
    assert "CHIN 1101" in language["quarter_equivalents"]
    assert "SPAN 1101" in language["quarter_equivalents"]
    assert "WLC 1101" in language["quarter_equivalents"]
    assert english_courses["ENGL UD GWR"]["title"] == "Upper-Division English GWR Elective"
    assert english_courses["ENGL Diversity"]["title"] == "4000-Level Diversity Elective"
    assert english_courses["ENGL 4461"]["title"] == "Senior Project"
    assert english_courses["GE UD-3"]["category"] == "ge"
    assert "ENGL" not in CONCENTRATIONS


def test_music_flowchart_contains_expected_core_and_catalog_buckets():
    music_courses = {course["course_number"]: course for course in FLOWCHARTS["MU"]["courses"]}

    assert FLOWCHARTS["MU"]["total_units"] == 120
    assert music_courses["MU 1100"]["title"] == "Introduction to Music Studies"
    assert music_courses["MU 1104"]["title"] == "Musicianship I"
    assert music_courses["MU 1106"]["prerequisites"] == ["MU 1104"]
    assert music_courses["MU 1122"]["title"] == "Ethnomusicology and World Music I"
    assert music_courses["MU 2222"]["title"] == "Ethnomusicology and World Music II"
    assert music_courses["MU 3311"]["title"] == "Introduction to Music Technology and Composition"
    assert music_courses["MU 3331"]["title"] == "Historical Musicology I"
    assert music_courses["MU 4431"]["title"] == "Historical Musicology II"
    assert music_courses["MU 4461"]["title"] == "Senior Project"
    assert music_courses["MU 3000+ 1"]["title"] == "Upper-Division Music Elective"
    assert music_courses["MU 1101 / MU 1103"]["is_placeholder"] is True
    assert "MU 1101" in music_courses["MU 1101 / MU 1103"]["quarter_equivalents"]
    assert "MU 1103" in music_courses["MU 1101 / MU 1103"]["quarter_equivalents"]
    assert music_courses["MU 1103 / MU 2203"]["is_placeholder"] is True
    assert "MU 1103" in music_courses["MU 1103 / MU 2203"]["quarter_equivalents"]
    assert "MU 2203" in music_courses["MU 1103 / MU 2203"]["quarter_equivalents"]
    assert music_courses["MU 2221 / MU 2227"]["is_placeholder"] is True
    assert "MU 2221" in music_courses["MU 2221 / MU 2227"]["quarter_equivalents"]
    assert "MU 2227" in music_courses["MU 2221 / MU 2227"]["quarter_equivalents"]
    assert music_courses["GE UD-3"]["category"] == "ge"
    assert "MU" not in CONCENTRATIONS


def test_agricultural_communication_flowchart_contains_expected_core_and_support():
    agc_courses = {course["course_number"]: course for course in FLOWCHARTS["AGC"]["courses"]}
    agc_by_id = {course["id"]: course for course in FLOWCHARTS["AGC"]["courses"]}

    assert FLOWCHARTS["AGC"]["total_units"] == 120
    assert agc_courses["AGC 1102"]["title"] == "Orientation to Agricultural Communication & Agricultural Science"
    assert agc_courses["AGC 2205"]["title"] == "Agricultural Communications"
    assert agc_courses["AGC 2225"]["title"] == "Digital Communication in Agriculture and Science"
    assert agc_courses["AGC 3301"]["title"] == "New Media Communication Strategies in Agriculture"
    assert agc_courses["AGC 3339"]["title"] == "Internship in Agricultural Communications"
    assert agc_courses["AGC 4463"]["title"] == "Senior Project"
    assert agc_courses["AGC 4475"]["title"] == "Crisis Communication in Food and Agriculture"
    assert agc_courses["STAT 1000 / DATA 1000"]["category"] == "support"
    assert agc_courses["STAT 1000 / DATA 1000"]["is_placeholder"] is True
    assert agc_courses["JOUR 2203"]["category"] == "support"
    assert agc_courses["ENGL 3310"]["category"] == "support"
    assert agc_courses["AGC 2225"]["prerequisites"] == ["AGC 2207"]
    assert agc_courses["AGC 4407"]["prerequisites"] == ["AGC 2205", "AGC 2207"]
    assert agc_courses["AGC 4425"]["prerequisites"] == ["AGC 2225"]
    assert agc_courses["AGB 3312"]["prerequisites"] == ["AGB 2212", "ECON 2040"]
    assert agc_by_id["AGC_MARKETING"]["prerequisites"] == ["AGB 2212"]
    assert agc_by_id["AGC_MARKETING"]["is_placeholder"] is True
    assert agc_by_id["AGC_MARKETING"]["elective_key"] == "agc_ags_marketing"
    assert agc_by_id["AGC_STATDATA1000"]["elective_key"] == "agc_stat_data_1000"
    assert "STAT 1000" in agc_by_id["AGC_STATDATA1000"]["quarter_equivalents"]
    assert "DATA 1000" in agc_by_id["AGC_STATDATA1000"]["quarter_equivalents"]
    assert agc_by_id["AGC_CHEM5A5C"]["elective_key"] == "agc_chem_elective"
    assert "CHEM 1110" in agc_by_id["AGC_CHEM5A5C"]["quarter_equivalents"]
    assert "CHEM 1120" in agc_by_id["AGC_CHEM5A5C"]["quarter_equivalents"]
    assert agc_by_id["AGC_FSN"]["elective_key"] == "agc_fsn_elective"
    assert "FSN 1111" in agc_by_id["AGC_FSN"]["quarter_equivalents"]
    assert "FSN 2245" in agc_by_id["AGC_FSN"]["quarter_equivalents"]
    assert agc_by_id["AGC_PLSC1120"]["elective_key"] == "agc_plsc_pair"
    assert "PLSC 1120" in agc_by_id["AGC_PLSC1120"]["quarter_equivalents"]
    assert "PLSC 1120L" in agc_by_id["AGC_PLSC1120"]["quarter_equivalents"]
    assert agc_courses["GE UD-3"]["category"] == "ge"
    assert "AGC" not in CONCENTRATIONS


def test_agricultural_science_flowchart_contains_expected_core_and_emphasis_slots():
    ags_courses = {course["course_number"]: course for course in FLOWCHARTS["AGS"]["courses"]}
    ags_by_id = {course["id"]: course for course in FLOWCHARTS["AGS"]["courses"]}

    assert FLOWCHARTS["AGS"]["total_units"] == 120
    assert ags_courses["AGC 1102"]["title"] == "Orientation to Agricultural Communication & Agricultural Science"
    assert ags_courses["BRAE 1141"]["title"] == "Agricultural Machinery Safety"
    assert ags_courses["AGB 2202"]["title"] == "Introduction to Sales"
    assert ags_courses["AGB 2212"]["title"] == "Agricultural Economics"
    assert ags_courses["AGED 4421"]["title"] == "Agricultural Mechanics"
    assert ags_courses["AGC 4426"]["title"] == "Presentation Methods in Agricultural Communication"
    assert ags_courses["AGC 4463"]["title"] == "Senior Project"
    assert ags_courses["GE UD-4"]["category"] == "ge"
    assert ags_by_id["AGS_EMP_JRF1"]["category"] == "concentration"
    assert ags_by_id["AGS_EMP_SRS2"]["is_placeholder"] is True


def test_agricultural_science_emphasis_areas_cover_catalog_options():
    ags_concentrations = CONCENTRATIONS["AGS"]
    concentration_ids = {concentration["id"] for concentration in ags_concentrations}

    assert {
        "none",
        "ag_engineering_tech",
        "agribusiness",
        "animal_science",
        "plant_crop_soil",
        "forestry_natural_resources",
        "ornamental_horticulture",
    } <= concentration_ids

    engineering = next(c for c in ags_concentrations if c["id"] == "ag_engineering_tech")
    assert engineering["slot_overrides"]["AGS_EMP_JRF1"]["course_number"] == "BRAE 1150"

    agribusiness = next(c for c in ags_concentrations if c["id"] == "agribusiness")
    assert agribusiness["slot_overrides"]["AGS_EMP_SRS2"]["course_number"] == "AGB 3313"

    ornamental = next(c for c in ags_concentrations if c["id"] == "ornamental_horticulture")
    assert ornamental["slot_overrides"]["AGS_EMP_SRS2"]["course_number"] == "PLSC 3334"


def test_animal_science_flowchart_contains_expected_core_and_placeholders():
    asci_courses = {course["course_number"]: course for course in FLOWCHARTS["ASCI"]["courses"]}

    assert FLOWCHARTS["ASCI"]["total_units"] == 120
    assert asci_courses["ASCI 1100"]["title"] == "Introduction to the Animal Sciences"
    assert asci_courses["ASCI 2210/2211"]["title"] == "Meat Science and Meat Science Laboratory"
    assert asci_courses["ASCI 2220"]["title"] == "Animal Nutrition and Feeding"
    assert asci_courses["ASCI 2229"]["title"] == "Anatomy and Physiology of Farm Animals"
    assert asci_courses["ASCI 3302"]["title"] == "Animal Genetics"
    assert asci_courses["ASCI 3304"]["title"] == "Animal Genomics"
    assert asci_courses["ASCI 3351"]["title"] == "Mechanisms of Hormone Action and Reproductive Physiology"
    assert asci_courses["ASCI 4477/4478/4479"]["title"] == "Senior Project"
    assert asci_courses["MATH 1006"]["category"] == "support"
    assert asci_courses["GE UD-4"]["category"] == "ge"
    assert asci_courses["Animal Mgmt 1"]["is_placeholder"] is True
    assert asci_courses["Free"]["category"] == "concentration"
    assert "ASCI" not in CONCENTRATIONS


def test_animal_science_prerequisites_and_quarter_equivalents_are_mapped():
    asci_courses = {course["course_number"]: course for course in FLOWCHARTS["ASCI"]["courses"]}

    assert asci_courses["ASCI 2220"]["prerequisites"] == ["ASCI 1101", "BIO 1151", "CHEM 1120"]
    assert asci_courses["ASCI 3302"]["prerequisites"] == ["BIO 1151", "STAT 1110"]
    assert asci_courses["ASCI 3304"]["prerequisites"] == ["ASCI 3302"]
    assert asci_courses["ASCI 3351"]["prerequisites"] == ["ASCI 2229"]
    assert "ASCI 101" in asci_courses["ASCI 1100"]["quarter_equivalents"]
    assert "ASCI 220" in asci_courses["ASCI 2220"]["quarter_equivalents"]
    assert "ASCI 302" in asci_courses["ASCI 3302"]["quarter_equivalents"]
    assert "ASCI 477" in asci_courses["ASCI 4477/4478/4479"]["quarter_equivalents"]


def test_anthropology_geography_flowchart_contains_expected_core_and_placeholders():
    antgeog_courses = {course["course_number"]: course for course in FLOWCHARTS["ANTGEOG"]["courses"]}
    antgeog_by_id = {course["id"]: course for course in FLOWCHARTS["ANTGEOG"]["courses"]}

    assert FLOWCHARTS["ANTGEOG"]["total_units"] == 120
    assert antgeog_courses["ANT 2201"]["title"] == "Cultural Anthropology"
    assert antgeog_courses["GEOG 1150"]["title"] == "Human Geography"
    assert antgeog_courses["ANT 2250"]["title"] == "Biological Anthropology"
    assert antgeog_courses["ANT 3307"]["title"] == "World Prehistory"
    assert antgeog_courses["GEOG 3320"]["title"] == "Applications in GIS"
    assert antgeog_courses["GEOG 4410"]["title"] == "Advanced Applications in GIS"
    assert antgeog_courses["ANT 4461 / GEOG 4461"]["title"] == "Anthropology or Geography Senior Project I"
    assert antgeog_courses["ANT 4462 / GEOG 4462"]["title"] == "Anthropology or Geography Senior Project II"
    assert antgeog_courses["STAT 1110"]["category"] == "support"
    assert antgeog_courses["GE 4B"]["category"] == "ge"
    assert antgeog_by_id["ANTGEOG_LDC1"]["is_placeholder"] is True
    assert antgeog_by_id["ANTGEOG_CON_JRS1"]["category"] == "concentration"
    assert antgeog_by_id["ANTGEOG_CON_JRS1"]["is_placeholder"] is True
    assert antgeog_by_id["ANTGEOG_FREE1"]["category"] == "concentration"
    assert antgeog_by_id["ANTGEOG_FREE1"]["is_placeholder"] is True
    assert "ANTGEOG" in CONCENTRATIONS


def test_anthropology_geography_prerequisites_and_quarter_equivalents_are_mapped():
    antgeog_courses = {course["course_number"]: course for course in FLOWCHARTS["ANTGEOG"]["courses"]}

    assert antgeog_courses["ANT 3307"]["prerequisites"] == ["ANT 2202"]
    assert antgeog_courses["ANT 3303"]["prerequisites"] == ["ANT 2201"]
    assert antgeog_courses["GEOG 3320"]["prerequisites"] == ["GEOG 1150"]
    assert antgeog_courses["GEOG 4410"]["prerequisites"] == ["GEOG 3320"]
    assert antgeog_courses["ANT 4461 / GEOG 4461"]["prerequisites"] == ["ANT 3303", "GEOG 3350"]
    assert antgeog_courses["ANT 4462 / GEOG 4462"]["prerequisites"] == ["ANT 4461 / GEOG 4461"]
    assert "ANT 201" in antgeog_courses["ANT 2201"]["quarter_equivalents"]
    assert "GEOG 150" in antgeog_courses["GEOG 1150"]["quarter_equivalents"]
    assert "ANT 307" in antgeog_courses["ANT 3307"]["quarter_equivalents"]
    assert antgeog_courses["ANT 4461 / GEOG 4461"]["is_placeholder"] is True
    assert "ANT 4461" in antgeog_courses["ANT 4461 / GEOG 4461"]["quarter_equivalents"]
    assert "GEOG 4461" in antgeog_courses["ANT 4461 / GEOG 4461"]["quarter_equivalents"]
    assert antgeog_courses["ANT 4462 / GEOG 4462"]["is_placeholder"] is True
    assert "ANT 4462" in antgeog_courses["ANT 4462 / GEOG 4462"]["quarter_equivalents"]
    assert "GEOG 4462" in antgeog_courses["ANT 4462 / GEOG 4462"]["quarter_equivalents"]
    assert "GEOG 462" in antgeog_courses["ANT 4462 / GEOG 4462"]["quarter_equivalents"]


def test_anthropology_geography_concentrations_cover_catalog_options():
    antgeog_concentrations = CONCENTRATIONS["ANTGEOG"]
    concentration_ids = {concentration["id"] for concentration in antgeog_concentrations}

    assert {
        "none",
        "environmental_sustainability",
        "global_studies",
        "human_ecology",
        "individualized",
    } <= concentration_ids

    environmental = next(c for c in antgeog_concentrations if c["id"] == "environmental_sustainability")
    assert environmental["slot_overrides"]["ANTGEOG_CON_JRS2"]["course_number"] == "GEOG 4435"

    global_studies = next(c for c in antgeog_concentrations if c["id"] == "global_studies")
    assert global_studies["slot_overrides"]["ANTGEOG_CON_JRS1"]["course_number"] == "GEOG 4408"
    assert global_studies["slot_overrides"]["ANTGEOG_CON_SRF1"]["course_number"] == "ANT 4401"

    human_ecology = next(c for c in antgeog_concentrations if c["id"] == "human_ecology")
    assert human_ecology["slot_overrides"]["ANTGEOG_CON_JRS1"]["course_number"] == "ANT 3309/3320"


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
    assert psy_courses["PSY 4449 / PSY 4454"]["prerequisites"] == ["PSY 4448 / PSY 4453"]


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
    assert "PSY 2205" in psy_by_id["PSY_FOUND"]["quarter_equivalents"]
    assert "PSY 2252" in psy_by_id["PSY_FOUND"]["quarter_equivalents"]
    assert "PSY 2256" in psy_by_id["PSY_FOUND"]["quarter_equivalents"]
    assert "PSY 4448" in psy_by_id["PSY_INTERN1"]["quarter_equivalents"]
    assert "PSY 4453" in psy_by_id["PSY_INTERN1"]["quarter_equivalents"]
    assert psy_by_id["PSY_INTERN2"]["is_placeholder"] is True
    assert "PSY 4449" in psy_by_id["PSY_INTERN2"]["quarter_equivalents"]
    assert "PSY 4454" in psy_by_id["PSY_INTERN2"]["quarter_equivalents"]


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


def test_agricultural_business_flowchart_contains_expected_core_sequence():
    agb_courses = {course["course_number"]: course for course in FLOWCHARTS["AGB"]["courses"]}
    agb_by_id = {course["id"]: course for course in FLOWCHARTS["AGB"]["courses"]}

    assert FLOWCHARTS["AGB"]["total_units"] == 120
    assert agb_courses["AGB 1101"]["title"] == "Introduction to Agribusiness"
    assert agb_courses["AGB 2202"]["title"] == "Introduction to Sales"
    assert agb_courses["AGB 2212"]["category"] == "major"
    assert agb_courses["AGB 2214"]["category"] == "major"
    assert agb_courses["AGB 2260"]["category"] == "major"
    assert agb_courses["MATH 1267"]["category"] == "support"
    assert agb_courses["ECON 2040"]["category"] == "support"
    assert agb_courses["STAT 1210"]["category"] == "support"
    assert agb_courses["AGB 3301"]["prerequisites"] == ["AGB 2212"]
    assert agb_courses["AGB 3308"]["prerequisites"] == ["AGB 2214", "AGB 2260"]
    assert agb_courses["AGB 3327"]["prerequisites"] == ["AGB 2260", "STAT 1210"]
    assert agb_courses["AGB 3322"]["prerequisites"] == ["AGB 2212", "AGB 2214"]
    assert agb_courses["AGB 3328"]["prerequisites"] == ["AGB 2260", "MATH 1267", "STAT 1210"]
    assert agb_courses["AGB 3312"]["prerequisites"] == ["AGB 2212", "ECON 2040"]
    assert agb_courses["AGB 3369"]["prerequisites"] == ["AGB 2212"]
    assert agb_courses["AGB 4462 / AGB 4463"]["title"] == "Senior Project"
    assert agb_courses["AGB 4462 / AGB 4463"]["is_placeholder"] is True
    assert "AGB 4462" in agb_courses["AGB 4462 / AGB 4463"]["quarter_equivalents"]
    assert "AGB 4463" in agb_courses["AGB 4462 / AGB 4463"]["quarter_equivalents"]
    assert agb_courses["GE UD-3"]["category"] == "ge"
    assert agb_courses["GE UD-4"]["category"] == "ge"
    assert agb_by_id["AGB_AGELE1"]["elective_key"] == "agb_agricultural_elective"
    assert "ASCI 1112" in agb_by_id["AGB_AGELE1"]["quarter_equivalents"]
    assert "PLSC 1120L" in agb_by_id["AGB_AGELE1"]["quarter_equivalents"]
    assert "SS 120" in agb_by_id["AGB_AGELE1"]["quarter_equivalents"]
    assert agb_by_id["AGB_GEN1"]["is_placeholder"] is True
    assert agb_by_id["AGB_GEN1"]["category"] == "major"
    assert agb_by_id["AGB_GEN1"]["elective_key"] == "agb_general_elective"
    assert agb_by_id["AGB_GEN5"]["elective_key"] == "agb_4000_elective"
    assert agb_by_id["AGB_CAFES1"]["title"] == "CAFES Prefix Elective"
    assert agb_by_id["AGB_CAFES1"]["elective_key"] == "agb_cafes_prefix_elective"
    assert agb_by_id["AGB_CAFES2"]["elective_key"] == "agb_cafes_prefix_elective"
    assert "AGB" not in CONCENTRATIONS


def test_architectural_engineering_flowchart_contains_expected_core_sequence():
    arce_courses = {course["course_number"]: course for course in FLOWCHARTS["ARCE"]["courses"]}
    arce_by_id = {course["id"]: course for course in FLOWCHARTS["ARCE"]["courses"]}

    assert FLOWCHARTS["ARCE"]["total_units"] == 128
    assert arce_courses["ARCE 1110"]["title"] == "Introduction to Architectural Engineering"
    assert arce_courses["ARCE 1121"]["category"] == "major"
    assert arce_courses["ARCE 1121"]["prerequisites"] == ["ARCE 1110"]
    assert arce_courses["ARCE 2211"]["prerequisites"] == ["ARCE 1121"]
    assert arce_courses["ARCE 3311"]["prerequisites"] == ["ARCE 2211"]
    assert arce_courses["ARCE 3332"]["prerequisites"] == ["ARCE 3331"]
    assert arce_courses["ARCE 3341"]["prerequisites"] == ["ARCE 3311"]
    assert arce_courses["ARCE 4411"]["prerequisites"] == ["ARCE 3311"]
    assert arce_courses["ARCE 4413"]["prerequisites"] == ["ARCE 4411"]
    assert arce_courses["ARCE 4461"]["prerequisites"] == ["ARCE 3311"]
    assert arce_courses["ARCE 4462"]["title"] == "Senior Project"
    assert arce_courses["MATH 1261"]["category"] == "support"
    assert arce_courses["CHEM 1120"]["category"] == "support"
    assert arce_courses["STAT 3210"]["category"] == "support"
    assert arce_courses["GE 4A"]["category"] == "ge"
    assert arce_courses["GE UD-3"]["category"] == "ge"
    assert arce_by_id["ARCE_FE_TE1"]["is_placeholder"] is True
    assert arce_by_id["ARCE_SURVEY"]["is_placeholder"] is True
    assert arce_by_id["ARCE_ELEC"]["is_placeholder"] is True
    assert "ARCE" not in CONCENTRATIONS


def test_architecture_flowchart_contains_expected_five_year_core_and_placeholders():
    arch_courses = {course["course_number"]: course for course in FLOWCHARTS["ARCH"]["courses"]}
    arch_by_id = {course["id"]: course for course in FLOWCHARTS["ARCH"]["courses"]}

    assert FLOWCHARTS["ARCH"]["total_units"] == 150
    assert FLOWCHARTS["ARCH"]["columns"][-1] == {"year": "Fifth Year", "term": "Spring"}
    assert arch_courses["ARCH 1101"]["title"] == "Architectural Design I"
    assert arch_courses["ARCH 2201"]["title"] == "Architectural Design III"
    assert arch_courses["ARCH 3301"]["title"] == "Integrated Architectural Design"
    assert arch_courses["ARCH 4425"]["title"] == "Seminar in Architectural History, Theory and Criticism"
    assert arch_courses["ARCH 4461"]["title"] == "Senior Project: Architectural Thesis I"
    assert arch_courses["ARCH 4462"]["title"] == "Senior Project: Architectural Thesis II"
    assert arch_courses["EDES 1123"]["category"] == "support"
    assert arch_courses["ARCE 3301"]["category"] == "support"
    assert arch_courses["GE UD-4"]["category"] == "ge"
    assert arch_by_id["ARCH_MATH_CHOICE"]["is_placeholder"] is True
    assert arch_by_id["ARCH_PHYS_CHOICE"]["is_placeholder"] is True
    assert "MATH 1007" in arch_by_id["ARCH_MATH_CHOICE"]["quarter_equivalents"]
    assert "MATH 1261" in arch_by_id["ARCH_MATH_CHOICE"]["quarter_equivalents"]
    assert "PHYS 1121" in arch_by_id["ARCH_PHYS_CHOICE"]["quarter_equivalents"]
    assert "PHYS 1141" in arch_by_id["ARCH_PHYS_CHOICE"]["quarter_equivalents"]
    assert arch_by_id["ARCH_PROF_ELEC1"]["category"] == "concentration"
    assert arch_by_id["ARCH_PROF_ELEC1"]["is_placeholder"] is True
    assert arch_by_id["ARCH_GE_UD25"]["is_placeholder"] is True
    assert "ARCH" not in CONCENTRATIONS


def test_architecture_prerequisites_and_quarter_equivalents_are_mapped():
    arch_courses = {course["course_number"]: course for course in FLOWCHARTS["ARCH"]["courses"]}

    assert arch_courses["ARCH 1102"]["prerequisites"] == ["ARCH 1101"]
    assert arch_courses["ARCH 2201"]["prerequisites"] == ["ARCH 1102"]
    assert arch_courses["ARCH 2242"]["prerequisites"] == ["ARCH 2241"]
    assert arch_courses["ARCE 3301"]["prerequisites"] == ["ARCE 1121"]
    assert arch_courses["ARCE 1121"]["prerequisites"] == ["PHYS 1121 / PHYS 1141", "MATH 1007 / MATH 1261"]
    assert arch_courses["ARCH 3301"]["prerequisites"] == ["ARCE 3301", "ARCH 2202", "ARCH 3341"]
    assert arch_courses["ARCH 4462"]["prerequisites"] == ["ARCH 4461"]
    assert "ARCH 131" in arch_courses["ARCH 1101"]["quarter_equivalents"]
    assert "ARCH 251" in arch_courses["ARCH 2201"]["quarter_equivalents"]
    assert "ARCH 351" in arch_courses["ARCH 4401"]["quarter_equivalents"]
    assert "ARCH 481" in arch_courses["ARCH 4461"]["quarter_equivalents"]


def test_biological_sciences_flowchart_contains_expected_core_and_placeholders():
    bio_courses = {course["course_number"]: course for course in FLOWCHARTS["BIO"]["courses"]}
    bio_by_id = {course["id"]: course for course in FLOWCHARTS["BIO"]["courses"]}

    assert FLOWCHARTS["BIO"]["total_units"] == 120
    assert bio_courses["BIO 1150"]["title"] == "Life: History and Diversity"
    assert bio_courses["BIO 1151"]["title"] == "Life: Molecules and Cells"
    assert bio_courses["BIO 2253"]["title"] == "Principles of Ecology and Evolution"
    assert bio_courses["BIO 3351"]["title"] == "Principles of Genetics"
    assert bio_courses["BIO 3352"]["title"] == "Principles of Animal Physiology"
    assert bio_courses["BIO 4461/4462/4463"]["title"] == "Senior Project"
    assert bio_courses["CHEM 1120"]["category"] == "support"
    assert bio_courses["MATH 1264"]["category"] == "support"
    assert bio_courses["GE UD-4"]["category"] == "ge"
    assert bio_by_id["BIO_CHEM2240_2242"]["is_placeholder"] is True
    assert bio_by_id["BIO_PHYS1121_1141"]["is_placeholder"] is True
    assert bio_by_id["BIO_CON_JRF1"]["category"] == "concentration"
    assert bio_by_id["BIO_CON_JRF1"]["is_placeholder"] is True
    assert bio_by_id["BIO_FREE_SRS"]["category"] == "concentration"
    assert bio_by_id["BIO_FREE_SRS"]["is_placeholder"] is True
    assert "BIO" in CONCENTRATIONS


def test_biological_sciences_prerequisites_and_quarter_equivalents_are_mapped():
    bio_courses = {course["course_number"]: course for course in FLOWCHARTS["BIO"]["courses"]}

    assert bio_courses["CHEM 1122"]["prerequisites"] == ["CHEM 1120"]
    assert bio_courses["BIO 2253"]["prerequisites"] == ["BIO 1150", "BIO 1151"]
    assert bio_courses["BIO 3351"]["prerequisites"] == ["BIO 1151", "CHEM 1120", "CHEM 1122"]
    assert bio_courses["BIO 3352"]["prerequisites"] == ["BIO 1151", "CHEM 1120", "CHEM 1122"]
    assert bio_courses["BIO 4461/4462/4463"]["prerequisites"] == ["STAT 1110"]
    assert "BIO 150" in bio_courses["BIO 1150"]["quarter_equivalents"]
    assert "BIO 161" in bio_courses["BIO 1151"]["quarter_equivalents"]
    assert "BIO 263" in bio_courses["BIO 2253"]["quarter_equivalents"]
    assert "BIO 351" in bio_courses["BIO 3351"]["quarter_equivalents"]
    assert "BIO 461" in bio_courses["BIO 4461/4462/4463"]["quarter_equivalents"]


def test_biological_sciences_concentrations_cover_catalog_options():
    bio_concentrations = CONCENTRATIONS["BIO"]
    concentration_ids = {concentration["id"] for concentration in bio_concentrations}

    assert {
        "none",
        "anatomy_physiology",
        "ecology_evolution_biodiversity_conservation",
        "molecular_cellular",
    } <= concentration_ids

    anatomy = next(c for c in bio_concentrations if c["id"] == "anatomy_physiology")
    assert anatomy["slot_overrides"]["BIO_CON_JRF1"]["course_number"] == "BIO 4431"
    assert anatomy["slot_overrides"]["BIO_CON_JRS1"]["course_number"] == "BIO 4432"

    ecology = next(c for c in bio_concentrations if c["id"] == "ecology_evolution_biodiversity_conservation")
    assert ecology["slot_overrides"]["BIO_CON_JRS1"]["course_number"] == "BIO 4413/4414"
    assert ecology["slot_overrides"]["BIO_CON_SRF1"]["course_number"] == "BIO 3343"

    molecular = next(c for c in bio_concentrations if c["id"] == "molecular_cellular")
    assert molecular["slot_overrides"]["BIO_CON_JRF1"]["course_number"] == "BIO 4457"
    assert molecular["slot_overrides"]["BIO_CON_JRS1"]["course_number"] == "BIO 4452"


def test_biomedical_engineering_flowchart_contains_expected_core_and_placeholders():
    bmed_courses = {course["course_number"]: course for course in FLOWCHARTS["BMED"]["courses"]}
    bmed_by_id = {course["id"]: course for course in FLOWCHARTS["BMED"]["courses"]}

    assert FLOWCHARTS["BMED"]["total_units"] == 130
    assert bmed_courses["BMED 1101"]["title"] == "Introduction to Biomedical Engineering"
    assert bmed_courses["BMED 2212"]["title"] == "Biomedical Engineering Fundamentals"
    assert bmed_courses["BMED 2420"]["title"] == "Biomaterials"
    assert bmed_courses["BMED 3430"]["title"] == "Modeling of Biomedical Systems"
    assert bmed_courses["BMED 4440"]["title"] == "Biomedical Instrumentation"
    assert bmed_courses["BMED 4599"]["title"] == "Biomedical Engineering Senior Project"
    assert bmed_courses["BIO 1151"]["category"] == "support"
    assert bmed_courses["MATH 2341"]["category"] == "support"
    assert bmed_courses["GE UD-2/5"]["category"] == "ge"
    assert bmed_by_id["BMED_BIO2231_2232"]["is_placeholder"] is True
    assert bmed_by_id["BMED_CON_JRF1"]["category"] == "concentration"
    assert bmed_by_id["BMED_CON_JRF1"]["is_placeholder"] is True
    assert bmed_by_id["BMED_FREE1"]["category"] == "concentration"
    assert bmed_by_id["BMED_FREE1"]["is_placeholder"] is True
    assert "BMED" in CONCENTRATIONS


def test_biomedical_engineering_prerequisites_and_quarter_equivalents_are_mapped():
    bmed_courses = {course["course_number"]: course for course in FLOWCHARTS["BMED"]["courses"]}

    assert bmed_courses["CHEM 1122"]["prerequisites"] == ["CHEM 1120"]
    assert bmed_courses["MATH 1262"]["prerequisites"] == ["MATH 1261"]
    assert bmed_courses["PHYS 1143"]["prerequisites"] == ["PHYS 1141", "MATH 1261"]
    assert bmed_courses["BMED 2420"]["prerequisites"] == ["BMED 2212", "CHEM 1120", "ENGR 2211"]
    assert bmed_courses["BMED 4440"]["prerequisites"] == ["BMED 2310", "BMED 2311"]
    assert bmed_courses["BMED 4599"]["prerequisites"] == ["BMED 3425"]
    assert "BMED 101" in bmed_courses["BMED 1101"]["quarter_equivalents"]
    assert "BMED 420" in bmed_courses["BMED 2420"]["quarter_equivalents"]
    assert "BMED 440" in bmed_courses["BMED 4440"]["quarter_equivalents"]
    assert "BMED 455" in bmed_courses["BMED 4599"]["quarter_equivalents"]


def test_biomedical_engineering_concentrations_cover_catalog_options():
    bmed_concentrations = CONCENTRATIONS["BMED"]
    concentration_ids = {concentration["id"] for concentration in bmed_concentrations}

    assert {
        "none",
        "bioinstrumentation",
        "cell_and_tissue_engineering",
        "mechanical_design",
        "individualized",
    } <= concentration_ids

    bioinstrumentation = next(c for c in bmed_concentrations if c["id"] == "bioinstrumentation")
    assert bioinstrumentation["slot_overrides"]["BMED_CON_JRF1"]["course_number"] == "BMED 3355"
    assert bioinstrumentation["slot_overrides"]["BMED_CON_SRS1"]["course_number"] == "BMED 4445"

    cell_tissue = next(c for c in bmed_concentrations if c["id"] == "cell_and_tissue_engineering")
    assert cell_tissue["slot_overrides"]["BMED_CON_JRF1"]["course_number"] == "BIO/BMED 3360"
    assert cell_tissue["slot_overrides"]["BMED_CON_SRS1"]["course_number"] == "BMED 4465"

    mechanical = next(c for c in bmed_concentrations if c["id"] == "mechanical_design")
    assert mechanical["slot_overrides"]["BMED_CON_JRS1"]["course_number"] == "ME 3328"
    assert mechanical["slot_overrides"]["BMED_CON_SRS1"]["course_number"] == "ME 4421"


def test_biochemistry_flowchart_contains_expected_core_sequence():
    bioc_courses = {course["course_number"]: course for course in FLOWCHARTS["BIOC"]["courses"]}
    bioc_by_id = {course["id"]: course for course in FLOWCHARTS["BIOC"]["courses"]}

    assert FLOWCHARTS["BIOC"]["total_units"] == 120
    assert bioc_courses["CHEM 1120"]["title"] == "Fundamentals of Chemical Structure and Properties"
    assert bioc_courses["CHEM 1120"]["category"] == "major"
    assert bioc_courses["BIO 1151"]["title"] == "Life: Molecules and Cells"
    assert bioc_courses["BIO 1151"]["category"] == "support"
    assert bioc_courses["CHEM 2242"]["title"] == "Organic Chemistry I"
    assert bioc_courses["CHEM 3352"]["title"] == "Biochemistry"
    assert bioc_courses["CHEM 3356"]["title"] == "Genetic Information Processing"
    assert bioc_courses["CHEM 3354"]["title"] == "Metabolism"
    assert bioc_courses["CHEM 4461"]["title"] == "Senior Project I"
    assert bioc_courses["CHEM 4462"]["title"] == "Senior Project II"
    assert bioc_courses["GE 1A"]["category"] == "ge"
    assert bioc_by_id["BIOC_CHEM2201_2203"]["is_placeholder"] is True
    assert bioc_by_id["BIOC_CON_JRF"]["category"] == "concentration"
    assert bioc_by_id["BIOC_CON_JRF"]["is_placeholder"] is True
    assert bioc_by_id["BIOC_FREE1"]["is_placeholder"] is True
    assert "BIOC" in CONCENTRATIONS


def test_biochemistry_prerequisites_and_quarter_equivalents_are_mapped():
    bioc_courses = {course["course_number"]: course for course in FLOWCHARTS["BIOC"]["courses"]}

    assert bioc_courses["CHEM 1122"]["prerequisites"] == ["CHEM 1120"]
    assert bioc_courses["MATH 1262"]["prerequisites"] == ["MATH 1261"]
    assert bioc_courses["CHEM 2242"]["prerequisites"] == ["CHEM 1122"]
    assert bioc_courses["CHEM 3352"]["prerequisites"] == ["CHEM 2242"]
    assert bioc_courses["CHEM 3356"]["prerequisites"] == ["CHEM 3352"]
    assert bioc_courses["CHEM 4462"]["prerequisites"] == ["CHEM 4461"]
    assert "CHEM 124" in bioc_courses["CHEM 1120"]["quarter_equivalents"]
    assert "CHEM 125" in bioc_courses["CHEM 1122"]["quarter_equivalents"]
    assert "MATH 141" in bioc_courses["MATH 1261"]["quarter_equivalents"]
    assert "CHEM 312" in bioc_courses["CHEM 2242"]["quarter_equivalents"]
    assert "CHEM 350" in bioc_courses["CHEM 3352"]["quarter_equivalents"]


def test_biochemistry_concentrations_cover_catalog_options():
    bioc_concentrations = CONCENTRATIONS["BIOC"]
    concentration_ids = {concentration["id"] for concentration in bioc_concentrations}

    assert {"none", "polymers_coatings"} <= concentration_ids

    polymers = next(c for c in bioc_concentrations if c["id"] == "polymers_coatings")
    assert polymers["slot_overrides"]["BIOC_CON_JRF"]["course_number"] == "CHEM 3380"
    assert polymers["slot_overrides"]["BIOC_CON_JRS"]["course_number"] == "CHEM 4480/4481"
    assert polymers["slot_overrides"]["BIOC_CON_SRF"]["course_number"] == "CHEM 4482/4483"
    assert polymers["slot_overrides"]["BIOC_CON_SRS"]["course_number"] == "CHEM 4486"


def test_agricultural_systems_management_flowchart_contains_expected_core_sequence():
    asm_courses = {course["course_number"]: course for course in FLOWCHARTS["ASM"]["courses"]}
    asm_by_id = {course["id"]: course for course in FLOWCHARTS["ASM"]["courses"]}

    assert FLOWCHARTS["ASM"]["total_units"] == 121
    assert asm_courses["BRAE 1128"]["title"] == "Careers in BioResource and Agricultural Engineering"
    assert asm_courses["BRAE 2203"]["title"] == "Systems Management I"
    assert asm_courses["BRAE 3317"]["title"] == "Systems Management II"
    assert asm_courses["BRAE 4419"]["title"] == "Systems Management III"
    assert asm_courses["BRAE 3340"]["title"] == "Irrigation Water Management"
    assert asm_courses["BRAE 4460"]["title"] == "Senior Project I"
    assert asm_courses["BRAE 4461"]["title"] == "Senior Project II"
    assert asm_courses["BRAE 2203"]["category"] == "major"
    assert asm_courses["AGB 2212"]["category"] == "support"
    assert asm_courses["GE 1A"]["category"] == "ge"
    assert asm_by_id["ASM_MATH1007_STAT1110"]["is_placeholder"] is True
    assert asm_by_id["ASM_ELEC1"]["category"] == "concentration"
    assert asm_by_id["ASM_ELEC1"]["is_placeholder"] is True
    assert "ASM" not in CONCENTRATIONS


def test_agricultural_systems_management_prerequisites_are_mapped():
    asm_courses = {course["course_number"]: course for course in FLOWCHARTS["ASM"]["courses"]}

    assert asm_courses["BRAE 2203"]["prerequisites"] == ["BRAE 1128", "BRAE 1150"]
    assert asm_courses["BRAE 2142"]["prerequisites"] == ["BRAE 1150"]
    assert asm_courses["BRAE 3317"]["prerequisites"] == ["BRAE 2203"]
    assert asm_courses["BRAE 3343"]["prerequisites"] == ["BRAE 2142"]
    assert asm_courses["BRAE 4419"]["prerequisites"] == ["BRAE 3317"]
    assert asm_courses["BRAE 4440"]["prerequisites"] == ["BRAE 3340"]
    assert asm_courses["BRAE 4461"]["prerequisites"] == ["BRAE 4460"]
    assert "STAT 218" in asm_courses["MATH 1007 / STAT 1110 / MATH 1267"]["quarter_equivalents"]
    assert "MATH 1267" in asm_courses["MATH 1007 / STAT 1110 / MATH 1267"]["quarter_equivalents"]
    assert "AGB 212" in asm_courses["AGB 2212"]["quarter_equivalents"]
    assert "AGB 308" in asm_courses["AGB 3308"]["quarter_equivalents"]


def test_bioresource_agricultural_engineering_flowchart_contains_expected_core_sequence():
    brae_courses = {course["course_number"]: course for course in FLOWCHARTS["BRAE"]["courses"]}
    brae_by_id = {course["id"]: course for course in FLOWCHARTS["BRAE"]["courses"]}

    assert FLOWCHARTS["BRAE"]["total_units"] == 128
    assert brae_courses["BRAE 1128"]["title"] == "Careers in BioResource and Agricultural Engineering"
    assert brae_courses["BRAE 1128"]["category"] == "major"
    assert brae_courses["MATH 1261"]["category"] == "support"
    assert brae_courses["BRAE 2221"]["title"] == "Engineering Mechanics with Agricultural Applications I"
    assert brae_courses["BRAE 2222"]["title"] == "Engineering Mechanics with Agricultural Applications II"
    assert brae_courses["BRAE 4414"]["title"] == "Irrigation Engineering"
    assert brae_courses["BRAE 4461"]["title"] == "Senior Project II"
    assert brae_by_id["BRAE_GE1A"]["is_placeholder"] is True
    assert brae_by_id["BRAE_ELECTIVE"]["is_placeholder"] is True
    assert brae_by_id["BRAE_FOCUS1"]["category"] == "concentration"
    assert brae_by_id["BRAE_ECON"]["is_placeholder"] is True
    assert "BRAE" not in CONCENTRATIONS


def test_bioresource_agricultural_engineering_prerequisites_are_mapped():
    brae_courses = {course["course_number"]: course for course in FLOWCHARTS["BRAE"]["courses"]}

    assert "MATH 1261" in brae_courses["MATH 1262"]["prerequisites"]
    assert "MATH 1262" in brae_courses["MATH 2263"]["prerequisites"]
    assert "PHYS 1141" in brae_courses["PHYS 1143"]["prerequisites"]
    assert "BRAE 1128" in brae_courses["BRAE 1150"]["prerequisites"]
    assert "BRAE 2221" in brae_courses["BRAE 2222"]["prerequisites"]
    assert "BRAE 2221" in brae_courses["BRAE 3312"]["prerequisites"]
    assert "BRAE 2236" in brae_courses["BRAE 4414"]["prerequisites"]
    assert "BRAE 2216" in brae_courses["BRAE 4428"]["prerequisites"]
    assert "BRAE 3234" in brae_courses["BRAE 4422"]["prerequisites"]
    assert "BRAE 4460" in brae_courses["BRAE 4461"]["prerequisites"]
    assert "MATH 141" in brae_courses["MATH 1261"]["quarter_equivalents"]
    assert "BRAE 236" in brae_courses["BRAE 2236"]["quarter_equivalents"]
    assert "PHYS 132" in brae_courses["PHYS 1143"]["quarter_equivalents"]


def test_business_administration_flowchart_contains_expected_core_sequence():
    bus_courses = {course["course_number"]: course for course in FLOWCHARTS["BUS"]["courses"]}
    bus_by_id = {course["id"]: course for course in FLOWCHARTS["BUS"]["courses"]}

    assert FLOWCHARTS["BUS"]["total_units"] == 120
    assert bus_courses["BUS 1100"]["title"] == "Career Readiness I"
    assert bus_courses["BUS 2214"]["title"] == "Financial Accounting"
    assert bus_courses["BUS 2215"]["title"] == "Managerial Accounting"
    assert bus_courses["BUS 3346"]["title"] == "Principles of Marketing"
    assert bus_courses["BUS 3387"]["title"] == "Organizational Behavior"
    assert bus_courses["BUS 4401 & 4411"]["title"] == "Strategic Management and Assessment"
    assert bus_courses["BUS 2214"]["category"] == "major"
    assert bus_courses["ECON 2001"]["category"] == "support"
    assert bus_courses["STAT 1210"]["category"] == "support"
    assert bus_courses["STAT 1220"]["category"] == "support"
    assert bus_courses["GE 1A"]["category"] == "ge"
    assert bus_by_id["BUS_GE1A"]["is_placeholder"] is True
    assert bus_by_id["BUS_MATH"]["is_placeholder"] is True
    assert "MATH 1264" in bus_by_id["BUS_MATH"]["quarter_equivalents"]
    assert "MATH 1267" in bus_by_id["BUS_MATH"]["quarter_equivalents"]
    assert bus_by_id["BUS_FIN_ELEC"]["is_placeholder"] is True
    assert "BUS 1342" in bus_by_id["BUS_FIN_ELEC"]["quarter_equivalents"]
    assert "BUS 3343" in bus_by_id["BUS_FIN_ELEC"]["quarter_equivalents"]
    assert bus_by_id["BUS_CON1"]["is_placeholder"] is True
    assert bus_by_id["BUS_CON1"]["category"] == "concentration"
    assert bus_by_id["BUS_FREE1"]["is_placeholder"] is True
    assert "BUS" in CONCENTRATIONS


def test_business_administration_prerequisites_are_mapped():
    bus_courses = {course["course_number"]: course for course in FLOWCHARTS["BUS"]["courses"]}

    assert bus_courses["BUS 2215"]["prerequisites"] == ["BUS 2214"]
    assert bus_courses["STAT 1220"]["prerequisites"] == ["STAT 1210"]
    assert bus_courses["BUS 2206"]["prerequisites"] == ["BUS 1100"]
    assert bus_courses["BUS 3306"]["prerequisites"] == ["BUS 2206"]
    assert bus_courses["BUS 4404"]["prerequisites"] == ["BUS 2207"]
    assert "BUS 3346" in bus_courses["BUS 4401 & 4411"]["prerequisites"]
    assert "BUS 3387" in bus_courses["BUS 4401 & 4411"]["prerequisites"]
    assert "BUS 214" in bus_courses["BUS 2214"]["quarter_equivalents"]
    assert "BUS 215" in bus_courses["BUS 2215"]["quarter_equivalents"]
    assert "STAT 251" in bus_courses["STAT 1210"]["quarter_equivalents"]
    assert "STAT 252" in bus_courses["STAT 1220"]["quarter_equivalents"]


def test_business_administration_ge_placeholders_are_present():
    bus_by_id = {course["id"]: course for course in FLOWCHARTS["BUS"]["courses"]}

    for ge_id in ["BUS_GE1A", "BUS_GE1B", "BUS_GE1C", "BUS_GE3A", "BUS_GE3B",
                  "BUS_GE4A", "BUS_GE5A", "BUS_GE5B", "BUS_GE5C", "BUS_GE6",
                  "BUS_GE_UD4", "BUS_GE_UD25", "BUS_GE_UD3"]:
        assert ge_id in bus_by_id, f"{ge_id} missing from BUS flowchart"
        assert bus_by_id[ge_id]["is_placeholder"] is True


def test_business_administration_concentrations_cover_catalog_options():
    bus_concentrations = CONCENTRATIONS["BUS"]
    concentration_ids = {c["id"] for c in bus_concentrations}

    assert {"accounting", "consumer_packaging", "entrepreneurship",
            "financial_management", "information_systems_analytics",
            "management_human_resources", "marketing_management",
            "real_estate_finance", "supply_chain_management"} <= concentration_ids

    acct = next(c for c in bus_concentrations if c["id"] == "accounting")
    assert acct["slot_overrides"]["BUS_CON1"]["course_number"] == "BUS 3319"
    assert acct["slot_overrides"]["BUS_CON5"]["units"] == 4
    assert acct["slot_overrides"]["BUS_CON7"]["course_number"] == "BUS 3323"

    isa = next(c for c in bus_concentrations if c["id"] == "information_systems_analytics")
    assert isa["slot_overrides"]["BUS_CON1"]["course_number"] == "BUS 3393"
    assert isa["slot_overrides"]["BUS_CON3"]["course_number"] == "BUS 3394"


def test_cpe_ethics_or_stats_is_or_choice_placeholder():
    cpe_by_id = {course["id"]: course for course in FLOWCHARTS["CPE"]["courses"]}
    cpe_by_num = {course["course_number"]: course for course in FLOWCHARTS["CPE"]["courses"]}

    # The ethics/stats slot must be a single slash placeholder
    assert "CPE_PHIL3323" in cpe_by_id
    slot = cpe_by_id["CPE_PHIL3323"]
    assert slot["is_placeholder"] is True
    assert "PHIL 3323" in slot["course_number"]
    assert "STAT 3210" in slot["course_number"]
    assert "STAT 3310" in slot["course_number"]
    assert slot.get("elective_key") == "cpe_ethics_or_stats"
    assert "STAT 312" in slot["quarter_equivalents"]

    # STAT 3210 must NOT appear as a separate required course
    assert "STAT 3210" not in cpe_by_num


def test_arce_history_elective_includes_all_three_options():
    arce_by_id = {course["id"]: course for course in FLOWCHARTS["ARCE"]["courses"]}

    hist = arce_by_id["ARCE_HIST"]
    assert hist["is_placeholder"] is True
    assert "ARCH 2221" in hist["course_number"]
    assert "ARCH 2222" in hist["course_number"]
    assert "ARCE 2280" in hist["course_number"]
    assert hist.get("elective_key") == "arce_hist_elective"
    assert "ARCH 2222" in hist["quarter_equivalents"]
    assert "ARCH 2221" in hist["quarter_equivalents"]
    assert "ARCE 2280" in hist["quarter_equivalents"]

    survey = arce_by_id["ARCE_SURVEY"]
    assert survey["is_placeholder"] is True
    assert survey.get("elective_key") == "arce_surveying_elective"


def test_me_ime_manufacturing_selective_has_elective_key():
    me_by_id = {course["id"]: course for course in FLOWCHARTS["ME"]["courses"]}

    slot = me_by_id["ME_IME114X"]
    assert slot["is_placeholder"] is True
    assert "IME 1141" in slot["course_number"]
    assert slot.get("elective_key") == "me_ime_mfg_selective"
    assert "IME 1141" in slot["quarter_equivalents"]
    assert "IME 1142" in slot["quarter_equivalents"]
    assert "IME 1149" in slot["quarter_equivalents"]


def test_bmed_anatomy_physiology_slash_placeholder_has_elective_key():
    bmed_by_id = {course["id"]: course for course in FLOWCHARTS["BMED"]["courses"]}

    slot = bmed_by_id["BMED_BIO2231_2232"]
    assert slot["is_placeholder"] is True
    assert "BIO 2231" in slot["course_number"]
    assert "BIO 2232" in slot["course_number"]
    assert slot.get("elective_key") == "bmed_anat_phys"
    assert "BIO 2231" in slot["quarter_equivalents"]
    assert "BIO 2232" in slot["quarter_equivalents"]


def test_brae_econ_slash_placeholder_has_elective_key():
    brae_by_id = {course["id"]: course for course in FLOWCHARTS["BRAE"]["courses"]}

    slot = brae_by_id["BRAE_ECON"]
    assert slot["is_placeholder"] is True
    assert "ECON 2001" in slot["course_number"]
    assert "ECON 2040" in slot["course_number"]
    assert slot.get("elective_key") == "brae_econ_elective"
    assert "ECON 2001" in slot["quarter_equivalents"]
    assert "ECON 2040" in slot["quarter_equivalents"]
