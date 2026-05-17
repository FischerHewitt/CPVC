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
    me_by_id = {course["id"]: course for course in FLOWCHARTS["ME"]["courses"]}

    assert FLOWCHARTS["ME"]["total_units"] == 129
    assert sum(course["units"] for course in FLOWCHARTS["ME"]["courses"]) == 129
    assert me_courses["ME 1125"]["title"] == "Introduction to Mechanical Engineering"
    assert me_courses["MATH 1261"]["category"] == "support"
    assert me_courses["CHEM 1120"]["category"] == "support"
    assert me_courses["EE 2115 & EE 2115L"]["category"] == "support"
    assert me_courses["MATE 1220 & MATE 1215"]["units"] == 3
    assert me_courses["ME 3341 & ME 3342"]["title"] == "Fluid Mechanics with Laboratory"
    assert me_courses["ME 3234"]["category"] == "major"
    assert me_courses["ME 3236"]["category"] == "major"
    assert me_courses["BIO 1111 / BIO 2213 / BIO 2215 / BIO 2217"]["category"] == "support"
    assert me_by_id["ME_GE5B"]["elective_key"] == "me_life_science"
    assert me_by_id["ME_TE_SRF1"]["elective_key"] == "me_tech_elective"
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
    assert hvac["slot_overrides"]["ME_TE_SRF1"]["elective_key"] is None

    mechatronics = next(c for c in me_concentrations if c["id"] == "mechatronics")
    assert mechatronics["slot_overrides"]["ME3317"]["course_number"] == "ME 3305"
    assert mechatronics["slot_overrides"]["ME3317"]["prerequisites"] == ["EE 2115 & EE 2115L", "ME 2240"]
    assert mechatronics["slot_overrides"]["ME_TE_SRS1"]["elective_key"] == "me_mechatronics_technical_elective"

    manufacturing = next(c for c in me_concentrations if c["id"] == "manufacturing")
    assert manufacturing["slot_overrides"]["ME_TE_SRF1"]["course_number"] == "IME 3327"
    assert manufacturing["slot_overrides"]["ME_TE_SRS1"]["elective_key"] == "me_manufacturing_elective"


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
    assert sum(course["units"] for course in FLOWCHARTS["POLS"]["courses"]) == 120
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
    assert sum(course["units"] for course in FLOWCHARTS["ENGL"]["courses"]) == 120
    assert english_courses["ENGL 1101"]["title"] == "Introduction to English Studies"
    assert english_courses["ENGL GE 3B"]["title"] == "Literature Elective"
    language = english_courses["CHIN 1101 / FR 1101 / GER 1101 / ITAL 1101 / JPNS 1101 / SPAN 1101 / WLC 1101"]
    assert language["category"] == "support"
    assert language["is_placeholder"] is True
    assert "CHIN 1101" in language["quarter_equivalents"]
    assert "SPAN 1101" in language["quarter_equivalents"]
    assert "WLC 1101" in language["quarter_equivalents"]
    assert english_courses["ENGL UD GWR"]["title"] == "Upper-Division English GWR Elective"
    divers = english_courses["ENGL Diversity"]
    assert divers["title"] == "4000-Level Diversity Elective"
    assert "ENGL 4467" in divers["quarter_equivalents"]
    assert english_courses["ENGL 4461"]["title"] == "Senior Project"
    # GE UD-3 is satisfied by the GWR major course; no separate tile
    assert "GE UD-3" not in english_courses
    assert "ENGL" not in CONCENTRATIONS


def test_music_flowchart_contains_expected_core_and_catalog_buckets():
    music_courses = {course["course_number"]: course for course in FLOWCHARTS["MU"]["courses"]}

    assert FLOWCHARTS["MU"]["total_units"] == 120
    assert sum(course["units"] for course in FLOWCHARTS["MU"]["courses"]) == 120
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
    assert ags_courses["BIO 1111 / BIO 1151 / BOT 1121 / MCRO 2221"]["is_placeholder"] is True
    assert ags_courses["ASCI 1102 + ASCI 1103"]["is_placeholder"] is True
    assert ags_courses["PLSC 1120 + PLSC 1120L"]["is_placeholder"] is True
    assert ags_courses["SS 1120 / SS 1130"]["is_placeholder"] is True
    assert ags_courses["DSCI 2229 / FSN 2245"]["is_placeholder"] is True
    assert ags_courses["AGED 4410 / AGC 3314"]["is_placeholder"] is True
    assert ags_courses["AGB 3301 / WVIT 3343"]["prerequisites"] == ["AGB 2212"]
    assert ags_courses["NR 3308 / NR 3323"]["is_placeholder"] is True
    assert ags_courses["PLSC 3301"]["prerequisites"] == ["PLSC 1120 + PLSC 1120L"]
    assert ags_courses["AGC 4452 / AG 4452"]["is_placeholder"] is True
    assert ags_courses["GE UD-4"]["category"] == "ge"
    assert ags_by_id["AGS_BIO5B"]["elective_key"] == "ags_life_science"
    assert "BOT 1121" in ags_by_id["AGS_BIO5B"]["quarter_equivalents"]
    assert ags_by_id["AGS_ASCI1102_1103"]["elective_key"] == "ags_asci_pair"
    assert "ASCI 1103" in ags_by_id["AGS_ASCI1102_1103"]["quarter_equivalents"]
    assert ags_by_id["AGS_SS1120"]["elective_key"] == "ags_soil_science"
    assert "SS 1130" in ags_by_id["AGS_SS1120"]["quarter_equivalents"]
    assert ags_by_id["AGS_DSCI_FSN"]["elective_key"] == "ags_dairy_food_safety"
    assert "DSCI 2229" in ags_by_id["AGS_DSCI_FSN"]["quarter_equivalents"]
    assert "FSN 2245" in ags_by_id["AGS_DSCI_FSN"]["quarter_equivalents"]
    assert ags_by_id["AGS_AGED_AGC"]["elective_key"] == "ags_aged_agc_choice"
    assert ags_by_id["AGS_NR3308"]["elective_key"] == "ags_nr_choice"
    assert ags_by_id["AGS_AGC4452"]["elective_key"] == "ags_agc_ag_issues"
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
    assert engineering["slot_overrides"]["AGS_EMP_JRF1"]["units"] == 2
    assert engineering["slot_overrides"]["AGS_EMP_SRS2"]["course_number"] == "BRAE/MSCI 4438 / BRAE 4440"
    assert engineering["slot_overrides"]["AGS_EMP_SRS2"]["elective_key"] == "ags_brae_aquaculture_irrigation"

    agribusiness = next(c for c in ags_concentrations if c["id"] == "agribusiness")
    assert agribusiness["slot_overrides"]["AGS_EMP_SRS2"]["course_number"] == "AGB 3313"

    animal = next(c for c in ags_concentrations if c["id"] == "animal_science")
    assert animal["slot_overrides"]["AGS_EMP_JRF1"]["units"] == 1
    assert animal["slot_overrides"]["AGS_EMP_JRS1"]["units"] == 2

    plant = next(c for c in ags_concentrations if c["id"] == "plant_crop_soil")
    assert plant["slot_overrides"]["AGS_EMP_JRF1"]["units"] == 4
    assert plant["slot_overrides"]["AGS_EMP_SRF1"]["units"] == 4

    forestry = next(c for c in ags_concentrations if c["id"] == "forestry_natural_resources")
    assert forestry["slot_overrides"]["AGS_EMP_JRS1"]["units"] == 4
    assert forestry["slot_overrides"]["AGS_EMP_SRF2"]["units"] == 4

    ornamental = next(c for c in ags_concentrations if c["id"] == "ornamental_horticulture")
    assert ornamental["slot_overrides"]["AGS_EMP_JRF1"]["units"] == 4
    assert ornamental["slot_overrides"]["AGS_EMP_SRS2"]["course_number"] == "PLSC 3334"


def test_animal_science_flowchart_contains_expected_core_and_placeholders():
    asci_courses = {course["course_number"]: course for course in FLOWCHARTS["ASCI"]["courses"]}
    asci_by_id = {course["id"]: course for course in FLOWCHARTS["ASCI"]["courses"]}

    assert FLOWCHARTS["ASCI"]["total_units"] == 120
    assert sum(course["units"] for course in FLOWCHARTS["ASCI"]["courses"]) == 120
    assert asci_courses["ASCI 1100"]["title"] == "Introduction to the Animal Sciences"
    assert asci_courses["ASCI 2210 + ASCI 2211"]["title"] == "Meat Science and Meat Science Laboratory"
    assert asci_courses["ASCI 2220"]["title"] == "Animal Nutrition and Feeding"
    assert asci_courses["ASCI 2229"]["title"] == "Anatomy and Physiology of Farm Animals"
    assert asci_courses["ASCI 3302"]["title"] == "Animal Genetics"
    assert asci_courses["ASCI 3304"]["title"] == "Animal Genomics"
    assert asci_courses["ASCI 3351"]["title"] == "Mechanisms of Hormone Action and Reproductive Physiology"
    assert asci_courses["ASCI 4477 / ASCI 4478 / ASCI 4479"]["title"] == "Senior Project"
    assert asci_courses["MATH 1006"]["category"] == "support"
    assert asci_courses["GE UD-4"]["category"] == "ge"
    assert asci_courses["Animal Mgmt 1"]["is_placeholder"] is True
    assert asci_by_id["ASCI_MGMT1"]["elective_key"] == "asci_animal_management"
    assert asci_by_id["ASCI_ENTERPRISE"]["elective_key"] == "asci_enterprise_elective"
    assert asci_by_id["ASCI_NUTRITION"]["elective_key"] == "asci_nutrition_elective"
    assert asci_by_id["ASCI_PHYSIOLOGY"]["elective_key"] == "asci_physiology_elective"
    assert asci_by_id["ASCI_APPROVED1"]["elective_key"] == "asci_approved_elective"
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
    assert "ASCI 2210" in asci_courses["ASCI 2210 + ASCI 2211"]["quarter_equivalents"]
    assert "ASCI 2230" in asci_courses["Animal Mgmt 1"]["quarter_equivalents"]
    assert "ASCI 3346" in asci_courses["Nutrition"]["quarter_equivalents"]
    assert "DSCI 3330" in asci_courses["Physiology"]["quarter_equivalents"]
    assert "ASCI 477" in asci_courses["ASCI 4477 / ASCI 4478 / ASCI 4479"]["quarter_equivalents"]
    assert "ASCI 4479" in asci_courses["ASCI 4477 / ASCI 4478 / ASCI 4479"]["quarter_equivalents"]


