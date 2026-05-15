# Real semester flowchart data from Cal Poly 2026-2028 catalog.
# quarter_equivalents: old quarter course numbers that satisfy this requirement.
# prerequisites: semester course numbers that must be completed first.
# grid_col: 0=Fr.Fall 1=Fr.Spring 2=So.Fall 3=So.Spring 4=Jr.Fall 5=Jr.Spring 6=Sr.Fall 7=Sr.Spring

from typing import TypedDict


class Course(TypedDict):
    id: str
    course_number: str
    title: str
    units: int
    category: str           # "major" | "support" | "concentration" | "ge"
    grid_col: int
    grid_row: int
    prerequisites: list[str]   # semester course_number strings
    quarter_equivalents: list[str]
    is_placeholder: bool


# ─────────────────────────────────────────────────────────────────────────────
# COMPUTER SCIENCE — General Curriculum (120 units)
# Source: catalog.calpoly.edu/engineering/computer-science-software/computer-science-bs/
# ─────────────────────────────────────────────────────────────────────────────
CS_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "CSC1000",  "course_number": "CSC 1000",  "title": "Computing Majors Orientation",         "units": 1, "category": "major",   "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CSC1024",  "course_number": "CSC 1024",  "title": "Introduction to Computing",            "units": 2, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["CSC 101"], "is_placeholder": False},
    {"id": "MATH1261", "course_number": "MATH 1261", "title": "Calculus I",                           "units": 4, "category": "support", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "LIFESCI",  "course_number": "BIO/BOT",   "title": "Life Science Elective",                "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "GE1A",     "course_number": "GE 1A",     "title": "Written Communication",                "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "CSC1001",  "course_number": "CSC 1001",  "title": "Fundamentals of Computer Science",     "units": 4, "category": "major",   "grid_col": 1, "grid_row": 0, "prerequisites": ["CSC 1024"], "quarter_equivalents": ["CSC 101"], "is_placeholder": False},
    {"id": "PHYS1141", "course_number": "PHYS 1141", "title": "General Physics I",                    "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["PHYS 141", "CHEM 124", "CHEM 1120"], "is_placeholder": False},
    {"id": "MATH1262", "course_number": "MATH 1262", "title": "Calculus II",                          "units": 4, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "GE1B",     "course_number": "GE 1B",     "title": "Critical Thinking",                    "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "CSC2001",  "course_number": "CSC 2001",  "title": "Data Structures",                      "units": 4, "category": "major",   "grid_col": 2, "grid_row": 0, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CSC 202"], "is_placeholder": False},
    {"id": "MATH1151", "course_number": "MATH 1151", "title": "Linear Algebra",                       "units": 3, "category": "support", "grid_col": 2, "grid_row": 1, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 244"], "is_placeholder": False},
    {"id": "GE1C",     "course_number": "GE 1C",     "title": "Oral Communication",                   "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "GE3A",     "course_number": "GE 3A",     "title": "Arts",                                 "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "CPE2300",  "course_number": "CPE 2300",  "title": "Introduction to Computer Systems",     "units": 3, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CPE 225"], "is_placeholder": False},
    {"id": "CSC2050",  "course_number": "CSC 2050",  "title": "System Software Mechanics",            "units": 3, "category": "major",   "grid_col": 3, "grid_row": 1, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CSC 357", "CSC 203"], "is_placeholder": False},
    {"id": "MATH2031", "course_number": "MATH 2031", "title": "Transition to Advanced Mathematics",   "units": 3, "category": "support", "grid_col": 3, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "GE3B",     "course_number": "GE 3B",     "title": "Humanities",                           "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE4A",     "course_number": "GE 4A",     "title": "American Institutions",                "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "CSC3001",  "course_number": "CSC 3001",  "title": "Modern Application Development",       "units": 4, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": ["CSC 2001"], "quarter_equivalents": ["CSC 203"], "is_placeholder": False},
    {"id": "CSC3201",  "course_number": "CSC 3201",  "title": "Introduction to Computer Security",    "units": 3, "category": "major",   "grid_col": 4, "grid_row": 1, "prerequisites": ["CSC 2001", "CPE 2300"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CSC3449",  "course_number": "CSC 3449",  "title": "Algorithms and Complexity",            "units": 4, "category": "major",   "grid_col": 4, "grid_row": 2, "prerequisites": ["CSC 2001", "MATH 2031"], "quarter_equivalents": ["CSC 349"], "is_placeholder": False},
    {"id": "GE4B",     "course_number": "GE 4B",     "title": "Social & Behavioral Sciences",         "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE6",      "course_number": "GE 6",      "title": "Ethnic Studies",                       "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CSC3100",  "course_number": "CSC 3100",  "title": "Software Engineering",                 "units": 4, "category": "major",   "grid_col": 5, "grid_row": 0, "prerequisites": ["CSC 2001"], "quarter_equivalents": ["CSC 307"], "is_placeholder": False},
    {"id": "CSC3300",  "course_number": "CSC 3300",  "title": "Programming Languages",                "units": 3, "category": "major",   "grid_col": 5, "grid_row": 1, "prerequisites": ["CSC 2001"], "quarter_equivalents": ["CSC 430"], "is_placeholder": False},
    {"id": "STAT3210", "course_number": "STAT 3210", "title": "Engineering Statistics",               "units": 3, "category": "support", "grid_col": 5, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["STAT 312"], "is_placeholder": False},
    {"id": "CON_JRS1", "course_number": "Conc.",     "title": "Technical/Conc. Elective",             "units": 4, "category": "concentration", "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE_UDIV4", "course_number": "GE UD-4",  "title": "Upper-Div Social Sciences",            "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "CSC4553",  "course_number": "CSC 4553",  "title": "Introduction to Operating Systems",   "units": 3, "category": "major",   "grid_col": 6, "grid_row": 0, "prerequisites": ["CSC 2050"], "quarter_equivalents": ["CSC 453"], "is_placeholder": False},
    {"id": "PHIL3323", "course_number": "PHIL 3323", "title": "Ethics, Science, and Technology",     "units": 3, "category": "support", "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "WGQS3350", "course_number": "WGQS 3350", "title": "Gender, Race, Culture, Sci & Tech",   "units": 4, "category": "support", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CON_SRF1", "course_number": "Conc.",     "title": "Technical/Conc. Elective",             "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CSC4460",  "course_number": "CSC 4460",  "title": "Senior Project",                       "units": 4, "category": "major",   "grid_col": 7, "grid_row": 0, "prerequisites": ["CSC 3100"], "quarter_equivalents": ["CSC 480", "CSC 481"], "is_placeholder": False},
    {"id": "CON_SRS1", "course_number": "Conc.",     "title": "Technical/Conc. Elective",             "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRS2", "course_number": "Conc.",     "title": "Technical/Conc. Elective",             "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRS3", "course_number": "Ext.",      "title": "External Elective",                    "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# AEROSPACE ENGINEERING — General (128 units)
# Source: catalog.calpoly.edu/engineering/aerospace/aerospace-engineering-bs/
# ─────────────────────────────────────────────────────────────────────────────
AERO_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "AERO1121", "course_number": "AERO 1121", "title": "Aerospace Fundamentals",              "units": 2, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AERO 121"], "is_placeholder": False},
    {"id": "IME1143",  "course_number": "IME 1143",  "title": "Introduction to Design & Manufacturing","units":3, "category": "support", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["IME 144"], "is_placeholder": False},
    {"id": "MATH1261", "course_number": "MATH 1261", "title": "Calculus I",                          "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "PHYS1141", "course_number": "PHYS 1141", "title": "General Physics I",                   "units": 4, "category": "support", "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["PHYS 141"], "is_placeholder": False},
    {"id": "GE1A",     "course_number": "GE 1A",     "title": "Written Communication",               "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "CHEM1120", "course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure",  "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["CHEM 124"], "is_placeholder": False},
    {"id": "MATH1262", "course_number": "MATH 1262", "title": "Calculus II",                         "units": 4, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "PHYS1143", "course_number": "PHYS 1143", "title": "General Physics II",                  "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["PHYS 132"], "is_placeholder": False},
    {"id": "GE1B",     "course_number": "GE 1B",     "title": "Critical Thinking",                   "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE3A",     "course_number": "GE 3A",     "title": "Arts",                                "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "ENGR2211", "course_number": "ENGR 2211", "title": "Introduction to Mechanics",           "units": 4, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["ME 211"], "is_placeholder": False},
    {"id": "MATE1220", "course_number": "MATE 1220", "title": "Principles of Materials Engineering", "units": 2, "category": "support", "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MATE 210"], "is_placeholder": False},
    {"id": "MATH2263", "course_number": "MATH 2263", "title": "Calculus III",                        "units": 3, "category": "support", "grid_col": 2, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 143"], "is_placeholder": False},
    {"id": "GE1C",     "course_number": "GE 1C",     "title": "Oral Communication",                  "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "GE6",      "course_number": "GE 6",      "title": "Ethnic Studies",                      "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "AERO2220", "course_number": "AERO 2220", "title": "Aerospace Engineering Dynamics",      "units": 3, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["ENGR 2211"], "quarter_equivalents": ["AERO 215", "ME 212"], "is_placeholder": False},
    {"id": "MATH2341", "course_number": "MATH 2341", "title": "Linear Analysis",                     "units": 4, "category": "support", "grid_col": 3, "grid_row": 1, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 244"], "is_placeholder": False},
    {"id": "GE3B",     "course_number": "GE 3B",     "title": "Humanities",                          "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE4A",     "course_number": "GE 4A",     "title": "American Institutions",               "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE4B",     "course_number": "GE 4B",     "title": "Social & Behavioral Sciences",        "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AERO3300", "course_number": "AERO 3300", "title": "Engineering Numerical Analysis",      "units": 4, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": ["MATH 2341"], "quarter_equivalents": ["AERO 300"], "is_placeholder": False},
    {"id": "AERO3301", "course_number": "AERO 3301", "title": "Thermo Fluid Dynamics",               "units": 4, "category": "major",   "grid_col": 4, "grid_row": 1, "prerequisites": ["AERO 2220", "MATH 2341"], "quarter_equivalents": ["AERO 302", "AERO 299"], "is_placeholder": False},
    {"id": "AERO3302", "course_number": "AERO 3302", "title": "Thermo Fluids Laboratory",            "units": 1, "category": "major",   "grid_col": 4, "grid_row": 2, "prerequisites": ["AERO 3301"], "quarter_equivalents": ["AERO 321"], "is_placeholder": False},
    {"id": "AERO3331", "course_number": "AERO 3331", "title": "Aerospace Structural Analysis I",     "units": 4, "category": "major",   "grid_col": 4, "grid_row": 3, "prerequisites": ["ENGR 2211"], "quarter_equivalents": ["AERO 331"], "is_placeholder": False},
    {"id": "AERO3460", "course_number": "AERO 3460", "title": "Aerospace Professional Preparation",  "units": 1, "category": "major",   "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["AERO 460", "AERO 350"], "is_placeholder": False},
    {"id": "GE5B",     "course_number": "GE 5B",     "title": "Life Sciences",                       "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AERO3303", "course_number": "AERO 3303", "title": "Heat and Mass Transfer",              "units": 2, "category": "major",   "grid_col": 5, "grid_row": 0, "prerequisites": ["AERO 3301"], "quarter_equivalents": ["AERO 303"], "is_placeholder": False},
    {"id": "AERO3304", "course_number": "AERO 3304", "title": "Aerospace Propulsion Systems",        "units": 3, "category": "major",   "grid_col": 5, "grid_row": 1, "prerequisites": ["AERO 3301"], "quarter_equivalents": ["AERO 303"], "is_placeholder": False},
    {"id": "AERO3320", "course_number": "AERO 3320", "title": "System Dynamics",                     "units": 3, "category": "major",   "grid_col": 5, "grid_row": 2, "prerequisites": ["AERO 2220", "MATH 2341"], "quarter_equivalents": ["AERO 320"], "is_placeholder": False},
    {"id": "AERO4431", "course_number": "AERO 4431", "title": "Aerospace Structural Analysis II",    "units": 3, "category": "major",   "grid_col": 5, "grid_row": 3, "prerequisites": ["AERO 3331"], "quarter_equivalents": ["AERO 431"], "is_placeholder": False},
    {"id": "AERO4433", "course_number": "AERO 4433", "title": "Experimental Stress Analysis",        "units": 1, "category": "major",   "grid_col": 5, "grid_row": 4, "prerequisites": ["AERO 3331"], "quarter_equivalents": ["AERO 433"], "is_placeholder": False},
    {"id": "CON_JRS1", "course_number": "Conc.",     "title": "Concentration Elective",              "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AERO4403", "course_number": "AERO 4403", "title": "Propulsion Laboratory",               "units": 1, "category": "major",   "grid_col": 6, "grid_row": 0, "prerequisites": ["AERO 3304"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CON_SRF1", "course_number": "Conc.",     "title": "Concentration Course",                "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRF2", "course_number": "Conc.",     "title": "Concentration Course",                "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRF3", "course_number": "Conc.",     "title": "Concentration Course",                "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRF4", "course_number": "Conc.",     "title": "Concentration Course",                "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRF5", "course_number": "Conc.",     "title": "Concentration Course",                "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CON_SRS1", "course_number": "Conc.",     "title": "Concentration Course",                "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRS2", "course_number": "TE",        "title": "Concentration Tech Elective",         "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CON_SRS3", "course_number": "TE",        "title": "Concentration Tech Elective",         "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE_UD3",   "course_number": "GE UD-3",  "title": "Upper-Div Arts & Humanities",         "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE_UD4",   "course_number": "GE UD-4",  "title": "Upper-Div Social Sciences",           "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# SOFTWARE ENGINEERING — General Curriculum (120 units)
# Source: catalog.calpoly.edu/engineering/computer-science-software/software-engineering-bs/
# ─────────────────────────────────────────────────────────────────────────────
SE_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "SE_CSC1000",  "course_number": "CSC 1000",  "title": "Computing Majors Orientation",             "units": 1, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "SE_CSC1024",  "course_number": "CSC 1024",  "title": "Introduction to Computing",                "units": 2, "category": "major",   "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["CSC 101"], "is_placeholder": False},
    {"id": "SE_MATH1261", "course_number": "MATH 1261", "title": "Calculus I",                               "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "SE_GLSC",     "course_number": "GE 5B",     "title": "Life Science Elective",                    "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "SE_GE1A",     "course_number": "GE 1A",     "title": "Written Communication",                    "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "SE_CSC1001",  "course_number": "CSC 1001",  "title": "Fundamentals of Computer Science",         "units": 4, "category": "major",   "grid_col": 1, "grid_row": 0, "prerequisites": ["CSC 1024"], "quarter_equivalents": ["CSC 101"], "is_placeholder": False},
    {"id": "SE_MATH1262", "course_number": "MATH 1262", "title": "Calculus II",                              "units": 4, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "SE_PHYS1141", "course_number": "PHYS 1141", "title": "General Physics I",                        "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["PHYS 141"], "is_placeholder": False},
    {"id": "SE_GE1B",     "course_number": "GE 1B",     "title": "Critical Thinking",                        "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "SE_CSC2001",  "course_number": "CSC 2001",  "title": "Data Structures",                          "units": 4, "category": "major",   "grid_col": 2, "grid_row": 0, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CSC 202"], "is_placeholder": False},
    {"id": "SE_MATH2031", "course_number": "MATH 2031", "title": "Transition to Advanced Mathematics",       "units": 3, "category": "support", "grid_col": 2, "grid_row": 1, "prerequisites": ["MATH 1262"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "SE_STAT3210", "course_number": "STAT 3210", "title": "Engineering Statistics",                   "units": 3, "category": "support", "grid_col": 2, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["STAT 312"], "is_placeholder": False},
    {"id": "SE_GE1C",     "course_number": "GE 1C",     "title": "Oral Communication",                       "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "SE_GE3A",     "course_number": "GE 3A",     "title": "Arts",                                     "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "SE_CSC2050",  "course_number": "CSC 2050",  "title": "System Software Mechanics",                "units": 3, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CSC 357", "CSC 203"], "is_placeholder": False},
    {"id": "SE_CSC3001",  "course_number": "CSC 3001",  "title": "Modern Application Development",           "units": 4, "category": "major",   "grid_col": 3, "grid_row": 1, "prerequisites": ["CSC 2001"], "quarter_equivalents": ["CSC 203"], "is_placeholder": False},
    {"id": "SE_CSC3100",  "course_number": "CSC 3100",  "title": "Software Engineering",                     "units": 4, "category": "major",   "grid_col": 3, "grid_row": 2, "prerequisites": ["CSC 2001"], "quarter_equivalents": ["CSC 307"], "is_placeholder": False},
    {"id": "SE_GE3B",     "course_number": "GE 3B",     "title": "Humanities",                               "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "SE_GE4A",     "course_number": "GE 4A",     "title": "American Institutions",                    "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "SE_CSC3201",  "course_number": "CSC 3201",  "title": "Introduction to Computer Security",        "units": 3, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": ["CSC 2001"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "SE_CSC3449",  "course_number": "CSC 3449",  "title": "Algorithms and Complexity",                "units": 4, "category": "major",   "grid_col": 4, "grid_row": 1, "prerequisites": ["CSC 2001", "MATH 2031"], "quarter_equivalents": ["CSC 349"], "is_placeholder": False},
    {"id": "SE_CSC3660",  "course_number": "CSC 3660",  "title": "Database Modeling, Design and Implementation", "units": 4, "category": "major", "grid_col": 4, "grid_row": 2, "prerequisites": ["CSC 2001"], "quarter_equivalents": ["CSC 365"], "is_placeholder": False},
    {"id": "SE_GE4B",     "course_number": "GE 4B",     "title": "Social & Behavioral Sciences",             "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "SE_GE6",      "course_number": "GE 6",      "title": "Ethnic Studies",                           "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "SE_CSC3300",  "course_number": "CSC 3300",  "title": "Programming Languages",                    "units": 3, "category": "major",   "grid_col": 5, "grid_row": 0, "prerequisites": ["CSC 2001"], "quarter_equivalents": ["CSC 430"], "is_placeholder": False},
    {"id": "SE_CSC3665",  "course_number": "CSC 3665",  "title": "Database Applications",                    "units": 3, "category": "major",   "grid_col": 5, "grid_row": 1, "prerequisites": ["CSC 3660"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "SE_COMS2217", "course_number": "COMS 2217", "title": "Small Group Collaboration and Creativity",  "units": 3, "category": "support", "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "SE_CON_JRS1", "course_number": "Conc.",     "title": "Technical Elective",                       "units": 4, "category": "concentration", "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "SE_GE_UD4",   "course_number": "GE UD-4",  "title": "Upper-Div Social Sciences",                 "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "SE_CSC4160",  "course_number": "CSC 4160",  "title": "Software Requirements Engineering",        "units": 4, "category": "major",   "grid_col": 6, "grid_row": 0, "prerequisites": ["CSC 3100"], "quarter_equivalents": ["CSC 308"], "is_placeholder": False},
    {"id": "SE_PSY2201",  "course_number": "PSY 2201",  "title": "Introductory Psychology",                  "units": 3, "category": "support", "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["PSY 201"], "is_placeholder": False},
    {"id": "SE_WGQS3350", "course_number": "WGQS 3350", "title": "Gender, Race, Culture, Science & Technology", "units": 4, "category": "support", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "SE_CON_SRF1", "course_number": "Conc.",     "title": "Technical Elective",                       "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "SE_CSC4161",  "course_number": "CSC 4161",  "title": "Software Deployment and Operations",        "units": 4, "category": "major",   "grid_col": 7, "grid_row": 0, "prerequisites": ["CSC 4160"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "SE_CON_SRS1", "course_number": "Conc.",     "title": "Technical Elective",                       "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "SE_CON_SRS2", "course_number": "Conc.",     "title": "Technical Elective",                       "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "SE_GE_UD3",   "course_number": "GE UD-3",  "title": "Upper-Div Arts & Humanities",               "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# COMPUTER ENGINEERING — General Curriculum (125-128 units)
# Source: catalog.calpoly.edu/engineering/electrical-engineering/computer-engineering-bs/
# ─────────────────────────────────────────────────────────────────────────────
CPE_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "CPE1000",  "course_number": "CPE 1000",  "title": "Computing Majors Orientation",         "units": 1, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CPE1024",  "course_number": "CPE 1024",  "title": "Introduction to Computing",            "units": 2, "category": "major",   "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["CPE 101", "CSC 101"], "is_placeholder": False},
    {"id": "CPE_MATH1261", "course_number": "MATH 1261", "title": "Calculus I",                        "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "CPE_PHYS1141", "course_number": "PHYS 1141", "title": "General Physics I",                 "units": 4, "category": "support", "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["PHYS 141"], "is_placeholder": False},
    {"id": "CPE_GE1A", "course_number": "GE 1A",     "title": "Written Communication",                "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "CPE_CSC1001", "course_number": "CSC 1001",  "title": "Fundamentals of Computer Science",  "units": 4, "category": "major",   "grid_col": 1, "grid_row": 0, "prerequisites": ["CPE 1024"], "quarter_equivalents": ["CPE 101", "CSC 101"], "is_placeholder": False},
    {"id": "CPE_MATH1262", "course_number": "MATH 1262", "title": "Calculus II",                       "units": 4, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "CPE_PHYS1143", "course_number": "PHYS 1143", "title": "General Physics II",                "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["PHYS 132"], "is_placeholder": False},
    {"id": "CPE_GE1B", "course_number": "GE 1B",     "title": "Critical Thinking",                    "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "CPE_CSC2001", "course_number": "CSC 2001",  "title": "Data Structures",                   "units": 4, "category": "major",   "grid_col": 2, "grid_row": 0, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CSC 202"], "is_placeholder": False},
    {"id": "CPE2300",  "course_number": "CPE 2300",  "title": "Introduction to Computer Systems",     "units": 3, "category": "major",   "grid_col": 2, "grid_row": 1, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CPE 225"], "is_placeholder": False},
    {"id": "CPE_MATH2031", "course_number": "MATH 2031", "title": "Transition to Advanced Mathematics", "units": 3, "category": "support", "grid_col": 2, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CPE_GE1C", "course_number": "GE 1C",     "title": "Oral Communication",                   "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "CPE_GE3A", "course_number": "GE 3A",     "title": "Arts",                                 "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "CPE2050",  "course_number": "CPE 2050",  "title": "System Software Mechanics",            "units": 3, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["CSC 1001"], "quarter_equivalents": ["CPE 357"], "is_placeholder": False},
    {"id": "CPE2301",  "course_number": "CPE 2301",  "title": "Computer Design and Assembly Language Programming", "units": 3, "category": "major", "grid_col": 3, "grid_row": 1, "prerequisites": ["CPE 2300"], "quarter_equivalents": ["CPE 233"], "is_placeholder": False},
    {"id": "CPE_EE2211", "course_number": "EE 2211", "title": "Circuits I",                           "units": 3, "category": "support", "grid_col": 3, "grid_row": 2, "prerequisites": ["PHYS 1141", "MATH 1262"], "quarter_equivalents": ["EE 211"], "is_placeholder": False},
    {"id": "CPE_MATH1151", "course_number": "MATH 1151", "title": "Linear Algebra",                    "units": 3, "category": "support", "grid_col": 3, "grid_row": 3, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 244"], "is_placeholder": False},
    {"id": "CPE_GE3B", "course_number": "GE 3B",     "title": "Humanities",                           "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "CPE3201",  "course_number": "CPE 3201",  "title": "Introduction to Computer Security",    "units": 3, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": ["CSC 2001", "CPE 2300"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CPE3300",  "course_number": "CPE 3300",  "title": "Introduction to Computer Architecture", "units": 4, "category": "major",  "grid_col": 4, "grid_row": 1, "prerequisites": ["CPE 2301"], "quarter_equivalents": ["CPE 333"], "is_placeholder": False},
    {"id": "CPE4553",  "course_number": "CPE 4553",  "title": "Introduction to Operating Systems",   "units": 3, "category": "major",   "grid_col": 4, "grid_row": 2, "prerequisites": ["CPE 2050"], "quarter_equivalents": ["CPE 453"], "is_placeholder": False},
    {"id": "CPE_PHIL3323", "course_number": "PHIL 3323", "title": "Ethics, Science, and Technology",  "units": 3, "category": "support", "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "CPE_GE4B", "course_number": "GE 4B",     "title": "Social & Behavioral Sciences",         "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CPE3160",  "course_number": "CPE 3160",  "title": "Microcontrollers and Embedded Applications", "units": 4, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["CPE 2301"], "quarter_equivalents": ["CPE 316"], "is_placeholder": False},
    {"id": "CPE4464",  "course_number": "CPE 4464",  "title": "Introduction to Computer Networks",  "units": 3, "category": "major",   "grid_col": 5, "grid_row": 1, "prerequisites": ["CPE 3300"], "quarter_equivalents": ["CPE 464"], "is_placeholder": False},
    {"id": "CPE_STAT3210", "course_number": "STAT 3210", "title": "Engineering Statistics",          "units": 3, "category": "support", "grid_col": 5, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["STAT 312"], "is_placeholder": False},
    {"id": "CPE_GE4A", "course_number": "GE 4A",     "title": "American Institutions",                "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CPE_GE6",  "course_number": "GE 6",      "title": "Ethnic Studies",                       "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "CPE3500",  "course_number": "CPE 3500",  "title": "Digital Design Using Hardware Description Languages", "units": 4, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["CPE 3160"], "quarter_equivalents": ["CPE 350"], "is_placeholder": False},
    {"id": "CPE3520",  "course_number": "CPE 3520",  "title": "Digital System Design and Implementation", "units": 4, "category": "major", "grid_col": 6, "grid_row": 1, "prerequisites": ["CPE 3500"], "quarter_equivalents": ["CPE 329"], "is_placeholder": False},
    {"id": "CPE_CON_SRF1", "course_number": "TE",    "title": "Technical Elective",                   "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CPE_CON_SRF2", "course_number": "TE",    "title": "Technical Elective",                   "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CPE4610",  "course_number": "CPE 4610",  "title": "Computer Engineering Senior Project", "units": 4, "category": "major",   "grid_col": 7, "grid_row": 0, "prerequisites": ["CPE 3520"], "quarter_equivalents": ["CPE 461", "CPE 462"], "is_placeholder": False},
    {"id": "CPE_CON_SRS1", "course_number": "TE",    "title": "Technical Elective",                   "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CPE_CON_SRS2", "course_number": "TE",    "title": "Technical Elective",                   "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CPE_GE_UD3", "course_number": "GE UD-3", "title": "Upper-Div Arts & Humanities",          "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# CIVIL ENGINEERING — General Curriculum (132 units)
# Source: catalog.calpoly.edu/engineering/civil-environmental/civil-engineering-bs/
# ─────────────────────────────────────────────────────────────────────────────
CE_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "CE1111",     "course_number": "CE 1111",    "title": "Introduction to Civil Engineering",                 "units": 1, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["CE 111"], "is_placeholder": False},
    {"id": "CE_CHEM1120","course_number": "CHEM 1120",  "title": "Fundamentals of Chemical Structure and Properties", "units": 4, "category": "support", "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["CHEM 124"], "is_placeholder": False},
    {"id": "CE_MATH1261","course_number": "MATH 1261",  "title": "Calculus I",                                        "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "CE_PHYS1141","course_number": "PHYS 1141",  "title": "General Physics I",                                 "units": 4, "category": "support", "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["PHYS 141"], "is_placeholder": False},
    {"id": "CE_GE1A",    "course_number": "GE 1A",      "title": "Written Communication",                            "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "CE1112",     "course_number": "CE 1112",    "title": "Spatial Visualization and Drawing",                 "units": 3, "category": "major",   "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["CE 112", "ENVE 1112"], "is_placeholder": False},
    {"id": "CE_MATH1262","course_number": "MATH 1262",  "title": "Calculus II",                                       "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "CE_PHYS1143","course_number": "PHYS 1143",  "title": "General Physics II",                                "units": 4, "category": "support", "grid_col": 1, "grid_row": 3, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["PHYS 132"], "is_placeholder": False},
    {"id": "CE_GE1B",    "course_number": "GE 1B",      "title": "Critical Thinking",                                "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_GE1C",    "course_number": "GE 1C",      "title": "Oral Communication",                               "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "CE2251",     "course_number": "CE 2251",    "title": "Computational Applications in Civil and Environmental Engineering", "units": 2, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["CE 251"], "is_placeholder": False},
    {"id": "CE_ENGR2211","course_number": "ENGR 2211",  "title": "Introduction to Mechanics",                        "units": 4, "category": "support", "grid_col": 2, "grid_row": 3, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["ME 211"], "is_placeholder": False},
    {"id": "CE_MATH2263","course_number": "MATH 2263",  "title": "Calculus III",                                      "units": 3, "category": "support", "grid_col": 2, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 143"], "is_placeholder": False},
    {"id": "CE_GE3A",    "course_number": "GE 3A",      "title": "Arts",                                              "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_GE3B",    "course_number": "GE 3B",      "title": "Humanities",                                        "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "CE2259",     "course_number": "CE 2259",    "title": "Civil Engineering Materials",                       "units": 3, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["CHEM 1120"], "quarter_equivalents": ["CE 259"], "is_placeholder": False},
    {"id": "CE_ENGR2212","course_number": "ENGR 2212",  "title": "Introduction to Engineering Dynamics",              "units": 2, "category": "support", "grid_col": 3, "grid_row": 3, "prerequisites": ["ENGR 2211"], "quarter_equivalents": ["ME 212"], "is_placeholder": False},
    {"id": "CE_GEOL2240","course_number": "GEOL 2240",  "title": "Physical Geology",                                  "units": 3, "category": "support", "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["GEOL 201"], "is_placeholder": False},
    {"id": "CE_MATH2341","course_number": "MATH 2341",  "title": "Linear Analysis",                                   "units": 4, "category": "support", "grid_col": 3, "grid_row": 2, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 244"], "is_placeholder": False},
    {"id": "CE_GE4A",    "course_number": "GE 4A",      "title": "American Institutions",                             "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "CE3321",     "course_number": "CE 3321",    "title": "Fundamentals of Transportation Engineering",         "units": 4, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": ["CE 2251"], "quarter_equivalents": ["CE 321"], "is_placeholder": False},
    {"id": "CE3336",     "course_number": "CE 3336",    "title": "Environmental Fluid Mechanics and Hydraulic Systems","units": 4, "category": "major",   "grid_col": 4, "grid_row": 1, "prerequisites": ["ENGR 2212", "MATH 2341"], "quarter_equivalents": ["CE 336", "ENVE 3336"], "is_placeholder": False},
    {"id": "CE3352",     "course_number": "CE 3352",    "title": "Structural Analysis",                               "units": 4, "category": "major",   "grid_col": 4, "grid_row": 2, "prerequisites": ["ENGR 2211"], "quarter_equivalents": ["CE 352"], "is_placeholder": False},
    {"id": "CE_STAT3210","course_number": "STAT 3210",  "title": "Engineering Statistics",                            "units": 3, "category": "support", "grid_col": 4, "grid_row": 3, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["STAT 312"], "is_placeholder": False},
    {"id": "CE_GE4B",    "course_number": "GE 4B",      "title": "Social & Behavioral Sciences",                      "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CE3337",     "course_number": "CE 3337",    "title": "Water Resources & Environmental Engineering",        "units": 4, "category": "major",   "grid_col": 5, "grid_row": 0, "prerequisites": ["CE 3336"], "quarter_equivalents": ["CE 337", "ENVE 3337"], "is_placeholder": False},
    {"id": "CE3355",     "course_number": "CE 3355",    "title": "Reinforced Concrete Design",                        "units": 3, "category": "major",   "grid_col": 5, "grid_row": 1, "prerequisites": ["CE 3352"], "quarter_equivalents": ["CE 355"], "is_placeholder": False},
    {"id": "CE3381",     "course_number": "CE 3381",    "title": "Geotechnical Engineering",                          "units": 4, "category": "major",   "grid_col": 5, "grid_row": 2, "prerequisites": ["CE 2259", "ENGR 2211"], "quarter_equivalents": ["CE 381"], "is_placeholder": False},
    {"id": "CE3465",     "course_number": "CE 3465",    "title": "Infrastructure Systems",                            "units": 2, "category": "major",   "grid_col": 5, "grid_row": 3, "prerequisites": ["CE 2251"], "quarter_equivalents": ["CE 465", "ENVE 3465"], "is_placeholder": False},
    {"id": "CE_GE5B",    "course_number": "GE 5B",      "title": "Life Sciences",                                      "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "CE3375",     "course_number": "CE 3375",    "title": "Fundamentals of Construction Engineering and Management", "units": 4, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["CE 2259"], "quarter_equivalents": ["CE 375"], "is_placeholder": False},
    {"id": "CE4466",     "course_number": "CE 4466",    "title": "Senior Design Project I",                            "units": 1, "category": "major",   "grid_col": 6, "grid_row": 1, "prerequisites": ["CE 3337", "CE 3355", "CE 3381"], "quarter_equivalents": ["CE 466"], "is_placeholder": False},
    {"id": "CE_TE_SRF1", "course_number": "CE TE 1",    "title": "Technical Elective",                                 "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_TE_SRF2", "course_number": "CE TE 2",    "title": "Technical Elective",                                 "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_TE_SRF3", "course_number": "CE TE 3",    "title": "Technical Elective",                                 "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_GE6",     "course_number": "GE 6",       "title": "Ethnic Studies",                                     "units": 3, "category": "ge",      "grid_col": 6, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CE4467",     "course_number": "CE 4467",    "title": "Senior Design Project II",                           "units": 3, "category": "major",   "grid_col": 7, "grid_row": 0, "prerequisites": ["CE 4466"], "quarter_equivalents": ["CE 467"], "is_placeholder": False},
    {"id": "CE_TE_SRS1", "course_number": "CE TE 4",    "title": "Technical Elective",                                 "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_TE_SRS2", "course_number": "CE TE 5",    "title": "Technical Elective",                                 "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_TE_SRS3", "course_number": "CE TE 6",    "title": "Technical Elective",                                 "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_GE_UD3",  "course_number": "GE UD-3",    "title": "Upper-Division Arts and Humanities",                  "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CE_GE_UD4",  "course_number": "GE UD-4",    "title": "Upper-Division Social Sciences",                     "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# MECHANICAL ENGINEERING — General Curriculum (128-129 units)
# Source: catalog.calpoly.edu/engineering/mechanical/mechanical-engineering-bs/
# ─────────────────────────────────────────────────────────────────────────────
ME_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "ME1125",      "course_number": "ME 1125",    "title": "Introduction to Mechanical Engineering",           "units": 1, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ME 128"], "is_placeholder": False},
    {"id": "ME1148",      "course_number": "ME 1148",    "title": "Engineering Design Communication",                 "units": 2, "category": "major",   "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ME 129"], "is_placeholder": False},
    {"id": "ME_CHEM1120", "course_number": "CHEM 1120",  "title": "Fundamentals of Chemical Structure and Properties", "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["CHEM 124"], "is_placeholder": False},
    {"id": "ME_IME1143",  "course_number": "IME 1143",   "title": "Introduction to Design and Manufacturing",          "units": 2, "category": "support", "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["IME 144"], "is_placeholder": False},
    {"id": "ME_MATH1261", "course_number": "MATH 1261",  "title": "Calculus I",                                        "units": 4, "category": "support", "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "ME_GE1A",     "course_number": "GE 1A",      "title": "Written Communication",                            "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "ME_IME114X",  "course_number": "IME 1141/1142/1149", "title": "Manufacturing Process Selective",          "units": 1, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["IME 141", "IME 142"], "is_placeholder": True},
    {"id": "ME_MATH1262", "course_number": "MATH 1262",  "title": "Calculus II",                                       "units": 4, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "ME_PHYS1141", "course_number": "PHYS 1141",  "title": "General Physics I",                                 "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["PHYS 141"], "is_placeholder": False},
    {"id": "ME_GE1B",     "course_number": "GE 1B",      "title": "Critical Thinking",                                 "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ME_GE1C",     "course_number": "GE 1C",      "title": "Oral Communication",                                "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "ME2240",      "course_number": "ME 2240",    "title": "Applied Programming for Mechanical Engineering",    "units": 1, "category": "major",   "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ME 228"], "is_placeholder": False},
    {"id": "ME2248",      "course_number": "ME 2248",    "title": "Design Using Solid Modeling",                       "units": 1, "category": "major",   "grid_col": 2, "grid_row": 1, "prerequisites": ["ME 1148"], "quarter_equivalents": ["ME 130"], "is_placeholder": False},
    {"id": "ME_ENGR2211", "course_number": "ENGR 2211",  "title": "Introduction to Mechanics",                         "units": 4, "category": "support", "grid_col": 2, "grid_row": 2, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["ME 211"], "is_placeholder": False},
    {"id": "ME_MATH2263", "course_number": "MATH 2263",  "title": "Calculus III",                                       "units": 3, "category": "support", "grid_col": 2, "grid_row": 3, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 143"], "is_placeholder": False},
    {"id": "ME_PHYS1143", "course_number": "PHYS 1143",  "title": "General Physics II",                                 "units": 4, "category": "support", "grid_col": 2, "grid_row": 4, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["PHYS 132"], "is_placeholder": False},
    {"id": "ME_GE3A",     "course_number": "GE 3A",      "title": "Arts",                                               "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "ME2212",      "course_number": "ME 2212",    "title": "Engineering Dynamics",                              "units": 3, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["ENGR 2211"], "quarter_equivalents": ["ME 212"], "is_placeholder": False},
    {"id": "ME_EE2115",   "course_number": "EE 2115",    "title": "Circuits and Electronics for Non-Majors",           "units": 4, "category": "support", "grid_col": 3, "grid_row": 1, "prerequisites": ["PHYS 1143"], "quarter_equivalents": ["EE 201"], "is_placeholder": False},
    {"id": "ME_MATE1220", "course_number": "MATE 1220",  "title": "Principles of Materials Engineering for Non-Majors", "units": 3, "category": "support", "grid_col": 3, "grid_row": 2, "prerequisites": ["CHEM 1120"], "quarter_equivalents": ["MATE 210"], "is_placeholder": False},
    {"id": "ME_MATH2341", "course_number": "MATH 2341",  "title": "Linear Analysis",                                    "units": 4, "category": "support", "grid_col": 3, "grid_row": 3, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 244"], "is_placeholder": False},
    {"id": "ME_GE4A",     "course_number": "GE 4A",      "title": "American Institutions",                              "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ME3234",      "course_number": "ME 3234",    "title": "Design Thinking and Creativity",                    "units": 3, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": ["ME 1125"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ME3236",      "course_number": "ME 3236",    "title": "Engineering Measurement and Data Analysis",         "units": 3, "category": "major",   "grid_col": 4, "grid_row": 1, "prerequisites": ["ME 2240"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ME3302",      "course_number": "ME 3302",    "title": "Thermodynamics",                                    "units": 3, "category": "major",   "grid_col": 4, "grid_row": 2, "prerequisites": ["MATH 1262", "PHYS 1143"], "quarter_equivalents": ["ME 302"], "is_placeholder": False},
    {"id": "ME3328",      "course_number": "ME 3328",    "title": "Design for Strength and Stiffness",                 "units": 4, "category": "major",   "grid_col": 4, "grid_row": 3, "prerequisites": ["ENGR 2211"], "quarter_equivalents": ["ME 328"], "is_placeholder": False},
    {"id": "ME_GE3B",     "course_number": "GE 3B",      "title": "Humanities",                                        "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ME3317",      "course_number": "ME 3317",    "title": "Vibrations and System Modeling",                    "units": 4, "category": "major",   "grid_col": 5, "grid_row": 0, "prerequisites": ["ME 2212", "MATH 2341"], "quarter_equivalents": ["ME 317"], "is_placeholder": False},
    {"id": "ME3329",      "course_number": "ME 3329",    "title": "Mechanical Systems Design",                        "units": 3, "category": "major",   "grid_col": 5, "grid_row": 1, "prerequisites": ["ME 3328"], "quarter_equivalents": ["ME 329"], "is_placeholder": False},
    {"id": "ME3341",      "course_number": "ME 3341",    "title": "Fluid Mechanics",                                  "units": 4, "category": "major",   "grid_col": 5, "grid_row": 2, "prerequisites": ["ME 2212", "MATH 2341"], "quarter_equivalents": ["ME 341", "ME 342"], "is_placeholder": False},
    {"id": "ME_GE5B",     "course_number": "GE 5B",      "title": "Life Sciences",                                     "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "ME_GE4B",     "course_number": "GE 4B",      "title": "Social and Behavioral Sciences",                    "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ME3343",      "course_number": "ME 3343",    "title": "Heat Transfer",                                    "units": 4, "category": "major",   "grid_col": 6, "grid_row": 0, "prerequisites": ["ME 3341"], "quarter_equivalents": ["ME 343"], "is_placeholder": False},
    {"id": "ME4417",      "course_number": "ME 4417",    "title": "Mechanical Controls and Implementations",          "units": 3, "category": "major",   "grid_col": 6, "grid_row": 1, "prerequisites": ["ME 3317"], "quarter_equivalents": ["ME 417"], "is_placeholder": False},
    {"id": "ME4460",      "course_number": "ME 4460",    "title": "Senior Design Project I",                          "units": 2, "category": "major",   "grid_col": 6, "grid_row": 2, "prerequisites": ["ME 3234", "ME 3329", "ME 3343"], "quarter_equivalents": ["ME 428", "ME 429"], "is_placeholder": False},
    {"id": "ME_TE_SRF1",  "course_number": "ME TE 1",    "title": "Technical Elective",                               "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ME_TE_SRF2",  "course_number": "ME TE 2",    "title": "Technical Elective",                               "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ME_GE6",      "course_number": "GE 6",       "title": "Ethnic Studies",                                   "units": 3, "category": "ge",      "grid_col": 6, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ME4440",      "course_number": "ME 4440",    "title": "Thermal System Design",                            "units": 3, "category": "major",   "grid_col": 7, "grid_row": 0, "prerequisites": ["ME 3343"], "quarter_equivalents": ["ME 440"], "is_placeholder": False},
    {"id": "ME4461",      "course_number": "ME 4461",    "title": "Senior Design Project II",                         "units": 2, "category": "major",   "grid_col": 7, "grid_row": 1, "prerequisites": ["ME 4460"], "quarter_equivalents": ["ME 430"], "is_placeholder": False},
    {"id": "ME_TE_SRS1",  "course_number": "ME TE 3",    "title": "Technical Elective",                               "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ME_TE_SRS2",  "course_number": "ME TE 4",    "title": "Technical Elective",                               "units": 2, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ME_GE_UD3",   "course_number": "GE UD-3",    "title": "Upper-Division Arts and Humanities",                "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# ART AND DESIGN (BFA) — Concentration Not Yet Declared (120 units)
# Source: catalog.calpoly.edu/liberal-arts/art-design/art-design-bfa/
# ─────────────────────────────────────────────────────────────────────────────
AD_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "AD_ART1101", "course_number": "ART 1101", "title": "Fundamentals of Drawing",                   "units": 3, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ART 101"], "is_placeholder": False},
    {"id": "AD_ART1102", "course_number": "ART 1102", "title": "2D Design",                                 "units": 3, "category": "major", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ART 102"], "is_placeholder": False},
    {"id": "AD_GE1A",    "course_number": "GE 1A",   "title": "Written Communication",                     "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "AD_GE1C",    "course_number": "GE 1C",   "title": "Oral Communication",                        "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "AD_GE2",     "course_number": "GE 2",    "title": "Mathematics and Quantitative Reasoning",     "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "AD_ART1103", "course_number": "ART 1103", "title": "3D Design",                                 "units": 3, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ART 104"], "is_placeholder": False},
    {"id": "AD_ART1141", "course_number": "ART 1141", "title": "Design Thinking and Methods",               "units": 3, "category": "major", "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ART 183"], "is_placeholder": False},
    {"id": "AD_ART2260", "course_number": "ART 2260", "title": "Camera and Light",                          "units": 3, "category": "major", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ART 224"], "is_placeholder": False},
    {"id": "AD_GE1B",    "course_number": "GE 1B",   "title": "Critical Thinking",                         "units": 3, "category": "ge",    "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_GE5A",    "course_number": "GE 5A",   "title": "Physical Sciences",                         "units": 3, "category": "ge",    "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "AD_ART1104", "course_number": "ART 1104", "title": "4D Design",                                 "units": 3, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "AD_ART1184_2282", "course_number": "ART 1184/2282", "title": "Beginning Sculpture or Painting", "units": 3, "category": "major", "grid_col": 2, "grid_row": 1, "prerequisites": ["ART 1101"], "quarter_equivalents": ["ART 1184", "ART 2282", "ART 148", "ART 209"], "is_placeholder": True},
    {"id": "AD_ART2201", "course_number": "ART 2201", "title": "Visual Culture and Society",                "units": 3, "category": "major", "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ART 222"], "is_placeholder": False},
    {"id": "AD_ART2215", "course_number": "ART 2215", "title": "Global Contemporary Art",                   "units": 3, "category": "major", "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ART 213"], "is_placeholder": False},
    {"id": "AD_GE3B",    "course_number": "GE 3B",   "title": "Humanities",                                "units": 3, "category": "ge",    "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "AD_ART2212", "course_number": "ART 2212", "title": "Renaissance to Modern Art",                 "units": 3, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ART 212"], "is_placeholder": False},
    {"id": "AD_PORTFOLIO", "course_number": "ART 3359/3379/3399", "title": "Portfolio Review",             "units": 3, "category": "major", "grid_col": 3, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ART 260", "ART 3359", "ART 3379", "ART 3399"], "is_placeholder": True},
    {"id": "AD_GE4A",    "course_number": "GE 4A",   "title": "American Institutions",                    "units": 3, "category": "ge",    "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_GE5B",    "course_number": "GE 5B",   "title": "Life Sciences",                            "units": 3, "category": "ge",    "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "AD_GE6",     "course_number": "GE 6",    "title": "Ethnic Studies",                           "units": 3, "category": "ge",    "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AD_CON_JRF1", "course_number": "Conc.",  "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_JRF2", "course_number": "Conc.",  "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_JRF3", "course_number": "Conc.",  "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_GE_UD25",  "course_number": "GE UD-2/5", "title": "Upper-Div Math/Science",                 "units": 3, "category": "ge", "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_GE5C",     "course_number": "GE 5C",  "title": "Laboratory",                               "units": 1, "category": "ge", "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AD_CON_JRS1", "course_number": "Conc.",  "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_JRS2", "course_number": "Conc.",  "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_JRS3", "course_number": "Conc.",  "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_JRS4", "course_number": "Conc.",  "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_GE_UD4",   "course_number": "GE UD-4", "title": "Upper-Div Social Sciences",               "units": 3, "category": "ge", "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AD_ART_HIST_UD", "course_number": "ART UD Hist", "title": "Upper-Division Art History Elective", "units": 3, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ART 3310", "ART 3311", "ART 3314", "ART 3317", "ART 3320", "ART 3321", "ART 3322", "ART 3323", "ART 3324"], "is_placeholder": True},
    {"id": "AD_ART_ADV1", "course_number": "ART 3000+", "title": "3000-4000 Level Art Course",             "units": 4, "category": "major", "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_SRF1", "course_number": "Conc.",    "title": "Concentration Course",                   "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_SRF2", "course_number": "Conc.",    "title": "Concentration Course",                   "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_SRF3", "course_number": "Conc.",    "title": "Concentration Course",                   "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AD_ART_ADV2", "course_number": "ART 3000+ (2)", "title": "3000-4000 Level Art Course",           "units": 4, "category": "major", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_SRS1", "course_number": "Conc.",    "title": "Concentration Course",                   "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_SRS2", "course_number": "Conc.",    "title": "Concentration Course",                   "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_CON_SRS3", "course_number": "Conc.",    "title": "Concentration Course",                   "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_FREE",     "course_number": "Free",     "title": "Free Elective",                          "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


COLUMN_LABELS = [
    {"year": "Freshman",  "term": "Fall"},
    {"year": "Freshman",  "term": "Spring"},
    {"year": "Sophomore", "term": "Fall"},
    {"year": "Sophomore", "term": "Spring"},
    {"year": "Junior",    "term": "Fall"},
    {"year": "Junior",    "term": "Spring"},
    {"year": "Senior",    "term": "Fall"},
    {"year": "Senior",    "term": "Spring"},
]


_CATEGORY_LAYOUT_ORDER = {
    "major": 0,
    "support": 1,
    "concentration": 3,
    "ge": 4,
}

_DEFERRED_LAYOUT_TITLE_PARTS = (
    "orientation",
    "professional preparation",
)


def _layout_bucket(course: Course) -> int:
    title = course["title"].lower()
    if any(part in title for part in _DEFERRED_LAYOUT_TITLE_PARTS):
        return 2
    return _CATEGORY_LAYOUT_ORDER.get(course["category"], 5)


def _compact_rows_by_category(courses: list[Course], pinned_rows: dict[str, int] | None = None) -> list[Course]:
    pinned_rows = pinned_rows or {}

    for grid_col in range(len(COLUMN_LABELS)):
        column_courses = [course for course in courses if course["grid_col"] == grid_col]
        used_rows = {
            pinned_rows[course["id"]]
            for course in column_courses
            if course["id"] in pinned_rows
        }
        next_row = 0

        for course in sorted(column_courses, key=lambda c: (_layout_bucket(c), c["grid_row"])):
            if course["id"] in pinned_rows:
                course["grid_row"] = pinned_rows[course["id"]]
                continue
            while next_row in used_rows:
                next_row += 1
            course["grid_row"] = next_row
            used_rows.add(next_row)
            next_row += 1

    return courses


CS_FLOWCHART = _compact_rows_by_category(CS_FLOWCHART)
AERO_FLOWCHART = _compact_rows_by_category(AERO_FLOWCHART)
SE_FLOWCHART = _compact_rows_by_category(SE_FLOWCHART)
CPE_FLOWCHART = _compact_rows_by_category(CPE_FLOWCHART)
CE_FLOWCHART = _compact_rows_by_category(
    CE_FLOWCHART,
    {
        "CE_MATH1261": 2,
        "CE_MATH1262": 2,
        "CE_MATH2263": 2,
    },
)
ME_FLOWCHART = _compact_rows_by_category(ME_FLOWCHART)
AD_FLOWCHART = _compact_rows_by_category(AD_FLOWCHART)


FLOWCHARTS = {
    "CS": {
        "major": "Computer Science",
        "code": "CS",
        "total_units": 120,
        "courses": CS_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "AERO": {
        "major": "Aerospace Engineering",
        "code": "AERO",
        "total_units": 128,
        "courses": AERO_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "SE": {
        "major": "Software Engineering",
        "code": "SE",
        "total_units": 120,
        "courses": SE_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "CPE": {
        "major": "Computer Engineering",
        "code": "CPE",
        "total_units": 128,
        "courses": CPE_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "CE": {
        "major": "Civil Engineering",
        "code": "CE",
        "total_units": 132,
        "courses": CE_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "ME": {
        "major": "Mechanical Engineering",
        "code": "ME",
        "total_units": 129,
        "courses": ME_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "AD": {
        "major": "Art and Design",
        "code": "AD",
        "total_units": 120,
        "courses": AD_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
}
