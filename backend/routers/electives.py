import re

from fastapi import APIRouter, HTTPException, Query
from services.catalog import get_course_info, get_dept_courses

router = APIRouter()

# Static elective lists for well-defined small sets
_STATIC: dict[str, dict] = {
    "cs_calc_seq_1": {
        "title": "Calculus I or Calculus for Data Science I",
        "description": "CS and SE students may take the standard calculus sequence (MATH 1261 + MATH 1262) or the data science calculus sequence (MATH 1264 + MATH 1265). Choose one first-semester option.",
        "courses": [
            {"course_number": "MATH 1261", "title": "Calculus I", "units": 4},
            {"course_number": "MATH 1264", "title": "Calculus for Data Science I", "units": 4},
        ],
    },
    "cs_calc_seq_2": {
        "title": "Calculus II or Calculus for Data Science II",
        "description": "Take MATH 1262 after MATH 1261, or MATH 1265 after MATH 1264. Follow the same sequence you started.",
        "courses": [
            {"course_number": "MATH 1262", "title": "Calculus II", "units": 4},
            {"course_number": "MATH 1265", "title": "Calculus for Data Science II", "units": 4},
        ],
    },
    "cs_ethics_elective": {
        "title": "Ethics / Gender, Race & Technology",
        "description": "CS and SE students must take one of these three courses covering ethics, technology, and society.",
        "courses": [
            {"course_number": "PHIL 3323", "title": "Ethics, Science, and Technology", "units": 3},
            {"course_number": "WGQS 3350", "title": "Gender, Race, Culture, Science, and Technology", "units": 4},
            {"course_number": "WGQS 3351", "title": "Gender, Race, Class, Nation: Critical Computing and Engineering Studies", "units": 4},
        ],
    },
    "agc_chem_elective": {
        "title": "Chemistry Elective",
        "description": "AGC and ASM students must take one chemistry course: a survey (CHEM 1110) or the more rigorous fundamentals course (CHEM 1120).",
        "courses": [
            {"course_number": "CHEM 1110", "title": "World of Chemistry", "units": 4},
            {"course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure and Properties", "units": 4},
        ],
    },
    "agc_stat_data_1000": {
        "title": "Statistical and Data Literacy",
        "description": "AGC students complete the cross-listed Statistical and Data Literacy course as STAT 1000 or DATA 1000.",
        "courses": [
            {"course_number": "STAT 1000", "title": "Statistical and Data Literacy", "units": 3},
            {"course_number": "DATA 1000", "title": "Statistical and Data Literacy", "units": 3},
        ],
    },
    "asm_chem_elective": {
        "title": "Chemistry Elective",
        "description": "ASM students must take one chemistry course: CHEM 1110 (survey) or CHEM 1120 (fundamentals).",
        "courses": [
            {"course_number": "CHEM 1110", "title": "World of Chemistry", "units": 4},
            {"course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure and Properties", "units": 4},
        ],
    },
    "agc_fsn_elective": {
        "title": "Food Science Elective",
        "description": "AGC students take one food science course: FSN 1111 (Food Processing) or FSN 2245 (Food Safety).",
        "courses": [
            {"course_number": "FSN 1111", "title": "Elements of Food Processing", "units": 3},
            {"course_number": "FSN 2245", "title": "Elements of Food Safety", "units": 3},
        ],
    },
    "agc_plsc_pair": {
        "title": "Principles of Plant Sciences with Lab",
        "description": "AGC students take both PLSC 1120 and PLSC 1120L for the plant sciences support requirement.",
        "courses": [
            {"course_number": "PLSC 1120", "title": "Principles of Plant Sciences", "units": 2},
            {"course_number": "PLSC 1120L", "title": "Principles of Plant Sciences Lab", "units": 1},
        ],
    },
    "agc_ags_marketing": {
        "title": "Food Marketing Elective",
        "description": "AGC and AGS students take one marketing course covering food or wine marketing.",
        "courses": [
            {"course_number": "AGB 3301", "title": "Food Marketing", "units": 3},
            {"course_number": "WVIT 3343", "title": "Branded Wine Marketing", "units": 3},
        ],
    },
    "ags_math_elective": {
        "title": "Mathematics Support Elective",
        "description": "AGS students take one math or statistics course at an appropriate level for their background. MATH 1006 is college algebra; MATH 1007 is precalculus; MATH 1261 and 1264 are calculus options; MATH 1267 is business calculus.",
        "courses": [
            {"course_number": "MATH 1006", "title": "College Algebra", "units": 3},
            {"course_number": "MATH 1007", "title": "Precalculus", "units": 3},
            {"course_number": "MATH 1261", "title": "Calculus I", "units": 4},
            {"course_number": "MATH 1264", "title": "Calculus for Data Science I", "units": 4},
            {"course_number": "MATH 1267", "title": "Business Calculus", "units": 3},
        ],
    },
    "asm_math_elective": {
        "title": "Math / Statistics Elective",
        "description": "ASM students take one of these courses based on their math placement: MATH 1007 (Precalculus), STAT 1110 (Applied Statistics), or MATH 1267 (Business Calculus).",
        "courses": [
            {"course_number": "MATH 1007", "title": "Precalculus", "units": 3},
            {"course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3},
            {"course_number": "MATH 1267", "title": "Business Calculus", "units": 3},
        ],
    },
    "asci_org_chem": {
        "title": "Organic Chemistry Elective",
        "description": "ASCI students take one organic chemistry course: CHEM 2240 (Fundamentals, 4 units) or CHEM 2242 (Organic Chemistry I, 5 units).",
        "courses": [
            {"course_number": "CHEM 2240", "title": "Organic Chemistry: Fundamentals and Applications", "units": 4},
            {"course_number": "CHEM 2242", "title": "Organic Chemistry I", "units": 5},
        ],
    },
    "asci_biochem_elective": {
        "title": "Biochemistry Elective",
        "description": "ASCI students take one biochemistry course: ASCI 3319, CHEM 3350, or CHEM 3352.",
        "courses": [
            {"course_number": "ASCI 3319", "title": "Physiological Chemistry of Animals", "units": 3},
            {"course_number": "CHEM 3350", "title": "Biochemistry: Fundamentals and Applications", "units": 3},
            {"course_number": "CHEM 3352", "title": "Biochemistry", "units": 4},
        ],
    },
    "agb_senior_project": {
        "title": "Senior Project",
        "description": "AGB students complete one senior project option: AGB 4462 (Applied Agribusiness Problems) or AGB 4463 (Agribusiness Consulting).",
        "courses": [
            {"course_number": "AGB 4462", "title": "Senior Project - Applied Agribusiness Problems", "units": 3},
            {"course_number": "AGB 4463", "title": "Senior Project - Agribusiness Consulting", "units": 3},
        ],
    },
    "agb_agricultural_elective": {
        "title": "Agricultural Elective",
        "description": "AGB students must take one agricultural elective from the catalog list. PLSC 1120 and PLSC 1120L are the paired plant sciences lecture/lab option.",
        "courses": [
            {"course_number": "ASCI 1112", "title": "Principles of Animal Science", "units": 3},
            {"course_number": "ASCI 2215", "title": "Safe Handling of Animal-Derived Foods", "units": 4},
            {"course_number": "ASCI 2239", "title": "Principles of Rangeland Management", "units": 3},
            {"course_number": "DSCI 2229", "title": "General Dairy Manufacturing", "units": 4},
            {"course_number": "FSN 2245", "title": "Elements of Food Safety", "units": 3},
            {"course_number": "PLSC 1120", "title": "Principles of Plant Sciences", "units": 2},
            {"course_number": "PLSC 1120L", "title": "Principles of Plant Sciences Lab", "units": 1},
            {"course_number": "SS 1120", "title": "Introductory Soil Science", "units": 4},
        ],
    },
    "cs_phys_or_chem": {
        "title": "Physics I or Fund. Chemistry",
        "description": "CS students must take one of these two courses as a science support requirement.",
        "courses": [
            {"course_number": "PHYS 1141", "title": "General Physics I", "units": 4},
            {"course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure and Properties", "units": 4},
        ],
    },
    "cs_life_science": {
        "title": "Life Science Elective",
        "description": "One life science course from Biology, Botany, or Microbiology (4 units). If you take BIO 1111 (3-unit lecture), also enroll in BIO 1112 (1-unit lab) to meet the full 4-unit requirement.",
        "courses": [
            {"course_number": "BIO 1111", "title": "General Biology (lecture)", "units": 3},
            {"course_number": "BIO 1112", "title": "Biology Laboratory for Non-Majors (lab — take with BIO 1111)", "units": 1},
            {"course_number": "BIO 1150", "title": "Life: History and Diversity", "units": 4},
            {"course_number": "BIO 1151", "title": "Life: Molecules and Cells", "units": 4},
            {"course_number": "BOT 1121", "title": "General Botany", "units": 4},
            {"course_number": "MCRO 2221", "title": "Introduction to Microbiology", "units": 4},
        ],
    },
    "ad_sculpture_or_painting": {
        "title": "Beginning Sculpture or Painting",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "ART 1184", "title": "Beginning Sculpture", "units": 3},
            {"course_number": "ART 2282", "title": "Beginning Painting", "units": 3},
        ],
    },
    "ad_portfolio_review": {
        "title": "Portfolio Review",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "ART 3359", "title": "Portfolio: Graphic Design", "units": 3},
            {"course_number": "ART 3379", "title": "Portfolio: Photo Video", "units": 3},
            {"course_number": "ART 3399", "title": "Portfolio: Studio Art", "units": 3},
        ],
    },
    "pols_support_4b": {
        "title": "Social and Behavioral Sciences Support",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "ANT 2201", "title": "Cultural Anthropology", "units": 3},
            {"course_number": "GEOG 1150", "title": "Human Geography", "units": 3},
            {"course_number": "HIST 2222", "title": "World History to 1500", "units": 3},
            {"course_number": "HIST 2223", "title": "World History since 1500", "units": 3},
            {"course_number": "SOC 1110", "title": "Comparative Societies", "units": 3},
        ],
    },
    "psy_foundation_course": {
        "title": "Foundation Course",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "PSY 2205", "title": "Personality", "units": 3},
            {"course_number": "PSY 2252", "title": "Social Psychology", "units": 3},
            {"course_number": "PSY 2256", "title": "Developmental Psychology", "units": 3},
        ],
    },
    "psy_professional_skills": {
        "title": "Professional Skills Support Course",
        "description": "One approved professional skills course required for the Psychology BS. These courses develop interpersonal, intercultural, and teamwork competencies relevant to psychology careers.",
        "courses": [
            {"course_number": "COMS 3316", "title": "Intercultural Communication", "units": 4},
            {"course_number": "COMS 3320", "title": "Intergroup Communication", "units": 4},
            {"course_number": "PSY 3304", "title": "Intergroup Dialogues", "units": 4},
            {"course_number": "PSY 3323", "title": "The Helping Relationship", "units": 4},
            {"course_number": "PSY 3350", "title": "Teamwork", "units": 4},
        ],
    },
    "psy_dei": {
        "title": "Diversity, Equity and Inclusion Course",
        "description": "One approved DEI course required for the Psychology BS. These courses examine systems of power, identity, and social justice from multiple perspectives.",
        "courses": [
            {"course_number": "ES 3380", "title": "Critical Race Theory", "units": 4},
            {"course_number": "ES 3381", "title": "Social Constructions of Whiteness", "units": 4},
            {"course_number": "PSY 3304", "title": "Intergroup Dialogues", "units": 4},
            {"course_number": "WGQS 3301", "title": "Contemporary Issues in Women's and Gender Studies", "units": 4},
            {"course_number": "WGQS 3330", "title": "Feminist/Queer Transnational Studies", "units": 4},
            {"course_number": "WGQS 3351", "title": "Gender, Race, Class, Nation: Critical Computing and Engineering Studies", "units": 4},
        ],
    },
    "psy_upper_div_science": {
        "title": "Upper-Division Science Course",
        "description": "One approved upper-division science course required for the Psychology BS. Courses cover biological, environmental, or social science topics with scientific rigor.",
        "courses": [
            {"course_number": "BIO 3312", "title": "Human Genetics", "units": 4},
            {"course_number": "FSN 3305", "title": "Nutrition and Exercise for Health and Disease Prevention", "units": 3},
            {"course_number": "IME 3320", "title": "Human Factors and Technology", "units": 4},
            {"course_number": "ISLA 3305", "title": "Public Engagements with STEM", "units": 4},
            {"course_number": "NR 3310", "title": "Global Climate Change", "units": 4},
            {"course_number": "PSY 3344", "title": "Behavioral Genetics", "units": 4},
            {"course_number": "WGQS 3350", "title": "Gender, Race, Culture, Science, and Technology", "units": 4},
        ],
    },
    "psy_internship_i": {
        "title": "Internship I",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "PSY 4448", "title": "Research Internship I", "units": 3},
            {"course_number": "PSY 4453", "title": "Supervised Fieldwork Internship I", "units": 3},
        ],
    },
    "psy_internship_ii": {
        "title": "Internship II",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "PSY 4449", "title": "Research Internship II", "units": 3},
            {"course_number": "PSY 4454", "title": "Supervised Fieldwork Internship II", "units": 3},
        ],
    },
    "engl_language_1101": {
        "title": "Elementary Language and Culture",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "CHIN 1101", "title": "Elementary Chinese Language and Culture I", "units": 4},
            {"course_number": "FR 1101", "title": "Elementary French Language and Culture I", "units": 4},
            {"course_number": "GER 1101", "title": "Elementary German Language and Culture", "units": 4},
            {"course_number": "ITAL 1101", "title": "Elementary Italian I", "units": 4},
            {"course_number": "JPNS 1101", "title": "Elementary Japanese I", "units": 4},
            {"course_number": "SPAN 1101", "title": "Elementary Spanish I", "units": 4},
            {"course_number": "WLC 1101", "title": "Elementary World Language and Culture I", "units": 4},
        ],
    },
    "mu_fundamentals_or_materials_i": {
        "title": "Music Fundamentals or Materials and Structures I",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "MU 1101", "title": "Music Fundamentals", "units": 3},
            {"course_number": "MU 1103", "title": "Materials and Structures of Music I", "units": 4},
        ],
    },
    "mu_materials_i_or_ii": {
        "title": "Materials and Structures of Music I or II",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "MU 1103", "title": "Materials and Structures of Music I", "units": 4},
            {"course_number": "MU 2203", "title": "Materials and Structures of Music II", "units": 4},
        ],
    },
    "mu_uscp_music_choice": {
        "title": "Jazz Styles or Popular Music of the United States",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "MU 2221", "title": "Jazz Styles", "units": 3},
            {"course_number": "MU 2227", "title": "Popular Music of the United States", "units": 4},
        ],
    },
    "antgeog_senior_project_i": {
        "title": "Senior Project I",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "ANT 4461", "title": "Senior Project I", "units": 3},
            {"course_number": "GEOG 4461", "title": "Senior Project I", "units": 3},
        ],
    },
    "antgeog_senior_project_ii": {
        "title": "Senior Project II",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "ANT 4462", "title": "Senior Project II", "units": 4},
            {"course_number": "GEOG 4462", "title": "Senior Project II", "units": 4},
        ],
    },
    "arch_precalc_or_calculus": {
        "title": "Precalculus or Calculus I",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "MATH 1007", "title": "Precalculus", "units": 3},
            {"course_number": "MATH 1261", "title": "Calculus I", "units": 4},
        ],
    },
    "arch_physics_i": {
        "title": "College Physics I or General Physics I",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "PHYS 1121", "title": "College Physics I", "units": 4},
            {"course_number": "PHYS 1141", "title": "General Physics I", "units": 4},
        ],
    },
    "bus_calculus_choice": {
        "title": "Calculus for Data Science I or Business Calculus",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "MATH 1264", "title": "Calculus for Data Science I", "units": 4},
            {"course_number": "MATH 1267", "title": "Business Calculus", "units": 3},
        ],
    },
    "bus_finance_methods_choice": {
        "title": "Financial Institutions or Quantitative Methods in Finance",
        "description": "Students must take one of these courses.",
        "courses": [
            {"course_number": "BUS 1342", "title": "Financial Institutions", "units": 3},
            {"course_number": "BUS 3343", "title": "Quantitative Methods in Finance", "units": 3},
        ],
    },
    "cpe_ethics_or_stats": {
        "title": "Ethics / Engineering Statistics",
        "description": "CPE students must take one of these three courses as a support requirement.",
        "courses": [
            {"course_number": "PHIL 3323", "title": "Ethics, Science, and Technology", "units": 3},
            {"course_number": "STAT 3210", "title": "Engineering Statistics", "units": 3},
            {"course_number": "STAT 3310", "title": "Probability and Random Processes for Engineers", "units": 3},
        ],
    },
    "arce_hist_elective": {
        "title": "History of Architecture or Structures",
        "description": "ARCE students select one history course from history of world architecture or history of structures.",
        "courses": [
            {"course_number": "ARCH 2221", "title": "History of World Architecture I: Prehistory to 17th Century", "units": 3},
            {"course_number": "ARCH 2222", "title": "History of World Architecture II: 17th Century to the Present", "units": 3},
            {"course_number": "ARCE 2280", "title": "History of Structures", "units": 3},
        ],
    },
    "arce_surveying_elective": {
        "title": "FE/PE Surveying Elective",
        "description": "ARCE students select one surveying course (2–3 units) for FE/PE exam preparation.",
        "courses": [
            {"course_number": "BRAE 1239", "title": "Engineering Surveying", "units": 3},
            {"course_number": "BRAE 2237", "title": "Introduction to Engineering Surveying", "units": 2},
            {"course_number": "CM 2239", "title": "Construction Surveying", "units": 3},
        ],
    },
    "me_ime_mfg_selective": {
        "title": "Manufacturing Process Selective",
        "description": "ME students select one 1-unit manufacturing process course.",
        "courses": [
            {"course_number": "IME 1141", "title": "Introduction to Metal Casting and Prototyping", "units": 1},
            {"course_number": "IME 1142", "title": "Materials Joining", "units": 1},
            {"course_number": "IME 1149", "title": "Introduction to Manufacturing Processes", "units": 1},
        ],
    },
    "bmed_anat_phys": {
        "title": "Human Anatomy and Physiology I or II",
        "description": "BMED students take either Human Anatomy and Physiology I or Human Anatomy and Physiology II.",
        "courses": [
            {"course_number": "BIO 2231", "title": "Human Anatomy and Physiology I", "units": 4},
            {"course_number": "BIO 2232", "title": "Human Anatomy and Physiology II", "units": 4},
        ],
    },
    "brae_econ_elective": {
        "title": "Survey of Economics",
        "description": "BRAE students take either the general Survey of Economics or the agriculture-focused Principles of Economics.",
        "courses": [
            {"course_number": "ECON 2001", "title": "Survey of Economics", "units": 3},
            {"course_number": "ECON 2040", "title": "Principles of Economics: Agricultural", "units": 3},
        ],
    },
}