def test_anthropology_geography_flowchart_contains_expected_core_and_placeholders():
    antgeog_courses = {course["course_number"]: course for course in FLOWCHARTS["ANTGEOG"]["courses"]}
    antgeog_by_id = {course["id"]: course for course in FLOWCHARTS["ANTGEOG"]["courses"]}

    assert FLOWCHARTS["ANTGEOG"]["total_units"] == 120
    assert sum(course["units"] for course in FLOWCHARTS["ANTGEOG"]["courses"]) == 120
    assert antgeog_courses["ANT 2201"]["title"] == "Cultural Anthropology"
    assert antgeog_courses["GEOG 1150"]["title"] == "Human Geography"
    assert antgeog_courses["ANT 2250"]["title"] == "Biological Anthropology"
    assert antgeog_courses["GEOG 2250 / ERSC 2250"]["title"] == "Physical Geography"
    assert antgeog_courses["ANT 3384 / GEOG 3384"]["title"] == "Professional Preparation for Anthropologists/Geographers"
    assert antgeog_courses["GEOG 2218"]["title"] == "Applications in GIS"
    assert antgeog_courses["Methods Elective"]["elective_key"] == "antgeog_methods_elective"
    assert antgeog_courses["ANT 4465 / GEOG 4465"]["title"] == "Internship"
    assert antgeog_courses["GEOG 3308"]["title"] == "Global Geography"
    assert antgeog_courses["GEOG 3350"]["title"] == "The Global Environment"
    assert antgeog_courses["ANT 4455 / GEOG 4455"]["title"] == "Anthropology-Geography Research Design and Methods"
    assert antgeog_courses["ANT 4461 / GEOG 4461"]["title"] == "Senior Project I"
    assert antgeog_courses["ANT 4461 / GEOG 4461"]["units"] == 1
    assert antgeog_courses["ANT 4462 / GEOG 4462"]["title"] == "Senior Project II"
    assert antgeog_courses["ANT 4462 / GEOG 4462"]["units"] == 2
    assert antgeog_courses["STAT 1110"]["category"] == "support"
    assert antgeog_courses["GE 4B"]["category"] == "ge"
    assert antgeog_by_id["ANTGEOG_PHYS_GEOG"]["is_placeholder"] is True
    assert antgeog_by_id["ANTGEOG_RESEARCH_DESIGN"]["elective_key"] == "antgeog_research_design"
    assert antgeog_by_id["ANTGEOG_CON_JRS1"]["category"] == "concentration"
    assert antgeog_by_id["ANTGEOG_CON_JRS1"]["is_placeholder"] is True
    assert antgeog_by_id["ANTGEOG_FREE5"]["category"] == "concentration"
    assert antgeog_by_id["ANTGEOG_FREE5"]["is_placeholder"] is True
    assert "ANTGEOG" in CONCENTRATIONS


def test_anthropology_geography_prerequisites_and_quarter_equivalents_are_mapped():
    antgeog_courses = {course["course_number"]: course for course in FLOWCHARTS["ANTGEOG"]["courses"]}

    assert antgeog_courses["ANT 3360"]["prerequisites"] == ["ANT 2201"]
    assert antgeog_courses["ANT 4455 / GEOG 4455"]["prerequisites"] == []
    assert antgeog_courses["ANT 4461 / GEOG 4461"]["prerequisites"] == []
    assert antgeog_courses["ANT 4462 / GEOG 4462"]["prerequisites"] == ["ANT 4461 / GEOG 4461"]
    assert "ANT 201" in antgeog_courses["ANT 2201"]["quarter_equivalents"]
    assert "GEOG 150" in antgeog_courses["GEOG 1150"]["quarter_equivalents"]
    assert "GEOG 2250" in antgeog_courses["GEOG 2250 / ERSC 2250"]["quarter_equivalents"]
    assert "ERSC 250" in antgeog_courses["GEOG 2250 / ERSC 2250"]["quarter_equivalents"]
    assert "ANT 3384" in antgeog_courses["ANT 3384 / GEOG 3384"]["quarter_equivalents"]
    assert "GEOG 218" in antgeog_courses["GEOG 2218"]["quarter_equivalents"]
    assert "ANT 465" in antgeog_courses["ANT 4465 / GEOG 4465"]["quarter_equivalents"]
    assert "GEOG 308" in antgeog_courses["GEOG 3308"]["quarter_equivalents"]
    assert "GEOG 350" in antgeog_courses["GEOG 3350"]["quarter_equivalents"]
    assert "ANT 455" in antgeog_courses["ANT 4455 / GEOG 4455"]["quarter_equivalents"]
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
    assert environmental["slot_overrides"]["ANTGEOG_CON_JRS2"]["title"] == "Biodiversity and Biogeography Methods"
    assert environmental["slot_overrides"]["ANTGEOG_CON_JRS2"]["units"] == 3
    assert environmental["slot_overrides"]["ANTGEOG_CON_JRS1"]["elective_key"] == "antgeog_env_climate"
    assert environmental["slot_overrides"]["ANTGEOG_CON_SRF1"]["elective_key"] == "antgeog_env_geospatial"
    assert environmental["slot_overrides"]["ANTGEOG_CON_SRF2"]["units"] == 4

    global_studies = next(c for c in antgeog_concentrations if c["id"] == "global_studies")
    assert global_studies["slot_overrides"]["ANTGEOG_CON_JRS1"]["course_number"] == "GEOG 4408"
    assert global_studies["slot_overrides"]["ANTGEOG_CON_JRS1"]["title"] == "Geography of International Development"
    assert global_studies["slot_overrides"]["ANTGEOG_CON_SRF1"]["course_number"] == "ANT 4401"
    assert global_studies["slot_overrides"]["ANTGEOG_CON_SRF1"]["title"] == "Culture and Health"
    assert global_studies["slot_overrides"]["ANTGEOG_CON_JRS2"]["elective_key"] == "antgeog_global_problems"

    human_ecology = next(c for c in antgeog_concentrations if c["id"] == "human_ecology")
    assert human_ecology["slot_overrides"]["ANTGEOG_CON_JRS1"]["course_number"] == "ANT 3309 / ANT 3320"
    assert human_ecology["slot_overrides"]["ANTGEOG_CON_JRS1"]["units"] == 3
    assert human_ecology["slot_overrides"]["ANTGEOG_CON_JRS1"]["elective_key"] == "antgeog_human_ecology_foundation"
    assert human_ecology["slot_overrides"]["ANTGEOG_CON_JRS2"]["units"] == 3
    assert human_ecology["slot_overrides"]["ANTGEOG_CON_SRF2"]["elective_key"] == "antgeog_human_ecology_geog"


