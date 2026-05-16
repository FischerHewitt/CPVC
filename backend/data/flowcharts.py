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
    {"id": "LIFESCI",  "course_number": "BIO/BOT",   "title": "Life Science Elective",                "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111", "BIO 1150", "BIO 1151", "BOT 1121", "MCRO 2221"], "is_placeholder": True},
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
    {"id": "IME1143",  "course_number": "IME 1143",  "title": "Introduction to Design and Manufacturing", "units": 2, "category": "support", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["IME 144"], "is_placeholder": False},
    {"id": "MATH1261", "course_number": "MATH 1261", "title": "Calculus I",                          "units": 4, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "PHYS1141", "course_number": "PHYS 1141", "title": "General Physics I",                   "units": 4, "category": "support", "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["PHYS 141"], "is_placeholder": False},
    {"id": "GE1A",     "course_number": "GE 1A",     "title": "Written Communication",               "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "CHEM1120", "course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure and Properties", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["CHEM 124"], "is_placeholder": False},
    {"id": "MATH1262", "course_number": "MATH 1262", "title": "Calculus II",                         "units": 4, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "PHYS1143", "course_number": "PHYS 1143", "title": "General Physics II",                  "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["PHYS 132"], "is_placeholder": False},
    {"id": "GE1B",     "course_number": "GE 1B",     "title": "Critical Thinking",                   "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "GE3A",     "course_number": "GE 3A",     "title": "Arts",                                "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "ENGR2211", "course_number": "ENGR 2211", "title": "Introduction to Mechanics",           "units": 4, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["ME 211"], "is_placeholder": False},
    {"id": "MATE1220", "course_number": "MATE 1220", "title": "Principles of Materials Engineering for Non-Majors", "units": 2, "category": "support", "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MATE 210"], "is_placeholder": False},
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
    {"id": "AERO3460", "course_number": "AERO 3460", "title": "Aerospace Engineering Professional Preparation", "units": 1, "category": "major",   "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["AERO 460", "AERO 350"], "is_placeholder": False},
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
    {"id": "CPE_PHIL3323", "course_number": "PHIL 3323 / STAT 3210 / STAT 3310", "title": "Ethics, Science & Technology or Engineering Statistics", "units": 3, "category": "support", "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["STAT 312"], "elective_key": "cpe_ethics_or_stats", "is_placeholder": True},
    {"id": "CPE_GE4B", "course_number": "GE 4B",     "title": "Social & Behavioral Sciences",         "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "CPE3160",  "course_number": "CPE 3160",  "title": "Microcontrollers and Embedded Applications", "units": 4, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["CPE 2301"], "quarter_equivalents": ["CPE 316"], "is_placeholder": False},
    {"id": "CPE4464",  "course_number": "CPE 4464",  "title": "Introduction to Computer Networks",  "units": 3, "category": "major",   "grid_col": 5, "grid_row": 1, "prerequisites": ["CPE 3300"], "quarter_equivalents": ["CPE 464"], "is_placeholder": False},
    {"id": "CPE_GE4A", "course_number": "GE 4A",     "title": "American Institutions",                "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "CPE_GE6",  "course_number": "GE 6",      "title": "Ethnic Studies",                       "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

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
    {"id": "ME_IME114X",  "course_number": "IME 1141/1142/1149", "title": "Manufacturing Process Selective",          "units": 1, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["IME 141", "IME 142", "IME 1141", "IME 1142", "IME 1149"], "elective_key": "me_ime_mfg_selective", "is_placeholder": True},
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
    {"id": "AD_ART1184_2282", "course_number": "ART 1184 / ART 2282", "title": "Beginning Sculpture or Beginning Painting", "units": 3, "category": "major", "grid_col": 2, "grid_row": 1, "prerequisites": ["ART 1101"], "quarter_equivalents": ["ART 1184", "ART 2282", "ART 148", "ART 209"], "elective_key": "ad_sculpture_or_painting", "is_placeholder": True},
    {"id": "AD_ART2201", "course_number": "ART 2201", "title": "Visual Culture and Society",                "units": 3, "category": "major", "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ART 222"], "is_placeholder": False},
    {"id": "AD_ART2215", "course_number": "ART 2215", "title": "Global Contemporary Art",                   "units": 3, "category": "major", "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ART 213"], "is_placeholder": False},
    {"id": "AD_GE3B",    "course_number": "GE 3B",   "title": "Humanities",                                "units": 3, "category": "ge",    "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "AD_ART2212", "course_number": "ART 2212", "title": "Renaissance to Modern Art",                 "units": 3, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ART 212"], "is_placeholder": False},
    {"id": "AD_PORTFOLIO", "course_number": "ART 3359 / ART 3379 / ART 3399", "title": "Graphic Design or Photo Video or Studio Art Portfolio", "units": 3, "category": "major", "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ART 260", "ART 3359", "ART 3379", "ART 3399"], "elective_key": "ad_portfolio_review", "is_placeholder": True},
    {"id": "AD_GE4A",    "course_number": "GE 4A",   "title": "American Institutions",                    "units": 3, "category": "ge",    "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AD_GE5B",    "course_number": "GE 5B",   "title": "Life Sciences",                            "units": 3, "category": "ge",    "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
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
    {"id": "AD_GE3A",     "course_number": "GE 3A",   "title": "Arts and Creative Expression",            "units": 3, "category": "ge", "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

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


# ─────────────────────────────────────────────────────────────────────────────
# POLITICAL SCIENCE (BA) — Concentration Not Yet Declared (120 units)
# Source: catalog.calpoly.edu/liberal-arts/political-science/political-science-ba/
# ─────────────────────────────────────────────────────────────────────────────
POLS_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "POLS1112",       "course_number": "POLS 1112", "title": "U.S. and California Government",            "units": 3, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["POLS 112"], "is_placeholder": False},
    {"id": "POLS1180",       "course_number": "POLS 1180", "title": "Political Inquiry",                        "units": 3, "category": "major", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["POLS 180"], "is_placeholder": False},
    {"id": "POLS2229",       "course_number": "POLS 2229", "title": "Introduction to Comparative Politics",      "units": 3, "category": "major", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["POLS 229"], "is_placeholder": False},
    {"id": "POLS_GE1A",      "course_number": "GE 1A",     "title": "Written Communication",                    "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "POLS_GE1C",      "course_number": "GE 1C",     "title": "Oral Communication",                       "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "POLS2225",       "course_number": "POLS 2225", "title": "Introduction to International Relations",   "units": 3, "category": "major",   "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["POLS 225"], "is_placeholder": False},
    {"id": "POLS2230",       "course_number": "POLS 2230", "title": "Basic Concepts of Political Thought",       "units": 3, "category": "major",   "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["POLS 230"], "is_placeholder": False},
    {"id": "POLS_SUPPORT4B", "course_number": "ANT 2201 / GEOG 1150 / HIST 2222 / HIST 2223 / SOC 1110", "title": "Social and Behavioral Sciences Support", "units": 3, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ANT 2201", "GEOG 1150", "HIST 2222", "HIST 2223", "SOC 1110", "ANT 201", "GEOG 150", "HIST 110", "HIST 111", "SOC 110"], "elective_key": "pols_support_4b", "is_placeholder": True},
    {"id": "POLS_GE1B",      "course_number": "GE 1B",     "title": "Critical Thinking",                        "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_GE3A",      "course_number": "GE 3A",     "title": "Arts",                                     "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "POLS_STAT1110",  "course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["STAT 217"], "is_placeholder": False},
    {"id": "POLS_UD1",       "course_number": "POLS UD",   "title": "3000-4000 Level POLS Elective",            "units": 3, "category": "major",   "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_GE3B",      "course_number": "GE 3B",     "title": "Humanities",                               "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_GE5A",      "course_number": "GE 5A",     "title": "Physical Sciences",                        "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_GE6",       "course_number": "GE 6",      "title": "Ethnic Studies",                           "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "POLS_UD2",       "course_number": "POLS UD 2", "title": "3000-4000 Level POLS Elective",            "units": 3, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_UD3",       "course_number": "POLS UD 3", "title": "3000-4000 Level POLS Elective",            "units": 3, "category": "major",         "grid_col": 3, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_GE5B",      "course_number": "GE 5B",     "title": "Life Sciences",                            "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "POLS_GE5C",      "course_number": "GE 5C",     "title": "Laboratory",                               "units": 1, "category": "ge",            "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_FREE1",     "course_number": "Free",      "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "POLS3359",       "course_number": "POLS 3359", "title": "Research Design",                          "units": 3, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["POLS 359"], "is_placeholder": False},
    {"id": "POLS_DEI",       "course_number": "POLS DEI",  "title": "Diversity, Equity, and Inclusion Elective", "units": 3, "category": "major",         "grid_col": 4, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_CON_JRF1",  "course_number": "Conc.",     "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_CON_JRF2",  "course_number": "Conc.",     "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_GE_UD25",   "course_number": "GE UD-2/5", "title": "Upper-Div Math or Science",                 "units": 3, "category": "ge",            "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "POLS3361",       "course_number": "POLS 3361", "title": "Data Analysis in Political Science",        "units": 3, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": ["POLS 3359"], "quarter_equivalents": ["POLS 361"], "is_placeholder": False},
    {"id": "POLS_UD4",       "course_number": "POLS UD 4", "title": "3000-4000 Level POLS Elective",            "units": 3, "category": "major",         "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_CON_JRS1",  "course_number": "Conc.",     "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_CON_JRS2",  "course_number": "Conc.",     "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_GE_UD3",    "course_number": "GE UD-3",   "title": "Upper-Division Arts and Humanities",        "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "POLS4461",       "course_number": "POLS 4461", "title": "Senior Project I",                         "units": 2, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": ["POLS 3359"], "quarter_equivalents": ["POLS 461"], "is_placeholder": False},
    {"id": "POLS_CON_SRF1",  "course_number": "Conc.",     "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_CON_SRF2",  "course_number": "Conc.",     "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_FREE2",     "course_number": "Free 2",    "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_FREE3",     "course_number": "Free 3",    "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "POLS4462",       "course_number": "POLS 4462", "title": "Senior Project II",                        "units": 2, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": ["POLS 4461"], "quarter_equivalents": ["POLS 462"], "is_placeholder": False},
    {"id": "POLS_CON_SRS1",  "course_number": "Conc.",     "title": "Concentration Course",                     "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_FREE4",     "course_number": "Free 4",    "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_FREE5",     "course_number": "Free 5",    "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "POLS_FREE6",     "course_number": "Free 6",    "title": "Free Elective",                            "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# PSYCHOLOGY (BS) — General Curriculum (120 units)
# Source: catalog.calpoly.edu/liberal-arts/psychology-child-development/psychology-bs/
# ─────────────────────────────────────────────────────────────────────────────
PSY_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "PSY1102",      "course_number": "PSY 1102",  "title": "Orientation to the Psychology Major",         "units": 2, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "PSY2201",      "course_number": "PSY 2201",  "title": "Introductory Psychology",                    "units": 3, "category": "major",   "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["PSY 201"], "is_placeholder": False},
    {"id": "PSY_STAT1110", "course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods",   "units": 3, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["STAT 217"], "is_placeholder": False},
    {"id": "PSY_GE1A",     "course_number": "GE 1A",     "title": "Written Communication",                      "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "PSY_GE1C",     "course_number": "GE 1C",     "title": "Oral Communication",                         "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "PSY_FOUND",    "course_number": "PSY 2205 / PSY 2252 / PSY 2256", "title": "Personality or Social or Developmental Psychology", "units": 3, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": ["PSY 2201"], "quarter_equivalents": ["PSY 2205", "PSY 2252", "PSY 2256", "PSY 305", "PSY 252", "PSY 256"], "elective_key": "psy_foundation_course", "is_placeholder": True},
    {"id": "PSY2240",      "course_number": "PSY 2240",  "title": "Biopsychology",                              "units": 3, "category": "major",   "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["PSY 340"], "is_placeholder": False},
    {"id": "PSY2229",      "course_number": "PSY 2229",  "title": "Research Methods in Psychology",             "units": 3, "category": "major",   "grid_col": 1, "grid_row": 2, "prerequisites": ["PSY 2201", "STAT 1110"], "quarter_equivalents": ["PSY 329"], "is_placeholder": False},
    {"id": "PSY_GE1B",     "course_number": "GE 1B",     "title": "Critical Thinking",                          "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_GE3A",     "course_number": "GE 3A",     "title": "Arts",                                       "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "PSY_SOC_PERS", "course_number": "PSY Soc/Per", "title": "Social and Personality Elective",          "units": 4, "category": "major",   "grid_col": 2, "grid_row": 0, "prerequisites": ["PSY 2201"], "quarter_equivalents": ["PSY 302", "PSY 324", "PSY 352", "PSY 360", "PSY 419", "PSY 465", "PSY 475"], "elective_key": "psy_social_personality", "is_placeholder": True},
    {"id": "PSY3372",      "course_number": "PSY 3372",  "title": "Multicultural Psychology",                   "units": 4, "category": "major",   "grid_col": 2, "grid_row": 1, "prerequisites": ["PSY 2201"], "quarter_equivalents": ["PSY 372"], "is_placeholder": False},
    {"id": "PSY_GE3B",     "course_number": "GE 3B",     "title": "Humanities",                                 "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_GE4A",     "course_number": "GE 4A",     "title": "American Institutions",                      "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_GE5A",     "course_number": "GE 5A",     "title": "Physical Sciences",                          "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "PSY_MENTH",    "course_number": "PSY Mnt/Hlt", "title": "Mental and Physical Health Elective",      "units": 4, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["PSY 2201"], "quarter_equivalents": ["PSY 320", "PSY 356", "PSY 370", "PSY 405", "PSY 460"], "elective_key": "psy_mental_health", "is_placeholder": True},
    {"id": "PSY3333",      "course_number": "PSY 3333",  "title": "Advanced Research Methods",                  "units": 4, "category": "major",   "grid_col": 3, "grid_row": 1, "prerequisites": ["PSY 2229", "STAT 1110"], "quarter_equivalents": ["PSY 333"], "is_placeholder": False},
    {"id": "PSY_GE5B",     "course_number": "GE 5B",     "title": "Life Sciences",                              "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "PSY_GE5C",     "course_number": "GE 5C",     "title": "Laboratory",                                 "units": 1, "category": "ge",      "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_GE6",      "course_number": "GE 6",      "title": "Ethnic Studies",                             "units": 3, "category": "ge",      "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "PSY_COGN",     "course_number": "PSY Cogn",  "title": "Cognitive Elective",                         "units": 4, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": ["PSY 2201"], "quarter_equivalents": ["PSY 357", "PSY 430", "PSY 440", "PSY 480"], "elective_key": "psy_cognitive", "is_placeholder": True},
    {"id": "PSY_DEI",      "course_number": "PSY DEI",   "title": "Diversity, Equity and Inclusion Course",     "units": 4, "category": "support", "grid_col": 4, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "elective_key": "psy_dei", "is_placeholder": True},
    {"id": "PSY_PROF",     "course_number": "Prof. Skills", "title": "Professional Skills Support Course",      "units": 3, "category": "support", "grid_col": 4, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "elective_key": "psy_professional_skills", "is_placeholder": True},
    {"id": "PSY_GE_UD4",   "course_number": "GE UD-4",   "title": "Upper-Div Social Sciences",                  "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_FREE1",    "course_number": "Free",      "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "PSY_ELEC1",    "course_number": "PSY 3000+", "title": "PSY Approved Elective",                      "units": 4, "category": "major",   "grid_col": 5, "grid_row": 0, "prerequisites": ["PSY 2201"], "quarter_equivalents": [], "elective_key": "psy_upper_div", "is_placeholder": True},
    {"id": "PSY_SCI",      "course_number": "UD Science", "title": "Upper-Division Science Course",             "units": 4, "category": "support", "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["BIO 332", "PSY 344"], "elective_key": "psy_upper_div_science", "is_placeholder": True},
    {"id": "PSY_GE_UD3",   "course_number": "GE UD-3",   "title": "Upper-Div Arts and Humanities",              "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_FREE2",    "course_number": "Free 2",    "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_FREE3",    "course_number": "Free 3",    "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "PSY_INTERN1",  "course_number": "PSY 4448 / PSY 4453", "title": "Research or Fieldwork Internship I", "units": 3, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["PSY 2229"], "quarter_equivalents": ["PSY 4448", "PSY 4453", "PSY 448", "PSY 453"], "elective_key": "psy_internship_i", "is_placeholder": True},
    {"id": "PSY4461",      "course_number": "PSY 4461",  "title": "Senior Project Seminar",                     "units": 2, "category": "major",   "grid_col": 6, "grid_row": 1, "prerequisites": ["PSY 2229"], "quarter_equivalents": ["PSY 461"], "is_placeholder": False},
    {"id": "PSY_FREE4",    "course_number": "Free 4",    "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_FREE5",    "course_number": "Free 5",    "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_FREE6",    "course_number": "Free 6",    "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "PSY_INTERN2",  "course_number": "PSY 4449 / PSY 4454", "title": "Research or Fieldwork Internship II", "units": 3, "category": "major", "grid_col": 7, "grid_row": 0, "prerequisites": ["PSY 4448 / PSY 4453"], "quarter_equivalents": ["PSY 4449", "PSY 4454", "PSY 449", "PSY 454"], "elective_key": "psy_internship_ii", "is_placeholder": True},
    {"id": "PSY4462",      "course_number": "PSY 4462",  "title": "Senior Project",                             "units": 2, "category": "major",   "grid_col": 7, "grid_row": 1, "prerequisites": ["PSY 4461"], "quarter_equivalents": ["PSY 462"], "is_placeholder": False},
    {"id": "PSY_ELEC2",    "course_number": "PSY 3000+ (2)", "title": "PSY Approved Elective",                  "units": 4, "category": "major",   "grid_col": 7, "grid_row": 2, "prerequisites": ["PSY 2201"], "quarter_equivalents": [], "elective_key": "psy_upper_div", "is_placeholder": True},
    {"id": "PSY_FREE7",    "course_number": "Free 7",    "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "PSY_FREE8",    "course_number": "Free 8",    "title": "Free Elective",                              "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# ENGLISH (BA) — General Curriculum (120 units)
# Source: catalog.calpoly.edu/liberal-arts/english/english-ba/
# ─────────────────────────────────────────────────────────────────────────────
ENGL_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "ENGL1101",     "course_number": "ENGL 1101",    "title": "Introduction to English Studies",          "units": 4, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ENGL_LIT_3B",  "course_number": "ENGL GE 3B",   "title": "Literature Elective",                      "units": 3, "category": "major", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_GE1A",    "course_number": "GE 1A",        "title": "Written Communication",                    "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "ENGL_GE1C",    "course_number": "GE 1C",        "title": "Oral Communication",                       "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "ENGL_GE2",     "course_number": "GE 2",         "title": "Mathematics and Quantitative Reasoning",    "units": 3, "category": "ge",    "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "ENGL_LD1",     "course_number": "ENGL LD 1",    "title": "Lower-Division English Elective",          "units": 3, "category": "major",   "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 2200", "ENGL 2201", "ENGL 2220", "ENGL 2222", "ENGL 2290"], "is_placeholder": True},
    {"id": "ENGL_LD2",     "course_number": "ENGL LD 2",    "title": "Lower-Division English Elective",          "units": 3, "category": "major",   "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ENGL 2202", "ENGL 2203", "ENGL 2234", "ENGL 2245", "ENGL 2250"], "is_placeholder": True},
    {"id": "ENGL_LANG",    "course_number": "CHIN 1101 / FR 1101 / GER 1101 / ITAL 1101 / JPNS 1101 / SPAN 1101 / WLC 1101", "title": "Elementary Language and Culture", "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["CHIN 1101", "FR 1101", "GER 1101", "ITAL 1101", "JPNS 1101", "SPAN 1101", "WLC 1101", "CHIN 101", "FR 101", "GER 101", "ITAL 101", "JPNS 101", "SPAN 101"], "elective_key": "engl_language_1101", "is_placeholder": True},
    {"id": "ENGL_GE1B",    "course_number": "GE 1B",        "title": "Critical Thinking",                        "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_GE3A",    "course_number": "GE 3A",        "title": "Arts",                                     "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "ENGL_LD3",     "course_number": "ENGL LD 3",    "title": "Lower-Division English Elective",          "units": 3, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 2204", "ENGL 2205", "ENGL 2246", "ENGL 2270"], "is_placeholder": True},
    {"id": "ENGL_LD4",     "course_number": "ENGL LD 4",    "title": "Lower-Division English Elective",          "units": 3, "category": "major",         "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ENGL 2206", "ENGL 2207", "ENGL 2250", "ENGL 2290"], "is_placeholder": True},
    {"id": "ENGL_GE4A",    "course_number": "GE 4A",        "title": "American Institutions",                    "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_GE5A",    "course_number": "GE 5A",        "title": "Physical Sciences",                        "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_FREE1",   "course_number": "Free",         "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "ENGL_GWR",     "course_number": "ENGL UD GWR",  "title": "Upper-Division English GWR Elective",      "units": 4, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 3611", "ENGL 3618", "ENGL 3625", "ENGL 3626"], "is_placeholder": True},
    {"id": "ENGL_INT1",    "course_number": "ENGL 3000+ 1", "title": "Intermediate English Elective",            "units": 3, "category": "major",         "grid_col": 3, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ENGL 3301", "ENGL 3302", "ENGL 3390", "ENGL 3601"], "is_placeholder": True},
    {"id": "ENGL_GE4B",    "course_number": "GE 4B",        "title": "Social and Behavioral Sciences",           "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_GE5B",    "course_number": "GE 5B",        "title": "Life Sciences",                            "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "ENGL_FREE2",   "course_number": "Free 2",       "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ENGL_INT2",    "course_number": "ENGL 3000+ 2", "title": "Intermediate English Elective",            "units": 3, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 3303", "ENGL 3304", "ENGL 3391", "ENGL 3602"], "is_placeholder": True},
    {"id": "ENGL_INT3",    "course_number": "ENGL 3000+ 3", "title": "Intermediate English Elective",            "units": 3, "category": "major",         "grid_col": 4, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ENGL 3305", "ENGL 3306", "ENGL 3395", "ENGL 3603"], "is_placeholder": True},
    {"id": "ENGL_INT4",    "course_number": "ENGL 3000+ 4", "title": "Intermediate English Elective",            "units": 3, "category": "major",         "grid_col": 4, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ENGL 3612", "ENGL 3613", "ENGL 3614", "ENGL 3627"], "is_placeholder": True},
    {"id": "ENGL_GE5C",    "course_number": "GE 5C",        "title": "Laboratory",                               "units": 1, "category": "ge",            "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_FREE3",   "course_number": "Free 3",       "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ENGL_ADV1",    "course_number": "ENGL 4000+ 1", "title": "Advanced English Elective",                "units": 4, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 4401", "ENGL 4402", "ENGL 4403", "ENGL 4424"], "is_placeholder": True},
    {"id": "ENGL_ADV2",    "course_number": "ENGL 4000+ 2", "title": "Advanced English Elective",                "units": 4, "category": "major",         "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ENGL 4427", "ENGL 4428", "ENGL 4439", "ENGL 4449"], "is_placeholder": True},
    {"id": "ENGL_GE_UD25", "course_number": "GE UD-2/5",    "title": "Upper-Div Math or Science",                 "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_GE_UD4",  "course_number": "GE UD-4",      "title": "Upper-Div Social Sciences",                 "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_FREE4",   "course_number": "Free 4",       "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ENGL_ADV3",    "course_number": "ENGL 4000+ 3", "title": "Advanced English Elective",                "units": 4, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 4459", "ENGL 4469", "ENGL 4470", "ENGL 4474"], "is_placeholder": True},
    {"id": "ENGL_DIVERS",  "course_number": "ENGL Diversity", "title": "4000-Level Diversity Elective",          "units": 4, "category": "major",         "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ENGL 4427", "ENGL 4439", "ENGL 4449", "ENGL 4459", "ENGL 4495"], "is_placeholder": True},
    {"id": "ENGL_GE6",     "course_number": "GE 6",         "title": "Ethnic Studies",                           "units": 3, "category": "ge",            "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},
    {"id": "ENGL_FREE5",   "course_number": "Free 5",       "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_FREE6",   "course_number": "Free 6",       "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ENGL_ADV4",    "course_number": "ENGL 4000+ 4", "title": "Advanced English Elective",                "units": 4, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 4475", "ENGL 4476", "ENGL 4487", "ENGL 4488"], "is_placeholder": True},
    {"id": "ENGL4461",     "course_number": "ENGL 4461",    "title": "Senior Project",                           "units": 4, "category": "major",         "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ENGL 461"], "is_placeholder": False},
    {"id": "ENGL_GE_UD3",  "course_number": "GE UD-3",      "title": "Upper-Division Arts and Humanities",        "units": 3, "category": "ge",            "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_FREE7",   "course_number": "Free 7",       "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ENGL_FREE8",   "course_number": "Free 8",       "title": "Free Elective",                            "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# MUSIC (BA) — General Curriculum (120 units)
# Source: catalog.calpoly.edu/liberal-arts/music/music-ba/
# ─────────────────────────────────────────────────────────────────────────────
MU_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "MU1100",       "course_number": "MU 1100",      "title": "Introduction to Music Studies",             "units": 1, "category": "major",         "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU_MATS1",     "course_number": "MU 1101 / MU 1103", "title": "Music Fundamentals or Materials and Structures I", "units": 4, "category": "major", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MU 1101", "MU 1103"], "elective_key": "mu_fundamentals_or_materials_i", "is_placeholder": True},
    {"id": "MU1104",       "course_number": "MU 1104",      "title": "Musicianship I",                           "units": 2, "category": "major",         "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU1150_FF",    "course_number": "MU 1150",      "title": "Applied Music I",                          "units": 1, "category": "major",         "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU_ENS_FF",    "course_number": "Ensemble 1",   "title": "Major Ensemble",                           "units": 1, "category": "major",         "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["MU 1168", "MU 1171", "MU 1172", "MU 1173", "MU 1174", "MU 1181", "MU 1182", "MU 1183", "MU 1184", "MU 1187", "MU 1188"], "is_placeholder": True},
    {"id": "MU_GE1A",      "course_number": "GE 1A",        "title": "Written Communication",                    "units": 3, "category": "ge",            "grid_col": 0, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "MU_GE1C",      "course_number": "GE 1C",        "title": "Oral Communication",                       "units": 3, "category": "ge",            "grid_col": 0, "grid_row": 6, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "MU_FREE1",     "course_number": "Free",         "title": "Free Elective",                            "units": 1, "category": "concentration", "grid_col": 0, "grid_row": 7, "prerequisites": [], "quarter_equivalents": ["MU 1161"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "MU_MATS2",     "course_number": "MU 1103 / MU 2203", "title": "Materials and Structures of Music I or II", "units": 4, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["MU 1103", "MU 2203"], "elective_key": "mu_materials_i_or_ii", "is_placeholder": True},
    {"id": "MU1122",       "course_number": "MU 1122",      "title": "Ethnomusicology and World Music I",         "units": 4, "category": "major",         "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU1150_FS",    "course_number": "MU 1150 (2)",  "title": "Applied Music I",                          "units": 1, "category": "major",         "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MU 1150"], "is_placeholder": False},
    {"id": "MU1106",       "course_number": "MU 1106",      "title": "Musicianship II",                          "units": 2, "category": "major",         "grid_col": 1, "grid_row": 3, "prerequisites": ["MU 1104"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU_ENS_FS",    "course_number": "Ensemble 2",   "title": "Major Ensemble",                           "units": 1, "category": "major",         "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["MU 1168", "MU 1171", "MU 1172", "MU 1173", "MU 1174", "MU 1181", "MU 1182", "MU 1183", "MU 1184", "MU 1187", "MU 1188"], "is_placeholder": True},
    {"id": "MU_GE1B",      "course_number": "GE 1B",        "title": "Critical Thinking",                        "units": 3, "category": "ge",            "grid_col": 1, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_FREE2",     "course_number": "Free 2",       "title": "Free Elective",                            "units": 1, "category": "concentration", "grid_col": 1, "grid_row": 6, "prerequisites": [], "quarter_equivalents": ["MU 1162"], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "MU2203",       "course_number": "MU 2203",      "title": "Materials and Structures of Music II",      "units": 4, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU2222",       "course_number": "MU 2222",      "title": "Ethnomusicology and World Music II",        "units": 4, "category": "major",         "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU2250_SF",    "course_number": "MU 2250",      "title": "Applied Music II",                         "units": 1, "category": "major",         "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU_ENS_SF",    "course_number": "Ensemble 3",   "title": "Major Ensemble",                           "units": 1, "category": "major",         "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["MU 1168", "MU 1171", "MU 1172", "MU 1173", "MU 1174", "MU 1181", "MU 1182", "MU 1183", "MU 1184", "MU 1187", "MU 1188"], "is_placeholder": True},
    {"id": "MU_GE2",       "course_number": "GE 2",         "title": "Mathematics and Quantitative Reasoning",    "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_GE3B",      "course_number": "GE 3B",        "title": "Humanities",                               "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_FREE3",     "course_number": "Free 3",       "title": "Free Elective",                            "units": 1, "category": "concentration", "grid_col": 2, "grid_row": 6, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "MU2250_SS",    "course_number": "MU 2250 (2)",  "title": "Applied Music II",                         "units": 1, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["MU 2250"], "is_placeholder": False},
    {"id": "MU_USCP",      "course_number": "MU 2221 / MU 2227", "title": "Jazz Styles or Popular Music of the United States", "units": 4, "category": "major", "grid_col": 3, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MU 2221", "MU 2227"], "elective_key": "mu_uscp_music_choice", "is_placeholder": True},
    {"id": "MU_ENS_SS",    "course_number": "Ensemble 4",   "title": "Major Ensemble",                           "units": 1, "category": "major",         "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MU 1168", "MU 1171", "MU 1172", "MU 1173", "MU 1174", "MU 1181", "MU 1182", "MU 1183", "MU 1184", "MU 1187", "MU 1188"], "is_placeholder": True},
    {"id": "MU_GE4A",      "course_number": "GE 4A",        "title": "American Institutions",                    "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_GE5A",      "course_number": "GE 5A",        "title": "Physical Sciences",                        "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_GE5C",      "course_number": "GE 5C",        "title": "Laboratory",                               "units": 1, "category": "ge",            "grid_col": 3, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_GE4B",      "course_number": "GE 4B",        "title": "Social and Behavioral Sciences",           "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 6, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_FREE4",     "course_number": "Free 4",       "title": "Free Elective",                            "units": 1, "category": "concentration", "grid_col": 3, "grid_row": 7, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "MU3311",       "course_number": "MU 3311",      "title": "Introduction to Music Technology and Composition", "units": 4, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU3350_JF",    "course_number": "MU 3350",      "title": "Applied Music III",                        "units": 1, "category": "major",         "grid_col": 4, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU_ENS_JF",    "course_number": "Ensemble 5",   "title": "Major Ensemble",                           "units": 1, "category": "major",         "grid_col": 4, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MU 3368", "MU 3371", "MU 3372", "MU 3373", "MU 3374", "MU 3381", "MU 3382", "MU 3383", "MU 3384", "MU 3387", "MU 3388"], "is_placeholder": True},
    {"id": "MU_GE5B",      "course_number": "GE 5B",        "title": "Life Sciences",                            "units": 3, "category": "ge",            "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "MU_GE6",       "course_number": "GE 6",         "title": "Ethnic Studies",                           "units": 3, "category": "ge",            "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "MU3331",       "course_number": "MU 3331",      "title": "Historical Musicology I",                  "units": 4, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU3350_JS",    "course_number": "MU 3350 (2)",  "title": "Applied Music III",                        "units": 1, "category": "major",         "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MU 3350"], "is_placeholder": False},
    {"id": "MU_ENS_JS",    "course_number": "Ensemble 6",   "title": "Major Ensemble",                           "units": 1, "category": "major",         "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MU 3368", "MU 3371", "MU 3372", "MU 3373", "MU 3374", "MU 3381", "MU 3382", "MU 3383", "MU 3384", "MU 3387", "MU 3388"], "is_placeholder": True},
    {"id": "MU_ELEC1",     "course_number": "MU 3000+ 1",   "title": "Upper-Division Music Elective",             "units": 4, "category": "major",         "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["MU 3301", "MU 3312", "MU 3320", "MU 3325", "MU 3326", "MU 3336", "MU 3340", "MU 3341", "MU 3342", "MU 3351", "MU 3352", "MU 4411", "MU 4412"], "is_placeholder": True},
    {"id": "MU_GE_UD25",   "course_number": "GE UD-2/5",    "title": "Upper-Div Math or Science",                 "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_FREE5",     "course_number": "Free 5",       "title": "Free Elective",                            "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "MU4431",       "course_number": "MU 4431",      "title": "Historical Musicology II",                 "units": 4, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU_ELEC2",     "course_number": "MU 3000+ 2",   "title": "Upper-Division Music Elective",             "units": 4, "category": "major",         "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MU 3301", "MU 3312", "MU 3320", "MU 3325", "MU 3326", "MU 3336", "MU 3340", "MU 3341", "MU 3342", "MU 3351", "MU 3352", "MU 4411", "MU 4412"], "is_placeholder": True},
    {"id": "MU_GE_UD4",    "course_number": "GE UD-4",      "title": "Upper-Div Social Sciences",                 "units": 3, "category": "ge",            "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_FREE6",     "course_number": "Free 6",       "title": "Free Elective",                            "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "MU4461",       "course_number": "MU 4461",      "title": "Senior Project",                           "units": 2, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "MU_ELEC3",     "course_number": "MU 3000+ 3",   "title": "Upper-Division Music Elective",             "units": 4, "category": "major",         "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MU 3301", "MU 3312", "MU 3320", "MU 3325", "MU 3326", "MU 3336", "MU 3340", "MU 3341", "MU 3342", "MU 3351", "MU 3352", "MU 4411", "MU 4412"], "is_placeholder": True},
    {"id": "MU_GE_UD3",    "course_number": "GE UD-3",      "title": "Upper-Division Arts and Humanities",        "units": 3, "category": "ge",            "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "MU_FREE7",     "course_number": "Free 7",       "title": "Free Elective",                            "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# AGRICULTURAL COMMUNICATION (BS) — General Curriculum (120 units)
# Source: catalog.calpoly.edu/agriculture-food-environmental-sciences/agricultural-education-communication/agricultural-communication-bs/
# ─────────────────────────────────────────────────────────────────────────────
AGC_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "AGC1102",        "course_number": "AGC 1102",        "title": "Orientation to Agricultural Communication & Agricultural Science", "units": 1, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "AGC2207",        "course_number": "AGC 2207",        "title": "Software Applications for Agricultural Publications",             "units": 2, "category": "major",   "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["AGC 207"], "is_placeholder": False},
    {"id": "AGC_BIO1111",    "course_number": "BIO 1111",        "title": "General Biology",                                                "units": 3, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BIO 111"], "is_placeholder": False},
    {"id": "AGC_STATDATA1000", "course_number": "STAT 1000 / DATA 1000", "title": "Statistical and Data Literacy",                             "units": 3, "category": "support", "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["STAT 150", "DATA 100", "STAT 1000", "DATA 1000"], "elective_key": "agc_stat_data_1000", "is_placeholder": True},
    {"id": "AGC_GE1A",       "course_number": "GE 1A",           "title": "Written Communication",                                           "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "AGC_GE1C",       "course_number": "GE 1C",           "title": "Oral Communication",                                              "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "AGC_ASCI1101",   "course_number": "ASCI 1101",       "title": "Principles of Animal Physiology",                                 "units": 3, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ASCI 112"], "is_placeholder": False},
    {"id": "AGC_ASCI1102",   "course_number": "ASCI 1102",       "title": "Animal Management Systems",                                       "units": 3, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ASCI 112"], "is_placeholder": False},
    {"id": "AGC_ASCI1103",   "course_number": "ASCI 1103",       "title": "Animal Science Laboratory",                                       "units": 1, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["ASCI 112"], "is_placeholder": False},
    {"id": "AGC_CHEM5A5C",   "course_number": "CHEM 1110 / CHEM 1120", "title": "World of Chemistry or Fundamentals of Chemical Structure and Properties", "units": 4, "category": "support", "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["CHEM 111", "CHEM 124", "CHEM 1110", "CHEM 1120"], "elective_key": "agc_chem_elective", "is_placeholder": True},
    {"id": "AGC_MATH1006",   "course_number": "MATH 1006",       "title": "College Algebra",                                                 "units": 3, "category": "support", "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["MATH 118"], "is_placeholder": False},
    {"id": "AGC_GE1B",       "course_number": "GE 1B",           "title": "Critical Thinking",                                               "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "AGC2205",        "course_number": "AGC 2205",        "title": "Agricultural Communications",                                     "units": 3, "category": "major",   "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGC 205"], "is_placeholder": False},
    {"id": "AGC_FSN",        "course_number": "FSN 1111 / FSN 2245", "title": "Elements of Food Processing or Elements of Food Safety",         "units": 3, "category": "support", "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["FSN 101", "FSN 275", "FSN 1111", "FSN 2245"], "elective_key": "agc_fsn_elective", "is_placeholder": True},
    {"id": "AGC_JOUR2203",   "course_number": "JOUR 2203",       "title": "News Reporting and Writing",                                      "units": 3, "category": "support", "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["JOUR 203"], "is_placeholder": False},
    {"id": "AGC_PLSC1120",   "course_number": "PLSC 1120 + PLSC 1120L", "title": "Principles of Plant Sciences with Lab",                      "units": 3, "category": "support", "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["PLSC 120", "PLSC 1120", "PLSC 1120L"], "elective_key": "agc_plsc_pair", "is_placeholder": True},
    {"id": "AGC_GE3A",       "course_number": "GE 3A",           "title": "Arts",                                                            "units": 3, "category": "ge",      "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "AGC2225",        "course_number": "AGC 2225",        "title": "Digital Communication in Agriculture and Science",                 "units": 3, "category": "major",   "grid_col": 3, "grid_row": 0, "prerequisites": ["AGC 2207"], "quarter_equivalents": ["AGC 225"], "is_placeholder": False},
    {"id": "AGC_AGB2212",    "course_number": "AGB 2212",        "title": "Agricultural Economics",                                          "units": 3, "category": "support", "grid_col": 3, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["AGB 212"], "is_placeholder": False},
    {"id": "AGC_AGB2260",    "course_number": "AGB 2260",        "title": "Agribusiness Data Literacy",                                      "units": 3, "category": "support", "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["AGB 260"], "is_placeholder": False},
    {"id": "AGC_ECON2040",   "course_number": "ECON 2040",       "title": "Macroeconomics",                                                 "units": 3, "category": "support", "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ECON 222"], "is_placeholder": False},
    {"id": "AGC_SS1120",     "course_number": "SS 1120",         "title": "Introductory Soil Science",                                       "units": 4, "category": "support", "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["SS 120"], "is_placeholder": False},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AGC3301",        "course_number": "AGC 3301",        "title": "New Media Communication Strategies in Agriculture",               "units": 3, "category": "major",   "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGC 301"], "is_placeholder": False},
    {"id": "AGC_MARKETING",  "course_number": "AGB 3301 / WVIT 3343", "title": "Food Marketing or Branded Wine Marketing",                  "units": 3, "category": "support", "grid_col": 4, "grid_row": 1, "prerequisites": ["AGB 2212"], "quarter_equivalents": ["AGB 301", "WVIT 343", "AGB 3301", "WVIT 3343"], "elective_key": "agc_ags_marketing", "is_placeholder": True},
    {"id": "AGC_AGB3312",    "course_number": "AGB 3312",        "title": "Agricultural Policy",                                            "units": 3, "category": "support", "grid_col": 4, "grid_row": 2, "prerequisites": ["AGB 2212", "ECON 2040"], "quarter_equivalents": ["AGB 312"], "is_placeholder": False},
    {"id": "AGC_COMS3316",   "course_number": "COMS 3316",       "title": "Intercultural Communication",                                     "units": 3, "category": "support", "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["COMS 316"], "is_placeholder": False},
    {"id": "AGC_GE3B",       "course_number": "GE 3B",           "title": "Humanities",                                                      "units": 3, "category": "ge",      "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AGC3339",        "course_number": "AGC 3339",        "title": "Internship in Agricultural Communications",                       "units": 3, "category": "major",   "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGC 339"], "is_placeholder": False},
    {"id": "AGC_BRAE3340",   "course_number": "BRAE 3340",       "title": "Irrigation Water Management",                                     "units": 3, "category": "support", "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["BRAE 340"], "is_placeholder": False},
    {"id": "AGC_NR3308",     "course_number": "NR 3308",         "title": "Fire and Society",                                               "units": 3, "category": "support", "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["NR 308"], "is_placeholder": False},
    {"id": "AGC_GE4A",       "course_number": "GE 4A",           "title": "American Institutions",                                           "units": 3, "category": "ge",      "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AGC4404",        "course_number": "AGC 4404",        "title": "Applications of Agricultural Leadership",                         "units": 3, "category": "major",   "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGC 404"], "is_placeholder": False},
    {"id": "AGC4407",        "course_number": "AGC 4407",        "title": "Agricultural Publications",                                      "units": 3, "category": "major",   "grid_col": 6, "grid_row": 1, "prerequisites": ["AGC 2205", "AGC 2207"], "quarter_equivalents": ["AGC 407"], "is_placeholder": False},
    {"id": "AGC4425",        "course_number": "AGC 4425",        "title": "Multimedia Storytelling in Agriculture and Science",              "units": 3, "category": "major",   "grid_col": 6, "grid_row": 2, "prerequisites": ["AGC 2225"], "quarter_equivalents": ["AGC 425"], "is_placeholder": False},
    {"id": "AGC_ENGL3310",   "course_number": "ENGL 3310",       "title": "Corporate Communication",                                        "units": 3, "category": "support", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ENGL 310"], "is_placeholder": False},
    {"id": "AGC_GE_UD3",     "course_number": "GE UD-3",         "title": "Upper-Division Arts and Humanities",                             "units": 3, "category": "ge",      "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AGC4426",        "course_number": "AGC 4426",        "title": "Presentation Methods in Agricultural Communication",              "units": 3, "category": "major",   "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGC 426"], "is_placeholder": False},
    {"id": "AGC4452",        "course_number": "AGC 4452",        "title": "Current Trends and Issues in Agricultural Communication",         "units": 3, "category": "major",   "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["AGC 452"], "is_placeholder": False},
    {"id": "AGC4463",        "course_number": "AGC 4463",        "title": "Senior Project",                                                 "units": 3, "category": "major",   "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["AGC 463"], "is_placeholder": False},
    {"id": "AGC4475",        "course_number": "AGC 4475",        "title": "Crisis Communication in Food and Agriculture",                    "units": 3, "category": "major",   "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["AGC 475"], "is_placeholder": False},
    {"id": "AGC_GE6",        "course_number": "GE 6",            "title": "Ethnic Studies",                                                "units": 3, "category": "ge",      "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# AGRICULTURAL SCIENCE (BS) — Emphasis Not Yet Declared (120 units)
# Source: catalog.calpoly.edu/agriculture-food-environmental-sciences/agricultural-education-communication/agricultural-science-bs/
# ─────────────────────────────────────────────────────────────────────────────
AGS_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "AGS_AGC1102",    "course_number": "AGC 1102",        "title": "Orientation to Agricultural Communication & Agricultural Science", "units": 1, "category": "major",   "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "AGS_ASCI1101",   "course_number": "ASCI 1101",       "title": "Principles of Animal Physiology",                                 "units": 3, "category": "major",   "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "AGS_BIO5B",      "course_number": "BIO 1111/1151",   "title": "Life Science Support Elective",                                    "units": 3, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BIO 111", "BIO 1111", "BIO 1151", "BOT 1121", "MCRO 2221"], "is_placeholder": True},
    {"id": "AGS_BRAE1141",   "course_number": "BRAE 1141",       "title": "Agricultural Machinery Safety",                                    "units": 2, "category": "major",   "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["BRAE 141"], "is_placeholder": False},
    {"id": "AGS_GE1A",       "course_number": "GE 1A",           "title": "Written Communication",                                           "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "AGS_GE1C",       "course_number": "GE 1C",           "title": "Oral Communication",                                              "units": 3, "category": "ge",      "grid_col": 0, "grid_row": 5, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "AGS_ASCI1102_1103", "course_number": "ASCI 1102/1103", "title": "Animal Management Systems and Laboratory",                      "units": 4, "category": "major",   "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ASCI 112"], "is_placeholder": True},
    {"id": "AGS_CHEM1110",   "course_number": "CHEM 1110",       "title": "World of Chemistry",                                             "units": 4, "category": "support", "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["CHEM 111"], "is_placeholder": False},
    {"id": "AGS_PLSC1120",   "course_number": "PLSC 1120/1120L", "title": "Principles of Plant Sciences with Lab",                           "units": 3, "category": "major",   "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["PLSC 120"], "is_placeholder": True},
    {"id": "AGS_GE1B",       "course_number": "GE 1B",           "title": "Critical Thinking",                                               "units": 3, "category": "ge",      "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "AGS_AGB2202",    "course_number": "AGB 2202",        "title": "Introduction to Sales",                                          "units": 3, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGB 202"], "is_placeholder": False},
    {"id": "AGS_MATH2",      "course_number": "MATH 1006–1267",  "title": "Mathematics Support Elective",                                    "units": 3, "category": "support",       "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["MATH 118", "MATH 119", "MATH 141", "MATH 221", "MATH 1006", "MATH 1007", "MATH 1261", "MATH 1264", "MATH 1267"], "elective_key": "ags_math_elective", "is_placeholder": True},
    {"id": "AGS_SS1120",     "course_number": "SS 1120/1130",    "title": "Introductory Soil Science",                                       "units": 3, "category": "major",         "grid_col": 2, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["SS 120"], "is_placeholder": True},
    {"id": "AGS_GE3A",       "course_number": "GE 3A",           "title": "Arts",                                                            "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_FREE1",      "course_number": "Free",            "title": "Free Elective",                                                   "units": 2, "category": "concentration", "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "AGS_AGB2212",    "course_number": "AGB 2212",        "title": "Agricultural Economics",                                         "units": 3, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGB 212"], "is_placeholder": False},
    {"id": "AGS_DSCI_FSN",   "course_number": "DSCI 2229/FSN 2245", "title": "Safe Practices in Handling Food Products",                    "units": 3, "category": "major",         "grid_col": 3, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["DSCI 229", "FSN 245"], "is_placeholder": True},
    {"id": "AGS_GE3B",       "course_number": "GE 3B",           "title": "Humanities",                                                      "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_GE4A",       "course_number": "GE 4A",           "title": "American Institutions",                                           "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_FREE2",      "course_number": "Free 2",          "title": "Free Elective",                                                   "units": 3, "category": "concentration", "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AGS_AGED_AGC",   "course_number": "AGED 4410/AGC 3314", "title": "Computer Applications or Fairgrounds and Expositions",          "units": 3, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGED 410", "AGC 314"], "is_placeholder": True},
    {"id": "AGS_AGB3301",    "course_number": "AGB 3301/WVIT 3343", "title": "Food Marketing or Branded Wine Marketing",                     "units": 3, "category": "major",         "grid_col": 4, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["AGB 301", "WVIT 343", "AGB 3301", "WVIT 3343"], "elective_key": "agc_ags_marketing", "is_placeholder": True},
    {"id": "AGS_AGED4421",   "course_number": "AGED 4421",       "title": "Agricultural Mechanics",                                          "units": 3, "category": "major",         "grid_col": 4, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["AGED 421"], "is_placeholder": False},
    {"id": "AGS_EMP_JRF1",   "course_number": "Emphasis 1",      "title": "Approved Agricultural Science Emphasis Course",                  "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_FREE3",      "course_number": "Free 3",          "title": "Free Elective",                                                   "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AGS_BRAE3340",   "course_number": "BRAE 3340",       "title": "Irrigation Water Management",                                     "units": 3, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["BRAE 340"], "is_placeholder": False},
    {"id": "AGS_NR3308",     "course_number": "NR 3308/3323",    "title": "Fire and Society or Human Dimensions in Natural Resources Management", "units": 3, "category": "major",      "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["NR 308", "NR 323"], "is_placeholder": True},
    {"id": "AGS_PLSC3301",   "course_number": "PLSC 3301",       "title": "Horticultural Production Techniques",                             "units": 3, "category": "major",         "grid_col": 5, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["PLSC 301"], "is_placeholder": False},
    {"id": "AGS_EMP_JRS1",   "course_number": "Emphasis 2",      "title": "Approved Agricultural Science Emphasis Course",                  "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_GE_UD3",     "course_number": "GE UD-3",         "title": "Upper-Division Arts and Humanities",                             "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AGS_AGC4404",    "course_number": "AGC 4404",        "title": "Applications of Agricultural Leadership",                         "units": 3, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGC 404"], "is_placeholder": False},
    {"id": "AGS_AGC4452",    "course_number": "AGC 4452/AG 4452", "title": "Current Trends and Issues in Agriculture",                       "units": 3, "category": "major",         "grid_col": 6, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["AGC 452", "AG 452"], "is_placeholder": True},
    {"id": "AGS_EMP_SRF1",   "course_number": "Emphasis 3",      "title": "Approved Agricultural Science Emphasis Course",                  "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_EMP_SRF2",   "course_number": "Emphasis 4",      "title": "Approved Agricultural Science Emphasis Course",                  "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_GE6",        "course_number": "GE 6",            "title": "Ethnic Studies",                                                "units": 3, "category": "ge",            "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AGS_AGC4426",    "course_number": "AGC 4426",        "title": "Presentation Methods in Agricultural Communication",             "units": 3, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGC 426"], "is_placeholder": False},
    {"id": "AGS_AGC4463",    "course_number": "AGC 4463",        "title": "Senior Project",                                                "units": 3, "category": "major",         "grid_col": 7, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["AGC 463"], "is_placeholder": False},
    {"id": "AGS_EMP_SRS1",   "course_number": "Emphasis 5",      "title": "Approved Agricultural Science Emphasis Course",                  "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_EMP_SRS2",   "course_number": "Emphasis 6",      "title": "Approved Agricultural Science Emphasis Course",                  "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_GE_UD4",     "course_number": "GE UD-4",         "title": "Upper-Div Social Sciences",                                      "units": 3, "category": "ge",            "grid_col": 7, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "AGS_FREE4",      "course_number": "Free 4",          "title": "Free Elective",                                                   "units": 2, "category": "concentration", "grid_col": 7, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# AGRICULTURAL BUSINESS (BS) — General Curriculum (120 units)
# Source: catalog.calpoly.edu/agriculture-food-environmental-sciences/agribusiness/agricultural-business-bs/
# ─────────────────────────────────────────────────────────────────────────────
AGB_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "AGB1101",      "course_number": "AGB 1101",  "title": "Introduction to Agribusiness",          "units": 3, "category": "major",         "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["AGB 101"],               "is_placeholder": False},
    {"id": "AGB2202",      "course_number": "AGB 2202",  "title": "Introduction to Sales",                 "units": 3, "category": "major",         "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["AGB 202"],               "is_placeholder": False},
    {"id": "AGB_BUS2207",  "course_number": "BUS 2207",  "title": "Legal Responsibilities of Business",    "units": 3, "category": "support",       "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BUS 207"],               "is_placeholder": False},
    {"id": "AGB_GE1A",     "course_number": "GE 1A",     "title": "Written Communication",                 "units": 3, "category": "ge",            "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "AGB_GE1C",     "course_number": "GE 1C",     "title": "Oral Communication",                    "units": 3, "category": "ge",            "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["COMS 101"],              "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "AGB2212",      "course_number": "AGB 2212",  "title": "Agricultural Economics",                "units": 3, "category": "major",         "grid_col": 1, "grid_row": 0, "prerequisites": [],              "quarter_equivalents": ["AGB 212"],  "is_placeholder": False},
    {"id": "AGB2214",      "course_number": "AGB 2214",  "title": "Agribusiness Financial Accounting",     "units": 3, "category": "major",         "grid_col": 1, "grid_row": 1, "prerequisites": [],              "quarter_equivalents": ["AGB 214"],  "is_placeholder": False},
    {"id": "AGB_MATH1267", "course_number": "MATH 1267", "title": "Business Calculus",                     "units": 3, "category": "support",       "grid_col": 1, "grid_row": 2, "prerequisites": [],              "quarter_equivalents": ["MATH 221"], "is_placeholder": False},
    {"id": "AGB_GE1B",     "course_number": "GE 1B",     "title": "Critical Thinking",                     "units": 3, "category": "ge",            "grid_col": 1, "grid_row": 3, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},
    {"id": "AGB_GE3A",     "course_number": "GE 3A",     "title": "Arts",                                  "units": 3, "category": "ge",            "grid_col": 1, "grid_row": 4, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "AGB2260",      "course_number": "AGB 2260",  "title": "Agribusiness Data Literacy",            "units": 3, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": False},
    {"id": "AGB_ECON2040", "course_number": "ECON 2040", "title": "Macroeconomics",                        "units": 3, "category": "support",       "grid_col": 2, "grid_row": 1, "prerequisites": [],              "quarter_equivalents": ["ECON 201"], "is_placeholder": False},
    {"id": "AGB_STAT1210", "course_number": "STAT 1210", "title": "Business Statistics I",                 "units": 3, "category": "support",       "grid_col": 2, "grid_row": 2, "prerequisites": [],              "quarter_equivalents": ["STAT 217"], "is_placeholder": False},
    {"id": "AGB_AGELE1",   "course_number": "Ag Elec.",  "title": "Agricultural Elective",                 "units": 3, "category": "support",       "grid_col": 2, "grid_row": 3, "prerequisites": [],              "quarter_equivalents": ["ASCI 112", "ASCI 215", "ASCI 239", "DSCI 229", "FSN 275", "PLSC 120", "SS 120", "ASCI 1112", "ASCI 2215", "ASCI 2239", "DSCI 2229", "FSN 2245", "PLSC 1120", "PLSC 1120L", "SS 1120"], "elective_key": "agb_agricultural_elective", "is_placeholder": True},
    {"id": "AGB_GE4A",     "course_number": "GE 4A",     "title": "American Institutions",                 "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 4, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "AGB3301",      "course_number": "AGB 3301",  "title": "Food Marketing",                        "units": 3, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": ["AGB 2212"],    "quarter_equivalents": ["AGB 301"],  "is_placeholder": False},
    {"id": "AGB3308",      "course_number": "AGB 3308",  "title": "Introduction to Agribusiness Finance",  "units": 3, "category": "major",         "grid_col": 3, "grid_row": 1, "prerequisites": ["AGB 2214", "AGB 2260"], "quarter_equivalents": ["AGB 308"],  "is_placeholder": False},
    {"id": "AGB3327",      "course_number": "AGB 3327",  "title": "Agribusiness Data Analysis",            "units": 3, "category": "major",         "grid_col": 3, "grid_row": 2, "prerequisites": ["AGB 2260", "STAT 1210"], "quarter_equivalents": ["AGB 327"],  "is_placeholder": False},
    {"id": "AGB_GE4B",     "course_number": "GE 4B",     "title": "Social and Behavioral Sciences",        "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 3, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},
    {"id": "AGB_GE6",      "course_number": "GE 6",      "title": "Ethnic Studies",                        "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 4, "prerequisites": [],              "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AGB3322",      "course_number": "AGB 3322",  "title": "Principles of Agribusiness Management", "units": 3, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": ["AGB 2212", "AGB 2214"], "quarter_equivalents": ["AGB 322"],  "is_placeholder": False},
    {"id": "AGB3328",      "course_number": "AGB 3328",  "title": "Decision Tools for Agribusiness",       "units": 3, "category": "major",         "grid_col": 4, "grid_row": 1, "prerequisites": ["AGB 2260", "MATH 1267", "STAT 1210"], "quarter_equivalents": ["AGB 328"], "is_placeholder": False},
    {"id": "AGB_GEN1",     "course_number": "AGB Elec.", "title": "Agribusiness General Elective",          "units": 3, "category": "major",         "grid_col": 4, "grid_row": 2, "prerequisites": [],              "quarter_equivalents": [],           "elective_key": "agb_general_elective", "is_placeholder": True},
    {"id": "AGB_CAFES1",   "course_number": "CAFES",     "title": "CAFES Prefix Elective",                 "units": 3, "category": "support",       "grid_col": 4, "grid_row": 3, "prerequisites": [],              "quarter_equivalents": [],           "elective_key": "agb_cafes_prefix_elective", "is_placeholder": True},
    {"id": "AGB_GE3B",     "course_number": "GE 3B",     "title": "Humanities",                            "units": 3, "category": "ge",            "grid_col": 4, "grid_row": 4, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AGB3312",      "course_number": "AGB 3312",  "title": "Agricultural Policy",                   "units": 3, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": ["AGB 2212", "ECON 2040"], "quarter_equivalents": ["AGB 312"],  "is_placeholder": False},
    {"id": "AGB3369",      "course_number": "AGB 3369",  "title": "Agricultural Personnel Management",     "units": 3, "category": "major",         "grid_col": 5, "grid_row": 1, "prerequisites": ["AGB 2212"],    "quarter_equivalents": ["AGB 369"],  "is_placeholder": False},
    {"id": "AGB_GEN2",     "course_number": "AGB Elec.", "title": "Agribusiness General Elective",          "units": 3, "category": "major",         "grid_col": 5, "grid_row": 2, "prerequisites": [],              "quarter_equivalents": [],           "elective_key": "agb_general_elective", "is_placeholder": True},
    {"id": "AGB_GE_UD3",   "course_number": "GE UD-3",  "title": "Upper-Division Arts and Humanities",     "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 3, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},
    {"id": "AGB_GE_UD4",   "course_number": "GE UD-4",  "title": "Upper-Division Social Sciences",         "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 4, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "AGB_GEN3",     "course_number": "AGB Elec.", "title": "Agribusiness General Elective",          "units": 3, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": [],              "quarter_equivalents": [],           "elective_key": "agb_general_elective", "is_placeholder": True},
    {"id": "AGB_GEN4",     "course_number": "AGB Elec.", "title": "Agribusiness General Elective",          "units": 3, "category": "major",         "grid_col": 6, "grid_row": 1, "prerequisites": [],              "quarter_equivalents": [],           "elective_key": "agb_general_elective", "is_placeholder": True},
    {"id": "AGB_CAFES2",   "course_number": "CAFES",     "title": "CAFES Prefix Elective",                 "units": 3, "category": "support",       "grid_col": 6, "grid_row": 2, "prerequisites": [],              "quarter_equivalents": [],           "elective_key": "agb_cafes_prefix_elective", "is_placeholder": True},
    {"id": "AGB_GE5A",     "course_number": "GE 5A",     "title": "Life Sciences",                         "units": 3, "category": "ge",            "grid_col": 6, "grid_row": 3, "prerequisites": [],              "quarter_equivalents": ["BIO 111", "BIO 1111"], "is_placeholder": True},
    {"id": "AGB_FREE1",    "course_number": "Free",      "title": "Free Elective",                         "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 4, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "AGB4462",      "course_number": "AGB 4462 / AGB 4463", "title": "Senior Project",               "units": 3, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": [],              "quarter_equivalents": ["AGB 462", "AGB 463", "AGB 4462", "AGB 4463"], "elective_key": "agb_senior_project", "is_placeholder": True},
    {"id": "AGB_GEN5",     "course_number": "AGB 4000",  "title": "4000-Level Agribusiness Elective",       "units": 3, "category": "major",         "grid_col": 7, "grid_row": 1, "prerequisites": [],              "quarter_equivalents": [],           "elective_key": "agb_4000_elective", "is_placeholder": True},
    {"id": "AGB_GE5B",     "course_number": "GE 5B",     "title": "Physical Sciences",                     "units": 3, "category": "ge",            "grid_col": 7, "grid_row": 2, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},
    {"id": "AGB_FREE2",    "course_number": "Free",      "title": "Free Elective",                         "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 3, "prerequisites": [],              "quarter_equivalents": [],           "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# ANIMAL SCIENCE (BS) — General Curriculum (120 units)
# Source: catalog.calpoly.edu/agriculture-food-environmental-sciences/animal-science/animal-science-bs/
# ─────────────────────────────────────────────────────────────────────────────
ASCI_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "ASCI_ASCI1100", "course_number": "ASCI 1100", "title": "Introduction to the Animal Sciences", "units": 1, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ASCI 101"], "is_placeholder": False},
    {"id": "ASCI_ASCI1101", "course_number": "ASCI 1101", "title": "Principles of Animal Physiology", "units": 3, "category": "major", "grid_col": 0, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ASCI 112"], "is_placeholder": False},
    {"id": "ASCI_MATH1006", "course_number": "MATH 1006", "title": "College Algebra", "units": 3, "category": "support", "grid_col": 0, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["MATH 118"], "is_placeholder": False},
    {"id": "ASCI_GE1A", "course_number": "GE 1A", "title": "Written Communication", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "ASCI_GE1C", "course_number": "GE 1C", "title": "Oral Communication", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 4, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},
    {"id": "ASCI_GE_LD1", "course_number": "GE", "title": "General Education Requirement", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "ASCI_ASCI1102", "course_number": "ASCI 1102", "title": "Animal Management Systems", "units": 3, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ASCI 112"], "is_placeholder": False},
    {"id": "ASCI_ASCI1103", "course_number": "ASCI 1103", "title": "Animal Science Laboratory", "units": 1, "category": "major", "grid_col": 1, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ASCI 112"], "is_placeholder": False},
    {"id": "ASCI_BIO1151", "course_number": "BIO 1151", "title": "Life: Molecules and Cells", "units": 4, "category": "support", "grid_col": 1, "grid_row": 2, "prerequisites": [], "quarter_equivalents": ["BIO 161"], "is_placeholder": False},
    {"id": "ASCI_CHEM1120", "course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure and Properties", "units": 4, "category": "support", "grid_col": 1, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["CHEM 124"], "is_placeholder": False},
    {"id": "ASCI_GE1B", "course_number": "GE 1B", "title": "Critical Thinking", "units": 3, "category": "ge", "grid_col": 1, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "ASCI_ASCI2210_2211", "course_number": "ASCI 2210/2211", "title": "Meat Science and Meat Science Laboratory", "units": 3, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ASCI 211"], "is_placeholder": True},
    {"id": "ASCI_STAT1110", "course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3, "category": "support", "grid_col": 2, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["STAT 218"], "is_placeholder": False},
    {"id": "ASCI_MGMT1", "course_number": "Animal Mgmt 1", "title": "Animal Management Elective", "units": 3, "category": "major", "grid_col": 2, "grid_row": 2, "prerequisites": ["ASCI 1101", "ASCI 1102", "ASCI 1103"], "quarter_equivalents": ["ASCI 221", "ASCI 222", "ASCI 223", "ASCI 224", "ASCI 225", "ASCI 227"], "is_placeholder": True},
    {"id": "ASCI_GE_LD2", "course_number": "GE 3A", "title": "Arts", "units": 3, "category": "ge", "grid_col": 2, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ASCI_GE_LD3", "course_number": "GE 3B", "title": "Humanities", "units": 3, "category": "ge", "grid_col": 2, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "ASCI_ASCI2220", "course_number": "ASCI 2220", "title": "Animal Nutrition and Feeding", "units": 3, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["ASCI 1101", "BIO 1151", "CHEM 1120"], "quarter_equivalents": ["ASCI 220"], "is_placeholder": False},
    {"id": "ASCI_ASCI2229", "course_number": "ASCI 2229", "title": "Anatomy and Physiology of Farm Animals", "units": 3, "category": "major", "grid_col": 3, "grid_row": 1, "prerequisites": ["ASCI 1101", "BIO 1151"], "quarter_equivalents": ["ASCI 229"], "is_placeholder": False},
    {"id": "ASCI_MGMT2", "course_number": "Animal Mgmt 2", "title": "Animal Management Elective", "units": 3, "category": "major", "grid_col": 3, "grid_row": 2, "prerequisites": ["ASCI 1101", "ASCI 1102", "ASCI 1103"], "quarter_equivalents": ["ASCI 221", "ASCI 222", "ASCI 223", "ASCI 224", "ASCI 225", "ASCI 227"], "is_placeholder": True},
    {"id": "ASCI_ENTERPRISE", "course_number": "Enterprise", "title": "Enterprise Elective", "units": 3, "category": "major", "grid_col": 3, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ASCI 212"], "is_placeholder": True},
    {"id": "ASCI_FREE1", "course_number": "Free", "title": "Free Elective", "units": 3, "category": "concentration", "grid_col": 3, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ASCI_ASCI3302", "course_number": "ASCI 3302", "title": "Animal Genetics", "units": 3, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": ["BIO 1151", "STAT 1110"], "quarter_equivalents": ["ASCI 302"], "is_placeholder": False},
    {"id": "ASCI_CHEM2240", "course_number": "CHEM 2240 / CHEM 2242", "title": "Organic Chemistry: Fundamentals and Applications or Organic Chemistry I", "units": 4, "category": "support", "grid_col": 4, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["CHEM 216", "CHEM 312", "CHEM 2240", "CHEM 2242"], "elective_key": "asci_org_chem", "is_placeholder": True},
    {"id": "ASCI_APPROVED1", "course_number": "ASCI/DSCI 3000+", "title": "Approved Elective", "units": 3, "category": "major", "grid_col": 4, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ASCI_FREE2", "course_number": "Free 2", "title": "Free Elective", "units": 4, "category": "concentration", "grid_col": 4, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ASCI_GE_LD4", "course_number": "GE 4A", "title": "American Institutions", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ASCI_ASCI3304", "course_number": "ASCI 3304", "title": "Animal Genomics", "units": 2, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["ASCI 3302"], "quarter_equivalents": ["ASCI 304"], "is_placeholder": False},
    {"id": "ASCI_ASCI3340", "course_number": "ASCI 3340", "title": "Animal Welfare and Ethics", "units": 3, "category": "major", "grid_col": 5, "grid_row": 1, "prerequisites": [], "quarter_equivalents": ["ASCI 340"], "is_placeholder": False},
    {"id": "ASCI_ASCI3351", "course_number": "ASCI 3351", "title": "Mechanisms of Hormone Action and Reproductive Physiology", "units": 3, "category": "major", "grid_col": 5, "grid_row": 2, "prerequisites": ["ASCI 2229"], "quarter_equivalents": ["ASCI 351"], "is_placeholder": False},
    {"id": "ASCI_ASCI3363", "course_number": "ASCI 3363", "title": "Professional Development in the Animal Sciences", "units": 1, "category": "major", "grid_col": 5, "grid_row": 3, "prerequisites": [], "quarter_equivalents": ["ASCI 363"], "is_placeholder": False},
    {"id": "ASCI_GE_LD5", "course_number": "GE 4B", "title": "Social and Behavioral Sciences", "units": 3, "category": "ge", "grid_col": 5, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ASCI_FREE3", "course_number": "Free 3", "title": "Free Elective", "units": 4, "category": "concentration", "grid_col": 5, "grid_row": 5, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ASCI_NUTRITION", "course_number": "Nutrition", "title": "Nutrition Elective", "units": 3, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["ASCI 2220"], "quarter_equivalents": ["ASCI 346", "ASCI 350", "ASCI 355", "ASCI 419"], "is_placeholder": True},
    {"id": "ASCI_PHYSIOLOGY", "course_number": "Physiology", "title": "Physiology Elective", "units": 4, "category": "major", "grid_col": 6, "grid_row": 1, "prerequisites": ["ASCI 2229"], "quarter_equivalents": ["ASCI 403", "ASCI 405", "ASCI 406", "ASCI 438", "ASCI 440", "ASCI 455"], "is_placeholder": True},
    {"id": "ASCI_APPROVED2", "course_number": "ASCI/DSCI 3000+ 2", "title": "Approved Elective", "units": 3, "category": "major", "grid_col": 6, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ASCI_APPROVED3", "course_number": "ASCI/DSCI 3000+ 3", "title": "Approved Elective", "units": 3, "category": "major", "grid_col": 6, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ASCI_GE_UD3", "course_number": "GE UD-3", "title": "Upper-Division Arts and Humanities", "units": 3, "category": "ge", "grid_col": 6, "grid_row": 4, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ASCI_SENIOR_PROJECT", "course_number": "ASCI 4477/4478/4479", "title": "Senior Project", "units": 2, "category": "major", "grid_col": 7, "grid_row": 0, "prerequisites": ["ASCI 3363"], "quarter_equivalents": ["ASCI 477", "ASCI 478", "ASCI 479"], "is_placeholder": True},
    {"id": "ASCI_BIOCHEM", "course_number": "Biochemistry", "title": "Biochemistry Elective", "units": 4, "category": "support", "grid_col": 7, "grid_row": 1, "prerequisites": ["ASCI 2229", "CHEM 2240 / CHEM 2242"], "quarter_equivalents": ["ASCI 319", "CHEM 319", "CHEM 369", "ASCI 3319", "CHEM 3350", "CHEM 3352"], "elective_key": "asci_biochem_elective", "is_placeholder": True},
    {"id": "ASCI_APPROVED4", "course_number": "ASCI/DSCI 3000+ 4", "title": "Approved Elective", "units": 3, "category": "major", "grid_col": 7, "grid_row": 2, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ASCI_GE_UD4", "course_number": "GE UD-4", "title": "Upper-Div Social Sciences", "units": 3, "category": "ge", "grid_col": 7, "grid_row": 3, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# ARCHITECTURAL ENGINEERING (BS) — General Curriculum (128 units)
# Source: catalog.calpoly.edu/architecture-environmental-design/architectural-engineering/architectural-engineering-bs/
# ─────────────────────────────────────────────────────────────────────────────
ARCE_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "ARCE_1110",      "course_number": "ARCE 1110",     "title": "Introduction to Architectural Engineering",       "units": 2, "category": "major",         "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["ARCE 110"],              "is_placeholder": False},
    {"id": "ARCE_ARCH1101",  "course_number": "ARCH 1101",     "title": "Architectural Design I",                          "units": 3, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["ARCH 101"],              "is_placeholder": False},
    {"id": "ARCE_ARCH1131",  "course_number": "ARCH 1131",     "title": "Architectural Representation I",                  "units": 3, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["ARCH 131"],              "is_placeholder": False},
    {"id": "ARCE_MATH1261",  "course_number": "MATH 1261",     "title": "Calculus I",                                      "units": 4, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["MATH 141"],              "is_placeholder": False},
    {"id": "ARCE_PHYS1141",  "course_number": "PHYS 1141",     "title": "General Physics I",                               "units": 4, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["PHYS 141"],              "is_placeholder": False},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "ARCE_1121",      "course_number": "ARCE 1121",     "title": "Structural Principles I",                         "units": 3, "category": "major",         "grid_col": 1, "grid_row": 0, "prerequisites": ["ARCE 1110"],                   "quarter_equivalents": ["ARCE 121"],              "is_placeholder": False},
    {"id": "ARCE_MATH1262",  "course_number": "MATH 1262",     "title": "Calculus II",                                     "units": 4, "category": "support",       "grid_col": 1, "grid_row": 0, "prerequisites": ["MATH 1261"],                   "quarter_equivalents": ["MATH 142"],              "is_placeholder": False},
    {"id": "ARCE_PHYS1143",  "course_number": "PHYS 1143",     "title": "General Physics II",                              "units": 4, "category": "support",       "grid_col": 1, "grid_row": 0, "prerequisites": ["PHYS 1141", "MATH 1261"],       "quarter_equivalents": ["PHYS 132"],              "is_placeholder": False},
    {"id": "ARCE_GE1A",      "course_number": "GE 1A",         "title": "Written Communication",                           "units": 3, "category": "ge",            "grid_col": 1, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "ARCE_GE1C",      "course_number": "GE 1C",         "title": "Oral Communication",                              "units": 3, "category": "ge",            "grid_col": 1, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["COMS 101"],              "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "ARCE_2211",      "course_number": "ARCE 2211",     "title": "Structural Principles II",                        "units": 3, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": ["ARCE 1121"],                   "quarter_equivalents": ["ARCE 211"],              "is_placeholder": False},
    {"id": "ARCE_2212",      "course_number": "ARCE 2212",     "title": "Structural Principles II Laboratory",             "units": 1, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": ["ARCE 1121"],                   "quarter_equivalents": ["ARCE 212"],              "is_placeholder": False},
    {"id": "ARCE_CM1115",    "course_number": "CM 1115",       "title": "Fundamentals of Construction Management",        "units": 4, "category": "support",       "grid_col": 2, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["CM 115"],                "is_placeholder": False},
    {"id": "ARCE_CSC1031",   "course_number": "CSC 1031",      "title": "Programming for Engineers",                       "units": 2, "category": "support",       "grid_col": 2, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": False},
    {"id": "ARCE_MATH2341",  "course_number": "MATH 2341",     "title": "Linear Analysis",                                 "units": 4, "category": "support",       "grid_col": 2, "grid_row": 0, "prerequisites": ["MATH 1262"],                   "quarter_equivalents": ["MATH 244"],              "is_placeholder": False},
    {"id": "ARCE_GE1B",      "course_number": "GE 1B",         "title": "Critical Thinking",                               "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "ARCE_2222",      "course_number": "ARCE 2222",     "title": "Structural Systems Laboratory",                   "units": 2, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": ["ARCE 2211"],                   "quarter_equivalents": ["ARCE 222"],              "is_placeholder": False},
    {"id": "ARCE_2223",      "course_number": "ARCE 2223",     "title": "Structural Drawings",                             "units": 2, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": ["ARCE 2211"],                   "quarter_equivalents": ["ARCE 223"],              "is_placeholder": False},
    {"id": "ARCE_HIST",      "course_number": "ARCH 2221 / ARCH 2222 / ARCE 2280", "title": "History of World Architecture I, II, or History of Structures", "units": 3, "category": "support", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ARCH 221", "ARCH 2221", "ARCH 222", "ARCH 2222", "ARCE 280", "ARCE 2280"], "elective_key": "arce_hist_elective", "is_placeholder": True},
    {"id": "ARCE_FE_TE1",    "course_number": "FE Tech Elec.", "title": "FE Technical Elective",                           "units": 3, "category": "concentration", "grid_col": 3, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},
    {"id": "ARCE_GE3A",      "course_number": "GE 3A",         "title": "Arts",                                            "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},
    {"id": "ARCE_GE3B",      "course_number": "GE 3B",         "title": "Humanities",                                      "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ARCE_3311",      "course_number": "ARCE 3311",     "title": "Structural Analysis",                             "units": 3, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": ["ARCE 2211"],                   "quarter_equivalents": ["ARCE 311"],              "is_placeholder": False},
    {"id": "ARCE_3312",      "course_number": "ARCE 3312",     "title": "Structural Analysis Laboratory",                  "units": 1, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": ["ARCE 2211"],                   "quarter_equivalents": ["ARCE 312"],              "is_placeholder": False},
    {"id": "ARCE_3331",      "course_number": "ARCE 3331",     "title": "Timber Design",                                   "units": 2, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": ["ARCE 2211"],                   "quarter_equivalents": ["ARCE 331"],              "is_placeholder": False},
    {"id": "ARCE_3353",      "course_number": "ARCE 3353",     "title": "Soil Mechanics and Foundation Design",            "units": 4, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": ["MATH 2341"],                   "quarter_equivalents": ["ARCE 353"],              "is_placeholder": False},
    {"id": "ARCE_CHEM1120",  "course_number": "CHEM 1120",     "title": "Fundamentals of Chemical Structure",              "units": 4, "category": "support",       "grid_col": 4, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["CHEM 124"],              "is_placeholder": False},
    {"id": "ARCE_GE4A",      "course_number": "GE 4A",         "title": "American Institutions",                           "units": 3, "category": "ge",            "grid_col": 4, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ARCE_3332",      "course_number": "ARCE 3332",     "title": "Timber Design and Constructability Laboratory",   "units": 2, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": ["ARCE 3331"],                   "quarter_equivalents": ["ARCE 332"],              "is_placeholder": False},
    {"id": "ARCE_3341",      "course_number": "ARCE 3341",     "title": "Steel Design",                                    "units": 2, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": ["ARCE 3311"],                   "quarter_equivalents": ["ARCE 341"],              "is_placeholder": False},
    {"id": "ARCE_4411",      "course_number": "ARCE 4411",     "title": "Structural Dynamics",                             "units": 3, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": ["ARCE 3311"],                   "quarter_equivalents": ["ARCE 411"],              "is_placeholder": False},
    {"id": "ARCE_4412",      "course_number": "ARCE 4412",     "title": "Structural Dynamics Computing Laboratory",        "units": 1, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": ["ARCE 3311"],                   "quarter_equivalents": ["ARCE 412"],              "is_placeholder": False},
    {"id": "ARCE_GE4B",      "course_number": "GE 4B",         "title": "Social and Behavioral Sciences",                  "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},
    {"id": "ARCE_GE6",       "course_number": "GE 6",          "title": "Ethnic Studies",                                  "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["ES 253", "ES 1112"],     "is_placeholder": True},
    {"id": "ARCE_GE_UD3",    "course_number": "GE UD-3",       "title": "Upper-Division Arts and Humanities",              "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ARCE_4413",      "course_number": "ARCE 4413",     "title": "Seismic Analysis and Design",                     "units": 3, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": ["ARCE 4411"],                   "quarter_equivalents": ["ARCE 413"],              "is_placeholder": False},
    {"id": "ARCE_4442",      "course_number": "ARCE 4442",     "title": "Steel Structures Design Laboratory",              "units": 2, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": ["ARCE 3341"],                   "quarter_equivalents": ["ARCE 442"],              "is_placeholder": False},
    {"id": "ARCE_4461",      "course_number": "ARCE 4461",     "title": "Reinforced Concrete and Masonry Design",          "units": 4, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": ["ARCE 3311"],                   "quarter_equivalents": ["ARCE 461"],              "is_placeholder": False},
    {"id": "ARCE_SURVEY",    "course_number": "Survey Elec.",  "title": "FE/PE Surveying Elective",                        "units": 3, "category": "support",       "grid_col": 6, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "elective_key": "arce_surveying_elective", "is_placeholder": True},
    {"id": "ARCE_FE_TE2",    "course_number": "FE Tech Elec.", "title": "FE Technical Elective",                           "units": 3, "category": "support",       "grid_col": 6, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ARCE_4421",      "course_number": "ARCE 4421",     "title": "Architectural Engineering Building Systems",      "units": 2, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": ["ARCE 4411"],                   "quarter_equivalents": ["ARCE 421"],              "is_placeholder": False},
    {"id": "ARCE_4462",      "course_number": "ARCE 4462",     "title": "Senior Project",                                  "units": 2, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": ["ARCE 4461"],                   "quarter_equivalents": ["ARCE 462"],              "is_placeholder": False},
    {"id": "ARCE_STAT3210",  "course_number": "STAT 3210",     "title": "Engineering Statistics",                          "units": 3, "category": "support",       "grid_col": 7, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["STAT 312"],              "is_placeholder": False},
    {"id": "ARCE_ELEC",      "course_number": "ARCE Elective", "title": "ARCE Upper-Division Elective",                    "units": 3, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},
    {"id": "ARCE_CAED",      "course_number": "CAED Elective", "title": "CAED Interdisciplinary Elective",                 "units": 3, "category": "support",       "grid_col": 7, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},
    {"id": "ARCE_GE_UD4",    "course_number": "GE UD-4",       "title": "Upper-Division Social Sciences",                  "units": 3, "category": "ge",            "grid_col": 7, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                        "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# ANTHROPOLOGY AND GEOGRAPHY (BS) - Concentration Curriculum (120 units)
# Source: catalog.calpoly.edu/liberal-arts/social-sciences/anthropology-geography-bs/
# ─────────────────────────────────────────────────────────────────────────────
ANTGEOG_FLOWCHART: list[Course] = [
    # Freshman Fall
    {"id": "ANTGEOG_ANT2201", "course_number": "ANT 2201", "title": "Cultural Anthropology", "units": 3, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ANT 201"], "is_placeholder": False},
    {"id": "ANTGEOG_GEOG1150", "course_number": "GEOG 1150", "title": "Human Geography", "units": 3, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["GEOG 150"], "is_placeholder": False},
    {"id": "ANTGEOG_LDC1", "course_number": "Lower-Division C", "title": "Lower-Division C or Elective", "units": 3, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE1A", "course_number": "GE 1A", "title": "Written Communication", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "ANTGEOG_GE1C", "course_number": "GE 1C", "title": "Oral Communication", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # Freshman Spring
    {"id": "ANTGEOG_ANT2250", "course_number": "ANT 2250", "title": "Biological Anthropology", "units": 3, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ANT 250"], "is_placeholder": False},
    {"id": "ANTGEOG_STAT1110", "course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["STAT 217"], "is_placeholder": False},
    {"id": "ANTGEOG_LDC2", "course_number": "Lower-Division C 2", "title": "Lower-Division C or Elective", "units": 3, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE1B", "course_number": "GE 1B", "title": "Critical Thinking", "units": 3, "category": "ge", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE3A", "course_number": "GE 3A", "title": "Arts", "units": 3, "category": "ge", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Sophomore Fall
    {"id": "ANTGEOG_ANT2202", "course_number": "ANT 2202", "title": "World History Before Writing", "units": 3, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ANT 202"], "is_placeholder": False},
    {"id": "ANTGEOG_ANT3307", "course_number": "ANT 3307", "title": "World Prehistory", "units": 4, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["ANT 2202"], "quarter_equivalents": ["ANT 307"], "is_placeholder": False},
    {"id": "ANTGEOG_GEOG2202", "course_number": "GEOG 2202", "title": "Earth Surface Processes", "units": 4, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["GEOG 202"], "is_placeholder": False},
    {"id": "ANTGEOG_GE2", "course_number": "GE 2", "title": "Mathematics and Quantitative Reasoning", "units": 3, "category": "ge", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Sophomore Spring
    {"id": "ANTGEOG_ANT3327", "course_number": "ANT 3327", "title": "Human Ecology", "units": 4, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["ANT 2201"], "quarter_equivalents": ["ANT 327"], "is_placeholder": False},
    {"id": "ANTGEOG_GEOG2261", "course_number": "GEOG 2261", "title": "Economic Geography", "units": 3, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ANTGEOG_GE3B", "course_number": "GE 3B", "title": "Humanities", "units": 3, "category": "ge", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE4A", "course_number": "GE 4A", "title": "American Institutions", "units": 3, "category": "ge", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE5A", "course_number": "GE 5A", "title": "Physical Sciences", "units": 3, "category": "ge", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Junior Fall
    {"id": "ANTGEOG_ANT3303", "course_number": "ANT 3303", "title": "Research Methods in Cultural Anthropology", "units": 4, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": ["ANT 2201"], "quarter_equivalents": ["ANT 303"], "is_placeholder": False},
    {"id": "ANTGEOG_ANT3310", "course_number": "ANT 3310", "title": "Archaeological Methods", "units": 4, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": ["ANT 2202"], "quarter_equivalents": ["ANT 310"], "is_placeholder": False},
    {"id": "ANTGEOG_GEOG3320", "course_number": "GEOG 3320", "title": "Applications in GIS", "units": 4, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": ["GEOG 1150"], "quarter_equivalents": ["GEOG 350"], "is_placeholder": False},
    {"id": "ANTGEOG_GE4B", "course_number": "GE 4B", "title": "Social and Behavioral Sciences", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Junior Spring
    {"id": "ANTGEOG_ANT3360", "course_number": "ANT 3360", "title": "Human Cultural Adaptations", "units": 4, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["ANT 2201"], "quarter_equivalents": ["ANT 360"], "is_placeholder": False},
    {"id": "ANTGEOG_GEOG3350", "course_number": "GEOG 3350", "title": "Methods in Human Geography", "units": 4, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["GEOG 1150"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ANTGEOG_CON_JRS1", "course_number": "Concentration", "title": "Concentration Course", "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_CON_JRS2", "course_number": "Concentration 2", "title": "Concentration Course", "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Senior Fall
    {"id": "ANTGEOG_GEOG4410", "course_number": "GEOG 4410", "title": "Advanced Applications in GIS", "units": 4, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["GEOG 3320"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ANTGEOG_ANTGEOG4461", "course_number": "ANT 4461 / GEOG 4461", "title": "Anthropology or Geography Senior Project I", "units": 3, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["ANT 3303", "GEOG 3350"], "quarter_equivalents": ["ANT 4461", "GEOG 4461", "ANT 461", "GEOG 461"], "elective_key": "antgeog_senior_project_i", "is_placeholder": True},
    {"id": "ANTGEOG_CON_SRF1", "course_number": "Concentration 3", "title": "Concentration Course", "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_CON_SRF2", "course_number": "Concentration 4", "title": "Concentration Course", "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE5B", "course_number": "GE 5B", "title": "Life Sciences", "units": 3, "category": "ge", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE5C", "course_number": "GE 5C", "title": "Laboratory", "units": 1, "category": "ge", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Senior Spring
    {"id": "ANTGEOG_ANTGEOG4462", "course_number": "ANT 4462 / GEOG 4462", "title": "Anthropology or Geography Senior Project II", "units": 4, "category": "major", "grid_col": 7, "grid_row": 0, "prerequisites": ["ANT 4461 / GEOG 4461"], "quarter_equivalents": ["ANT 4462", "GEOG 4462", "ANT 462", "GEOG 462"], "elective_key": "antgeog_senior_project_ii", "is_placeholder": True},
    {"id": "ANTGEOG_CON_SRS1", "course_number": "Concentration 5", "title": "Concentration Course", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_FREE1", "course_number": "Free", "title": "Free Elective", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE_UD3", "course_number": "GE UD-3", "title": "Upper-Division Arts and Humanities", "units": 3, "category": "ge", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ANTGEOG_GE6", "course_number": "GE 6", "title": "Ethnic Studies", "units": 3, "category": "ge", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# ARCHITECTURE (BARCH) - Five-Year Professional Curriculum (150 units)
# Source: catalog.calpoly.edu/architecture-environmental-design/architecture/architecture-barch/
# ─────────────────────────────────────────────────────────────────────────────
ARCH_FLOWCHART: list[Course] = [
    # First Year - Term 1
    {"id": "ARCH_ARCH1101", "course_number": "ARCH 1101", "title": "Architectural Design I", "units": 4, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ARCH 131"], "is_placeholder": False},
    {"id": "ARCH_ARCH1131", "course_number": "ARCH 1131", "title": "Architectural Representation I", "units": 2, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ARCH 101"], "is_placeholder": False},
    {"id": "ARCH_EDES1123", "course_number": "EDES 1123", "title": "Place, People, and the Built Environment", "units": 3, "category": "support", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ARCH_MATH_CHOICE", "course_number": "MATH 1007 / MATH 1261", "title": "Precalculus or Calculus I", "units": 3, "category": "support", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["MATH 1007", "MATH 1261", "MATH 119", "MATH 141"], "elective_key": "arch_precalc_or_calculus", "is_placeholder": True},
    {"id": "ARCH_GE1A", "course_number": "GE 1A", "title": "Written Communication", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # First Year - Term 2
    {"id": "ARCH_ARCH1102", "course_number": "ARCH 1102", "title": "Architectural Design II", "units": 4, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": ["ARCH 1101"], "quarter_equivalents": ["ARCH 132"], "is_placeholder": False},
    {"id": "ARCH_ARCH1121", "course_number": "ARCH 1121", "title": "Equity, Social Justice, and Architecture", "units": 3, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ARCH_ARCH1132", "course_number": "ARCH 1132", "title": "Architectural Representation II", "units": 2, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": ["ARCH 1101"], "quarter_equivalents": ["ARCH 133"], "is_placeholder": False},
    {"id": "ARCH_PHYS_CHOICE", "course_number": "PHYS 1121 / PHYS 1141", "title": "College Physics I or General Physics I", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": ["MATH 1007 / MATH 1261"], "quarter_equivalents": ["PHYS 1121", "PHYS 1141", "PHYS 121", "PHYS 141"], "elective_key": "arch_physics_i", "is_placeholder": True},
    {"id": "ARCH_GE1C", "course_number": "GE 1C", "title": "Oral Communication", "units": 3, "category": "ge", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # Second Year - Term 1
    {"id": "ARCH_ARCH2201", "course_number": "ARCH 2201", "title": "Architectural Design III", "units": 5, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["ARCH 1102"], "quarter_equivalents": ["ARCH 251"], "is_placeholder": False},
    {"id": "ARCH_ARCH2221", "course_number": "ARCH 2221", "title": "History of World Architecture I: Prehistory to 17th Century", "units": 3, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ARCH 217"], "is_placeholder": False},
    {"id": "ARCH_ARCH2231", "course_number": "ARCH 2231", "title": "Architectural Representation III", "units": 1, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["ARCH 1102"], "quarter_equivalents": ["ARCH 207"], "is_placeholder": False},
    {"id": "ARCH_ARCH2241", "course_number": "ARCH 2241", "title": "Architectural Technology Fundamentals I", "units": 4, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["ARCH 1101"], "quarter_equivalents": ["ARCH 241"], "is_placeholder": False},
    {"id": "ARCH_ARCE1121", "course_number": "ARCE 1121", "title": "Structural Principles I", "units": 3, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": ["PHYS 1121 / PHYS 1141", "MATH 1007 / MATH 1261"], "quarter_equivalents": ["ARCE 211"], "is_placeholder": False},

    # Second Year - Term 2
    {"id": "ARCH_ARCH2202", "course_number": "ARCH 2202", "title": "Architectural Design IV", "units": 5, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["ARCH 2201"], "quarter_equivalents": ["ARCH 252"], "is_placeholder": False},
    {"id": "ARCH_ARCH2222", "course_number": "ARCH 2222", "title": "History of World Architecture II: 17th Century to the Present", "units": 3, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ARCH 218"], "is_placeholder": False},
    {"id": "ARCH_ARCH2232", "course_number": "ARCH 2232", "title": "Architectural Representation IV", "units": 1, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["ARCH 2201"], "quarter_equivalents": ["ARCH 253"], "is_placeholder": False},
    {"id": "ARCH_ARCH2242", "course_number": "ARCH 2242", "title": "Architectural Technology Fundamentals II", "units": 4, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["ARCH 2241"], "quarter_equivalents": ["ARCH 242"], "is_placeholder": False},
    {"id": "ARCH_ARCE3301", "course_number": "ARCE 3301", "title": "Introduction to Structural Systems", "units": 4, "category": "support", "grid_col": 3, "grid_row": 0, "prerequisites": ["ARCE 1121"], "quarter_equivalents": ["ARCE 315"], "is_placeholder": False},

    # Third Year - Term 1
    {"id": "ARCH_ARCH3331", "course_number": "ARCH 3331", "title": "Building Information Modeling", "units": 2, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ARCH 353"], "is_placeholder": False},
    {"id": "ARCH_ARCH3341", "course_number": "ARCH 3341", "title": "Architectural Systems Integration I", "units": 4, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": ["ARCH 2242"], "quarter_equivalents": ["ARCH 341"], "is_placeholder": False},
    {"id": "ARCH_ARCH4401_1", "course_number": "ARCH 4401", "title": "Advanced Architectural Design", "units": 5, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": ["ARCH 2202", "ARCH 2232", "ARCH 2242", "PHYS 1121 / PHYS 1141", "MATH 1007 / MATH 1261"], "quarter_equivalents": ["ARCH 351"], "is_placeholder": False},
    {"id": "ARCH_GE1B", "course_number": "GE 1B", "title": "Critical Thinking", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ARCH_GE3B", "course_number": "GE 3B", "title": "Humanities", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Third Year - Term 2
    {"id": "ARCH_ARCH3301", "course_number": "ARCH 3301", "title": "Integrated Architectural Design", "units": 5, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["ARCE 3301", "ARCH 2202", "ARCH 3341"], "quarter_equivalents": ["ARCH 352"], "is_placeholder": False},
    {"id": "ARCH_ARCH3342", "course_number": "ARCH 3342", "title": "Architectural Systems Integration II", "units": 5, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["ARCH 3341"], "quarter_equivalents": ["ARCH 342"], "is_placeholder": False},
    {"id": "ARCH_ARCH4425", "course_number": "ARCH 4425", "title": "Seminar in Architectural History, Theory and Criticism", "units": 3, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["ARCH 1121", "ARCH 2221", "ARCH 2222"], "quarter_equivalents": ["ARCH 420"], "is_placeholder": False},
    {"id": "ARCH_GE4A", "course_number": "GE 4A", "title": "American Institutions", "units": 3, "category": "ge", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Fourth Year - Term 1
    {"id": "ARCH_ARCH4401_2", "course_number": "ARCH 4401 (2)", "title": "Advanced Architectural Design", "units": 5, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["ARCH 4401"], "quarter_equivalents": ["ARCH 351"], "is_placeholder": False},
    {"id": "ARCH_PROF_ELEC1", "course_number": "Professional Elective 1", "title": "Professional Elective", "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ARCH_PROF_ELEC2", "course_number": "Professional Elective 2", "title": "Professional Elective", "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ARCH_GE5B", "course_number": "GE 5B", "title": "Life Sciences", "units": 3, "category": "ge", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Fourth Year - Term 2
    {"id": "ARCH_ARCH4401_3", "course_number": "ARCH 4401 (3)", "title": "Advanced Architectural Design", "units": 5, "category": "major", "grid_col": 7, "grid_row": 0, "prerequisites": ["ARCH 4401 (2)"], "quarter_equivalents": ["ARCH 351"], "is_placeholder": False},
    {"id": "ARCH_PROF_ELEC3", "course_number": "Professional Elective 3", "title": "Professional Elective", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ARCH_PROF_ELEC4", "course_number": "Professional Elective 4", "title": "Professional Elective", "units": 2, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ARCH_GE6", "course_number": "GE 6", "title": "Ethnic Studies", "units": 3, "category": "ge", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # Fifth Year - Term 1
    {"id": "ARCH_ARCH4460", "course_number": "ARCH 4460", "title": "Senior Architectural Thesis Theory and Research Seminar", "units": 3, "category": "major", "grid_col": 8, "grid_row": 0, "prerequisites": ["ARCH 4425"], "quarter_equivalents": ["ARCH 420"], "is_placeholder": False},
    {"id": "ARCH_ARCH4461", "course_number": "ARCH 4461", "title": "Senior Project: Architectural Thesis I", "units": 5, "category": "major", "grid_col": 8, "grid_row": 0, "prerequisites": ["ARCH 3301", "ARCH 4401 (3)"], "quarter_equivalents": ["ARCH 481"], "is_placeholder": False},
    {"id": "ARCH_GE_UD25", "course_number": "GE UD-2/5", "title": "Upper-Division Mathematics or Science", "units": 3, "category": "ge", "grid_col": 8, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "ARCH_GE_UD3", "course_number": "GE UD-3", "title": "Upper-Division Arts and Humanities", "units": 3, "category": "ge", "grid_col": 8, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Fifth Year - Term 2
    {"id": "ARCH_ARCH4441", "course_number": "ARCH 4441", "title": "Issues in Contemporary Professional Practice", "units": 4, "category": "major", "grid_col": 9, "grid_row": 0, "prerequisites": ["ARCH 3342"], "quarter_equivalents": ["ARCH 443"], "is_placeholder": False},
    {"id": "ARCH_ARCH4462", "course_number": "ARCH 4462", "title": "Senior Project: Architectural Thesis II", "units": 5, "category": "major", "grid_col": 9, "grid_row": 0, "prerequisites": ["ARCH 4461"], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "ARCH_GE_UD4", "course_number": "GE UD-4", "title": "Upper-Division Social Sciences", "units": 3, "category": "ge", "grid_col": 9, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# BIOLOGICAL SCIENCES (BS) - General Curriculum in Biology (120 units)
# Source: catalog.calpoly.edu/science-mathematics/biological-sciences/biological-sciences-bs/
# ─────────────────────────────────────────────────────────────────────────────
BIO_FLOWCHART: list[Course] = [
    # Freshman Fall
    {"id": "BIO_BIO1150", "course_number": "BIO 1150", "title": "Life: History and Diversity", "units": 4, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["BIO 150"], "is_placeholder": False},
    {"id": "BIO_CHEM1120", "course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure and Properties", "units": 4, "category": "support", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["CHEM 124"], "is_placeholder": False},
    {"id": "BIO_STAT1110", "course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3, "category": "support", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["STAT 218"], "is_placeholder": False},
    {"id": "BIO_GE1A", "course_number": "GE 1A", "title": "Written Communication", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # Freshman Spring
    {"id": "BIO_BIO1151", "course_number": "BIO 1151", "title": "Life: Molecules and Cells", "units": 4, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["BIO 161"], "is_placeholder": False},
    {"id": "BIO_CHEM1122", "course_number": "CHEM 1122", "title": "Fundamentals of Chemical Reactivity", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": ["CHEM 1120"], "quarter_equivalents": ["CHEM 125"], "is_placeholder": False},
    {"id": "BIO_MATH1264", "course_number": "MATH 1264", "title": "Calculus for Data Science I", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "BIO_GE1B", "course_number": "GE 1B", "title": "Critical Thinking", "units": 3, "category": "ge", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Sophomore Fall
    {"id": "BIO_BIO2253", "course_number": "BIO 2253", "title": "Principles of Ecology and Evolution", "units": 4, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["BIO 1150", "BIO 1151"], "quarter_equivalents": ["BIO 263"], "is_placeholder": False},
    {"id": "BIO_CHEM2240_2242", "course_number": "CHEM 2240/2242", "title": "Organic Chemistry: Fundamentals and Applications or Organic Chemistry I", "units": 4, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": ["CHEM 1122"], "quarter_equivalents": ["CHEM 216", "CHEM 312"], "is_placeholder": True},
    {"id": "BIO_PHYS1121_1141", "course_number": "PHYS 1121/1141", "title": "College Physics I or General Physics I", "units": 4, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["PHYS 121", "PHYS 141"], "is_placeholder": True},
    {"id": "BIO_GE1C", "course_number": "GE 1C", "title": "Oral Communication", "units": 3, "category": "ge", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # Sophomore Spring
    {"id": "BIO_BIO3351", "course_number": "BIO 3351", "title": "Principles of Genetics", "units": 3, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["BIO 1151", "CHEM 1120", "CHEM 1122"], "quarter_equivalents": ["BIO 351"], "is_placeholder": False},
    {"id": "BIO_BIO3352", "course_number": "BIO 3352", "title": "Principles of Animal Physiology", "units": 4, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["BIO 1151", "CHEM 1120", "CHEM 1122"], "quarter_equivalents": ["BIO 361"], "is_placeholder": False},
    {"id": "BIO_TECH_ELEC", "course_number": "Technical Elective", "title": "Technical Elective", "units": 3, "category": "support", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE3A", "course_number": "GE 3A", "title": "Arts", "units": 3, "category": "ge", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Junior Fall
    {"id": "BIO_CON_JRF1", "course_number": "Bioscience Elective", "title": "Bioscience Elective", "units": 4, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_CON_JRF2", "course_number": "Approved Elective", "title": "Approved Elective", "units": 4, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE3B", "course_number": "GE 3B", "title": "Humanities", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE4A", "course_number": "GE 4A", "title": "American Institutions", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_FREE_JRF", "course_number": "Free", "title": "Free Elective", "units": 2, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Junior Spring
    {"id": "BIO_CON_JRS1", "course_number": "4000-level Elective", "title": "4000-level Biology Elective", "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_CON_JRS2", "course_number": "Bioscience Elective 2", "title": "Bioscience Elective", "units": 4, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_CON_JRS3", "course_number": "Approved Elective 2", "title": "Approved Elective", "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE4B", "course_number": "GE 4B", "title": "Social and Behavioral Sciences", "units": 3, "category": "ge", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE6", "course_number": "GE 6", "title": "Ethnic Studies", "units": 3, "category": "ge", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # Senior Fall
    {"id": "BIO_CON_SRF1", "course_number": "4000-level Elective 2", "title": "4000-level Biology Elective", "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_CON_SRF2", "course_number": "4000-level Elective 3", "title": "4000-level Biology Elective", "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_CON_SRF3", "course_number": "Approved Elective 3", "title": "Approved Elective", "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE_UD25", "course_number": "GE UD-2/5", "title": "Upper-Division Mathematics or Science", "units": 3, "category": "ge", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE_UD3", "course_number": "GE UD-3", "title": "Upper-Division Arts and Humanities", "units": 3, "category": "ge", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Senior Spring
    {"id": "BIO_SENIOR_PROJECT", "course_number": "BIO 4461/4462/4463", "title": "Senior Project", "units": 2, "category": "major", "grid_col": 7, "grid_row": 0, "prerequisites": ["STAT 1110"], "quarter_equivalents": ["BIO 461", "BIO 462"], "is_placeholder": True},
    {"id": "BIO_CON_SRS1", "course_number": "Approved Elective 4", "title": "Approved Elective", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_CON_SRS2", "course_number": "Approved Elective 5", "title": "Approved Elective", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_GE_UD4", "course_number": "GE UD-4", "title": "Upper-Division Social Sciences", "units": 3, "category": "ge", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BIO_FREE_SRS", "course_number": "Free 2", "title": "Free Elective", "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# BIOMEDICAL ENGINEERING (BS) - Concentration Not Yet Declared (130 units)
# Source: catalog.calpoly.edu/engineering/biomedical/biomedical-engineering-bs/
# ─────────────────────────────────────────────────────────────────────────────
BMED_FLOWCHART: list[Course] = [
    # Freshman Fall
    {"id": "BMED_BMED1101", "course_number": "BMED 1101", "title": "Introduction to Biomedical Engineering", "units": 3, "category": "major", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["BMED 101"], "is_placeholder": False},
    {"id": "BMED_BIO1151", "course_number": "BIO 1151", "title": "Life: Molecules and Cells", "units": 4, "category": "support", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["BIO 161"], "is_placeholder": False},
    {"id": "BMED_CHEM1120", "course_number": "CHEM 1120", "title": "Fundamentals of Chemical Structure and Properties", "units": 4, "category": "support", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["CHEM 124"], "is_placeholder": False},
    {"id": "BMED_MATH1261", "course_number": "MATH 1261", "title": "Calculus I", "units": 4, "category": "support", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["MATH 141"], "is_placeholder": False},
    {"id": "BMED_GE1A", "course_number": "GE 1A", "title": "Written Communication", "units": 3, "category": "ge", "grid_col": 0, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},

    # Freshman Spring
    {"id": "BMED_BMED2212", "course_number": "BMED 2212", "title": "Biomedical Engineering Fundamentals", "units": 3, "category": "major", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["BMED 212"], "is_placeholder": False},
    {"id": "BMED_CHEM1122", "course_number": "CHEM 1122", "title": "Fundamentals of Chemical Reactivity", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": ["CHEM 1120"], "quarter_equivalents": ["CHEM 125"], "is_placeholder": False},
    {"id": "BMED_MATH1262", "course_number": "MATH 1262", "title": "Calculus II", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": ["MATH 1261"], "quarter_equivalents": ["MATH 142"], "is_placeholder": False},
    {"id": "BMED_PHYS1141", "course_number": "PHYS 1141", "title": "General Physics I", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["PHYS 141"], "is_placeholder": False},
    {"id": "BMED_GE1B", "course_number": "GE 1B", "title": "Critical Thinking", "units": 3, "category": "ge", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Sophomore Fall
    {"id": "BMED_BMED2310", "course_number": "BMED 2310", "title": "Measurement and Analysis of Biomedical Signals", "units": 2, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["MATH 1262", "PHYS 1143"], "quarter_equivalents": ["BMED 310"], "is_placeholder": False},
    {"id": "BMED_BMED2311", "course_number": "BMED 2311", "title": "Measurement and Analysis of Biomedical Signals Laboratory", "units": 1, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": ["MATH 1262", "PHYS 1143"], "quarter_equivalents": ["BMED 310"], "is_placeholder": False},
    {"id": "BMED_ENGR2211", "course_number": "ENGR 2211", "title": "Engineering Mechanics: Statics", "units": 3, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": ["PHYS 1141"], "quarter_equivalents": ["ENGR 211"], "is_placeholder": False},
    {"id": "BMED_MATH2263", "course_number": "MATH 2263", "title": "Calculus III", "units": 4, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 143"], "is_placeholder": False},
    {"id": "BMED_PHYS1143", "course_number": "PHYS 1143", "title": "General Physics II", "units": 4, "category": "support", "grid_col": 2, "grid_row": 0, "prerequisites": ["PHYS 1141", "MATH 1261"], "quarter_equivalents": ["PHYS 132"], "is_placeholder": False},
    {"id": "BMED_GE1C", "course_number": "GE 1C", "title": "Oral Communication", "units": 3, "category": "ge", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["COMS 101"], "is_placeholder": True},

    # Sophomore Spring
    {"id": "BMED_BMED2420", "course_number": "BMED 2420", "title": "Biomaterials", "units": 3, "category": "major", "grid_col": 3, "grid_row": 0, "prerequisites": ["BMED 2212", "CHEM 1120", "ENGR 2211"], "quarter_equivalents": ["BMED 420"], "is_placeholder": False},
    {"id": "BMED_ENGR2212", "course_number": "ENGR 2212", "title": "Engineering Mechanics: Dynamics", "units": 3, "category": "support", "grid_col": 3, "grid_row": 0, "prerequisites": ["ENGR 2211"], "quarter_equivalents": ["ENGR 212"], "is_placeholder": False},
    {"id": "BMED_MATH2341", "course_number": "MATH 2341", "title": "Linear Analysis", "units": 4, "category": "support", "grid_col": 3, "grid_row": 0, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["MATH 244"], "is_placeholder": False},
    {"id": "BMED_GE3A", "course_number": "GE 3A", "title": "Arts", "units": 3, "category": "ge", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_GE4A", "course_number": "GE 4A", "title": "American Institutions", "units": 3, "category": "ge", "grid_col": 3, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Junior Fall
    {"id": "BMED_BMED3102", "course_number": "BMED 3102", "title": "Regulatory Issues in Biomedical Engineering", "units": 1, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": False},
    {"id": "BMED_BMED3430", "course_number": "BMED 3430", "title": "Modeling of Biomedical Systems", "units": 4, "category": "major", "grid_col": 4, "grid_row": 0, "prerequisites": ["MATH 2341"], "quarter_equivalents": ["BMED 430"], "is_placeholder": False},
    {"id": "BMED_STAT3210", "course_number": "STAT 3210", "title": "Engineering Statistics", "units": 3, "category": "support", "grid_col": 4, "grid_row": 0, "prerequisites": ["MATH 1262"], "quarter_equivalents": ["STAT 312"], "is_placeholder": False},
    {"id": "BMED_CON_JRF1", "course_number": "Concentration 1", "title": "Concentration Course or Elective", "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_GE3B", "course_number": "GE 3B", "title": "Humanities", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_GE4B", "course_number": "GE 4B", "title": "Social and Behavioral Sciences", "units": 3, "category": "ge", "grid_col": 4, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Junior Spring
    {"id": "BMED_BIO2231_2232", "course_number": "BIO 2231 / BIO 2232", "title": "Human Anatomy and Physiology I or II", "units": 4, "category": "support", "grid_col": 5, "grid_row": 0, "prerequisites": ["BIO 1151"], "quarter_equivalents": ["BIO 231", "BIO 2231", "BIO 232", "BIO 2232"], "elective_key": "bmed_anat_phys", "is_placeholder": True},
    {"id": "BMED_BMED3410", "course_number": "BMED 3410", "title": "Transport Phenomena in Biomedical Engineering", "units": 3, "category": "major", "grid_col": 5, "grid_row": 0, "prerequisites": ["ENGR 2211", "ENGR 2212"], "quarter_equivalents": ["BMED 410"], "is_placeholder": False},
    {"id": "BMED_ME3341", "course_number": "ME 3341", "title": "Thermodynamics I", "units": 3, "category": "support", "grid_col": 5, "grid_row": 0, "prerequisites": ["ENGR 2212"], "quarter_equivalents": ["ME 341"], "is_placeholder": False},
    {"id": "BMED_CON_JRS1", "course_number": "Concentration 2", "title": "Concentration Course or Elective", "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_GE_UD3", "course_number": "GE UD-3", "title": "Upper-Division Arts and Humanities", "units": 3, "category": "ge", "grid_col": 5, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},

    # Senior Fall
    {"id": "BMED_BMED3425", "course_number": "BMED 3425", "title": "Design for Biomedical Engineering", "units": 4, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["ENGR 2212", "ME 3341"], "quarter_equivalents": ["BMED 425"], "is_placeholder": False},
    {"id": "BMED_BMED4440", "course_number": "BMED 4440", "title": "Biomedical Instrumentation", "units": 3, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["BMED 2310", "BMED 2311"], "quarter_equivalents": ["BMED 440"], "is_placeholder": False},
    {"id": "BMED_BMED4460", "course_number": "BMED 4460", "title": "Stem Cell Bioengineering", "units": 3, "category": "major", "grid_col": 6, "grid_row": 0, "prerequisites": ["BIO 2231 / BIO 2232"], "quarter_equivalents": ["BMED 460"], "is_placeholder": False},
    {"id": "BMED_CON_SRF1", "course_number": "Concentration 3", "title": "Concentration Course or Elective", "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_GE_UD4", "course_number": "GE UD-4", "title": "Upper-Division Social Sciences", "units": 3, "category": "ge", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_GE6", "course_number": "GE 6", "title": "Ethnic Studies", "units": 3, "category": "ge", "grid_col": 6, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["ES 253", "ES 1112"], "is_placeholder": True},

    # Senior Spring
    {"id": "BMED_BMED4599", "course_number": "BMED 4599", "title": "Biomedical Engineering Senior Project", "units": 2, "category": "major", "grid_col": 7, "grid_row": 0, "prerequisites": ["BMED 3425"], "quarter_equivalents": ["BMED 455", "BMED 456"], "is_placeholder": False},
    {"id": "BMED_CON_SRS1", "course_number": "Concentration 4", "title": "Concentration Course or Elective", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_CON_SRS2", "course_number": "Concentration 5", "title": "Concentration Course or Elective", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_GE_UD25", "course_number": "GE UD-2/5", "title": "Upper-Division Mathematics or Science", "units": 3, "category": "ge", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
    {"id": "BMED_FREE1", "course_number": "Free", "title": "Free Elective", "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [], "quarter_equivalents": [], "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# BIOCHEMISTRY (BS) — 120 units
# Source: catalog.calpoly.edu/science-mathematics/chemistry-biochemistry/biochemistry-bs/
# ─────────────────────────────────────────────────────────────────────────────
BIOC_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "BIOC_CHEM1120",      "course_number": "CHEM 1120",       "title": "Fundamentals of Chemical Structure and Properties",    "units": 4, "category": "major",        "grid_col": 0, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["CHEM 124"],            "is_placeholder": False},
    {"id": "BIOC_BIO1151",       "course_number": "BIO 1151",        "title": "Life: Molecules and Cells",                           "units": 4, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["BIO 161"],             "is_placeholder": False},
    {"id": "BIOC_MATH1261",      "course_number": "MATH 1261",       "title": "Calculus I",                                          "units": 4, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["MATH 141"],            "is_placeholder": False},
    {"id": "BIOC_GE1A",          "course_number": "GE 1A",           "title": "Written Communication",                               "units": 3, "category": "ge",           "grid_col": 0, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["ENGL 134", "ENGL 1340"], "is_placeholder": True},
    {"id": "BIOC_FREE1",         "course_number": "Free",            "title": "Free Elective",                                       "units": 1, "category": "concentration", "grid_col": 0, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "BIOC_CHEM1103",      "course_number": "CHEM 1103",       "title": "Research Methods I",                                  "units": 1, "category": "major",        "grid_col": 1, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": False},
    {"id": "BIOC_CHEM1122",      "course_number": "CHEM 1122",       "title": "Fundamentals of Chemical Reactivity",                 "units": 4, "category": "major",        "grid_col": 1, "grid_row": 0, "prerequisites": ["CHEM 1120"],                "quarter_equivalents": ["CHEM 125"],            "is_placeholder": False},
    {"id": "BIOC_MATH1262",      "course_number": "MATH 1262",       "title": "Calculus II",                                         "units": 4, "category": "support",       "grid_col": 1, "grid_row": 0, "prerequisites": ["MATH 1261"],                "quarter_equivalents": ["MATH 142"],            "is_placeholder": False},
    {"id": "BIOC_PHYS1141",      "course_number": "PHYS 1141",       "title": "General Physics I",                                   "units": 4, "category": "support",       "grid_col": 1, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["PHYS 141"],            "is_placeholder": False},
    {"id": "BIOC_GE1C",          "course_number": "GE 1C",           "title": "Oral Communication",                                  "units": 3, "category": "ge",           "grid_col": 1, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["COMS 101"],            "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "BIOC_CHEM2242",      "course_number": "CHEM 2242",       "title": "Organic Chemistry I",                                 "units": 5, "category": "major",        "grid_col": 2, "grid_row": 0, "prerequisites": ["CHEM 1122"],                "quarter_equivalents": ["CHEM 312"],            "is_placeholder": False},
    {"id": "BIOC_MCRO2224",      "course_number": "MCRO 2224",       "title": "General Microbiology I",                              "units": 4, "category": "support",       "grid_col": 2, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["MCRO 224"],            "is_placeholder": False},
    {"id": "BIOC_PHYS1143",      "course_number": "PHYS 1143",       "title": "General Physics II",                                  "units": 4, "category": "support",       "grid_col": 2, "grid_row": 0, "prerequisites": ["PHYS 1141"],                "quarter_equivalents": ["PHYS 132"],            "is_placeholder": False},
    {"id": "BIOC_GE1B",          "course_number": "GE 1B",           "title": "Critical Thinking",                                   "units": 3, "category": "ge",           "grid_col": 2, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "BIOC_CHEM2201_2203", "course_number": "CHEM 2201/2203",  "title": "Undergraduate Research or Research Methods II",        "units": 1, "category": "major",        "grid_col": 3, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_CHEM3330",      "course_number": "CHEM 3330",       "title": "Foundations of Chemical Analysis",                    "units": 4, "category": "major",        "grid_col": 3, "grid_row": 0, "prerequisites": ["CHEM 2242"],                "quarter_equivalents": ["CHEM 301"],            "is_placeholder": False},
    {"id": "BIOC_CHEM3352",      "course_number": "CHEM 3352",       "title": "Biochemistry",                                        "units": 4, "category": "major",        "grid_col": 3, "grid_row": 0, "prerequisites": ["CHEM 2242"],                "quarter_equivalents": ["CHEM 350"],            "is_placeholder": False},
    {"id": "BIOC_GE4A",          "course_number": "GE 4A",           "title": "American Institutions",                               "units": 3, "category": "ge",           "grid_col": 3, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_GE3B",          "course_number": "GE 3B",           "title": "Humanities",                                          "units": 3, "category": "ge",           "grid_col": 3, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "BIOC_CHEM3302",      "course_number": "CHEM 3302",       "title": "Undergraduate Seminar II",                            "units": 1, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": False},
    {"id": "BIOC_CHEM3356",      "course_number": "CHEM 3356",       "title": "Genetic Information Processing",                      "units": 4, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["CHEM 3352"],                "quarter_equivalents": [],                      "is_placeholder": False},
    {"id": "BIOC_CHEM3390",      "course_number": "CHEM 3390",       "title": "Physical Chemistry for Life Sciences",                "units": 3, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["MATH 1262", "PHYS 1141"],   "quarter_equivalents": ["CHEM 371"],            "is_placeholder": False},
    {"id": "BIOC_CHEM3391",      "course_number": "CHEM 3391",       "title": "Physical Chemistry for Life Sciences Laboratory",     "units": 1, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["MATH 1262", "PHYS 1141"],   "quarter_equivalents": [],                      "is_placeholder": False},
    {"id": "BIOC_CON_JRF",       "course_number": "Conc.",           "title": "Concentration or Advanced Elective",                  "units": 4, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_GE6",           "course_number": "GE 6",            "title": "Ethnic Studies",                                      "units": 3, "category": "ge",           "grid_col": 4, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["ES 253", "ES 1112"],   "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "BIOC_CHEM3354",      "course_number": "CHEM 3354",       "title": "Metabolism",                                          "units": 3, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": ["CHEM 3352"],                "quarter_equivalents": [],                      "is_placeholder": False},
    {"id": "BIOC_CHEM4453_4454", "course_number": "CHEM 4453/4454",  "title": "Molecular Biology or Protein Techniques",             "units": 2, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_CON_JRS",       "course_number": "Conc.",           "title": "Concentration or Advanced Elective",                  "units": 4, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_GE3A",          "course_number": "GE 3A",           "title": "Arts and Creative Expression",                        "units": 3, "category": "ge",           "grid_col": 5, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_GE_UD4",        "course_number": "GE UD-4",         "title": "Upper-Division Social Sciences",                      "units": 3, "category": "ge",           "grid_col": 5, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "BIOC_CHEM4461",      "course_number": "CHEM 4461",       "title": "Senior Project I",                                    "units": 1, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": ["CHEM 461"],            "is_placeholder": False},
    {"id": "BIOC_CHEM_ELEC",     "course_number": "CHEM Elec.",      "title": "Biochemistry Advanced Elective",                      "units": 2, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_CON_SRF",       "course_number": "Conc.",           "title": "Concentration or Advanced Elective",                  "units": 5, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_GE_UD3",        "course_number": "GE UD-3",         "title": "Upper-Division Arts and Humanities",                  "units": 3, "category": "ge",           "grid_col": 6, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "BIOC_CHEM4462",      "course_number": "CHEM 4462",       "title": "Senior Project II",                                   "units": 1, "category": "major",        "grid_col": 7, "grid_row": 0, "prerequisites": ["CHEM 4461"],                "quarter_equivalents": ["CHEM 462"],            "is_placeholder": False},
    {"id": "BIOC_BIO_MCRO_ELEC", "course_number": "BIO/MCRO Elec.", "title": "BIO or MCRO Advanced Elective",                       "units": 4, "category": "support",       "grid_col": 7, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_CON_SRS",       "course_number": "Conc.",           "title": "Concentration or Advanced Elective",                  "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_GE4B",          "course_number": "GE 4B",           "title": "American Institutions",                               "units": 3, "category": "ge",           "grid_col": 7, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
    {"id": "BIOC_FREE2",         "course_number": "Free",            "title": "Free Elective",                                       "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                           "quarter_equivalents": [],                      "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# AGRICULTURAL SYSTEMS MANAGEMENT (BS) — 121 units
# Source: catalog.calpoly.edu/.../bioresource-agricultural-engineering/agricultural-systems-management-bs/
# ─────────────────────────────────────────────────────────────────────────────
ASM_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "ASM_BRAE1128",          "course_number": "BRAE 1128",          "title": "Careers in BioResource and Agricultural Engineering",  "units": 2, "category": "major",        "grid_col": 0, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE1150",          "course_number": "BRAE 1150",          "title": "Design Graphics and CAD for Agricultural Engineering",  "units": 2, "category": "major",        "grid_col": 0, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_MATH1007_STAT1110", "course_number": "MATH 1007 / STAT 1110 / MATH 1267", "title": "Math / Statistics Elective",                      "units": 3, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["MATH 117", "STAT 218", "MATH 1007", "STAT 1110", "MATH 1267"], "elective_key": "asm_math_elective", "is_placeholder": True},
    {"id": "ASM_PHYS1121",          "course_number": "PHYS 1121",          "title": "College Physics I",                                   "units": 4, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_GE1A",              "course_number": "GE 1A",              "title": "Written Communication",                               "units": 3, "category": "ge",           "grid_col": 0, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["ENGL 134", "ENGL 1340"],  "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "ASM_BRAE1239",          "course_number": "BRAE 1239",          "title": "Engineering Surveying",                               "units": 3, "category": "major",        "grid_col": 1, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_CHEM1110",          "course_number": "CHEM 1110 / CHEM 1120", "title": "World of Chemistry or Fundamentals of Chemical Structure", "units": 4, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["CHEM 111", "CHEM 124", "CHEM 1110", "CHEM 1120"], "elective_key": "asm_chem_elective", "is_placeholder": True},
    {"id": "ASM_GE1B",              "course_number": "GE 1B",              "title": "Critical Thinking",                                   "units": 3, "category": "ge",           "grid_col": 1, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
    {"id": "ASM_GE1C",              "course_number": "GE 1C",              "title": "Oral Communication",                                  "units": 3, "category": "ge",           "grid_col": 1, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["COMS 101"],               "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "ASM_BRAE2203",          "course_number": "BRAE 2203",          "title": "Systems Management I",                                "units": 4, "category": "major",        "grid_col": 2, "grid_row": 0, "prerequisites": ["BRAE 1128", "BRAE 1150"],    "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_AGB2260",           "course_number": "AGB 2260",           "title": "Agribusiness Data Literacy",                          "units": 3, "category": "support",       "grid_col": 2, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_GE4A",              "course_number": "GE 4A",              "title": "American Institutions",                               "units": 3, "category": "ge",           "grid_col": 2, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
    {"id": "ASM_GE5B",              "course_number": "GE 5B",              "title": "Life Sciences",                                       "units": 3, "category": "ge",           "grid_col": 2, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["BIO 111", "BIO 1111"],    "is_placeholder": True},
    {"id": "ASM_GE6",               "course_number": "GE 6",               "title": "Ethnic Studies",                                      "units": 3, "category": "ge",           "grid_col": 2, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["ES 253", "ES 1112"],      "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "ASM_BRAE2142",          "course_number": "BRAE 2142",          "title": "Agricultural Power and Machinery Management",          "units": 3, "category": "major",        "grid_col": 3, "grid_row": 0, "prerequisites": ["BRAE 1150"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_AGB2214",           "course_number": "AGB 2214",           "title": "Agribusiness Financial Accounting",                   "units": 3, "category": "support",       "grid_col": 3, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["AGB 214"],                "is_placeholder": False},
    {"id": "ASM_GE3A",              "course_number": "GE 3A",              "title": "Arts and Creative Expression",                        "units": 3, "category": "ge",           "grid_col": 3, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
    {"id": "ASM_GE3B",              "course_number": "GE 3B",              "title": "Humanities",                                          "units": 3, "category": "ge",           "grid_col": 3, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
    {"id": "ASM_GE5A",              "course_number": "GE 5A",              "title": "Physical Sciences",                                   "units": 3, "category": "ge",           "grid_col": 3, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ASM_BRAE3301",          "course_number": "BRAE 3301",          "title": "Hydraulic and Mechanical Power Systems",              "units": 3, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["PHYS 1121"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE3340",          "course_number": "BRAE 3340",          "title": "Irrigation Water Management",                         "units": 3, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["PHYS 1121"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_AGB2212",           "course_number": "AGB 2212",           "title": "Agricultural Economics",                              "units": 3, "category": "support",       "grid_col": 4, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": ["AGB 212"],                "is_placeholder": False},
    {"id": "ASM_AGB3308",           "course_number": "AGB 3308",           "title": "Introduction to Agribusiness Finance",                "units": 3, "category": "support",       "grid_col": 4, "grid_row": 0, "prerequisites": ["AGB 2214"],                 "quarter_equivalents": ["AGB 308"],                "is_placeholder": False},
    {"id": "ASM_ELEC1",             "course_number": "Elective",           "title": "Approved Elective",                                   "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ASM_BRAE3317",          "course_number": "BRAE 3317",          "title": "Systems Management II",                               "units": 4, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": ["BRAE 2203"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE3343",          "course_number": "BRAE 3343",          "title": "Mechanical Systems Analysis",                         "units": 4, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": ["BRAE 2142"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE3348",          "course_number": "BRAE 3348",          "title": "Energy for a Sustainable Society",                    "units": 3, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_AGB3369",           "course_number": "AGB 3369",           "title": "Agricultural Personnel Management",                   "units": 3, "category": "support",       "grid_col": 5, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "ASM_BRAE4419",          "course_number": "BRAE 4419",          "title": "Systems Management III",                              "units": 3, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": ["BRAE 3317"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE4425",          "course_number": "BRAE 4425",          "title": "Agricultural Mechatronics",                           "units": 5, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE4432",          "course_number": "BRAE 4432",          "title": "Agricultural Buildings",                              "units": 4, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE4440",          "course_number": "BRAE 4440",          "title": "Agricultural Irrigation Systems",                     "units": 4, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": ["BRAE 3340"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_BRAE4460",          "course_number": "BRAE 4460",          "title": "Senior Project I",                                    "units": 1, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": False},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "ASM_BRAE4461",          "course_number": "BRAE 4461",          "title": "Senior Project II",                                   "units": 2, "category": "major",        "grid_col": 7, "grid_row": 0, "prerequisites": ["BRAE 4460"],                "quarter_equivalents": [],                         "is_placeholder": False},
    {"id": "ASM_ELEC2",             "course_number": "Elective 2",         "title": "Approved Elective",                                   "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
    {"id": "ASM_ELEC3",             "course_number": "Elective 3",         "title": "Approved Elective",                                   "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
    {"id": "ASM_GE_UD3",            "course_number": "GE UD-3",            "title": "Upper-Division Arts and Humanities",                  "units": 3, "category": "ge",           "grid_col": 7, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
    {"id": "ASM_GE_UD4",            "course_number": "GE UD-4",            "title": "Upper-Division Social Sciences",                      "units": 3, "category": "ge",           "grid_col": 7, "grid_row": 0, "prerequisites": [],                            "quarter_equivalents": [],                         "is_placeholder": True},
]


BRAE_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "BRAE_BRAE1128",  "course_number": "BRAE 1128",      "title": "Careers in BioResource and Agricultural Engineering",       "units": 2, "category": "major",        "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["BRAE 128"],       "is_placeholder": False},
    {"id": "BRAE_MATH1261",  "course_number": "MATH 1261",      "title": "Calculus I",                                               "units": 4, "category": "support",      "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["MATH 141"],       "is_placeholder": False},
    {"id": "BRAE_PHYS1141",  "course_number": "PHYS 1141",      "title": "General Physics I",                                        "units": 4, "category": "support",      "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["PHYS 141"],       "is_placeholder": False},
    {"id": "BRAE_GE1A",      "course_number": "GE 1A",          "title": "Written Communication",                                    "units": 3, "category": "ge",           "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},
    {"id": "BRAE_GE1C",      "course_number": "GE 1C",          "title": "Oral Communication",                                       "units": 3, "category": "ge",           "grid_col": 0, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "BRAE_BRAE1150",  "course_number": "BRAE 1150",      "title": "Design Graphics and CAD for Agricultural Engineering",      "units": 2, "category": "major",        "grid_col": 1, "grid_row": 0, "prerequisites": ["BRAE 1128"],                   "quarter_equivalents": ["BRAE 150"],       "is_placeholder": False},
    {"id": "BRAE_MATH1262",  "course_number": "MATH 1262",      "title": "Calculus II",                                              "units": 4, "category": "support",      "grid_col": 1, "grid_row": 0, "prerequisites": ["MATH 1261"],                   "quarter_equivalents": ["MATH 142"],       "is_placeholder": False},
    {"id": "BRAE_PHYS1143",  "course_number": "PHYS 1143",      "title": "General Physics II",                                       "units": 4, "category": "support",      "grid_col": 1, "grid_row": 0, "prerequisites": ["PHYS 1141"],                   "quarter_equivalents": ["PHYS 132"],       "is_placeholder": False},
    {"id": "BRAE_GE1B",      "course_number": "GE 1B",          "title": "Critical Thinking",                                        "units": 3, "category": "ge",           "grid_col": 1, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},
    {"id": "BRAE_GE3A",      "course_number": "GE 3A",          "title": "Arts and Creative Expression",                             "units": 3, "category": "ge",           "grid_col": 1, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "BRAE_BRAE2236",  "course_number": "BRAE 2236",      "title": "Principles of Irrigation",                                 "units": 4, "category": "major",        "grid_col": 2, "grid_row": 0, "prerequisites": ["BRAE 1150"],                   "quarter_equivalents": ["BRAE 236"],       "is_placeholder": False},
    {"id": "BRAE_CHEM1122",  "course_number": "CHEM 1122",      "title": "Fundamentals of Chemical Reactivity",                      "units": 4, "category": "support",      "grid_col": 2, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["CHEM 125"],       "is_placeholder": False},
    {"id": "BRAE_MATH2263",  "course_number": "MATH 2263",      "title": "Calculus III",                                             "units": 3, "category": "support",      "grid_col": 2, "grid_row": 0, "prerequisites": ["MATH 1262"],                   "quarter_equivalents": ["MATH 143"],       "is_placeholder": False},
    {"id": "BRAE_GE3B",      "course_number": "GE 3B",          "title": "Social Sciences",                                          "units": 3, "category": "ge",           "grid_col": 2, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},
    {"id": "BRAE_GE4A",      "course_number": "GE 4A",          "title": "Diversity and Equity",                                     "units": 3, "category": "ge",           "grid_col": 2, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "BRAE_BRAE2216",  "course_number": "BRAE 2216",      "title": "Fundamentals of Electricity",                              "units": 4, "category": "major",        "grid_col": 3, "grid_row": 0, "prerequisites": ["PHYS 1141"],                   "quarter_equivalents": ["BRAE 216"],       "is_placeholder": False},
    {"id": "BRAE_BRAE2220",  "course_number": "BRAE 2220",      "title": "Introduction to Biological Systems",                       "units": 4, "category": "major",        "grid_col": 3, "grid_row": 0, "prerequisites": ["BRAE 1128"],                   "quarter_equivalents": ["BRAE 220"],       "is_placeholder": False},
    {"id": "BRAE_BRAE2221",  "course_number": "BRAE 2221",      "title": "Engineering Mechanics with Agricultural Applications I",    "units": 4, "category": "major",        "grid_col": 3, "grid_row": 0, "prerequisites": ["PHYS 1141", "MATH 1261"],      "quarter_equivalents": ["BRAE 321"],       "is_placeholder": False},
    {"id": "BRAE_CSC1032",   "course_number": "CSC 1032",       "title": "Programming for Scientists and Engineers",                 "units": 3, "category": "support",      "grid_col": 3, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["CSC 231"],        "is_placeholder": False},
    {"id": "BRAE_GE4B",      "course_number": "GE 4B",          "title": "Personal Development",                                     "units": 3, "category": "ge",           "grid_col": 3, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "BRAE_BRAE1239",  "course_number": "BRAE 1239",      "title": "Engineering Surveying",                                    "units": 3, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["BRAE 239"],       "is_placeholder": False},
    {"id": "BRAE_BRAE2222",  "course_number": "BRAE 2222",      "title": "Engineering Mechanics with Agricultural Applications II",   "units": 4, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["BRAE 2221"],                   "quarter_equivalents": ["BRAE 322"],       "is_placeholder": False},
    {"id": "BRAE_BRAE3312",  "course_number": "BRAE 3312",      "title": "Hydraulics",                                               "units": 3, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["BRAE 2221", "MATH 2263"],      "quarter_equivalents": ["BRAE 312"],       "is_placeholder": False},
    {"id": "BRAE_BRAE3332",  "course_number": "BRAE 3332",      "title": "Environmental Controls for Agricultural Structures",        "units": 3, "category": "major",        "grid_col": 4, "grid_row": 0, "prerequisites": ["BRAE 2220"],                   "quarter_equivalents": ["BRAE 332"],       "is_placeholder": False},
    {"id": "BRAE_ECON",      "course_number": "ECON 2001 / ECON 2040", "title": "Survey of Economics",                                  "units": 3, "category": "support",      "grid_col": 4, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["ECON 201", "ECON 2001", "ECON 2040"], "elective_key": "brae_econ_elective", "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "BRAE_BRAE3234",  "course_number": "BRAE 3234",      "title": "Equipment Engineering I",                                  "units": 4, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": ["BRAE 2221"],                   "quarter_equivalents": ["BRAE 334"],       "is_placeholder": False},
    {"id": "BRAE_BRAE3320",  "course_number": "BRAE 3320",      "title": "Bioresource Engineering",                                  "units": 3, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": ["BRAE 2220"],                   "quarter_equivalents": ["BRAE 320"],       "is_placeholder": False},
    {"id": "BRAE_BRAE4414",  "course_number": "BRAE 4414",      "title": "Irrigation Engineering",                                   "units": 3, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": ["BRAE 2236"],                   "quarter_equivalents": ["BRAE 414"],       "is_placeholder": False},
    {"id": "BRAE_BRAE4428",  "course_number": "BRAE 4428",      "title": "Agricultural Robotics and Automation",                     "units": 4, "category": "major",        "grid_col": 5, "grid_row": 0, "prerequisites": ["BRAE 2216"],                   "quarter_equivalents": ["BRAE 428"],       "is_placeholder": False},
    {"id": "BRAE_ELECTIVE",  "course_number": "Elective",       "title": "Approved Elective",                                        "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "BRAE_BRAE4403",  "course_number": "BRAE 4403",      "title": "Agricultural Engineering Ethics, Economics, and Optimization", "units": 3, "category": "major",   "grid_col": 6, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["BRAE 403"],       "is_placeholder": False},
    {"id": "BRAE_BRAE4422",  "course_number": "BRAE 4422",      "title": "Equipment Engineering II",                                 "units": 3, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": ["BRAE 3234"],                   "quarter_equivalents": ["BRAE 422"],       "is_placeholder": False},
    {"id": "BRAE_BRAE4433",  "course_number": "BRAE 4433",      "title": "Agricultural Structures Design",                           "units": 4, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": ["BRAE 3332"],                   "quarter_equivalents": ["BRAE 433"],       "is_placeholder": False},
    {"id": "BRAE_BRAE4460",  "course_number": "BRAE 4460",      "title": "Senior Project I",                                         "units": 1, "category": "major",        "grid_col": 6, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": ["BRAE 460"],       "is_placeholder": False},
    {"id": "BRAE_FOCUS1",    "course_number": "Focus Area",     "title": "Focus Area Elective",                                      "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "BRAE_BRAE4461",  "course_number": "BRAE 4461",      "title": "Senior Project II",                                        "units": 2, "category": "major",        "grid_col": 7, "grid_row": 0, "prerequisites": ["BRAE 4460"],                   "quarter_equivalents": ["BRAE 461"],       "is_placeholder": False},
    {"id": "BRAE_STAT3210",  "course_number": "STAT 3210",      "title": "Engineering Statistics",                                   "units": 3, "category": "support",      "grid_col": 7, "grid_row": 0, "prerequisites": ["MATH 1262"],                   "quarter_equivalents": ["STAT 321"],       "is_placeholder": False},
    {"id": "BRAE_FOCUS2",    "course_number": "Focus Area",     "title": "Focus Area Elective",                                      "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},
    {"id": "BRAE_GE_UD3",    "course_number": "GE UD-3",        "title": "Upper-Division Arts and Humanities",                       "units": 3, "category": "ge",           "grid_col": 7, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},
    {"id": "BRAE_GE_UD4",    "course_number": "GE UD-4",        "title": "Upper-Division Social Sciences",                           "units": 3, "category": "ge",           "grid_col": 7, "grid_row": 0, "prerequisites": [],                              "quarter_equivalents": [],                 "is_placeholder": True},
]


# ─────────────────────────────────────────────────────────────────────────────
# BUSINESS ADMINISTRATION (BS) — General Curriculum (120 units)
# Source: catalog.calpoly.edu/business/undergraduate/business-administration-bs/
# ─────────────────────────────────────────────────────────────────────────────
BUS_FLOWCHART: list[Course] = [
    # ── FRESHMAN FALL ─────────────────────────────────────────────────────────
    {"id": "BUS_1100",      "course_number": "BUS 1100",        "title": "Career Readiness I",                          "units": 1, "category": "major",         "grid_col": 0, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": False},
    {"id": "BUS_2214",      "course_number": "BUS 2214",        "title": "Financial Accounting",                        "units": 3, "category": "major",         "grid_col": 0, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["BUS 214"],          "is_placeholder": False},
    {"id": "BUS_ECON2001",  "course_number": "ECON 2001",       "title": "Survey of Economics",                         "units": 3, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["ECON 222"],         "is_placeholder": False},
    {"id": "BUS_STAT1210",  "course_number": "STAT 1210",       "title": "Business Statistics I",                       "units": 3, "category": "support",       "grid_col": 0, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["STAT 251"],         "is_placeholder": False},
    {"id": "BUS_GE1A",      "course_number": "GE 1A",           "title": "Written Communication",                       "units": 3, "category": "ge",            "grid_col": 0, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["ENGL 134"],         "is_placeholder": True},

    # ── FRESHMAN SPRING ───────────────────────────────────────────────────────
    {"id": "BUS_2207",      "course_number": "BUS 2207",        "title": "Legal Responsibilities of Business",          "units": 3, "category": "major",         "grid_col": 1, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["BUS 207"],          "is_placeholder": False},
    {"id": "BUS_2215",      "course_number": "BUS 2215",        "title": "Managerial Accounting",                       "units": 3, "category": "major",         "grid_col": 1, "grid_row": 0, "prerequisites": ["BUS 2214"],             "quarter_equivalents": ["BUS 215"],          "is_placeholder": False},
    {"id": "BUS_STAT1220",  "course_number": "STAT 1220",       "title": "Business Statistics II",                      "units": 3, "category": "support",       "grid_col": 1, "grid_row": 0, "prerequisites": ["STAT 1210"],            "quarter_equivalents": ["STAT 252"],         "is_placeholder": False},
    {"id": "BUS_MATH",      "course_number": "MATH 1264 / MATH 1267", "title": "Calculus for Data Science I or Business Calculus", "units": 3, "category": "support", "grid_col": 1, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["MATH 1264", "MATH 1267", "MATH 267"], "elective_key": "bus_calculus_choice", "is_placeholder": True},
    {"id": "BUS_GE1C",      "course_number": "GE 1C",           "title": "Oral Communication",                          "units": 3, "category": "ge",            "grid_col": 1, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["COMS 101"],         "is_placeholder": True},

    # ── SOPHOMORE FALL ────────────────────────────────────────────────────────
    {"id": "BUS_2206",      "course_number": "BUS 2206",        "title": "Career Readiness II",                         "units": 1, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": ["BUS 1100"],             "quarter_equivalents": ["BUS 206"],          "is_placeholder": False},
    {"id": "BUS_3391",      "course_number": "BUS 3391",        "title": "Information Systems",                         "units": 3, "category": "major",         "grid_col": 2, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["BUS 391"],          "is_placeholder": False},
    {"id": "BUS_FIN_ELEC",  "course_number": "BUS 1342 / BUS 3343", "title": "Financial Institutions or Quantitative Methods in Finance", "units": 3, "category": "major", "grid_col": 2, "grid_row": 0, "prerequisites": [], "quarter_equivalents": ["BUS 1342", "BUS 3343", "BUS 342", "BUS 343"], "elective_key": "bus_finance_methods_choice", "is_placeholder": True},
    {"id": "BUS_GE1B",      "course_number": "GE 1B",           "title": "Critical Thinking",                           "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE3A",      "course_number": "GE 3A",           "title": "Arts",                                        "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE4A",      "course_number": "GE 4A",           "title": "American Institutions",                       "units": 3, "category": "ge",            "grid_col": 2, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},

    # ── SOPHOMORE SPRING ──────────────────────────────────────────────────────
    {"id": "BUS_3346",      "course_number": "BUS 3346",        "title": "Principles of Marketing",                     "units": 3, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["BUS 346"],          "is_placeholder": False},
    {"id": "BUS_3387",      "course_number": "BUS 3387",        "title": "Organizational Behavior",                     "units": 3, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["BUS 387"],          "is_placeholder": False},
    {"id": "BUS_TECH_ELEC", "course_number": "ITP/Tech Elective","title": "Technology Management Elective",             "units": 3, "category": "major",         "grid_col": 3, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE3B",      "course_number": "GE 3B",           "title": "Humanities",                                  "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE5A",      "course_number": "GE 5A",           "title": "Physical Sciences",                           "units": 3, "category": "ge",            "grid_col": 3, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},

    # ── JUNIOR FALL ───────────────────────────────────────────────────────────
    {"id": "BUS_3306",      "course_number": "BUS 3306",        "title": "Career Readiness III",                        "units": 1, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": ["BUS 2206"],             "quarter_equivalents": ["BUS 306"],          "is_placeholder": False},
    {"id": "BUS_INTL_ELEC", "course_number": "Intl. Elective",  "title": "International Business Elective",             "units": 3, "category": "major",         "grid_col": 4, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_CON1",      "course_number": "Conc.",           "title": "Concentration Course",                        "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_CON2",      "course_number": "Conc.",           "title": "Concentration Course",                        "units": 3, "category": "concentration", "grid_col": 4, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE6",       "course_number": "GE 6",            "title": "Ethnic Studies",                              "units": 3, "category": "ge",            "grid_col": 4, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["ES 1112"],          "is_placeholder": True},

    # ── JUNIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "BUS_4404",      "course_number": "BUS 4404",        "title": "Law, Government, and Social Influences",      "units": 3, "category": "major",         "grid_col": 5, "grid_row": 0, "prerequisites": ["BUS 2207"],             "quarter_equivalents": ["BUS 404"],          "is_placeholder": False},
    {"id": "BUS_CON3",      "course_number": "Conc.",           "title": "Concentration Course",                        "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_CON4",      "course_number": "Conc.",           "title": "Concentration Course",                        "units": 3, "category": "concentration", "grid_col": 5, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE5B",      "course_number": "GE 5B",           "title": "Life Sciences",                               "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": ["BIO 1111"],         "is_placeholder": True},
    {"id": "BUS_GE5C",      "course_number": "GE 5C",           "title": "Laboratory",                                  "units": 1, "category": "ge",            "grid_col": 5, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE_UD4",    "course_number": "GE UD-4",         "title": "Upper-Division Social Sciences",              "units": 3, "category": "ge",            "grid_col": 5, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},

    # ── SENIOR FALL ───────────────────────────────────────────────────────────
    {"id": "BUS_SR_PROJ",   "course_number": "BUS Senior Proj.","title": "Senior Project or Capstone Elective",         "units": 3, "category": "major",         "grid_col": 6, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_CON5",      "course_number": "Conc.",           "title": "Concentration Course",                        "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_CON6",      "course_number": "Conc.",           "title": "Concentration Course",                        "units": 3, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE_UD25",   "course_number": "GE UD-2/5",       "title": "Upper-Division Math or Science",              "units": 3, "category": "ge",            "grid_col": 6, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_FREE1",     "course_number": "Free",            "title": "Free Elective",                               "units": 4, "category": "concentration", "grid_col": 6, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},

    # ── SENIOR SPRING ─────────────────────────────────────────────────────────
    {"id": "BUS_4401",      "course_number": "BUS 4401 & 4411", "title": "Strategic Management and Assessment",         "units": 3, "category": "major",         "grid_col": 7, "grid_row": 0, "prerequisites": ["BUS 3346", "BUS 3387"], "quarter_equivalents": ["BUS 401"],          "is_placeholder": False},
    {"id": "BUS_CON7",      "course_number": "Conc.",           "title": "Concentration Course",                        "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_GE_UD3",    "course_number": "GE UD-3",         "title": "Upper-Division Arts and Humanities",          "units": 3, "category": "ge",            "grid_col": 7, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_FREE2",     "course_number": "Free 2",          "title": "Free Elective",                               "units": 4, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
    {"id": "BUS_FREE3",     "course_number": "Free 3",          "title": "Free Elective",                               "units": 3, "category": "concentration", "grid_col": 7, "grid_row": 0, "prerequisites": [],                       "quarter_equivalents": [],                   "is_placeholder": True},
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

BARCH_COLUMN_LABELS = [
    *COLUMN_LABELS,
    {"year": "Fifth Year", "term": "Fall"},
    {"year": "Fifth Year", "term": "Spring"},
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
    column_count = max(len(COLUMN_LABELS), max((course["grid_col"] for course in courses), default=0) + 1)

    for grid_col in range(column_count):
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
POLS_FLOWCHART = _compact_rows_by_category(POLS_FLOWCHART)
PSY_FLOWCHART = _compact_rows_by_category(PSY_FLOWCHART)
ENGL_FLOWCHART = _compact_rows_by_category(ENGL_FLOWCHART)
MU_FLOWCHART = _compact_rows_by_category(MU_FLOWCHART)
AGC_FLOWCHART = _compact_rows_by_category(AGC_FLOWCHART)
AGS_FLOWCHART = _compact_rows_by_category(AGS_FLOWCHART)
ASCI_FLOWCHART = _compact_rows_by_category(ASCI_FLOWCHART)
AGB_FLOWCHART = _compact_rows_by_category(AGB_FLOWCHART)
ARCE_FLOWCHART = _compact_rows_by_category(ARCE_FLOWCHART)
ANTGEOG_FLOWCHART = _compact_rows_by_category(ANTGEOG_FLOWCHART)
ARCH_FLOWCHART = _compact_rows_by_category(ARCH_FLOWCHART)
BIO_FLOWCHART = _compact_rows_by_category(BIO_FLOWCHART)
BMED_FLOWCHART = _compact_rows_by_category(BMED_FLOWCHART)
BIOC_FLOWCHART = _compact_rows_by_category(BIOC_FLOWCHART)
ASM_FLOWCHART = _compact_rows_by_category(ASM_FLOWCHART)
BRAE_FLOWCHART = _compact_rows_by_category(BRAE_FLOWCHART)
BUS_FLOWCHART = _compact_rows_by_category(BUS_FLOWCHART)


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
    "POLS": {
        "major": "Political Science",
        "code": "POLS",
        "total_units": 120,
        "courses": POLS_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "PSY": {
        "major": "Psychology",
        "code": "PSY",
        "total_units": 120,
        "courses": PSY_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "ENGL": {
        "major": "English",
        "code": "ENGL",
        "total_units": 120,
        "courses": ENGL_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "MU": {
        "major": "Music",
        "code": "MU",
        "total_units": 120,
        "courses": MU_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "AGC": {
        "major": "Agricultural Communication",
        "code": "AGC",
        "total_units": 120,
        "courses": AGC_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "AGS": {
        "major": "Agricultural Science",
        "code": "AGS",
        "total_units": 120,
        "courses": AGS_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "ASCI": {
        "major": "Animal Science",
        "code": "ASCI",
        "total_units": 120,
        "courses": ASCI_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "AGB": {
        "major": "Agricultural Business",
        "code": "AGB",
        "total_units": 120,
        "courses": AGB_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "ARCE": {
        "major": "Architectural Engineering",
        "code": "ARCE",
        "total_units": 128,
        "courses": ARCE_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "ANTGEOG": {
        "major": "Anthropology and Geography",
        "code": "ANTGEOG",
        "total_units": 120,
        "courses": ANTGEOG_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "ARCH": {
        "major": "Architecture",
        "code": "ARCH",
        "total_units": 150,
        "courses": ARCH_FLOWCHART,
        "columns": BARCH_COLUMN_LABELS,
    },
    "BIO": {
        "major": "Biological Sciences",
        "code": "BIO",
        "total_units": 120,
        "courses": BIO_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "BMED": {
        "major": "Biomedical Engineering",
        "code": "BMED",
        "total_units": 130,
        "courses": BMED_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "BIOC": {
        "major": "Biochemistry",
        "code": "BIOC",
        "total_units": 120,
        "courses": BIOC_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "ASM": {
        "major": "Agricultural Systems Management",
        "code": "ASM",
        "total_units": 121,
        "courses": ASM_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "BRAE": {
        "major": "BioResource and Agricultural Engineering",
        "code": "BRAE",
        "total_units": 128,
        "courses": BRAE_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
    "BUS": {
        "major": "Business Administration",
        "code": "BUS",
        "total_units": 120,
        "courses": BUS_FLOWCHART,
        "columns": COLUMN_LABELS,
    },
}