# Dynamic elective configs: fetch all courses from listed depts, filter by level range
_DYNAMIC: dict[str, dict] = {
    "cs_tech_elective": {
        "title": "Technical / Concentration Elective",
        "description": "Any upper-division CSC course (4000-level). When a concentration is selected, specific required courses replace this slot.",
        "depts": ["csc"],
        "min_level": 4000,
        "max_level": 4999,
    },
    "se_tech_elective": {
        "title": "Technical Elective",
        "description": "Upper-division CSC course approved for Software Engineering technical elective credit.",
        "depts": ["csc"],
        "min_level": 4000,
        "max_level": 4999,
    },
    "cpe_tech_elective": {
        "title": "Technical Elective",
        "description": "Upper-division CPE or CSC course for Computer Engineering technical elective credit.",
        "depts": ["cpe", "csc"],
        "min_level": 4000,
        "max_level": 4999,
    },
    "me_tech_elective": {
        "title": "Technical Elective",
        "description": "Upper-division ME course for Mechanical Engineering technical elective credit.",
        "depts": ["me"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "ce_tech_elective": {
        "title": "Technical Elective",
        "description": "Upper-division CE course for Civil Engineering technical elective credit.",
        "depts": ["ce"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "psy_social_personality": {
        "title": "Social & Personality Elective",
        "description": "One upper-division PSY course covering social or personality psychology topics.",
        "depts": ["psy"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "psy_mental_health": {
        "title": "Mental & Physical Health Elective",
        "description": "One upper-division PSY course covering mental health, clinical, or health psychology topics.",
        "depts": ["psy"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "psy_cognitive": {
        "title": "Cognitive Elective",
        "description": "One upper-division PSY course covering cognitive psychology, learning, or neuroscience.",
        "depts": ["psy"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "psy_upper_div": {
        "title": "PSY Approved Elective",
        "description": "Any upper-division PSY course (3000–4000 level).",
        "depts": ["psy"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "bio_4000_level": {
        "title": "4000-Level Biology Elective",
        "description": "Any 4000-level BIO course.",
        "depts": ["bio"],
        "min_level": 4000,
        "max_level": 4999,
    },
    "bio_bioscience": {
        "title": "Bioscience Elective",
        "description": "Any upper-division BIO course (3000–4000 level).",
        "depts": ["bio"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "bio_approved": {
        "title": "Approved Elective",
        "description": "Approved BIO or MCRO upper-division elective. Consult your advisor for specific requirements.",
        "depts": ["bio", "mcro"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "agb_general_elective": {
        "title": "Agribusiness General Elective",
        "description": "Select any 3000-4000 level AGB course for the Agribusiness General Electives requirement.",
        "depts": ["agb"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "agb_4000_elective": {
        "title": "4000-Level Agribusiness Elective",
        "description": "Select any 4000-level AGB course for the final Agribusiness General Elective requirement.",
        "depts": ["agb"],
        "min_level": 4000,
        "max_level": 4999,
    },
    "agb_cafes_prefix_elective": {
        "title": "CAFES Prefix Elective",
        "description": "Select any course with one of the catalog-approved CAFES prefixes: AG, AGC, AGED, ASCI, BRAE, DSCI, EIM, ERSC, ESCI, FSN, NR, PLSC, SS, or WVIT.",
        "depts": ["ag", "agc", "aged", "asci", "brae", "dsci", "eim", "ersc", "esci", "fsn", "nr", "plsc", "ss", "wvit"],
        "min_level": 1000,
        "max_level": 4999,
    },
}


def _build_courses(depts: list[str], min_level: int, max_level: int) -> list[dict]:
    courses = []
    for dept in depts:
        dept_courses = get_dept_courses(dept)
        for course_num in sorted(dept_courses.keys()):
            parts = course_num.split()
            if len(parts) < 2:
                continue
            try:
                level = int(parts[-1])
            except ValueError:
                continue
            if not (min_level <= level <= max_level):
                continue
            info = dept_courses[course_num]
            raw_units = str(info.get("units", "4"))
            try:
                units = int(raw_units.split("-")[0].split("–")[0])
            except (ValueError, IndexError):
                units = 4
            courses.append({
                "course_number": course_num,
                "title": info.get("title", ""),
                "units": units,
            })
    return courses


_DEPT_RE = re.compile(r"\b[A-Z]{2,5}\b")
_COURSE_RE = re.compile(r"(?:(?P<dept>[A-Z]{2,5})\s*)?(?P<num>\d{3,4}[A-Z]?)")


def _course_units(info: dict | None, default: int = 3) -> int:
    if not info:
        return default
    raw_units = str(info.get("units", str(default)))
    try:
        return int(raw_units.split("-")[0].split("–")[0])
    except (ValueError, IndexError):
        return default


def _course_title(course_number: str, fallback: str) -> str:
    info = get_course_info(course_number)
    return info.get("title", fallback) if info else fallback


def _direct_course_numbers(course_number: str, quarter_equivalents: str) -> list[str]:
    text = f"{course_number} {quarter_equivalents}".replace(",", " ")
    courses: list[str] = []
    seen: set[str] = set()
    current_dept: str | None = None
    for match in _COURSE_RE.finditer(text.upper()):
        dept = match.group("dept") or current_dept
        num = match.group("num")
        if not dept:
            continue
        current_dept = dept
        value = f"{dept} {num}"
        if value not in seen:
            seen.add(value)
            courses.append(value)
    return courses


def _build_direct_courses(course_numbers: list[str], fallback_title: str) -> list[dict]:
    courses = []
    for course_number in course_numbers:
        info = get_course_info(course_number)
        courses.append({
            "course_number": course_number,
            "title": info.get("title", fallback_title) if info else fallback_title,
            "units": _course_units(info),
        })
    return courses


def _auto_config(course_id: str, course_number: str, title: str) -> dict:
    haystack = f"{course_id} {course_number} {title}".upper()
    prefix = course_id.split("_", 1)[0].upper()
    min_level = 3000
    max_level = 4999

    if "LOWER" in haystack or " LD" in haystack or "LDC" in haystack:
        min_level, max_level = 1000, 2999
    elif "3000-4000" in haystack or "3000+" in haystack or "3000" in haystack or "UPPER" in haystack or "TECH" in haystack:
        min_level, max_level = 3000, 4999
    elif "4000" in haystack:
        min_level, max_level = 4000, 4999

    if "ART HISTORY" in haystack or "HIST" in haystack:
        depts = ["art"] if prefix == "AD" else ["arch", "arce"]
    elif "ASCI/DSCI" in haystack:
        depts = ["asci", "dsci"]
    elif "BIO/MCRO" in haystack:
        depts = ["bio", "mcro"]
    elif "CAFES" in haystack:
        depts = ["agb", "agc", "aged", "asci", "brae", "dsci", "fsn", "plsc", "ss"]
    elif "MUSIC" in haystack or prefix == "MU":
        depts = ["mu"]
    elif prefix in {"CS", "SE"}:
        depts = ["csc"]
    elif prefix == "CPE":
        depts = ["cpe", "csc"]
    elif prefix == "CE":
        depts = ["ce"]
    elif prefix == "ME":
        depts = ["me"]
    elif prefix == "AERO":
        depts = ["aero"]
    elif prefix == "AD":
        depts = ["art"]
    elif prefix == "POLS":
        depts = ["pols"]
    elif prefix == "ENGL":
        depts = ["engl"]
    elif prefix in {"AGC", "AGS"}:
        depts = ["agc", "aged", "agb", "asci", "brae", "dsci", "fsn", "nr", "plsc", "ss"]
    elif prefix == "ASCI":
        depts = ["asci", "dsci"]
    elif prefix == "AGB":
        depts = ["agb"]
    elif prefix == "ARCE":
        depts = ["arce", "arch", "brae", "cm"]
    elif prefix == "ANTGEOG":
        depts = ["ant", "geog", "ersc"]
    elif prefix == "ARCH":
        depts = ["arch"]
    elif prefix == "BIO":
        depts = ["bio", "mcro"]
    elif prefix == "BMED":
        depts = ["bmed", "bio", "me", "ee"]
    elif prefix == "BIOC":
        depts = ["chem", "bio", "mcro"]
    elif prefix == "ASM":
        depts = ["brae", "agb", "aged", "asci"]
    elif prefix == "BRAE":
        depts = ["brae"]
    elif prefix == "BUS":
        depts = ["bus", "itp"]
    else:
        matched_depts = _DEPT_RE.findall(course_number.upper())
        depts = [dept.lower() for dept in matched_depts] or ["csc"]

    return {
        "title": title,
        "description": "Select a course for this requirement. Verify elective approval with your academic advisor.",
        "depts": depts,
        "min_level": min_level,
        "max_level": max_level,
    }


# Placeholder IDs that map directly to a named static or dynamic elective key,
# bypassing the auto-parser (which would otherwise expose quarter-system course numbers).
_PLACEHOLDER_ELECTIVE_KEY: dict[str, str] = {
    "LIFESCI": "cs_life_science",
    "AGC_STATDATA1000": "agc_stat_data_1000",
    "AGC_PLSC1120": "agc_plsc_pair",
}


@router.get("/auto/placeholder")
def get_placeholder_elective_courses(
    course_id: str = Query(...),
    course_number: str = Query(...),
    title: str = Query(...),
    quarter_equivalents: str = Query(""),
):
    if course_id in _PLACEHOLDER_ELECTIVE_KEY:
        key = _PLACEHOLDER_ELECTIVE_KEY[course_id]
        data = _STATIC.get(key) or _DYNAMIC.get(key)
        if data:
            courses = data["courses"] if "courses" in data else _build_courses(
                data["depts"], data["min_level"], data["max_level"]
            )
            return {"key": f"auto:{course_id}", "title": data["title"], "description": data["description"], "courses": courses}

    direct_courses = _direct_course_numbers(course_number, quarter_equivalents)
    if direct_courses:
        return {
            "key": f"auto:{course_id}",
            "title": title,
            "description": "Select one of the courses associated with this requirement.",
            "courses": _build_direct_courses(direct_courses, title),
        }

    cfg = _auto_config(course_id, course_number, title)
    return {
        "key": f"auto:{course_id}",
        "title": cfg["title"],
        "description": cfg["description"],
        "courses": _build_courses(cfg["depts"], cfg["min_level"], cfg["max_level"]),
    }


@router.get("/{key}")
def get_elective_courses(key: str):
    if key in _STATIC:
        data = _STATIC[key]
        return {"key": key, "title": data["title"], "description": data["description"], "courses": data["courses"]}
    if key in _DYNAMIC:
        cfg = _DYNAMIC[key]
        courses = _build_courses(cfg["depts"], cfg["min_level"], cfg["max_level"])
        return {"key": key, "title": cfg["title"], "description": cfg["description"], "courses": courses}
    raise HTTPException(status_code=404, detail=f"No elective data for key: {key}")