def test_psychology_flowchart_contains_expected_core_sequence():
    psy_courses = {course["course_number"]: course for course in FLOWCHARTS["PSY"]["courses"]}

    assert FLOWCHARTS["PSY"]["total_units"] == 120
    assert sum(course["units"] for course in FLOWCHARTS["PSY"]["courses"]) == 120
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
    assert sum(course["units"] for course in FLOWCHARTS["AGB"]["courses"]) == 120
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
    assert sum(course["units"] for course in FLOWCHARTS["ARCE"]["courses"]) == 128
    assert arce_courses["ARCE 1110"]["title"] == "Introduction to Architectural Engineering"
    assert arce_courses["ARCH 1101"]["units"] == 4
    assert arce_courses["ARCH 1131"]["units"] == 2
    assert arce_courses["ARCE 1121"]["category"] == "major"
    assert arce_courses["ARCE 1121"]["prerequisites"] == ["ARCE 1110"]
    assert arce_courses["ARCE 2211"]["prerequisites"] == ["ARCE 1121"]
    assert arce_courses["ARCE 3311"]["prerequisites"] == ["ARCE 2211"]
    assert arce_courses["ARCE 3332"]["prerequisites"] == ["ARCE 3331"]
    assert arce_courses["ARCE 3341"]["prerequisites"] == ["ARCE 3311"]
    assert arce_courses["ARCE 4411"]["prerequisites"] == ["ARCE 3311"]
    assert arce_courses["ARCE 4413"]["prerequisites"] == ["ARCE 4411"]
    assert arce_courses["ARCE 4461"]["prerequisites"] == ["ARCE 3311"]
    assert arce_courses["ARCE 4462"]["title"] == "Senior Project - Reinforced Concrete and Masonry Laboratory"
    assert arce_courses["MATH 1261"]["category"] == "support"
    assert arce_courses["CHEM 1120"]["title"] == "Fundamentals of Chemical Structure and Properties"
    assert arce_courses["CHEM 1120"]["category"] == "support"
    assert arce_courses["STAT 3210"]["category"] == "support"
    assert arce_courses["GE 4A"]["category"] == "ge"
    assert arce_courses["GE UD-3"]["category"] == "ge"
    assert arce_by_id["ARCE_FE_TE1"]["is_placeholder"] is True
    assert arce_by_id["ARCE_SURVEY"]["is_placeholder"] is True
    assert arce_by_id["ARCE_ELEC"]["is_placeholder"] is True
    assert arce_by_id["ARCE_CAED"]["is_placeholder"] is True
    assert arce_by_id["ARCE_FE_TE1"]["units"] == 2
    assert arce_by_id["ARCE_SURVEY"]["units"] == 2
    assert arce_by_id["ARCE_CAED"]["units"] == 2
    assert arce_by_id["ARCE_FE_TE1"]["elective_key"] == "arce_fe_technical_elective"
    assert arce_by_id["ARCE_FE_TE2"]["elective_key"] == "arce_fe_technical_elective"
    assert arce_by_id["ARCE_ELEC"]["elective_key"] == "arce_upper_division_elective"
    assert arce_by_id["ARCE_CAED"]["elective_key"] == "arce_caed_interdisciplinary_elective"
    assert "ARCH 131" in arce_courses["ARCH 1101"]["quarter_equivalents"]
    assert "ARCH 101" in arce_courses["ARCH 1131"]["quarter_equivalents"]
    assert "ARCE 211" in arce_courses["ARCE 1121"]["quarter_equivalents"]
    assert "ARCE 223" in arce_courses["ARCE 2211"]["quarter_equivalents"]
    assert "ARCE 224" in arce_courses["ARCE 2212"]["quarter_equivalents"]
    assert "ARCE 302" in arce_courses["ARCE 3311"]["quarter_equivalents"]
    assert "ARCE 451" in arce_courses["ARCE 3332"]["quarter_equivalents"]
    assert "ARCE 483" in arce_courses["ARCE 4413"]["quarter_equivalents"]
    assert "ARCE 452" in arce_courses["ARCE 4462"]["quarter_equivalents"]
    assert "ARCE" not in CONCENTRATIONS


def test_architecture_flowchart_contains_expected_five_year_core_and_placeholders():
    arch_courses = {course["course_number"]: course for course in FLOWCHARTS["ARCH"]["courses"]}
    arch_by_id = {course["id"]: course for course in FLOWCHARTS["ARCH"]["courses"]}

    assert FLOWCHARTS["ARCH"]["total_units"] == 150
    assert sum(course["units"] for course in FLOWCHARTS["ARCH"]["courses"]) == 150
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
    assert arch_by_id["ARCH_PROF_ELEC1"]["elective_key"] == "arch_professional_elective"
    assert arch_by_id["ARCH_PROF_ELEC4"]["elective_key"] == "arch_professional_elective"
    assert arch_by_id["ARCH_GE_UD25"]["is_placeholder"] is True
    assert "ARCH" not in CONCENTRATIONS


def test_architecture_prerequisites_and_quarter_equivalents_are_mapped():
    arch_courses = {course["course_number"]: course for course in FLOWCHARTS["ARCH"]["courses"]}
    arch_by_id = {course["id"]: course for course in FLOWCHARTS["ARCH"]["courses"]}

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
    assert "ARCH 4401" in arch_by_id["ARCH_ARCH4401_2"]["quarter_equivalents"]
    assert "ARCH 4401" in arch_by_id["ARCH_ARCH4401_3"]["quarter_equivalents"]
    assert "ARCH 420" in arch_courses["ARCH 4425"]["quarter_equivalents"]
    assert "ARCH 420" not in arch_courses["ARCH 4460"]["quarter_equivalents"]
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
    assert bmed_courses["BMED 2212"]["title"] == "Introduction to Mechanical Design in Biomedical Engineering"
    assert bmed_courses["BMED 2420"]["title"] == "Principles and Applications of Biomaterials"
    assert bmed_courses["BMED 3430"]["title"] == "Biomedical Modeling and Simulation"
    assert bmed_courses["BMED 4440"]["title"] == "Bioelectronics and Instrumentation"
    assert bmed_courses["BMED 4465"]["title"] == "Senior Project: Design I"
    assert bmed_courses["BMED 4466"]["title"] == "Senior Project: Design II"
    assert bmed_courses["BIO 1151"]["category"] == "support"
    assert bmed_courses["MATH 2341"]["category"] == "support"
    assert bmed_courses["GE UD-4"]["category"] == "ge"
    assert bmed_by_id["BMED_BIO2231_2232"]["is_placeholder"] is True
    assert bmed_by_id["BMED_CON_JRF1"]["category"] == "concentration"
    assert bmed_by_id["BMED_CON_JRF1"]["is_placeholder"] is True
    assert bmed_by_id["BMED_CON_SRS3"]["category"] == "concentration"
    assert bmed_by_id["BMED_CON_SRS3"]["is_placeholder"] is True
    assert "BMED" in CONCENTRATIONS


def test_biomedical_engineering_prerequisites_and_quarter_equivalents_are_mapped():
    bmed_courses = {course["course_number"]: course for course in FLOWCHARTS["BMED"]["courses"]}

    assert bmed_courses["CHEM 1122"]["prerequisites"] == ["CHEM 1120"]
    assert bmed_courses["MATH 1262"]["prerequisites"] == ["MATH 1261"]
    assert bmed_courses["PHYS 1143"]["prerequisites"] == ["PHYS 1141", "MATH 1261"]
    assert bmed_courses["BMED 2420"]["prerequisites"] == ["BMED 2212", "CHEM 1120", "ENGR 2211"]
    assert bmed_courses["BMED 4440"]["prerequisites"] == ["BMED 2310", "BMED 2311"]
    assert bmed_courses["BMED 4465"]["prerequisites"] == ["BMED 3430"]
    assert bmed_courses["BMED 4466"]["prerequisites"] == ["BMED 4465"]
    assert "BMED 101" in bmed_courses["BMED 1101"]["quarter_equivalents"]
    assert "BMED 420" in bmed_courses["BMED 2420"]["quarter_equivalents"]
    assert "BMED 440" in bmed_courses["BMED 4440"]["quarter_equivalents"]
    assert "BMED 455" in bmed_courses["BMED 4465"]["quarter_equivalents"]
    assert "BMED 456" in bmed_courses["BMED 4466"]["quarter_equivalents"]


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


def test_biochemistry_or_choice_placeholders_have_elective_keys():
    bioc_by_id = {c["id"]: c for c in FLOWCHARTS["BIOC"]["courses"]}

    # CHEM 2201 / CHEM 2203 OR choice
    r = bioc_by_id["BIOC_CHEM2201_2203"]
    assert r["is_placeholder"] is True
    assert r["elective_key"] == "bioc_research_or_methods2"
    assert "CHEM 2201" in r["course_number"]
    assert "CHEM 2203" in r["course_number"]

    # CHEM 4453 / CHEM 4454 OR choice
    mb = bioc_by_id["BIOC_CHEM4453_4454"]
    assert mb["is_placeholder"] is True
    assert mb["elective_key"] == "bioc_mol_bio_or_protein"
    assert "CHEM 4453" in mb["course_number"]
    assert "CHEM 4454" in mb["course_number"]

    # Biochemistry advanced elective (CHEM 4450, 4452, 4456, 4457, 4458)
    ce = bioc_by_id["BIOC_CHEM_ELEC"]
    assert ce["is_placeholder"] is True
    assert ce["elective_key"] == "bioc_chem_advanced_elective"
    assert ce["category"] == "major"

    # BIO/MCRO advanced elective — must be category "major" per catalog
    bm = bioc_by_id["BIOC_BIO_MCRO_ELEC"]
    assert bm["is_placeholder"] is True
    assert bm["elective_key"] == "bioc_bio_mcro_advanced_elective"
    assert bm["category"] == "major"


def test_agricultural_systems_management_flowchart_contains_expected_core_sequence():
    asm_courses = {course["course_number"]: course for course in FLOWCHARTS["ASM"]["courses"]}
    asm_by_id = {course["id"]: course for course in FLOWCHARTS["ASM"]["courses"]}

    assert FLOWCHARTS["ASM"]["total_units"] == 121
    assert sum(course["units"] for course in FLOWCHARTS["ASM"]["courses"]) == 121
    assert asm_courses["BRAE 1128"]["title"] == "Careers in BioResource and Agricultural Engineering"
    assert asm_courses["BRAE 2203"]["title"] == "Systems Management I"
    assert asm_courses["BRAE 3317"]["title"] == "Systems Management II"
    assert asm_courses["BRAE 4419"]["title"] == "Systems Management III"
    assert asm_courses["BRAE 3340"]["title"] == "Irrigation Water Management"
    assert asm_courses["BRAE 4460"]["title"] == "Senior Project I"
    assert asm_courses["BRAE 4461"]["title"] == "Senior Project II"
    assert asm_courses["BRAE 2203"]["category"] == "major"
    assert asm_courses["AGB 2212"]["category"] == "support"
    assert asm_courses["MATH 1267"]["category"] == "support"
    assert asm_courses["GE 1A"]["category"] == "ge"
    assert asm_by_id["ASM_MATH1007_STAT1110"]["is_placeholder"] is True
    assert asm_by_id["ASM_MATH1007_STAT1110"]["elective_key"] == "asm_math_elective"
    assert asm_by_id["ASM_ELEC1"]["category"] == "concentration"
    assert asm_by_id["ASM_ELEC1"]["is_placeholder"] is True
    assert asm_by_id["ASM_ELEC1"]["elective_key"] == "asm_approved_elective"
    assert asm_by_id["ASM_ELEC2"]["elective_key"] == "asm_approved_elective"
    assert asm_by_id["ASM_ELEC3"]["elective_key"] == "asm_approved_elective"
    assert "ASM" not in CONCENTRATIONS


def test_agricultural_systems_management_prerequisites_are_mapped():
    asm_courses = {course["course_number"]: course for course in FLOWCHARTS["ASM"]["courses"]}

    assert asm_courses["BRAE 2203"]["prerequisites"] == ["MATH 1267"]
    assert asm_courses["BRAE 2142"]["prerequisites"] == ["MATH 1267"]
    assert asm_courses["BRAE 3301"]["prerequisites"] == ["BRAE 1150", "PHYS 1121"]
    assert asm_courses["AGB 3308"]["prerequisites"] == ["AGB 2214", "AGB 2260"]
    assert asm_courses["BRAE 3317"]["prerequisites"] == ["AGB 2260", "BRAE 2203"]
    assert asm_courses["BRAE 3343"]["prerequisites"] == ["PHYS 1121"]
    assert asm_courses["AGB 3369"]["prerequisites"] == ["AGB 2212"]
    assert asm_courses["BRAE 4419"]["prerequisites"] == ["BRAE 3317"]
    assert asm_courses["BRAE 4425"]["prerequisites"] == ["MATH 1267", "PHYS 1121"]
    assert asm_courses["BRAE 4432"]["prerequisites"] == ["BRAE 3343", "PHYS 1121"]
    assert asm_courses["BRAE 4440"]["prerequisites"] == ["BRAE 3340"]
    assert asm_courses["BRAE 4461"]["prerequisites"] == ["BRAE 4460"]
    assert "STAT 218" in asm_courses["MATH 1007 / STAT 1110"]["quarter_equivalents"]
    assert "MATH 1267" not in asm_courses["MATH 1007 / STAT 1110"]["quarter_equivalents"]
    assert "MATH 221" in asm_courses["MATH 1267"]["quarter_equivalents"]
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

    # PHIL 3323 is now a fixed required course (not a placeholder)
    assert "CPE_PHIL3323" in cpe_by_id
    ethics = cpe_by_id["CPE_PHIL3323"]
    assert ethics["is_placeholder"] is False
    assert ethics["course_number"] == "PHIL 3323"
    assert ethics["title"] == "Ethics, Science, and Technology"

    # STAT is a separate placeholder slot
    assert "CPE_STAT" in cpe_by_id
    stat = cpe_by_id["CPE_STAT"]
    assert stat["is_placeholder"] is True
    assert "STAT 3210" in stat["course_number"]
    assert "STAT 3310" in stat["course_number"]
    assert stat.get("elective_key") == "cpe_stats"
    assert "STAT 312" in stat["quarter_equivalents"]


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
    assert "BRAE 1239" in survey["quarter_equivalents"]
    assert "BRAE 2237" in survey["quarter_equivalents"]
    assert "CM 2239" in survey["quarter_equivalents"]


def test_me_ime_manufacturing_selective_has_elective_key():
    me_by_id = {course["id"]: course for course in FLOWCHARTS["ME"]["courses"]}

    slot = me_by_id["ME_IME114X"]
    assert slot["is_placeholder"] is True
    assert "IME 1141" in slot["course_number"]
    assert slot.get("elective_key") == "me_ime_mfg_selective"
    assert "IME 1141" in slot["quarter_equivalents"]
    assert "IME 1142" in slot["quarter_equivalents"]
    assert "IME 1149" in slot["quarter_equivalents"]


def test_mechanical_engineering_catalog_mappings_cover_paired_and_elective_slots():
    me_courses = {course["course_number"]: course for course in FLOWCHARTS["ME"]["courses"]}
    me_by_id = {course["id"]: course for course in FLOWCHARTS["ME"]["courses"]}

    assert "EE 2115" in me_courses["EE 2115 & EE 2115L"]["quarter_equivalents"]
    assert "EE 2115L" in me_courses["EE 2115 & EE 2115L"]["quarter_equivalents"]
    assert "MATE 1220" in me_courses["MATE 1220 & MATE 1215"]["quarter_equivalents"]
    assert "MATE 1215" in me_courses["MATE 1220 & MATE 1215"]["quarter_equivalents"]
    assert "ME 3342" in me_courses["ME 3341 & ME 3342"]["quarter_equivalents"]
    assert me_courses["ME 3343"]["prerequisites"] == ["ME 3341 & ME 3342"]
    assert "ME 251" in me_courses["ME 2248"]["quarter_equivalents"]
    assert "ME 303" in me_courses["ME 3302"]["quarter_equivalents"]
    assert "ME 418" in me_courses["ME 4417"]["quarter_equivalents"]
    assert "ME 428" in me_courses["ME 4460"]["quarter_equivalents"]
    assert "ME 429" in me_courses["ME 4461"]["quarter_equivalents"]
    assert "ME 448" in me_courses["ME 4440"]["quarter_equivalents"]
    assert "BIO 2217" in me_by_id["ME_GE5B"]["quarter_equivalents"]


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


def test_stat_flowchart():
    stat = FLOWCHARTS.get("STAT")
    assert stat is not None, "STAT must be in FLOWCHARTS"
    assert stat["total_units"] == 120

    courses = stat["courses"]
    by_id = {c["id"]: c for c in courses}
    by_num = {c["course_number"]: c for c in courses}

    for c in courses:
        assert REQUIRED_COURSE_KEYS <= c.keys(), f"Missing keys on {c['id']}"
        assert c["category"] in VALID_CATEGORIES, f"Bad category on {c['id']}"

    # Key course titles and categories
    assert by_num["STAT 1510"]["title"] == "Statistics I"
    assert by_num["STAT 1510"]["category"] == "major"
    assert by_num["STAT 4610"]["title"] == "Probability Theory"
    assert by_num["STAT 4620"]["title"] == "Statistical Theory"
    assert by_num["STAT 3530"]["title"] == "Applied Linear Models"
    assert by_num["STAT 4366"]["title"] == "Statistical Communication, Collaboration, and Consulting"
    assert by_num["MATH 1264"]["category"] == "support"
    assert by_num["CSC 1001"]["category"] == "support"

    # Prerequisites
    assert "STAT 1510" in by_num["STAT 3520"]["prerequisites"]
    assert "MATH 1264" in by_num["MATH 1265"]["prerequisites"]
    assert "STAT 4610" in by_num["STAT 4620"]["prerequisites"]
    assert "STAT 4366" in by_num["STAT 4460"]["prerequisites"]

    # GE placeholders
    ge_courses = [c for c in courses if c["category"] == "ge"]
    assert len(ge_courses) >= 10
    ge_ids = {c["id"] for c in ge_courses}
    assert "STAT_GE1A" in ge_ids
    assert "STAT_GE1B" in ge_ids
    assert "STAT_GE5A" in ge_ids
    assert "STAT_GE6" in ge_ids
    for c in ge_courses:
        assert c["is_placeholder"] is True, f"{c['id']} GE must be placeholder"

    # Elective placeholders
    assert by_id["STAT_ELEC_A1"]["is_placeholder"] is True
    assert by_id["STAT_ELEC_B1"]["is_placeholder"] is True

    # No concentrations
    assert "STAT" not in CONCENTRATIONS

    # Category ordering invariant per column
    col_courses: dict[int, list] = {}
    for c in courses:
        col_courses.setdefault(c["grid_col"], []).append(c)
    for col, col_list in col_courses.items():
        rows_by_bucket: dict[int, list[int]] = {}
        for c in col_list:
            b = layout_bucket(c)
            rows_by_bucket.setdefault(b, []).append(c["grid_row"])
        sorted_buckets = sorted(rows_by_bucket.keys())
        for i in range(len(sorted_buckets) - 1):
            b1, b2 = sorted_buckets[i], sorted_buckets[i + 1]
            assert max(rows_by_bucket[b1]) < min(rows_by_bucket[b2]), (
                f"STAT col {col}: bucket {b1} rows {rows_by_bucket[b1]} "
                f"overlap with bucket {b2} rows {rows_by_bucket[b2]}"
            )


def test_chemistry_flowchart():
    chem = FLOWCHARTS["CHEM"]
    assert chem["total_units"] == 120

    # Verify unit sum matches 120
    total = sum(c["units"] for c in chem["courses"])
    assert total == 120

    chem_cn = {c["course_number"]: c for c in chem["courses"]}

    # Key course titles
    assert chem_cn["CHEM 1120"]["title"] == "Fundamentals of Chemical Structure and Properties"
    assert chem_cn["CHEM 1122"]["title"] == "Fundamentals of Chemical Reactivity"
    assert chem_cn["CHEM 2242"]["title"] == "Organic Chemistry I"
    assert chem_cn["CHEM 3330"]["title"] == "Foundations of Chemical Analysis"
    assert chem_cn["CHEM 3392"]["title"] == "Physical Chemistry I"
    assert chem_cn["CHEM 3380"]["title"] == "Foundations of Macromolecular Chemistry"

    # Categories
    assert chem_cn["CHEM 1120"]["category"] == "major"
    assert chem_cn["BIO 1151"]["category"] == "support"
    assert chem_cn["MATH 1261"]["category"] == "support"
    assert chem_cn["PHYS 1141"]["category"] == "support"
    assert chem_cn["MATH 2263"]["category"] == "support"

    # Prerequisites (at least 2)
    assert chem_cn["CHEM 1122"]["prerequisites"] == ["CHEM 1120"]
    assert chem_cn["CHEM 2242"]["prerequisites"] == ["CHEM 1122"]
    assert chem_cn["CHEM 3392"]["prerequisites"] == ["CHEM 1122", "MATH 1262", "PHYS 1141"]
    assert chem_cn["CHEM 4462"]["prerequisites"] == ["CHEM 4461"]

    # Quarter equivalents
    assert "CHEM 124" in chem_cn["CHEM 1120"]["quarter_equivalents"]
    assert "CHEM 125" in chem_cn["CHEM 1122"]["quarter_equivalents"]
    assert "CHEM 312" in chem_cn["CHEM 2242"]["quarter_equivalents"]
    assert "MATH 141" in chem_cn["MATH 1261"]["quarter_equivalents"]
    assert "PHYS 141" in chem_cn["PHYS 1141"]["quarter_equivalents"]

    # GE placeholders
    ge_placeholders = [c for c in chem["courses"] if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge_placeholders) >= 8

    # CHEM is in CONCENTRATIONS
    assert "CHEM" in CONCENTRATIONS


def test_chemistry_placeholders_have_elective_keys():
    chem_by_id = {c["id"]: c for c in FLOWCHARTS["CHEM"]["courses"]}

    research = chem_by_id["CHEM_CHEM2201_2203"]
    assert research["is_placeholder"] is True
    assert research["elective_key"] == "chem_research_or_methods"
    assert "CHEM 2201" in research["course_number"]

    subdisc = chem_by_id["CHEM_SUBDISC1"]
    assert subdisc["is_placeholder"] is True
    assert subdisc["elective_key"] == "chem_subdiscipline_elective"

    adv = chem_by_id["CHEM_ADV1"]
    assert adv["is_placeholder"] is True
    assert adv["elective_key"] == "chem_advanced_elective"


def test_chemistry_concentrations():
    chem_concentrations = CONCENTRATIONS["CHEM"]
    concentration_ids = {c["id"] for c in chem_concentrations}
    assert "none" in concentration_ids
    assert "polymers_coatings" in concentration_ids

    polymers = next(c for c in chem_concentrations if c["id"] == "polymers_coatings")
    overrides = polymers["slot_overrides"]

    assert "CHEM_SUBDISC2" in overrides
    assert overrides["CHEM_SUBDISC2"]["course_number"] == "CHEM 4486"
    assert overrides["CHEM_SUBDISC2"]["elective_key"] is None

    assert "CHEM_ADV1" in overrides
    assert overrides["CHEM_ADV1"]["course_number"] == "CHEM 4480"
    assert overrides["CHEM_ADV1"]["elective_key"] is None

    assert "CHEM_ADV3" in overrides
    assert overrides["CHEM_ADV3"]["course_number"] == "CHEM 4482"


def test_software_engineering_flowchart_unit_count():
    se = FLOWCHARTS["SE"]
    se_courses = {course["course_number"]: course for course in se["courses"]}
    se_by_id = {course["id"]: course for course in se["courses"]}

    assert se["total_units"] == 120
    assert sum(course["units"] for course in se["courses"]) == 120
    assert se_courses["CSC 1001"]["title"] == "Fundamentals of Computer Science"
    assert se_courses["CSC 1001"]["units"] == 3
    assert se_courses["CSC 2001"]["title"] == "Data Structures"
    assert se_courses["CSC 2001"]["units"] == 3
    assert se_courses["CSC 3660"]["title"] == "Database Modeling, Design and Implementation"
    assert se_courses["CSC 3660"]["units"] == 2
    assert se_courses["CSC 3660"]["prerequisites"] == ["CSC 2001"]
    assert se_courses["CSC 4160"]["prerequisites"] == ["CSC 3100"]
    assert se_courses["GE UD-4"]["category"] == "ge"
    assert se_by_id["SE_CON_JRS1"]["is_placeholder"] is True
    assert "SE" not in CONCENTRATIONS


def test_aerospace_engineering_flowchart_unit_count():
    aero = FLOWCHARTS["AERO"]
    aero_courses = {course["course_number"]: course for course in aero["courses"]}

    assert aero["total_units"] == 128
    assert sum(course["units"] for course in aero["courses"]) == 128
    assert aero_courses["IME 1143 / IME 1140"]["units"] == 3
    assert aero_courses["IME 1143 / IME 1140"]["category"] == "support"
    assert aero_courses["AERO 1121"]["category"] == "major"
    assert aero_courses["AERO 2220"]["prerequisites"] == ["ENGR 2211"]
    assert aero_courses["AERO 3331"]["prerequisites"] == ["ENGR 2211"]
    assert aero_courses["GE UD-4"]["category"] == "ge"


def test_child_development_flowchart():
    cd = FLOWCHARTS["CD"]
    assert cd["total_units"] == 120

    total = sum(c["units"] for c in cd["courses"])
    assert total == 120

    cd_cn = {c["course_number"]: c for c in cd["courses"]}

    # Key course titles
    assert cd_cn["CD 1102"]["title"] == "Orientation to the Child Development Major"
    assert cd_cn["CD 2229"]["title"] == "Research Methods in Psychology"
    assert cd_cn["CD 2256"]["title"] == "Developmental Psychology"
    assert cd_cn["CD 2230"]["title"] == "Preschool Laboratory"
    assert cd_cn["CD 3329"]["title"] == "Advanced Research Methods in Developmental Science"
    assert cd_cn["CD 4424"]["title"] == "Children's Development in Diverse Cultures"
    assert cd_cn["CD 4461"]["title"] == "Senior Project Seminar"
    assert cd_cn["CD 4462"]["title"] == "Senior Project"

    # Categories
    assert cd_cn["CD 1102"]["category"] == "major"
    assert cd_cn["PSY 2201"]["category"] == "support"
    assert cd_cn["STAT 1110"]["category"] == "support"
    assert cd_cn["PSY 2240"]["category"] == "support"
    assert cd_cn["CD 3329"]["category"] == "major"

    # Prerequisites (at least 2 chains)
    assert cd_cn["CD 2229"]["prerequisites"] == ["PSY 2201", "STAT 1110"]
    assert cd_cn["CD 2256"]["prerequisites"] == ["PSY 2201"]
    assert cd_cn["CD 3329"]["prerequisites"] == ["CD 2229", "STAT 1110"]
    assert cd_cn["CD 4462"]["prerequisites"] == ["CD 4461"]

    # Quarter equivalents
    assert "PSY 201" in cd_cn["PSY 2201"]["quarter_equivalents"]
    assert "STAT 217" in cd_cn["STAT 1110"]["quarter_equivalents"]
    assert "CD 256" in cd_cn["CD 2256"]["quarter_equivalents"]
    assert "CD 329" in cd_cn["CD 3329"]["quarter_equivalents"]
    assert "CD 424" in cd_cn["CD 4424"]["quarter_equivalents"]
    assert "CD 461" in cd_cn["CD 4461"]["quarter_equivalents"]

    # GE placeholders
    ge_placeholders = [c for c in cd["courses"] if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge_placeholders) >= 8

    # CD has no concentrations
    assert "CD" not in CONCENTRATIONS


def test_child_development_placeholders_have_elective_keys():
    cd_by_id = {c["id"]: c for c in FLOWCHARTS["CD"]["courses"]}

    found = cd_by_id["CD_FOUND"]
    assert found["is_placeholder"] is True
    assert found["elective_key"] == "cd_foundational_course"

    ls1 = cd_by_id["CD_LIFESTAGE1"]
    assert ls1["is_placeholder"] is True
    assert ls1["elective_key"] == "cd_lifestage_elective"

    ls2 = cd_by_id["CD_LIFESTAGE2"]
    assert ls2["is_placeholder"] is True
    assert ls2["elective_key"] == "cd_lifestage_elective"

    for elec_id in ("CD_ELEC1", "CD_ELEC2", "CD_ELEC3", "CD_ELEC4"):
        assert cd_by_id[elec_id]["is_placeholder"] is True
        assert cd_by_id[elec_id]["elective_key"] == "cd_upper_div_elective"

    prof = cd_by_id["CD_PROF"]
    assert prof["is_placeholder"] is True
    assert prof["elective_key"] == "cd_professional_skills"

    dei = cd_by_id["CD_DEI"]
    assert dei["is_placeholder"] is True
    assert dei["elective_key"] == "cd_dei_elective"

    udsci = cd_by_id["CD_UDSCI"]
    assert udsci["is_placeholder"] is True
    assert udsci["elective_key"] == "cd_upper_div_science"

    intern_ = cd_by_id["CD_INTERN"]
    assert intern_["is_placeholder"] is True
    assert intern_["elective_key"] == "cd_internship_i"

    # Free electives should have no elective_key
    assert cd_by_id["CD_FREE1"].get("elective_key") is None
    assert cd_by_id["CD_FREE7"].get("elective_key") is None


def test_city_and_regional_planning_flowchart():
    crp = FLOWCHARTS["CRP"]
    assert crp["total_units"] == 120

    total = sum(c["units"] for c in crp["courses"])
    assert total == 120

    crp_cn = {c["course_number"]: c for c in crp["courses"]}

    # Key course titles
    assert crp_cn["CRP 1211"]["title"] == "Urban Planning History"
    assert crp_cn["CRP 1212"]["title"] == "Introduction to City Planning"
    assert crp_cn["CRP 1213"]["title"] == "Methods of Population and Housing Analysis"
    assert crp_cn["CRP 1215"]["title"] == "Planning Approaches to a Just City"
    assert crp_cn["CRP 3202"]["title"] == "Urban Design Studio"
    assert crp_cn["CRP 3341"]["title"] == "Urban Development Studio"
    assert crp_cn["CRP 4410"]["title"] == "Urban Planning Studio"
    assert crp_cn["CRP 4420"]["title"] == "Land Use Law"

    # Categories
    assert crp_cn["CRP 1211"]["category"] == "major"
    assert crp_cn["CRP 2457"]["category"] == "major"
    assert crp_cn["DATA 1000 / STAT 1110"]["category"] == "support"

    # Prerequisites (at least 2 chains)
    assert crp_cn["CRP 3202"]["prerequisites"] == ["CRP 1212", "CRP 2216"]
    assert crp_cn["CRP 3336"]["prerequisites"] == ["CRP 1212"]
    assert crp_cn["CRP 3341"]["prerequisites"] == ["CRP 3202"]
    assert crp_cn["CRP 4410"]["prerequisites"] == ["CRP 1213", "CRP 2214"]

    # Quarter equivalents
    assert "CRP 112" in crp_cn["CRP 1212"]["quarter_equivalents"]
    assert "CRP 214" in crp_cn["CRP 2214"]["quarter_equivalents"]
    assert "CRP 410" in crp_cn["CRP 4410"]["quarter_equivalents"]
    assert "CRP 461" in crp_cn["CRP 4461 / CRP 4463"]["quarter_equivalents"]

    # GE placeholders
    ge_placeholders = [c for c in crp["courses"] if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge_placeholders) >= 10

    # Term unit counts
    by_col = {}
    for c in crp["courses"]:
        by_col.setdefault(c["grid_col"], []).append(c["units"])
    assert sum(by_col[0]) == 14  # FF
    assert sum(by_col[1]) == 14  # FS
    assert sum(by_col[2]) == 17  # SoF
    assert sum(by_col[3]) == 17  # SoS
    assert sum(by_col[6]) == 14  # SrF
    assert sum(by_col[7]) == 16  # SrS

    # CRP has no concentrations
    assert "CRP" not in CONCENTRATIONS


def test_crp_placeholders_have_elective_keys():
    crp_by_id = {c["id"]: c for c in FLOWCHARTS["CRP"]["courses"]}

    stat = crp_by_id["CRP_STAT"]
    assert stat["is_placeholder"] is True
    assert stat["elective_key"] == "crp_stat_data_support"

    senior = crp_by_id["CRP_SENIOR"]
    assert senior["is_placeholder"] is True
    assert senior["elective_key"] == "crp_senior_project"

    caed1 = crp_by_id["CRP_CAED1"]
    assert caed1["is_placeholder"] is True
    assert caed1["elective_key"] == "crp_caed_elective"

    caed2 = crp_by_id["CRP_CAED2"]
    assert caed2["is_placeholder"] is True
    assert caed2["elective_key"] == "crp_caed_elective"

    # Free electives have no elective_key
    assert crp_by_id["CRP_FREE1"].get("elective_key") is None
    assert crp_by_id["CRP_FREE5"].get("elective_key") is None


def test_electrical_engineering_flowchart():
    assert "EE" in FLOWCHARTS
    ee = FLOWCHARTS["EE"]
    assert ee["total_units"] == 128
    assert sum(c["units"] for c in ee["courses"]) == 128

    ee_cn = {c["course_number"]: c for c in ee["courses"]}

    # Key course titles
    assert "Introduction to Electrical Engineering and Lab" in ee_cn["EE 1111"]["title"]
    assert "Electric Circuit Analysis I" in ee_cn["EE 2211"]["title"]
    assert "Signals and Systems" in ee_cn["EE 2328"]["title"]
    assert "Classical Control Systems and Lab" in ee_cn["EE 3302"]["title"]
    assert "Electronics I" in ee_cn["EE 3306"]["title"]
    assert "Electromagnetic Fields" in ee_cn["EE 3335"]["title"]
    assert "Communication Systems" in ee_cn["EE 4314"]["title"]
    assert "Senior Project I" in ee_cn["EE 4461"]["title"]
    assert "Probability and Random Processes" in ee_cn["STAT 3310"]["title"]

    # Categories
    assert ee_cn["EE 1111"]["category"] == "major"
    assert ee_cn["MATH 1261"]["category"] == "support"
    assert ee_cn["PHYS 1141"]["category"] == "support"
    assert ee_cn["BIO 2213"]["category"] == "support"
    assert ee_cn["EE 2211"]["category"] == "major"
    assert ee_cn["GE 1A"]["category"] == "ge"

    # Prerequisites
    assert "EE 1111" in ee_cn["EE 2211"]["prerequisites"]
    assert "EE 2211" in ee_cn["EE 2212"]["prerequisites"]
    assert "EE 2211" in ee_cn["EE 2328"]["prerequisites"]
    assert "MATH 2341" in ee_cn["EE 2328"]["prerequisites"]
    assert "EE 2328" in ee_cn["EE 3302"]["prerequisites"]
    assert "MATH 2263" in ee_cn["EE 3302"]["prerequisites"]
    assert "EE 2212" in ee_cn["EE 3306"]["prerequisites"]
    assert "EE 3306" in ee_cn["EE 3255"]["prerequisites"]
    assert "EE 3329" in ee_cn["EE 4314"]["prerequisites"]
    assert "EE 4461" in ee_cn["EE 4462"]["prerequisites"]

    # Quarter equivalents
    assert "MATH 141" in ee_cn["MATH 1261"]["quarter_equivalents"]
    assert "MATH 142" in ee_cn["MATH 1262"]["quarter_equivalents"]
    assert "PHYS 141" in ee_cn["PHYS 1141"]["quarter_equivalents"]
    assert "EE 461" in ee_cn["EE 4461"]["quarter_equivalents"]

    # GE placeholders
    ge_placeholders = [c for c in ee["courses"] if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge_placeholders) >= 10

    # Term unit sums
    by_col = {}
    for c in ee["courses"]:
        by_col.setdefault(c["grid_col"], []).append(c["units"])
    assert sum(by_col[0]) == 16   # FF
    assert sum(by_col[1]) == 15   # FS
    assert sum(by_col[2]) == 18   # SoF
    assert sum(by_col[3]) == 16   # SoS
    assert sum(by_col[4]) == 18   # JF
    assert sum(by_col[5]) == 15   # JS
    assert sum(by_col[6]) == 14   # SrF
    assert sum(by_col[7]) == 16   # SrS

    # EE has 3 concentration tracks including general curriculum
    assert "EE" in CONCENTRATIONS


def test_ee_placeholders_have_elective_keys():
    ee_by_id = {c["id"]: c for c in FLOWCHARTS["EE"]["courses"]}

    # Senior project lab choices
    assert ee_by_id["EE_4463"]["elective_key"] == "ee_senior_proj_lab_i"
    assert ee_by_id["EE_4464"]["elective_key"] == "ee_senior_proj_lab_ii"

    # Technical electives
    assert ee_by_id["EE_TECH1"]["elective_key"] == "ee_technical_elective"
    assert ee_by_id["EE_TECH2"]["elective_key"] == "ee_technical_elective"

    # Lower-div / technical electives
    assert ee_by_id["EE_ELEC3"]["elective_key"] == "ee_lower_div_elective"
    assert ee_by_id["EE_ELEC4"]["elective_key"] == "ee_lower_div_elective"

    # GE UD-3 has no elective_key
    assert ee_by_id["EE_GE_UD3"].get("elective_key") is None


def test_industrial_engineering_flowchart():
    assert "IE" in FLOWCHARTS
    ie = FLOWCHARTS["IE"]
    assert ie["total_units"] == 127
    assert sum(c["units"] for c in ie["courses"]) == 127

    ie_cn = {c["course_number"]: c for c in ie["courses"]}

    # Key course titles
    assert "Introduction to Industrial and Manufacturing Engineering" in ie_cn["IME 1101"]["title"]
    assert "Process Improvement" in ie_cn["IME 1223"]["title"]
    assert "Enterprise Analytics" in ie_cn["IME 2212"]["title"]
    assert "Operations Research" in ie_cn["IME 3302"]["title"]
    assert "Quality Control" in ie_cn["IME 3326"]["title"]
    assert "Production Planning" in ie_cn["IME 3410"]["title"]
    assert "Supply Chain" in ie_cn["IME 4417"]["title"]
    assert "Senior Project - Design I" in ie_cn["IME 4461"]["title"]

    # Categories
    assert ie_cn["IME 1101"]["category"] == "major"
    assert ie_cn["MATH 1261"]["category"] == "support"
    assert ie_cn["CHEM 1120"]["category"] == "support"
    assert ie_cn["PSY 2201"]["category"] == "support"
    assert ie_cn["GE 1A"]["category"] == "ge"

    # Prerequisites
    assert "IME 1101" in ie_cn["IME 2315"]["prerequisites"]
    assert "MATH 1261" in ie_cn["MATH 1262"]["prerequisites"]
    assert "PHYS 1141" in ie_cn["PHYS 1143"]["prerequisites"]
    assert "IME 2212" in ie_cn["IME 3302"]["prerequisites"]
    assert "STAT 3210" in ie_cn["IME 3326"]["prerequisites"]
    assert "IME 3302" in ie_cn["IME 3410"]["prerequisites"]
    assert "IME 3302" in ie_cn["IME 3443"]["prerequisites"]
    assert "IME 4461" in ie_cn["IME 4462"]["prerequisites"]

    # GE placeholders
    ge_placeholders = [c for c in ie["courses"] if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge_placeholders) >= 10

    # Term unit sums
    by_col = {}
    for c in ie["courses"]:
        by_col.setdefault(c["grid_col"], []).append(c["units"])
    assert sum(by_col[0]) == 15   # FF
    assert sum(by_col[1]) == 16   # FS
    assert sum(by_col[2]) == 15   # SoF
    assert sum(by_col[3]) == 16   # SoS
    assert sum(by_col[4]) == 17   # JF
    assert sum(by_col[5]) == 15   # JS
    assert sum(by_col[6]) == 16   # SrF
    assert sum(by_col[7]) == 17   # SrS

    assert "IE" not in CONCENTRATIONS


def test_ie_placeholders_have_elective_keys():
    ie_by_id = {c["id"]: c for c in FLOWCHARTS["IE"]["courses"]}

    assert ie_by_id["IE_1141"]["elective_key"] == "ie_intro_lab"
    assert ie_by_id["IE_MATH1151"]["elective_key"] == "ie_linear_math"
    assert ie_by_id["IE_SUPPORT1"]["elective_key"] == "ie_support_elective"
    assert ie_by_id["IE_SUPPORT2"]["elective_key"] == "ie_support_elective"
    assert ie_by_id["IE_TECH1"]["elective_key"] == "ie_technical_elective"
    assert ie_by_id["IE_TECH2"]["elective_key"] == "ie_technical_elective"
    assert ie_by_id["IE_GE6"].get("elective_key") is None


def test_materials_engineering_flowchart():
    assert "MATE" in FLOWCHARTS
    mate = FLOWCHARTS["MATE"]
    assert mate["total_units"] == 125
    assert sum(c["units"] for c in mate["courses"]) == 125

    mate_cn = {c["course_number"]: c for c in mate["courses"]}

    # Key course titles
    assert "Introduction to Materials Engineering" in mate_cn["MATE 1110"]["title"]
    assert "Principles of Materials Engineering" in mate_cn["MATE 1210"]["title"]
    assert "Materials Thermodynamics" in mate_cn["MATE 2280"]["title"]
    assert "Metallurgical" in mate_cn["MATE 3360"]["title"]
    assert "Polymeric" in mate_cn["MATE 3310"]["title"]
    assert "Composite" in mate_cn["MATE 3480"]["title"]
    assert "Electronic" in mate_cn["MATE 3340"]["title"]
    assert "Ceramic" in mate_cn["MATE 4422"]["title"]
    assert "Senior Project I" in mate_cn["MATE 4461"]["title"]

    # Categories
    assert mate_cn["MATE 1110"]["category"] == "major"
    assert mate_cn["CHEM 1120"]["category"] == "support"
    assert mate_cn["MATH 1261"]["category"] == "support"
    assert mate_cn["ENGR 2211"]["category"] == "support"
    assert mate_cn["GE 1A"]["category"] == "ge"

    # Prerequisites
    assert "MATE 1110" in mate_cn["MATE 1210"]["prerequisites"]
    assert "MATE 1210" in mate_cn["MATE 2280"]["prerequisites"]
    assert "MATE 2280" in mate_cn["MATE 3360"]["prerequisites"]
    assert "MATE 2280" in mate_cn["MATE 3310"]["prerequisites"]
    assert "MATE 2280" in mate_cn["MATE 3340"]["prerequisites"]
    assert "MATE 4461" in mate_cn["MATE 4462"]["prerequisites"]

    # Quarter equivalents
    assert "MATH 141" in mate_cn["MATH 1261"]["quarter_equivalents"]
    assert "PHYS 141" in mate_cn["PHYS 1141"]["quarter_equivalents"]

    # GE placeholders
    ge_placeholders = [c for c in mate["courses"] if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge_placeholders) >= 9

    # Term unit sums
    by_col = {}
    for c in mate["courses"]:
        by_col.setdefault(c["grid_col"], []).append(c["units"])
    assert sum(by_col[0]) == 16   # FF
    assert sum(by_col[1]) == 16   # FS
    assert sum(by_col[2]) == 17   # SoF
    assert sum(by_col[3]) == 15   # SoS
    assert sum(by_col[4]) == 18   # JF
    assert sum(by_col[5]) == 16   # JS
    assert sum(by_col[6]) == 13   # SrF
    assert sum(by_col[7]) == 14   # SrS

    assert "MATE" not in CONCENTRATIONS


def test_mate_placeholders_have_elective_keys():
    mate_by_id = {c["id"]: c for c in FLOWCHARTS["MATE"]["courses"]}

    assert mate_by_id["MATE_CHEM"]["elective_key"] == "mate_chem_elective"
    assert mate_by_id["MATE_DESIGN"]["elective_key"] == "mate_design_elective"
    assert mate_by_id["MATE_TECH1"]["elective_key"] == "mate_technical_elective"
    assert mate_by_id["MATE_TECH2"]["elective_key"] == "mate_technical_elective"
    assert mate_by_id["MATE_PROF"]["elective_key"] == "mate_prof_dev_elective"
    assert mate_by_id["MATE_GE6"].get("elective_key") is None


def test_mathematics_flowchart():
    math = FLOWCHARTS["MATH"]
    assert math["total_units"] == 120

    courses = math["courses"]
    total = sum(c["units"] for c in courses)
    assert total == 120

    by_id = {c["id"]: c for c in courses}

    # Key course titles
    assert by_id["MATH_1261"]["title"] == "Calculus I"
    assert by_id["MATH_1262"]["title"] == "Calculus II"
    assert by_id["MATH_2031"]["title"] == "Transition to Advanced Mathematics"
    assert by_id["MATH_3152"]["title"] == "Advanced Linear Algebra"
    assert by_id["MATH_4201"]["title"] == "Abstract Algebra I"
    assert by_id["MATH_4264"]["title"] == "Real Analysis I"

    # Categories
    assert by_id["MATH_1261"]["category"] == "major"
    assert by_id["MATH_PHYS1141"]["category"] == "support"
    assert by_id["MATH_STAT1510"]["category"] == "support"
    assert by_id["MATH_GE1A"]["category"] == "ge"
    assert by_id["MATH_TRACK1"]["category"] == "concentration"

    # Prerequisites
    assert "MATH 1261" in by_id["MATH_1262"]["prerequisites"]
    assert "MATH 1261" in by_id["MATH_1151"]["prerequisites"]
    assert "MATH 1262" in by_id["MATH_2031"]["prerequisites"]
    assert "MATH 1262" in by_id["MATH_2263"]["prerequisites"]
    assert "MATH 2263" in by_id["MATH_2343"]["prerequisites"]
    assert "MATH 2031" in by_id["MATH_3152"]["prerequisites"]
    assert "MATH 4201" in by_id["MATH_4202"]["prerequisites"]
    assert "MATH 2343" in by_id["MATH_4264"]["prerequisites"]

    # Quarter equivalents
    assert "MATH 141" in by_id["MATH_1261"]["quarter_equivalents"]
    assert "MATH 142" in by_id["MATH_1262"]["quarter_equivalents"]
    assert "MATH 143" in by_id["MATH_2263"]["quarter_equivalents"]
    assert "MATH 244" in by_id["MATH_2343"]["quarter_equivalents"]

    # GE placeholders
    ge_placeholders = [c for c in courses if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge_placeholders) >= 10

    # Elective placeholders are marked
    assert by_id["MATH_TRACK1"]["is_placeholder"] is True
    assert by_id["MATH_FREE1"]["is_placeholder"] is True

    # Term unit sums
    by_col = {}
    for c in courses:
        by_col.setdefault(c["grid_col"], []).append(c["units"])
    assert sum(by_col[0]) == 15   # FF
    assert sum(by_col[1]) == 13   # FS
    assert sum(by_col[2]) == 16   # SoF
    assert sum(by_col[3]) == 16   # SoS
    assert sum(by_col[4]) == 16   # JF
    assert sum(by_col[5]) == 15   # JS
    assert sum(by_col[6]) == 13   # SrF
    assert sum(by_col[7]) == 16   # SrS

    assert "MATH" in CONCENTRATIONS
    math_concs = CONCENTRATIONS["MATH"]
    track_ids = [t["id"] for t in math_concs]
    assert "none" in track_ids
    assert "applied" in track_ids
    assert "teaching" in track_ids


def test_math_placeholders_have_elective_keys():
    math_by_id = {c["id"]: c for c in FLOWCHARTS["MATH"]["courses"]}

    assert math_by_id["MATH_PROG"]["elective_key"] == "math_programming_elective"
    assert math_by_id["MATH_UD1"]["elective_key"] == "math_upper_div_choice"
    assert math_by_id["MATH_SENIOR"]["elective_key"] == "math_senior_project"
    for i in range(1, 8):
        assert math_by_id[f"MATH_TRACK{i}"]["elective_key"] == "math_track_elective"

    # Teaching concentration overrides all track slots to math_track_teaching
    teaching = next(t for t in CONCENTRATIONS["MATH"] if t["id"] == "teaching")
    for i in range(1, 8):
        assert teaching["slot_overrides"][f"MATH_TRACK{i}"]["elective_key"] == "math_track_teaching"

    # Free electives have no elective_key
    assert math_by_id["MATH_FREE1"].get("elective_key") is None
    assert math_by_id["MATH_GE1A"].get("elective_key") is None


def test_kinesiology_flowchart():
    kine = FLOWCHARTS["KINE"]
    assert kine["total_units"] == 120

    courses = kine["courses"]
    assert sum(c["units"] for c in courses) == 120

    by_id = {c["id"]: c for c in courses}

    # Key titles
    assert by_id["KINE_1180"]["title"] == "Introduction to Kinesiology"
    assert by_id["KINE_3303"]["title"] == "Physiology of Exercise"
    assert by_id["KINE_3319"]["title"] == "Introduction to Research Methods in Kinesiology"
    assert by_id["KINE_4403"]["title"] == "Biomechanics"
    assert by_id["KINE_4451"]["title"] == "Nutrition for Fitness and Sport"

    # Categories
    assert by_id["KINE_1180"]["category"] == "major"
    assert by_id["KINE_BIO1151"]["category"] == "support"
    assert by_id["KINE_CHEM1120"]["category"] == "support"
    assert by_id["KINE_GE1A"]["category"] == "ge"
    assert by_id["KINE_CON1"]["category"] == "concentration"

    # Prerequisites
    assert "BIO 1151" in by_id["KINE_BIO2231"]["prerequisites"]
    assert "BIO 2231" in by_id["KINE_BIO2232"]["prerequisites"]
    assert "BIO 2232" in by_id["KINE_3303"]["prerequisites"]
    assert "KINE 3303" in by_id["KINE_4403"]["prerequisites"]
    assert "KINE 3319" in by_id["KINE_4412"]["prerequisites"]
    assert "KINE 4403" in by_id["KINE_SENIOR"]["prerequisites"]

    # GE placeholders
    ge = [c for c in courses if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge) >= 10

    # Elective placeholders marked
    assert by_id["KINE_CON1"]["is_placeholder"] is True
    assert by_id["KINE_FREE1"]["is_placeholder"] is True

    # Term unit sums
    by_col = {}
    for c in courses:
        by_col.setdefault(c["grid_col"], []).append(c["units"])
    assert sum(by_col[0]) == 15   # FF
    assert sum(by_col[1]) == 15   # FS
    assert sum(by_col[2]) == 16   # SoF
    assert sum(by_col[3]) == 16   # SoS
    assert sum(by_col[4]) == 14   # JF
    assert sum(by_col[5]) == 14   # JS
    assert sum(by_col[6]) == 15   # SrF
    assert sum(by_col[7]) == 15   # SrS

    assert "KINE" in CONCENTRATIONS
    tracks = [t["id"] for t in CONCENTRATIONS["KINE"]]
    assert "exercise_science" in tracks
    assert "health_promotion" in tracks
    assert "sport_science" in tracks


def test_kine_placeholders_have_elective_keys():
    kine_by_id = {c["id"]: c for c in FLOWCHARTS["KINE"]["courses"]}

    assert kine_by_id["KINE_HLTH_FF"]["elective_key"] == "kine_hlth_choice"
    assert kine_by_id["KINE_MATH_FF"]["elective_key"] == "kine_math_choice"
    assert kine_by_id["KINE_3323"]["elective_key"] == "kine_cultural_course"
    assert kine_by_id["KINE_SENIOR"]["elective_key"] == "kine_senior_project"

    # Base concentration slots have no elective_key (set by concentration)
    assert kine_by_id["KINE_CON1"].get("elective_key") is None

    # ES concentration wires elective keys on CON5/CON6
    es = next(t for t in CONCENTRATIONS["KINE"] if t["id"] == "exercise_science")
    assert es["slot_overrides"]["KINE_CON5"]["elective_key"] == "kine_es_elective"
    assert es["slot_overrides"]["KINE_CON6"]["elective_key"] == "kine_es_elective"
    assert es["slot_overrides"]["KINE_CON3"]["is_placeholder"] is False  # KINE 3330 is required
    assert es["slot_overrides"]["KINE_CON3"]["units"] == 2               # KINE 3330 is 2u

    # HP concentration
    hp = next(t for t in CONCENTRATIONS["KINE"] if t["id"] == "health_promotion")
    assert hp["slot_overrides"]["KINE_CON5"]["units"] == 4   # HLTH 4434 is 4u
    assert hp["slot_overrides"]["KINE_CON6"]["units"] == 2   # last HP elective slot is 2u

    # SS concentration overrides KINE_3323 to require KINE 3325
    ss = next(t for t in CONCENTRATIONS["KINE"] if t["id"] == "sport_science")
    assert ss["slot_overrides"]["KINE_3323"]["course_number"] == "KINE 3325"
    assert ss["slot_overrides"]["KINE_CON1"]["units"] == 2   # KINE 3330 is 2u
    assert ss["slot_overrides"]["KINE_FREE3"]["units"] == 3  # compensates CON1 1u drop


def test_food_science_flowchart():
    fsn = FLOWCHARTS["FSN"]
    assert fsn["total_units"] == 120

    courses = fsn["courses"]
    assert sum(c["units"] for c in courses) == 120

    by_id = {c["id"]: c for c in courses}

    # Key titles
    assert by_id["FSN_FDSC1110"]["title"] == "Introduction to Food Science and Sustainability"
    assert by_id["FSN_FDSC3350"]["title"] == "Food Chemistry"
    assert by_id["FSN_FDSC3345"]["title"] == "Food Safety and Sanitation"
    assert by_id["FSN_FDSC4425"]["title"] == "Food Product Development"
    assert by_id["FSN_STAT3320"]["title"] == "Statistical Methods for Food Science"

    # Categories
    assert by_id["FSN_FDSC1110"]["category"] == "major"
    assert by_id["FSN_CHEM1120"]["category"] == "support"
    assert by_id["FSN_GE1A"]["category"] == "ge"
    assert by_id["FSN_CON1"]["category"] == "concentration"

    # Prerequisites
    assert "CHEM 2240" in by_id["FSN_FDSC3330"]["prerequisites"]
    assert "FDSC 1110" in by_id["FSN_FDSC3340"]["prerequisites"]
    assert "CHEM 3350" in by_id["FSN_FDSC3350"]["prerequisites"]
    assert "MCRO 2221" in by_id["FSN_FDSC3345"]["prerequisites"]
    assert "FDSC 3350" in by_id["FSN_FDSC4425"]["prerequisites"]

    # GE placeholders
    ge = [c for c in courses if c.get("is_placeholder") and c["category"] == "ge"]
    assert len(ge) >= 7

    # Concentration placeholders
    assert by_id["FSN_CON1"]["is_placeholder"] is True
    assert by_id["FSN_CON4"]["is_placeholder"] is True

    # Term unit sums
    by_col = {}
    for c in courses:
        by_col.setdefault(c["grid_col"], []).append(c["units"])
    assert sum(by_col[0]) == 14   # FF
    assert sum(by_col[1]) == 14   # FS
    assert sum(by_col[2]) == 16   # SoF
    assert sum(by_col[3]) == 14   # SoS
    assert sum(by_col[4]) == 17   # JF
    assert sum(by_col[5]) == 14   # JS
    assert sum(by_col[6]) == 16   # SrF
    assert sum(by_col[7]) == 15   # SrS

    assert "FSN" in CONCENTRATIONS
    tracks = [t["id"] for t in CONCENTRATIONS["FSN"]]
    assert "none" in tracks
    assert "culinology" in tracks
    assert "food_safety" in tracks
    assert "sft" in tracks


def test_fsn_placeholders_have_elective_keys():
    # Concentration base slots have no elective_key (set by concentration overrides)
    fsn_by_id = {c["id"]: c for c in FLOWCHARTS["FSN"]["courses"]}
    assert fsn_by_id["FSN_CON1"].get("elective_key") is None
    assert fsn_by_id["FSN_CON3"].get("elective_key") is None

    # Concentration overrides wire elective keys
    food_safety = next(t for t in CONCENTRATIONS["FSN"] if t["id"] == "food_safety")
    assert food_safety["slot_overrides"]["FSN_CON1"]["elective_key"] == "fsn_fs_elective"
    assert food_safety["slot_overrides"]["FSN_CON4"]["elective_key"] == "fsn_senior_project"

    sft = next(t for t in CONCENTRATIONS["FSN"] if t["id"] == "sft")
    assert sft["slot_overrides"]["FSN_CON1"]["elective_key"] == "fsn_sft_elective"
    assert sft["slot_overrides"]["FSN_CON2"]["elective_key"] == "fsn_sft_elective"
    assert sft["slot_overrides"]["FSN_CON4"]["elective_key"] == "fsn_senior_project"
