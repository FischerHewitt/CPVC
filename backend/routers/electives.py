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
    "ags_life_science": {
        "title": "Life Science Support Elective",
        "description": "AGS students select one life science support course from the catalog list.",
        "courses": [
            {"course_number": "BIO 1111", "title": "General Biology", "units": 3},
            {"course_number": "BIO 1151", "title": "Life: Molecules and Cells", "units": 4},
            {"course_number": "BOT 1121", "title": "General Botany", "units": 4},
            {"course_number": "MCRO 2221", "title": "Introduction to Microbiology", "units": 4},
        ],
    },
    "ags_asci_pair": {
        "title": "Animal Management Systems and Laboratory",
        "description": "AGS students take both ASCI 1102 and ASCI 1103 for the animal science foundation requirement.",
        "courses": [
            {"course_number": "ASCI 1102", "title": "Animal Management Systems", "units": 3},
            {"course_number": "ASCI 1103", "title": "Animal Science Laboratory", "units": 1},
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
    "ags_soil_science": {
        "title": "Soil Science Requirement",
        "description": "AGS students take one soil science course from the catalog list.",
        "courses": [
            {"course_number": "SS 1120", "title": "Introductory Soil Science", "units": 4},
            {"course_number": "SS 1130", "title": "Soils in Environmental and Agricultural Systems", "units": 3},
        ],
    },
    "ags_dairy_food_safety": {
        "title": "Safe Practices in Handling Food Products",
        "description": "AGS students take either General Dairy Manufacturing or Elements of Food Safety.",
        "courses": [
            {"course_number": "DSCI 2229", "title": "General Dairy Manufacturing", "units": 4},
            {"course_number": "FSN 2245", "title": "Elements of Food Safety", "units": 3},
        ],
    },
    "ags_aged_agc_choice": {
        "title": "Computer Applications or Fairgrounds and Expositions",
        "description": "AGS students take either AGED 4410 or AGC 3314.",
        "courses": [
            {"course_number": "AGED 4410", "title": "Computer Applications in Agricultural Education", "units": 1},
            {"course_number": "AGC 3314", "title": "California Fairgrounds and Expositions", "units": 3},
        ],
    },
    "ags_nr_choice": {
        "title": "Natural Resources Requirement",
        "description": "AGS students take either NR 3308 or NR 3323.",
        "courses": [
            {"course_number": "NR 3308", "title": "Fire and Society", "units": 3},
            {"course_number": "NR 3323", "title": "Human Dimensions in Natural Resources Management", "units": 3},
        ],
    },
    "ags_agc_ag_issues": {
        "title": "Current Trends and Issues",
        "description": "AGS students take either AGC 4452 or AG 4452.",
        "courses": [
            {"course_number": "AGC 4452", "title": "Current Trends and Issues in Agricultural Communication", "units": 3},
            {"course_number": "AG 4452", "title": "Leadership Seminar on Issues Affecting California Agriculture, Food Systems, and Natural Resources", "units": 4},
        ],
    },
    "ags_brae_aquaculture_irrigation": {
        "title": "Aquaculture or Agricultural Irrigation Systems",
        "description": "Agricultural Engineering Technology emphasis students take Aquaculture or Agricultural Irrigation Systems.",
        "courses": [
            {"course_number": "BRAE 4438", "title": "Aquaculture", "units": 4},
            {"course_number": "MSCI 4438", "title": "Aquaculture", "units": 4},
            {"course_number": "BRAE 4440", "title": "Agricultural Irrigation Systems", "units": 4},
        ],
    },
    "asm_math_elective": {
        "title": "Math / Statistics Elective",
        "description": "ASM students take one of these courses based on their math placement: MATH 1007 (Precalculus) or STAT 1110 (Applied Statistics). MATH 1267 is a separate required support course.",
        "courses": [
            {"course_number": "MATH 1007", "title": "Precalculus", "units": 3},
            {"course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3},
        ],
    },
    "asm_approved_elective": {
        "title": "Approved Elective",
        "description": "ASM students complete 9 units from the approved elective list. Animal or plant production courses from ASCI, DSCI, or PLSC may also be eligible; verify those broad production choices with an advisor.",
        "courses": [
            {"course_number": "BRAE 2200", "title": "Special Problems for Undergraduates", "units": 1},
            {"course_number": "BRAE 3344", "title": "Fabrication Systems", "units": 2},
            {"course_number": "BRAE 3345", "title": "Photogrammetry and Remote Sensing with GIS Applications", "units": 3},
            {"course_number": "BRAE 3349", "title": "Water for a Sustainable Society", "units": 3},
            {"course_number": "NR 3349", "title": "Water for a Sustainable Society", "units": 3},
            {"course_number": "BRAE 4400", "title": "Special Problems", "units": 1},
            {"course_number": "BRAE 4447", "title": "Advanced Surveying with GIS Applications", "units": 3},
            {"course_number": "BRAE 4448", "title": "Bioconversion", "units": 3},
            {"course_number": "BRAE 5405", "title": "Chemigation", "units": 1},
            {"course_number": "BRAE 5435", "title": "Hydrology and Drainage", "units": 3},
            {"course_number": "BRAE 5436", "title": "Food and Agriculture Process Water Engineering", "units": 3},
            {"course_number": "BRAE 5532", "title": "Water Pumps and Wells", "units": 3},
            {"course_number": "BRAE 5533", "title": "Irrigation Project Design", "units": 3},
            {"course_number": "CRP 4408", "title": "Water Resource Law and Policy", "units": 4},
            {"course_number": "NR 4408", "title": "Water Resource Law and Policy", "units": 4},
            {"course_number": "EE 4434", "title": "Transportation Electrification and Energy Storage Systems", "units": 3},
            {"course_number": "FDSC 1110", "title": "Introduction to Food Science and Sustainability", "units": 3},
            {"course_number": "FSN 2202", "title": "Introduction to Human Nutrition", "units": 3},
            {"course_number": "FSN 2245", "title": "Elements of Food Safety", "units": 3},
            {"course_number": "FSN 2250", "title": "Food and Nutrition: Culture and Customs", "units": 3},
            {"course_number": "FSN 3305", "title": "Nutrition and Exercise for Health and Disease Prevention", "units": 3},
            {"course_number": "FSN 3316", "title": "Fermented Foods", "units": 3},
            {"course_number": "IME 1141", "title": "Introduction to Metal Casting and Prototyping", "units": 1},
            {"course_number": "IME 1142", "title": "Materials Joining", "units": 1},
            {"course_number": "IME 1143", "title": "Introduction to Design and Manufacturing", "units": 2},
            {"course_number": "IME 3320", "title": "Human Factors and Technology", "units": 3},
            {"course_number": "ITP 3330", "title": "Packaging Fundamentals", "units": 3},
            {"course_number": "ITP 3341", "title": "Packaging Polymers and Processing", "units": 3},
            {"course_number": "LA 2218", "title": "Introduction to Geographic Information Systems (GIS)", "units": 3},
            {"course_number": "NR 3306", "title": "Natural Resource Ecology and Habitat Management", "units": 4},
            {"course_number": "NR 4416", "title": "Environmental Impact Analysis and Management", "units": 4},
            {"course_number": "NUTR 3310", "title": "Maternal and Child Nutrition", "units": 3},
            {"course_number": "NUTR 3315", "title": "Nutrition in Aging", "units": 2},
            {"course_number": "SS 1120", "title": "Introductory Soil Science", "units": 4},
            {"course_number": "SS 2221", "title": "Soil Health and Plant Nutrition", "units": 4},
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
    "asci_meat_science_pair": {
        "title": "Meat Science with Laboratory",
        "description": "ASCI students take both Meat Science and Meat Science Laboratory.",
        "courses": [
            {"course_number": "ASCI 2210", "title": "Meat Science", "units": 2},
            {"course_number": "ASCI 2211", "title": "Meat Science Laboratory", "units": 1},
        ],
    },
    "asci_animal_management": {
        "title": "Animal Management Elective",
        "description": "ASCI students complete 6 units from the animal management elective list.",
        "courses": [
            {"course_number": "ASCI 2230", "title": "Beef and Dairy Cattle Management", "units": 3},
            {"course_number": "ASCI 2231", "title": "Swine and Poultry Management", "units": 3},
            {"course_number": "ASCI 2232", "title": "Small Ruminant and Rangeland Management", "units": 3},
            {"course_number": "ASCI 2233", "title": "Companion Animal Management", "units": 3},
        ],
    },
    "asci_enterprise_elective": {
        "title": "Enterprise Experience Elective",
        "description": "ASCI students complete 3 units from the enterprise experience elective list.",
        "courses": [
            {"course_number": "ASCI 2001", "title": "Beef Cattle Enterprise", "units": 1},
            {"course_number": "ASCI 2002", "title": "Broiler Production Enterprise", "units": 2},
            {"course_number": "ASCI 2003", "title": "Bull Test Enterprise", "units": 2},
            {"course_number": "ASCI 2004", "title": "Dairy Calving Enterprise", "units": 1},
            {"course_number": "ASCI 2005", "title": "Dairy Fit and Show Enterprise", "units": 1},
            {"course_number": "ASCI 2006", "title": "Dairy Herd Evaluation Enterprise", "units": 2},
            {"course_number": "ASCI 2007", "title": "Dairy Products Evaluation Enterprise", "units": 1},
            {"course_number": "ASCI 2008", "title": "Equine Care Enterprise", "units": 1},
            {"course_number": "ASCI 2009", "title": "Foaling Enterprise", "units": 2},
            {"course_number": "ASCI 2010", "title": "Lambing Enterprise", "units": 1},
            {"course_number": "ASCI 2011", "title": "Performance Horse Development Enterprise", "units": 3},
            {"course_number": "ASCI 2012", "title": "Reptile Husbandry Enterprise", "units": 1},
            {"course_number": "ASCI 2013", "title": "Sausage Production Enterprise", "units": 2},
            {"course_number": "ASCI 2014", "title": "Swine Enterprise", "units": 1},
            {"course_number": "ASCI 2015", "title": "Targeted Grazing Enterprise", "units": 1},
            {"course_number": "ASCI 2016", "title": "Veterinary Clinic Operations Enterprise", "units": 1},
            {"course_number": "ASCI 2017", "title": "Livestock Show Enterprise", "units": 1},
            {"course_number": "ASCI 4001", "title": "Artificial Insemination of Beef Cattle Advanced Enterprise", "units": 1},
            {"course_number": "ASCI 4002", "title": "Bull Test Management Advanced Enterprise", "units": 2},
            {"course_number": "ASCI 4003", "title": "Bull Test Sale Implementation Advanced Enterprise", "units": 1},
            {"course_number": "ASCI 4004", "title": "Equine Mustang Management Advanced Enterprise", "units": 2},
            {"course_number": "ASCI 4005", "title": "Ranch Management I Advanced Enterprise", "units": 1},
            {"course_number": "ASCI 4006", "title": "Ranch Management II Advanced Enterprise", "units": 1},
            {"course_number": "ASCI 4007", "title": "Horse and Mule Packing Advanced Enterprise", "units": 1},
            {"course_number": "ASCI 4008", "title": "Livestock Event Planning Advanced Enterprise", "units": 2},
            {"course_number": "ASCI 4009", "title": "Livestock Event Implementation Advanced Enterprise", "units": 1},
            {"course_number": "ASCI 4010", "title": "Livestock Judging Advanced Enterprise", "units": 1},
            {"course_number": "ASCI 4011", "title": "Marine Mammal Health Advanced Enterprise", "units": 3},
            {"course_number": "ASCI 4012", "title": "Performance Horse Production Advanced Enterprise", "units": 3},
            {"course_number": "ASCI 4013", "title": "Equine Sale Event Planning Advanced Enterprise", "units": 3},
            {"course_number": "ASCI 4014", "title": "Equine Sale Event Implementation Advanced Enterprise", "units": 3},
            {"course_number": "ASCI 4015", "title": "Veterinary Community Service Advanced Enterprise", "units": 2},
        ],
    },
    "asci_nutrition_elective": {
        "title": "Nutrition Elective",
        "description": "ASCI students take one nutrition course from the catalog list.",
        "courses": [
            {"course_number": "ASCI 3346", "title": "Equine Nutrition", "units": 3},
            {"course_number": "ASCI 3350", "title": "Nonruminant Nutrition", "units": 3},
            {"course_number": "ASCI 3355", "title": "Ruminant Nutrition", "units": 3},
            {"course_number": "ASCI 4419", "title": "Animal Metabolism and Nutritional Modeling", "units": 3},
        ],
    },
    "asci_physiology_elective": {
        "title": "Physiology Elective",
        "description": "ASCI students take one physiology course from the catalog list.",
        "courses": [
            {"course_number": "ASCI 4403", "title": "Applied Biotechnology in Animal Science", "units": 3},
            {"course_number": "ASCI 4405", "title": "Domestic Livestock Endocrinology", "units": 3},
            {"course_number": "ASCI 4406", "title": "Animal Embryology and Assisted Reproduction", "units": 3},
            {"course_number": "ASCI 4438", "title": "Systemic Animal Physiology", "units": 4},
            {"course_number": "ASCI 4440", "title": "Immunology and Diseases of Animals", "units": 3},
            {"course_number": "ASCI 4455", "title": "Equine Reproduction", "units": 3},
            {"course_number": "DSCI 3321", "title": "Lactation Physiology", "units": 3},
            {"course_number": "DSCI 3330", "title": "Dairy Cattle Reproductive Management and Artificial Insemination", "units": 3},
        ],
    },
    "asci_senior_project": {
        "title": "Senior Project",
        "description": "ASCI students complete one senior project option.",
        "courses": [
            {"course_number": "ASCI 4477", "title": "Senior Project - Research Experience in Animal Science", "units": 2},
            {"course_number": "ASCI 4478", "title": "Senior Project - Advanced Internship Experience in Animal Science", "units": 2},
            {"course_number": "ASCI 4479", "title": "Senior Project - Current Issues in Animal Science", "units": 2},
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
        "description": "Anthropology and Geography students take one senior project I course.",
        "courses": [
            {"course_number": "ANT 4461", "title": "Senior Project I", "units": 1},
            {"course_number": "GEOG 4461", "title": "Senior Project I", "units": 1},
        ],
    },
    "antgeog_senior_project_ii": {
        "title": "Senior Project II",
        "description": "Anthropology and Geography students take one senior project II course.",
        "courses": [
            {"course_number": "ANT 4462", "title": "Senior Project II", "units": 2},
            {"course_number": "GEOG 4462", "title": "Senior Project II", "units": 2},
        ],
    },
    "antgeog_physical_geography": {
        "title": "Physical Geography",
        "description": "Take the cross-listed Physical Geography course as GEOG 2250 or ERSC 2250.",
        "courses": [
            {"course_number": "GEOG 2250", "title": "Physical Geography", "units": 3},
            {"course_number": "ERSC 2250", "title": "Physical Geography", "units": 3},
        ],
    },
    "antgeog_professional_preparation": {
        "title": "Professional Preparation",
        "description": "Take the cross-listed professional preparation course as ANT 3384 or GEOG 3384.",
        "courses": [
            {"course_number": "ANT 3384", "title": "Professional Preparation for Anthropologists/Geographers", "units": 2},
            {"course_number": "GEOG 3384", "title": "Professional Preparation for Anthropologists/Geographers", "units": 2},
        ],
    },
    "antgeog_methods_elective": {
        "title": "Methodological Course Elective",
        "description": "Select one methodological course from the catalog list.",
        "courses": [
            {"course_number": "ANT 3310", "title": "Archaeological Field Methods", "units": 3},
            {"course_number": "ANT 3311", "title": "Archaeological Laboratory Methods", "units": 3},
            {"course_number": "ANT 3312", "title": "Introduction to Cultural Resources Management", "units": 4},
            {"course_number": "ISLA 3393", "title": "Action-oriented Ethnography", "units": 3},
            {"course_number": "GEOG 3328", "title": "Applications in Remote Sensing and GIS", "units": 3},
            {"course_number": "GEOG 4441", "title": "Advanced Applications in Geospatial Technologies", "units": 3},
        ],
    },
    "antgeog_internship": {
        "title": "Internship",
        "description": "Complete internship units through ANT 4465 or GEOG 4465. A study abroad course may substitute with advisor approval.",
        "courses": [
            {"course_number": "ANT 4465", "title": "Internship", "units": 2},
            {"course_number": "GEOG 4465", "title": "Internship", "units": 2},
        ],
    },
    "antgeog_regional_geography": {
        "title": "Regional Geography Elective",
        "description": "Select one regional geography course from the catalog list.",
        "courses": [
            {"course_number": "GEOG 3340", "title": "Geography of California", "units": 3},
            {"course_number": "GEOG 3370", "title": "Geography of Latin America", "units": 3},
            {"course_number": "GEOG 3380", "title": "Geography of the Caribbean", "units": 3},
        ],
    },
    "antgeog_research_design": {
        "title": "Research Design and Methods",
        "description": "Take the cross-listed research design course as ANT 4455 or GEOG 4455.",
        "courses": [
            {"course_number": "ANT 4455", "title": "Anthropology-Geography Research Design and Methods", "units": 4},
            {"course_number": "GEOG 4455", "title": "Anthropology-Geography Research Design and Methods", "units": 4},
        ],
    },
    "antgeog_env_climate": {
        "title": "Earth Systems or Climate Change Course",
        "description": "Environmental Studies and Sustainability students take one climate or earth systems course.",
        "courses": [
            {"course_number": "ERSC 3325", "title": "Climate and Humanity", "units": 3},
            {"course_number": "ERSC 4414", "title": "Global and Regional Climatology", "units": 3},
            {"course_number": "GEOG 4414", "title": "Global and Regional Climatology", "units": 3},
            {"course_number": "ERSC 4415", "title": "Applied Meteorology and Climatology", "units": 3},
            {"course_number": "GEOG 4415", "title": "Applied Meteorology and Climatology", "units": 3},
        ],
    },
    "antgeog_env_geospatial": {
        "title": "Remote Sensing or Geospatial Technologies",
        "description": "Environmental Studies and Sustainability students take one geospatial methods course.",
        "courses": [
            {"course_number": "GEOG 3328", "title": "Applications in Remote Sensing and GIS", "units": 3},
            {"course_number": "GEOG 4441", "title": "Advanced Applications in Geospatial Technologies", "units": 3},
        ],
    },
    "antgeog_human_ecology_foundation": {
        "title": "Archaeology or Indigenous Past",
        "description": "Human Ecology students take one course from this catalog pair.",
        "courses": [
            {"course_number": "ANT 3309", "title": "Elements of Archaeology", "units": 3},
            {"course_number": "ANT 3320", "title": "California's Indigenous Past", "units": 3},
        ],
    },
    "antgeog_human_ecology_geog": {
        "title": "Climate and Humanity or Global Geography",
        "description": "Human Ecology students take either Climate and Humanity or Global Geography.",
        "courses": [
            {"course_number": "ERSC 3325", "title": "Climate and Humanity", "units": 3},
            {"course_number": "GEOG 3308", "title": "Global Geography", "units": 3},
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
    "cpe_linear_math": {
        "title": "Linear Algebra or Linear Analysis",
        "description": "CPE students take either MATH 1151 (Linear Algebra) or MATH 2341 (Linear Analysis) as a math support requirement.",
        "courses": [
            {"course_number": "MATH 1151", "title": "Linear Algebra", "units": 3},
            {"course_number": "MATH 2341", "title": "Linear Analysis", "units": 3},
        ],
    },
    "cpe_ee_elective": {
        "title": "Electronics I or Signals and Systems",
        "description": "CPE students take either EE 3306 (Electronics I) or EE 2328 (Signals and Systems) as an EE support elective.",
        "courses": [
            {"course_number": "EE 3306", "title": "Electronics I", "units": 4},
            {"course_number": "EE 2328", "title": "Signals and Systems", "units": 4},
        ],
    },
    "cpe_stats": {
        "title": "Engineering Statistics",
        "description": "CPE students take either STAT 3210 (Engineering Statistics) or STAT 3310 (Probability and Random Processes for Engineers).",
        "courses": [
            {"course_number": "STAT 3210", "title": "Engineering Statistics", "units": 3},
            {"course_number": "STAT 3310", "title": "Probability and Random Processes for Engineers", "units": 3},
        ],
    },
    "cpe_wgqs": {
        "title": "Gender, Race, Culture, Science, and Technology",
        "description": "CPE students take either WGQS 3350 or WGQS 3351 as an ethics/society requirement.",
        "courses": [
            {"course_number": "WGQS 3350", "title": "Gender, Race, Culture, Science, and Technology", "units": 4},
            {"course_number": "WGQS 3351", "title": "Gender, Race, Class, Nation: Critical Computing and Engineering Studies", "units": 4},
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
    "arce_fe_technical_elective": {
        "title": "FE Technical Elective",
        "description": "ARCE students complete 5-6 units from the FE technical elective list.",
        "courses": [
            {"course_number": "GEOL 2240", "title": "Physical Geology", "units": 3},
            {"course_number": "GEOL 3305", "title": "Seismology and Earth Structure", "units": 3},
            {"course_number": "IME 2315", "title": "Financial Decision Making for Engineers", "units": 2},
            {"course_number": "MATH 2263", "title": "Calculus III", "units": 3},
            {"course_number": "ME 2212", "title": "Engineering Dynamics", "units": 3},
        ],
    },
    "arce_caed_interdisciplinary_elective": {
        "title": "CAED Interdisciplinary Elective",
        "description": "ARCE students take ARCE 4484, ARCE 4486, or an advisor-approved 3000-5000 level ARCH, CM, CRP, or LA course up to 3 units.",
        "courses": [
            {"course_number": "ARCE 4484", "title": "Interdisciplinary Project", "units": 3},
            {"course_number": "ARCE 4486", "title": "Collaborative Design Laboratory", "units": 2},
        ],
    },
    "me_ime_mfg_selective": {
        "title": "Manufacturing Process Selective",
        "description": "ME students select one 1-unit manufacturing process course.",
        "courses": [
            {"course_number": "IME 1141", "title": "Introduction to Metal Casting and Prototyping", "units": 1},
            {"course_number": "IME 1142", "title": "Materials Joining", "units": 1},
            {"course_number": "IME 1149", "title": "Introduction to Manufacturing Processes: Metal Casting and Joining", "units": 1},
        ],
    },
    "me_life_science": {
        "title": "Life Science Support Elective",
        "description": "ME students select one life science course that also fulfills GE Area 5B.",
        "courses": [
            {"course_number": "BIO 1111", "title": "General Biology", "units": 3},
            {"course_number": "BIO 2213", "title": "Life Science for Engineers", "units": 3},
            {"course_number": "BIO 2215", "title": "Biodiversity of California", "units": 3},
            {"course_number": "BIO 2217", "title": "Wildlife Conservation Biology", "units": 3},
        ],
    },
    "me_energy_technical_elective": {
        "title": "Energy Resources Technical Elective",
        "description": "Energy Resources students select from the approved technical elective list.",
        "courses": [
            {"course_number": "EE 3255 & EE 3255L", "title": "Electric Machines and Power Systems with Laboratory", "units": 4},
            {"course_number": "EE 4420", "title": "Sustainable Energy Generation", "units": 3},
            {"course_number": "ME 4437", "title": "Nuclear Energy Power Generation", "units": 3},
            {"course_number": "ME 4438", "title": "Nuclear Power Plant Design and Operation", "units": 3},
            {"course_number": "ME 4439", "title": "Nuclear Energy Resources", "units": 4},
            {"course_number": "ME 4443", "title": "Turbomachinery", "units": 2},
            {"course_number": "ME 4444", "title": "Design and Analysis of Internal Combustion Engines", "units": 4},
            {"course_number": "ME 4450", "title": "Solar Thermal Power Systems", "units": 3},
            {"course_number": "ME 4455", "title": "Building Energy Performance and Modeling", "units": 3},
            {"course_number": "ME 4488", "title": "Wind Power Engineering", "units": 3},
            {"course_number": "ME 5541", "title": "Advanced Thermodynamics", "units": 3},
        ],
    },
    "me_mechatronics_technical_elective": {
        "title": "Mechatronics Technical Elective",
        "description": "Mechatronics students select from the approved technical elective list.",
        "courses": [
            {"course_number": "ME 3313", "title": "Intermediate Dynamics", "units": 2},
            {"course_number": "ME 4423", "title": "Robotics: Fundamentals and Applications", "units": 4},
            {"course_number": "ME 4452", "title": "Machine Learning in Mechanical Engineering", "units": 4},
            {"course_number": "ME 5305", "title": "Mechatronics III", "units": 3},
            {"course_number": "ME 5506", "title": "System Dynamics", "units": 3},
        ],
    },
    "me_manufacturing_elective": {
        "title": "Manufacturing Elective",
        "description": "Manufacturing students select from the approved technical elective list.",
        "courses": [
            {"course_number": "IME 3331", "title": "Intermediate Metal Casting", "units": 4},
            {"course_number": "IME 3336", "title": "Advanced Computer Aided Manufacturing", "units": 3},
            {"course_number": "IME 3356", "title": "Manufacturing and Process Automation", "units": 4},
            {"course_number": "IME 4418", "title": "Product and Process Development", "units": 4},
            {"course_number": "IME 4428", "title": "Engineering Metrology", "units": 3},
            {"course_number": "IME 4432", "title": "Additive Manufacturing", "units": 3},
            {"course_number": "IME 4435", "title": "Reliability for Design and Testing", "units": 3},
            {"course_number": "IME 4450", "title": "Computer-Aided Manufacturing and Process Analysis", "units": 4},
            {"course_number": "IME 5543", "title": "Applied Human Factors", "units": 3},
            {"course_number": "MATE 4434 & MATE 4435", "title": "Micro/Nano Fabrication with Laboratory", "units": 3},
            {"course_number": "ME 3305", "title": "Mechatronics I", "units": 4},
            {"course_number": "ME 4380", "title": "Composites Manufacturing, Machining, and Testing", "units": 3},
            {"course_number": "ME 4480", "title": "Composite Materials Analysis and Design", "units": 3},
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
    "bioc_research_or_methods2": {
        "title": "Undergraduate Research or Research Methods II",
        "description": "BIOC students take one of these two research courses as a major requirement.",
        "courses": [
            {"course_number": "CHEM 2201", "title": "Undergraduate Research", "units": 1},
            {"course_number": "CHEM 2203", "title": "Research Methods II", "units": 1},
        ],
    },
    "bioc_mol_bio_or_protein": {
        "title": "Molecular Biology or Protein Techniques",
        "description": "BIOC students take one of these two laboratory technique courses as a major requirement.",
        "courses": [
            {"course_number": "CHEM 4453", "title": "Molecular Biology Techniques", "units": 2},
            {"course_number": "CHEM 4454", "title": "Protein Techniques", "units": 2},
        ],
    },
    "bioc_chem_advanced_elective": {
        "title": "Biochemistry Advanced Elective",
        "description": "BIOC students select 2–3 units from this list of advanced biochemistry electives.",
        "courses": [
            {"course_number": "CHEM 4450", "title": "Nutritional Biochemistry", "units": 2},
            {"course_number": "CHEM 4452", "title": "Physical Biochemistry Methods and Applications", "units": 2},
            {"course_number": "CHEM 4456", "title": "Chemical Biology", "units": 2},
            {"course_number": "CHEM 4457", "title": "Chemistry of Drugs and Poisons", "units": 2},
            {"course_number": "CHEM 4458", "title": "Neurochemistry", "units": 3},
        ],
    },
    "bioc_bio_mcro_advanced_elective": {
        "title": "BIO or MCRO Advanced Elective",
        "description": "BIOC students select 3–4 units from approved upper-division Biology and Microbiology courses.",
        "courses": [
            {"course_number": "BIO 3351", "title": "Principles of Genetics", "units": 3},
            {"course_number": "BIO 3352", "title": "Principles of Animal Physiology", "units": 4},
            {"course_number": "BIO 4433", "title": "Neuroscience", "units": 3},
            {"course_number": "BIO 4434", "title": "Endocrinology", "units": 3},
            {"course_number": "BIO 4451", "title": "Bioinformatics Applications", "units": 4},
            {"course_number": "BIO 4452", "title": "Cell Biology", "units": 3},
            {"course_number": "BIO 4455", "title": "Developmental Biology", "units": 3},
            {"course_number": "BIO 4456", "title": "Immunology", "units": 4},
            {"course_number": "BIO 4458", "title": "Hematology", "units": 3},
            {"course_number": "MCRO 4402", "title": "General Virology", "units": 3},
            {"course_number": "MCRO 4423", "title": "Medical Microbiology", "units": 4},
            {"course_number": "MCRO 4424", "title": "Microbial Physiology and Biochemistry", "units": 4},
        ],
    },
    "chem_research_or_methods": {
        "title": "Undergraduate Research or Research Methods II",
        "description": "CHEM students take one of these two research courses as a major requirement.",
        "courses": [
            {"course_number": "CHEM 2201", "title": "Undergraduate Research", "units": 1},
            {"course_number": "CHEM 2203", "title": "Research Methods II", "units": 1},
        ],
    },
    "chem_subdiscipline_elective": {
        "title": "Advanced Subdiscipline Elective",
        "description": "CHEM students select courses from two different subdisciplines: Analytical, Biochemistry, Inorganic, Organic, Physical Chemistry, or Polymers.",
        "courses": [
            {"course_number": "CHEM 2244", "title": "Organic Chemistry II", "units": 4},
            {"course_number": "CHEM 3320", "title": "Inorganic Chemistry II: Group Theory and Spectroscopy", "units": 3},
            {"course_number": "CHEM 3321", "title": "Inorganic Chemistry II Laboratory", "units": 2},
            {"course_number": "CHEM 3354", "title": "Metabolism", "units": 3},
            {"course_number": "CHEM 3356", "title": "Genetic Information Processing", "units": 4},
            {"course_number": "CHEM 3394", "title": "Physical Chemistry II", "units": 3},
            {"course_number": "CHEM 3395", "title": "Physical Chemistry Laboratory II", "units": 2},
            {"course_number": "CHEM 4420", "title": "Inorganic Chemistry III: Transition Metals in Context", "units": 2},
            {"course_number": "CHEM 4430", "title": "Instrumental Analysis", "units": 5},
            {"course_number": "CHEM 4432", "title": "Advanced Techniques in Chemical Analysis", "units": 2},
            {"course_number": "CHEM 4440", "title": "Advanced Organic Chemistry - Mechanisms", "units": 2},
            {"course_number": "CHEM 4442", "title": "Advanced Organic Chemistry - Synthesis", "units": 2},
            {"course_number": "CHEM 4444", "title": "Advanced Organic Chemistry Laboratory", "units": 2},
            {"course_number": "CHEM 4450", "title": "Nutritional Biochemistry", "units": 2},
            {"course_number": "CHEM 4451", "title": "Bioinformatics Applications", "units": 4},
            {"course_number": "CHEM 4452", "title": "Physical Biochemistry Methods and Applications", "units": 2},
            {"course_number": "CHEM 4453", "title": "Molecular Biology Techniques", "units": 2},
            {"course_number": "CHEM 4454", "title": "Protein Techniques", "units": 2},
            {"course_number": "CHEM 4456", "title": "Chemical Biology", "units": 2},
            {"course_number": "CHEM 4457", "title": "Chemistry of Drugs and Poisons", "units": 2},
            {"course_number": "CHEM 4458", "title": "Neurochemistry", "units": 3},
            {"course_number": "CHEM 4480", "title": "Polymer Synthesis and Characterization", "units": 3},
            {"course_number": "CHEM 4481", "title": "Polymer Synthesis and Characterization Laboratory", "units": 2},
            {"course_number": "CHEM 4482", "title": "Coatings and Formulations", "units": 3},
            {"course_number": "CHEM 4483", "title": "Coatings and Formulations Laboratory", "units": 2},
            {"course_number": "CHEM 4486", "title": "Surface Chemistry of Materials", "units": 3},
            {"course_number": "CHEM 4490", "title": "Computational Chemistry", "units": 2},
        ],
    },
    "mate_chem_elective": {
        "title": "Chemistry Elective",
        "description": "MATE students select one chemistry course: CHEM 1122 (Fundamentals of Chemical Reactivity) or CHEM 2240 (Organic Chemistry: Fundamentals and Applications).",
        "courses": [
            {"course_number": "CHEM 1122", "title": "Fundamentals of Chemical Reactivity", "units": 4},
            {"course_number": "CHEM 2240", "title": "Organic Chemistry: Fundamentals and Applications", "units": 4},
        ],
    },
    "mate_design_elective": {
        "title": "Design Elective",
        "description": "MATE students select one design elective: IME 3326 (Statistical Decision-Making and Quality Control) or ME 3234 (Design Thinking and Creativity).",
        "courses": [
            {"course_number": "IME 3326", "title": "Statistical Decision-Making and Quality Control", "units": 4},
            {"course_number": "ME 3234", "title": "Design Thinking and Creativity", "units": 3},
        ],
    },
    "ie_intro_lab": {
        "title": "IE Introductory Lab Course",
        "description": "IE students select one introductory laboratory course from the following options.",
        "courses": [
            {"course_number": "IME 1141", "title": "Introduction to Metal Casting and Prototyping", "units": 1},
            {"course_number": "IME 1142", "title": "Materials Joining", "units": 1},
            {"course_number": "IME 1156", "title": "Introduction to Modern Electronics Manufacturing", "units": 2},
        ],
    },
    "ie_linear_math": {
        "title": "Linear Mathematics",
        "description": "IE students select either Linear Algebra or Linear Analysis.",
        "courses": [
            {"course_number": "MATH 1151", "title": "Linear Algebra", "units": 3},
            {"course_number": "MATH 2341", "title": "Linear Analysis", "units": 4},
        ],
    },
    "ie_support_elective": {
        "title": "Technical Science Support Elective",
        "description": "IE students select one technical science support course track: mechanics, circuits, or materials.",
        "courses": [
            {"course_number": "ENGR 2211", "title": "Introduction to Mechanics", "units": 3},
            {"course_number": "EE 2115", "title": "Circuits & Electronics for Non-Majors (with lab)", "units": 3},
            {"course_number": "EE 2201", "title": "Electric Circuits for Non-Majors (with lab)", "units": 4},
            {"course_number": "MATE 1220", "title": "Principles of Materials Engineering for Non-Majors (with lab)", "units": 3},
        ],
    },
    "ee_power_required": {
        "title": "Power Required Course",
        "description": "Power concentration students take one of these as a required course in Senior Fall.",
        "courses": [
            {"course_number": "EE 4406", "title": "Power System Analysis I", "units": 3},
            {"course_number": "EE 4410", "title": "Fundamentals of Power Electronics", "units": 3},
        ],
    },
    "ee_power_elective": {
        "title": "Power Concentration Elective",
        "description": "Power concentration students select from the approved power-focused EE elective list.",
        "courses": [
            {"course_number": "EE 4406", "title": "Power System Analysis I", "units": 3},
            {"course_number": "EE 4407", "title": "Power System Analysis II", "units": 3},
            {"course_number": "EE 4410", "title": "Fundamentals of Power Electronics", "units": 3},
            {"course_number": "EE 4417", "title": "Electric Machines", "units": 3},
            {"course_number": "EE 4420", "title": "Sustainable Energy Generation", "units": 3},
            {"course_number": "EE 4433", "title": "Magnetic Apparatus Design", "units": 3},
            {"course_number": "EE 4434", "title": "Transportation Electrification and Energy Storage Systems", "units": 3},
            {"course_number": "EE 4435", "title": "Industrial Power Control and Automation", "units": 3},
            {"course_number": "EE 4450", "title": "Solar Photovoltaic System Engineering I", "units": 3},
            {"course_number": "EE 4470", "title": "Special Advanced Topics", "units": 3},
            {"course_number": "EE 4471", "title": "Special Advanced Laboratory", "units": 1},
            {"course_number": "EE 5510", "title": "Advanced Power Electronics", "units": 4},
            {"course_number": "EE 5511", "title": "Advanced Electric Machines and Design", "units": 4},
            {"course_number": "EE 5512", "title": "Advanced Control Techniques in Modern Power Systems", "units": 4},
            {"course_number": "EE 5517", "title": "Data Analytics for Cyber-Physical Systems", "units": 4},
            {"course_number": "EE 5518", "title": "Power System Protection", "units": 4},
            {"course_number": "EE 5519", "title": "Electric Power Distribution and Microgrids", "units": 4},
            {"course_number": "EE 5520", "title": "Advanced Solar-Photovoltaic Systems Design", "units": 4},
            {"course_number": "EE 5535", "title": "Utility Applications of Power Electronics and Power Quality", "units": 4},
        ],
    },
    "ee_ecc_elective": {
        "title": "Electronics, Controls, and Communications Elective",
        "description": "ECC concentration students select from the approved electronics, controls, and communications EE elective list.",
        "courses": [
            {"course_number": "BMED 4434", "title": "Micro/Nano Fabrication", "units": 3},
            {"course_number": "EE 4410", "title": "Fundamentals of Power Electronics", "units": 3},
            {"course_number": "EE 4412", "title": "Advanced Analog and Mixed-Signal Electronics", "units": 3},
            {"course_number": "EE 4416", "title": "Digital Communication Systems", "units": 3},
            {"course_number": "EE 4418", "title": "Photonic Component and System Engineering and Lab", "units": 4},
            {"course_number": "EE 4419", "title": "Digital Signal Processing", "units": 3},
            {"course_number": "EE 4425", "title": "Signal Integrity Electronics and Test Automation and Lab", "units": 4},
            {"course_number": "EE 4431", "title": "Computer-Aided Design of VLSI Devices", "units": 3},
            {"course_number": "EE 4440", "title": "Wireless Communications and Lab", "units": 4},
            {"course_number": "EE 4470", "title": "Special Advanced Topics", "units": 3},
            {"course_number": "EE 4471", "title": "Special Advanced Laboratory", "units": 1},
            {"course_number": "EE 5344", "title": "Phased Array Antennas", "units": 4},
            {"course_number": "EE 5424", "title": "Principles of Remote Sensing and Radar", "units": 4},
            {"course_number": "EE 5502", "title": "Microwave and Millimeter Wave Device and System Electronics", "units": 4},
            {"course_number": "EE 5504", "title": "Software Defined Radio", "units": 4},
            {"course_number": "EE 5509", "title": "Computational Intelligence", "units": 4},
            {"course_number": "EE 5513", "title": "Modern Control Systems", "units": 4},
            {"course_number": "EE 5514", "title": "Advanced Modern Control Systems", "units": 4},
            {"course_number": "EE 5515", "title": "Advanced Digital Signal Processing", "units": 4},
            {"course_number": "EE 5524", "title": "Solid State Electronics", "units": 4},
            {"course_number": "EE 5525", "title": "Stochastic Processes", "units": 4},
            {"course_number": "EE 5526", "title": "Advanced Digital Communications", "units": 4},
            {"course_number": "EE 5530", "title": "Advanced Photonic Systems", "units": 4},
            {"course_number": "EE 5531", "title": "Advanced VLSI Design and Validation", "units": 4},
            {"course_number": "EE 5532", "title": "VLSI Test Laboratory", "units": 1},
            {"course_number": "EE 5533", "title": "Antennas", "units": 4},
            {"course_number": "EE 5544", "title": "Solid-state Electronics Laboratory", "units": 1},
        ],
    },
    "ee_senior_proj_lab_i": {
        "title": "Senior Project Design Lab I",
        "description": "EE students complete one of these senior project design lab options in Senior Fall.",
        "courses": [
            {"course_number": "EE 4463", "title": "Senior Project Design Laboratory I", "units": 1},
            {"course_number": "EE 4465", "title": "Senior Design: Individual Project I", "units": 1},
        ],
    },
    "ee_senior_proj_lab_ii": {
        "title": "Senior Project Design Lab II",
        "description": "EE students complete one of these senior project design lab options in Senior Spring.",
        "courses": [
            {"course_number": "EE 4464", "title": "Senior Project Design Laboratory II", "units": 1},
            {"course_number": "EE 4466", "title": "Senior Design: Individual Project II", "units": 1},
        ],
    },
    "crp_stat_data_support": {
        "title": "Statistical and Data Literacy",
        "description": "CRP students select one statistics or data course that also satisfies GE Area 2.",
        "courses": [
            {"course_number": "DATA 1000", "title": "Statistical and Data Literacy", "units": 3},
            {"course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3},
        ],
    },
    "crp_senior_project": {
        "title": "Senior Project",
        "description": "CRP students complete their senior project as either a written report or a studio project.",
        "courses": [
            {"course_number": "CRP 4461", "title": "Senior Project", "units": 2},
            {"course_number": "CRP 4463", "title": "Senior Project - Studio", "units": 2},
        ],
    },
    "crp_caed_elective": {
        "title": "CAED Designated Elective",
        "description": "CRP students select from CAED-approved elective courses covering architecture, construction, landscape, environmental design, and planning topics.",
        "courses": [
            {"course_number": "ARCE 2280", "title": "History of Structures", "units": 3},
            {"course_number": "ARCH 3325", "title": "Topics in Architectural History, Theory, and Criticism", "units": 3},
            {"course_number": "ARCH 4445", "title": "Topics in Architectural Technology and Practice", "units": 3},
            {"course_number": "CM 3317", "title": "Sustainability and the Built Environment", "units": 3},
            {"course_number": "CM 3318", "title": "Housing and Communities", "units": 3},
            {"course_number": "CM 3334", "title": "Construction Law", "units": 2},
            {"course_number": "CM 3335", "title": "Construction Economics, Finance, and Accounting", "units": 3},
            {"course_number": "CM 4475", "title": "Real Property Development Principles", "units": 3},
            {"course_number": "CRP 3303", "title": "Smart Cities", "units": 3},
            {"course_number": "CRP 3334", "title": "Cities in a Global World", "units": 3},
            {"course_number": "CRP 4428", "title": "International Planning and Development", "units": 3},
            {"course_number": "CRP 4448", "title": "Principles of Urban Design", "units": 3},
            {"course_number": "CRP 4458", "title": "Hazard Mitigation Planning and Resilient Design", "units": 3},
            {"course_number": "CRP 4481", "title": "Urban Design and Real Estate Development Case Studies", "units": 3},
            {"course_number": "EDES 3350", "title": "The Global Environment", "units": 3},
            {"course_number": "EDES 4406", "title": "Sustainable Environments", "units": 4},
            {"course_number": "EDES 4408", "title": "Implementing Sustainability Principles", "units": 4},
            {"course_number": "LA 4410", "title": "Sustainability, Resilience, and Climate Ecology in Design", "units": 3},
            {"course_number": "LA 4413", "title": "Social Equity and Design", "units": 3},
            {"course_number": "LA 4417", "title": "Social and Behavioral Factors for Landscape Architecture", "units": 3},
            {"course_number": "LA 4418", "title": "Contemporary Issues in Landscape Architecture", "units": 3},
        ],
    },
    "cd_foundational_course": {
        "title": "Foundational CD Course",
        "description": "CD students select one of these foundational courses in their freshman year.",
        "courses": [
            {"course_number": "CD 1131", "title": "Observing and Interacting with Children", "units": 3},
            {"course_number": "CD 2202", "title": "Developmental Science Technology Activity", "units": 3},
            {"course_number": "CD 2254", "title": "Child, Family, and Community", "units": 3},
        ],
    },
    "cd_lifestage_elective": {
        "title": "Life Stage Development Course",
        "description": "CD students must take two different life stage development courses (one per semester) covering infancy/toddlerhood, childhood, or adolescence.",
        "courses": [
            {"course_number": "CD 3304", "title": "Infant and Toddler Development", "units": 4},
            {"course_number": "CD 3305", "title": "Early and Middle Childhood Development", "units": 4},
            {"course_number": "CD 3306", "title": "Adolescence", "units": 4},
        ],
    },
    "cd_professional_skills": {
        "title": "Professional Skills Course",
        "description": "CD students select one approved professional skills course developing interpersonal, intercultural, and teamwork competencies.",
        "courses": [
            {"course_number": "COMS 3316", "title": "Intercultural Communication", "units": 3},
            {"course_number": "COMS 3320", "title": "Intergroup Communication", "units": 3},
            {"course_number": "PSY 3304", "title": "Intergroup Dialogues", "units": 3},
            {"course_number": "PSY 3323", "title": "The Helping Relationship", "units": 4},
            {"course_number": "PSY 3350", "title": "Teamwork", "units": 4},
        ],
    },
    "cd_dei_elective": {
        "title": "Diversity, Equity and Inclusion Course",
        "description": "CD students select one approved DEI course examining systems of power, identity, and social justice. Also satisfies GE Upper-Division Area 4.",
        "courses": [
            {"course_number": "ES 3380", "title": "Critical Race Theory", "units": 4},
            {"course_number": "ES 3381", "title": "Social Constructions of Whiteness", "units": 4},
            {"course_number": "PSY 3304", "title": "Intergroup Dialogues", "units": 3},
            {"course_number": "WGQS 3301", "title": "Contemporary Issues in Women's and Gender Studies", "units": 3},
            {"course_number": "WGQS 3330", "title": "Feminist/Queer Transnational Studies", "units": 3},
            {"course_number": "WGQS 3351", "title": "Gender, Race, Class, Nation: Critical Computing and Engineering Studies", "units": 4},
        ],
    },
    "cd_upper_div_science": {
        "title": "Upper-Division Science Course",
        "description": "CD students select one approved upper-division science course. Also satisfies GE Upper-Division Area 2/5.",
        "courses": [
            {"course_number": "BIO 3312", "title": "Human Genetics", "units": 3},
            {"course_number": "ES 3350", "title": "Gender, Race, Culture, Science, and Technology", "units": 4},
            {"course_number": "FSN 3305", "title": "Nutrition and Exercise for Health and Disease Prevention", "units": 3},
            {"course_number": "IME 3320", "title": "Human Factors and Technology", "units": 3},
            {"course_number": "ISLA 3305", "title": "Public Engagements with STEM", "units": 3},
            {"course_number": "NR 3310", "title": "Global Climate Change", "units": 3},
            {"course_number": "PSY 3344", "title": "Behavioral Genetics", "units": 3},
        ],
    },
    "cd_internship_i": {
        "title": "Research or Fieldwork Internship I",
        "description": "CD students select one first-semester internship: a research internship or a supervised fieldwork internship.",
        "courses": [
            {"course_number": "CD 4448", "title": "Research Internship I", "units": 3},
            {"course_number": "CD 4453", "title": "Supervised Fieldwork Internship I", "units": 3},
        ],
    },
    "bio_chem_organic": {
        "title": "Organic Chemistry for Biology",
        "description": "BIO students take one organic chemistry course: CHEM 2240 (Fundamentals, 4 units) or CHEM 2242 (Organic Chemistry I, 5 units).",
        "courses": [
            {"course_number": "CHEM 2240", "title": "Organic Chemistry: Fundamentals and Applications", "units": 4},
            {"course_number": "CHEM 2242", "title": "Organic Chemistry I", "units": 5},
        ],
    },
    "bio_phys_intro": {
        "title": "Introductory Physics for Biology",
        "description": "BIO students take one introductory physics course: PHYS 1121 (College Physics I) or PHYS 1141 (General Physics I).",
        "courses": [
            {"course_number": "PHYS 1121", "title": "College Physics I", "units": 4},
            {"course_number": "PHYS 1141", "title": "General Physics I", "units": 4},
        ],
    },
    "bio_senior_project": {
        "title": "Biology Senior Project",
        "description": "BIO students complete one senior project option.",
        "courses": [
            {"course_number": "BIO 4461", "title": "Senior Project - Research Proposal", "units": 2},
            {"course_number": "BIO 4462", "title": "Senior Project - Research Experience", "units": 2},
            {"course_number": "BIO 4463", "title": "Senior Project - Meta-analysis in Biology", "units": 2},
        ],
    },
    "ad_art_history_elective": {
        "title": "Upper-Division Art History Elective",
        "description": "Art and Design students select one upper-division art history course.",
        "courses": [
            {"course_number": "ART 3310", "title": "Art of the Americas", "units": 3},
            {"course_number": "ART 3311", "title": "Nineteenth Century Art of Europe and the United States", "units": 3},
            {"course_number": "ART 3313", "title": "Design History", "units": 3},
            {"course_number": "ART 3314", "title": "History and Contemporary Practices of Photography", "units": 3},
            {"course_number": "ART 3317", "title": "Asian Art Survey", "units": 3},
            {"course_number": "ART 3320", "title": "Michelangelo", "units": 3},
            {"course_number": "ART 3321", "title": "Themes in Renaissance Art", "units": 3},
            {"course_number": "ART 3322", "title": "Themes in Modern and Contemporary Art", "units": 3},
            {"course_number": "ART 3323", "title": "New Media Art History", "units": 3},
            {"course_number": "ART 3324", "title": "Politics of Abstraction", "units": 3},
            {"course_number": "ART 3327", "title": "Intersectional Feminist Art Histories", "units": 3},
        ],
    },
    "mu_ensemble_lower": {
        "title": "Major Ensemble (Lower Division)",
        "description": "Music students enroll in one major ensemble per semester. Lower-division ensembles are 1000-level.",
        "courses": [
            {"course_number": "MU 1168", "title": "Piano Accompanying", "units": 1},
            {"course_number": "MU 1171", "title": "Jazz Band", "units": 1},
            {"course_number": "MU 1172", "title": "Symphonic Band", "units": 1},
            {"course_number": "MU 1173", "title": "Wind Ensemble", "units": 1},
            {"course_number": "MU 1174", "title": "Symphony Orchestra", "units": 1},
            {"course_number": "MU 1181", "title": "PolyPhonics", "units": 1},
            {"course_number": "MU 1182", "title": "Cantabile", "units": 1},
            {"course_number": "MU 1183", "title": "University Singers", "units": 1},
            {"course_number": "MU 1184", "title": "Chamber Choir", "units": 1},
            {"course_number": "MU 1187", "title": "Vocal Jazz Ensemble", "units": 1},
            {"course_number": "MU 1188", "title": "Arab Music Ensemble", "units": 1},
        ],
    },
    "mu_ensemble_upper": {
        "title": "Major Ensemble (Upper Division)",
        "description": "Music students enroll in one major ensemble per semester. Upper-division ensembles are 3000-level.",
        "courses": [
            {"course_number": "MU 3368", "title": "Piano Accompanying", "units": 1},
            {"course_number": "MU 3371", "title": "Jazz Band", "units": 1},
            {"course_number": "MU 3372", "title": "Symphonic Band", "units": 1},
            {"course_number": "MU 3373", "title": "Wind Ensemble", "units": 1},
            {"course_number": "MU 3374", "title": "Symphony Orchestra", "units": 1},
            {"course_number": "MU 3381", "title": "PolyPhonics", "units": 1},
            {"course_number": "MU 3382", "title": "Cantabile", "units": 1},
            {"course_number": "MU 3383", "title": "University Singers", "units": 1},
            {"course_number": "MU 3384", "title": "Chamber Choir", "units": 1},
            {"course_number": "MU 3387", "title": "Vocal Jazz Ensemble", "units": 1},
            {"course_number": "MU 3388", "title": "Arab Music Ensemble", "units": 1},
        ],
    },
    "bus_senior_project": {
        "title": "Business Senior Project / Capstone",
        "description": "BUS students complete one senior project or capstone elective from the approved list.",
        "courses": [
            {"course_number": "BUS 4461", "title": "Senior Project I", "units": 2},
            {"course_number": "BUS 4462", "title": "Senior Project II", "units": 2},
            {"course_number": "BUS 4464", "title": "Applied Senior Project Seminar", "units": 3},
            {"course_number": "BUS 4465", "title": "Senior Project: Building and Launching the Technology Startup", "units": 4},
            {"course_number": "BUS 4467", "title": "Senior Project: Growing the Early Stage Startup", "units": 4},
            {"course_number": "BUS 4472", "title": "Senior Project: Volunteer Income Tax Assistance", "units": 3},
            {"course_number": "BUS 4473", "title": "Senior Project: Auditing Analytics", "units": 3},
            {"course_number": "BUS 4474", "title": "Senior Project: Low Income Taxpayer Clinic", "units": 3},
        ],
    },
    "engl_gwr_elective": {
        "title": "Upper-Division English GWR Elective",
        "description": "English students complete one upper-division English course that satisfies the Graduation Writing Requirement (GWR).",
        "courses": [
            {"course_number": "ENGL 3611", "title": "Literary Themes", "units": 4},
            {"course_number": "ENGL 3618", "title": "Research Topics in Diversity in Twentieth- and Twenty-First Century U.S. Literature", "units": 4},
            {"course_number": "ENGL 3625", "title": "Research Topics in Queer and Trans Literature and Media", "units": 4},
            {"course_number": "ENGL 3626", "title": "Intermediate Topics in Film", "units": 4},
        ],
    },
    "engl_diversity_elective": {
        "title": "English Diversity Elective",
        "description": "English students complete one 4000-level diversity elective from the approved list.",
        "courses": [
            {"course_number": "ENGL 4427", "title": "User Experience Writing and Research for Social Impact", "units": 4},
            {"course_number": "ENGL 4439", "title": "Topics in British Literature", "units": 4},
            {"course_number": "ENGL 4449", "title": "Topics in U.S. Literature", "units": 4},
            {"course_number": "ENGL 4459", "title": "Topics in Transatlantic and/or World Literature", "units": 4},
            {"course_number": "ENGL 4467", "title": "Topics in Rhetoric and Writing", "units": 4},
            {"course_number": "ENGL 4495", "title": "Topics in Applied Language Study", "units": 3},
        ],
    },
    "pols_dei_elective": {
        "title": "POLS Diversity, Equity, and Inclusion Elective",
        "description": "POLS students complete one DEI-designated course from the approved list.",
        "courses": [
            {"course_number": "POLS 3310", "title": "Politics of Race, Class, Gender, and Sexuality in the U.S.", "units": 3},
            {"course_number": "POLS 3343", "title": "Civil Rights in the U.S.", "units": 3},
            {"course_number": "POLS 4417", "title": "Feminist Legal Theory", "units": 3},
            {"course_number": "POLS 4445", "title": "Voting Rights and Representation", "units": 3},
            {"course_number": "POLS 4457", "title": "U.S. Reproductive Politics", "units": 3},
            {"course_number": "POLS 4459", "title": "The Politics of Poverty", "units": 3},
        ],
    },
    "bus_intl_elective": {
        "title": "International Business Elective",
        "description": "BUS students select one international business elective from the approved list.",
        "courses": [
            {"course_number": "BUS 3300", "title": "International Business I", "units": 3},
            {"course_number": "BUS 3301", "title": "International Business II - Country Research Analysis and Global Marketing", "units": 3},
            {"course_number": "BUS 3302", "title": "International and Cross Cultural Management", "units": 3},
            {"course_number": "BUS 3304", "title": "International Supply Chains", "units": 3},
            {"course_number": "BUS 3311", "title": "Managing Technology in the International Legal Environment", "units": 3},
            {"course_number": "BUS 3433", "title": "Global Financial Institutions and Markets", "units": 3},
            {"course_number": "BUS 4410", "title": "The Legal Environment of International Business", "units": 3},
            {"course_number": "BUS 4446", "title": "International Marketing", "units": 3},
        ],
    },
    "kine_hlth_choice": {
        "title": "Health and Society Course (GE 4B)",
        "description": "KINE students fulfill GE Area 4B with one of these two health courses.",
        "courses": [
            {"course_number": "HLTH 1155", "title": "Multicultural Perspectives and Health", "units": 3},
            {"course_number": "HLTH 1160", "title": "Women's Health and Society",            "units": 3},
        ],
    },
    "kine_math_choice": {
        "title": "Precalculus or Calculus I (GE Area 2)",
        "description": "KINE students take Precalculus (most common) or Calculus I to satisfy GE Area 2 and the math support requirement.",
        "courses": [
            {"course_number": "MATH 1007", "title": "Precalculus",  "units": 3},
            {"course_number": "MATH 1261", "title": "Calculus I",   "units": 4},
        ],
    },
    "kine_cultural_course": {
        "title": "Sport and Society Course",
        "description": "KINE students choose one sport-and-society course. Sport Science concentration students must select KINE 3325.",
        "courses": [
            {"course_number": "KINE 3323", "title": "Sport and Gender",                                    "units": 3},
            {"course_number": "KINE 3324", "title": "Sports, Media, and United States Popular Culture",    "units": 3},
            {"course_number": "KINE 3325", "title": "Sport and Physical Activity Throughout Civilizations","units": 3},
        ],
    },
    "kine_senior_project": {
        "title": "Senior Project",
        "description": "KINE students complete a 2-unit senior project in one of four formats.",
        "courses": [
            {"course_number": "KINE 4460", "title": "Senior Project - Experiential", "units": 2},
            {"course_number": "KINE 4461", "title": "Senior Project - Report",       "units": 2},
            {"course_number": "KINE 4462", "title": "Senior Project - Research",     "units": 2},
            {"course_number": "KINE 4463", "title": "Senior Project - Internship",   "units": 2},
        ],
    },
    "kine_es_elective": {
        "title": "Exercise Science Concentration Elective",
        "description": "Exercise Science students select 6 units from this approved list.",
        "courses": [
            {"course_number": "KINE 2278", "title": "Introduction to Athletic Training",                            "units": 3},
            {"course_number": "KINE 3378", "title": "Prevention and Care of Athletic Injuries",                    "units": 3},
            {"course_number": "KINE 3382", "title": "Psychological Aspects of Injury in Sport and Physical Activity","units": 3},
            {"course_number": "KINE 4400", "title": "Special Problems for Advanced Undergraduates",                "units": 2},
            {"course_number": "KINE 4401", "title": "Leadership in Health and Physical Activity Programs",         "units": 3},
            {"course_number": "KINE 4408", "title": "Physical Activity and Aging",                                 "units": 3},
            {"course_number": "KINE 4409", "title": "Interdisciplinary Projects in Biomechanics",                  "units": 3},
            {"course_number": "KINE 4445", "title": "Cardiopulmonary Physiology and Assessment",                   "units": 3},
            {"course_number": "KINE 4448", "title": "Exercise Science Seminar",                                    "units": 2},
        ],
    },
    "kine_hp_elective": {
        "title": "Health Promotion Concentration Elective",
        "description": "Health Promotion students select 8 units from this approved list.",
        "courses": [
            {"course_number": "HLTH 2200", "title": "Special Problems for Undergraduates",                         "units": 2},
            {"course_number": "HLTH 2281", "title": "Health Ambassadors",                                          "units": 1},
            {"course_number": "HLTH 3305", "title": "Drugs in Society",                                            "units": 3},
            {"course_number": "HLTH 3310", "title": "Injury Prevention",                                           "units": 3},
            {"course_number": "HLTH 3318", "title": "Applied Epidemiology",                                        "units": 4},
            {"course_number": "HLTH 4400", "title": "Special Problems for Advanced Undergraduates",                "units": 2},
            {"course_number": "HLTH 4435", "title": "Health Promotion Program Implementation and Evaluation",      "units": 3},
            {"course_number": "KINE 3349", "title": "Exercise Testing and Prescription",                           "units": 3},
            {"course_number": "KINE 3382", "title": "Psychological Aspects of Injury in Sport and Physical Activity","units": 3},
            {"course_number": "KINE 4404", "title": "Clinical Exercise Physiology",                                "units": 4},
            {"course_number": "KINE 4408", "title": "Physical Activity and Aging",                                 "units": 3},
            {"course_number": "SCM 3301",  "title": "Application Strategies and Preparation for Health Profession Programs","units": 1},
            {"course_number": "SCM 3363",  "title": "Pre-Health Shadowing Fieldwork",                             "units": 2},
        ],
    },
    "kine_ss_elective": {
        "title": "Sport Science Concentration Elective",
        "description": "Sport Science students select 6 units from this approved list.",
        "courses": [
            {"course_number": "COMS 3387", "title": "Sports Communication",                                        "units": 3},
            {"course_number": "EIM 2260",  "title": "Community Relations and Sports-Based Youth Development",     "units": 3},
            {"course_number": "KINE 2278", "title": "Introduction to Athletic Training",                            "units": 3},
            {"course_number": "KINE 3349", "title": "Exercise Testing and Prescription",                           "units": 3},
            {"course_number": "KINE 3378", "title": "Prevention and Care of Athletic Injuries",                    "units": 3},
            {"course_number": "KINE 3382", "title": "Psychological Aspects of Injury in Sport and Physical Activity","units": 3},
            {"course_number": "KINE 4404", "title": "Clinical Exercise Physiology",                                "units": 4},
            {"course_number": "KINE 4408", "title": "Physical Activity and Aging",                                 "units": 3},
            {"course_number": "KINE 4448", "title": "Exercise Science Seminar",                                    "units": 2},
        ],
    },
    "math_programming_elective": {
        "title": "Programming / Scientific Computing Elective",
        "description": "MATH students take one computing course from this approved list.",
        "courses": [
            {"course_number": "CSC 2001",  "title": "Data Structures",                          "units": 3},
            {"course_number": "CSC 2600",  "title": "Computing with Data",                      "units": 4},
            {"course_number": "MATH 3681", "title": "Mathematical Programming",                  "units": 3},
            {"course_number": "PHYS 4202", "title": "Computational Physics",                    "units": 4},
            {"course_number": "STAT 2610", "title": "Introduction to Probability and Simulation","units": 3},
        ],
    },
    "math_senior_project": {
        "title": "Senior Project Seminar",
        "description": "MATH students complete their senior project as either the standard seminar or the applied seminar.",
        "courses": [
            {"course_number": "MATH 4463", "title": "Senior Project Seminar",         "units": 3},
            {"course_number": "MATH 4464", "title": "Senior Project Applied Seminar", "units": 3},
        ],
    },
    "math_upper_div_choice": {
        "title": "Upper-Division Math Elective (GE UD 2/5)",
        "description": "MATH students satisfy the Upper-Division GE Area 2/5 requirement with one of these courses.",
        "courses": [
            {"course_number": "MATH 3051", "title": "Combinatorics I",   "units": 3},
            {"course_number": "MATH 3111", "title": "Number Theory",      "units": 3},
            {"course_number": "MATH 3301", "title": "Complex Analysis",   "units": 3},
        ],
    },
    "math_track_elective": {
        "title": "Mathematics Track Elective (General / Applied)",
        "description": "Upper-division electives for the General Mathematics or Applied Mathematics track (List A).",
        "courses": [
            {"course_number": "MATH 3011", "title": "History of Mathematics",                    "units": 3},
            {"course_number": "MATH 3051", "title": "Combinatorics I",                          "units": 3},
            {"course_number": "MATH 3055", "title": "Graph Theory",                             "units": 3},
            {"course_number": "MATH 3111", "title": "Number Theory",                             "units": 3},
            {"course_number": "MATH 3301", "title": "Complex Analysis",                          "units": 3},
            {"course_number": "MATH 3351", "title": "Differential Equations and Boundary Value Problems", "units": 3},
            {"course_number": "MATH 3511", "title": "Euclidean Geometry",                        "units": 3},
            {"course_number": "MATH 3622", "title": "Mathematics of Data Science",               "units": 3},
            {"course_number": "MATH 3651", "title": "Introduction to Numerical Analysis",        "units": 3},
            {"course_number": "MATH 3681", "title": "Mathematical Programming",                  "units": 3},
            {"course_number": "MATH 4052", "title": "Combinatorics II",                          "units": 3},
            {"course_number": "MATH 4265", "title": "Real Analysis II",                          "units": 4},
            {"course_number": "MATH 4342", "title": "Nonlinear Dynamical Systems",               "units": 3},
            {"course_number": "MATH 4352", "title": "Partial Differential Equations",            "units": 3},
            {"course_number": "MATH 4512", "title": "Non-Euclidean Geometry",                    "units": 3},
            {"course_number": "MATH 4531", "title": "Differential Geometry",                     "units": 3},
            {"course_number": "MATH 4541", "title": "Introduction to Topology",                  "units": 3},
            {"course_number": "MATH 4652", "title": "Numerical Differential Equations",          "units": 3},
            {"course_number": "MATH 4653", "title": "Numerical Optimization",                    "units": 3},
            {"course_number": "MATH 4911", "title": "Game Theory",                               "units": 3},
            {"course_number": "MATH 4981", "title": "Advanced Topics in Mathematics",            "units": 3},
            {"course_number": "MATH 4982", "title": "Advanced Topics in Applied Mathematics",    "units": 3},
        ],
    },
    "math_track_teaching": {
        "title": "Teaching Mathematics Track Elective",
        "description": "Upper-division electives for the Teaching Mathematics track (List A plus teaching-specific courses).",
        "courses": [
            {"course_number": "MATH 3011", "title": "History of Mathematics",                    "units": 3},
            {"course_number": "MATH 3051", "title": "Combinatorics I",                          "units": 3},
            {"course_number": "MATH 3055", "title": "Graph Theory",                             "units": 3},
            {"course_number": "MATH 3111", "title": "Number Theory",                             "units": 3},
            {"course_number": "MATH 3301", "title": "Complex Analysis",                          "units": 3},
            {"course_number": "MATH 3351", "title": "Differential Equations and Boundary Value Problems", "units": 3},
            {"course_number": "MATH 3511", "title": "Euclidean Geometry",                        "units": 3},
            {"course_number": "MATH 3622", "title": "Mathematics of Data Science",               "units": 3},
            {"course_number": "MATH 3651", "title": "Introduction to Numerical Analysis",        "units": 3},
            {"course_number": "MATH 3681", "title": "Mathematical Programming",                  "units": 3},
            {"course_number": "MATH 3971", "title": "Technology in Mathematics Education",       "units": 3},
            {"course_number": "MATH 4052", "title": "Combinatorics II",                          "units": 3},
            {"course_number": "MATH 4265", "title": "Real Analysis II",                          "units": 4},
            {"course_number": "MATH 4342", "title": "Nonlinear Dynamical Systems",               "units": 3},
            {"course_number": "MATH 4352", "title": "Partial Differential Equations",            "units": 3},
            {"course_number": "MATH 4512", "title": "Non-Euclidean Geometry",                    "units": 3},
            {"course_number": "MATH 4531", "title": "Differential Geometry",                     "units": 3},
            {"course_number": "MATH 4541", "title": "Introduction to Topology",                  "units": 3},
            {"course_number": "MATH 4652", "title": "Numerical Differential Equations",          "units": 3},
            {"course_number": "MATH 4653", "title": "Numerical Optimization",                    "units": 3},
            {"course_number": "MATH 4911", "title": "Game Theory",                               "units": 3},
            {"course_number": "MATH 4972", "title": "Advanced Mathematics for Teaching",         "units": 3},
            {"course_number": "MATH 4981", "title": "Advanced Topics in Mathematics",            "units": 3},
            {"course_number": "MATH 4982", "title": "Advanced Topics in Applied Mathematics",    "units": 3},
        ],
    },
    # ── MANUFACTURING ENGINEERING ─────────────────────────────────────────────
    "mfge_linear_math": {
        "title": "Linear Algebra or Linear Analysis",
        "description": "Select MATH 1151 (Linear Algebra, 3 units) or MATH 2341 (Linear Analysis, 4 units). MATH 2341 adds 1 unit to the program total (128 → 129 units).",
        "courses": [
            {"course_number": "MATH 1151", "title": "Linear Algebra",   "units": 3},
            {"course_number": "MATH 2341", "title": "Linear Analysis",  "units": 4},
        ],
    },
    # ── PHYSICS ──────────────────────────────────────────────────────────────
    "phys_lab_elective": {
        "title": "Physics Lab Elective",
        "description": "Select one lab elective from: PHYS 3323 (Optics), PHYS 4425 (Solid State Physics), PHYS 4428 (Nonlinear Dynamics and Chaos), or ASTR 4444 (Observational Astronomy).",
        "courses": [
            {"course_number": "PHYS 3323", "title": "Optics",                                    "units": 4},
            {"course_number": "PHYS 4425", "title": "Solid State Physics",                       "units": 4},
            {"course_number": "PHYS 4428", "title": "Nonlinear Dynamics and Chaos",              "units": 4},
            {"course_number": "ASTR 4444", "title": "Observational Astronomy",                   "units": 4},
        ],
    },
    # ── JOURNALISM ───────────────────────────────────────────────────────────
    "jour_stat_choice": {
        "title": "Statistics",
        "description": "Select one statistics course to satisfy the support requirement. Any of these three options are accepted.",
        "courses": [
            {"course_number": "STAT 1000", "title": "Statistical and Data Literacy",       "units": 3},
            {"course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3},
            {"course_number": "STAT 1210", "title": "Business Statistics I",                "units": 3},
        ],
    },
    "jour_crosscultural": {
        "title": "Mass Media in a Cross-Cultural Society or Global Communication",
        "description": "Select either JOUR 2219 or JOUR 3319 to satisfy this cross-cultural communication requirement.",
        "courses": [
            {"course_number": "JOUR 2219", "title": "Mass Media in a Cross-Cultural Society", "units": 3},
            {"course_number": "JOUR 3319", "title": "Global Communication",                  "units": 3},
        ],
    },
    "jour_mi_method": {
        "title": "Media Innovation: Method Elective",
        "description": "Select JOUR 3345 (Social Media for Strategic Communication) or JOUR 3310 (Advanced Digital Journalism).",
        "courses": [
            {"course_number": "JOUR 3345", "title": "Social Media for Strategic Communication", "units": 3},
            {"course_number": "JOUR 3310", "title": "Advanced Digital Journalism",               "units": 3},
        ],
    },
    "jour_mi_practicum": {
        "title": "Media Innovation: Advanced Practicum",
        "description": "Select JOUR 3352 (Advanced News Reporting Practicum) or JOUR 3353 (Advanced Broadcast Journalism Practicum).",
        "courses": [
            {"course_number": "JOUR 3352", "title": "Advanced News Reporting Practicum",          "units": 3},
            {"course_number": "JOUR 3353", "title": "Advanced Broadcast Journalism Practicum",    "units": 3},
        ],
    },
    "jour_news_elective": {
        "title": "News Concentration Elective",
        "description": "Select from the Writing/Digital path (JOUR 3307, 3350, 3352) or the Audio/Visual path (JOUR 3333, 3338, 3346, 3348, 3353, 3378).",
        "courses": [
            {"course_number": "JOUR 3307", "title": "Feature Writing",                           "units": 3},
            {"course_number": "JOUR 3333", "title": "Broadcast News",                            "units": 3},
            {"course_number": "JOUR 3338", "title": "Podcasting",                                "units": 3},
            {"course_number": "JOUR 3346", "title": "Broadcast Announcing and Production",       "units": 3},
            {"course_number": "JOUR 3348", "title": "Video News Gathering",                      "units": 3},
            {"course_number": "JOUR 3350", "title": "Data Journalism",                           "units": 3},
            {"course_number": "JOUR 3352", "title": "Advanced News Reporting Practicum",         "units": 3},
            {"course_number": "JOUR 3353", "title": "Advanced Broadcast Journalism Practicum",   "units": 3},
            {"course_number": "JOUR 3378", "title": "Advanced Sportscasting",                    "units": 3},
        ],
    },
    "jour_pr_or_choice": {
        "title": "Public Relations: Or-Choice Elective",
        "description": "Select one of JOUR 3314 (PR & Crisis Management), JOUR 3315 (PR & Advertising Production), or JOUR 3345 (Social Media for Strategic Communication).",
        "courses": [
            {"course_number": "JOUR 3314", "title": "Public Relations and Crisis Management",          "units": 3},
            {"course_number": "JOUR 3315", "title": "Public Relations and Advertising Production",     "units": 3},
            {"course_number": "JOUR 3345", "title": "Social Media for Strategic Communication",        "units": 3},
        ],
    },
    # ── FOOD SCIENCE AND NUTRITION ────────────────────────────────────────────
    "fsn_senior_project": {
        "title": "Food Science Senior Project",
        "description": "Choose one senior project option: FDSC 4460 (Undergraduate Research), FDSC 4461 (Senior Project I), or FDSC 4462 (Senior Project II, Culinology emphasis).",
        "courses": [
            {"course_number": "FDSC 4460", "title": "Undergraduate Research",                    "units": 2},
            {"course_number": "FDSC 4461", "title": "Senior Project in Food Science I",          "units": 2},
            {"course_number": "FDSC 4462", "title": "Senior Project in Food Science II",         "units": 2},
        ],
    },
    "fsn_fs_elective": {
        "title": "Food Safety Concentration Elective",
        "description": "Approved electives for the Food Safety concentration. Select from agricultural, food, or microbiology courses at the 3000–5000 level.",
        "courses": [
            {"course_number": "ASCI 4415", "title": "Food Animal Welfare",                       "units": 3},
            {"course_number": "DSCI 3344", "title": "Dairy Foods Technology",                    "units": 3},
            {"course_number": "DSCI 4402", "title": "Dairy Plant Operations",                    "units": 3},
            {"course_number": "FDSC 5545", "title": "Advanced Food Safety",                      "units": 3},
            {"course_number": "MCRO 3342", "title": "Industrial Microbiology",                   "units": 3},
            {"course_number": "PLSC 4421", "title": "Postharvest Physiology and Technology",     "units": 3},
        ],
    },
    "fsn_sft_elective": {
        "title": "Sustainable Food Technology Concentration Elective",
        "description": "Approved electives for the Sustainable Food Technology concentration. Select from bioresource and agricultural engineering courses.",
        "courses": [
            {"course_number": "BRAE 3348", "title": "Irrigation Systems Design",                 "units": 3},
            {"course_number": "BRAE 3349", "title": "Drainage and Water Management",             "units": 3},
            {"course_number": "BRAE 5436", "title": "Precision Agriculture",                     "units": 3},
            {"course_number": "NR 3324",   "title": "Ecosystem Management",                      "units": 3},
        ],
    },
    "cm_accounting_choice": {
        "title": "Financial Accounting Course Choice",
        "description": "Select one: Financial Accounting for Nonbusiness Majors (BUS 2212) or Financial Accounting (BUS 2214).",
        "courses": [
            {"course_number": "BUS 2212", "title": "Financial Accounting for Nonbusiness Majors", "units": 3},
            {"course_number": "BUS 2214", "title": "Financial Accounting",                         "units": 3},
        ],
    },
    "cm_major_elective": {
        "title": "Construction Management Major Elective",
        "description": "Select one 3-unit elective from the approved list of architecture, construction, planning, and landscape architecture courses.",
        "courses": [
            {"course_number": "ARCH 4415", "title": "Topics in Design",                                                    "units": 3},
            {"course_number": "ARCH 4435", "title": "Advanced Topics in Architectural Representation",                     "units": 3},
            {"course_number": "CM 4421",   "title": "Interdisciplinary Practices",                                         "units": 3},
            {"course_number": "CM 4475",   "title": "Real Property Development Principles",                                "units": 3},
            {"course_number": "CRP 3303",  "title": "Smart Cities",                                                        "units": 3},
            {"course_number": "CRP 3334",  "title": "Cities in a Global World",                                            "units": 3},
            {"course_number": "CRP 4325",  "title": "Planning for Bicycling and Walking",                                  "units": 3},
            {"course_number": "CRP 4433",  "title": "Latino Urbanism",                                                     "units": 3},
            {"course_number": "CRP 4442",  "title": "Planning and Housing",                                                "units": 3},
            {"course_number": "CRP 4445",  "title": "Green Infrastructure",                                                "units": 3},
            {"course_number": "CRP 4455",  "title": "Transportation Policy and Planning",                                  "units": 3},
            {"course_number": "CRP 4458",  "title": "Hazard Mitigation Planning and Resilient Design",                    "units": 3},
            {"course_number": "CRP 4481",  "title": "Urban Design and Real Estate Development Case Studies",               "units": 3},
            {"course_number": "LA 3304",   "title": "Contemporary Issues in Cultural Landscapes",                          "units": 3},
            {"course_number": "LA 4410",   "title": "Sustainability, Resilience, and Climate Ecology in Design",           "units": 3},
            {"course_number": "LA 4413",   "title": "Social Equity and Design",                                            "units": 3},
            {"course_number": "LA 4417",   "title": "Social and Behavioral Factors for Landscape Architecture",            "units": 3},
            {"course_number": "LA 4418",   "title": "Contemporary Issues in Landscape Architecture",                       "units": 3},
        ],
    },
    "soc_wi_elective": {
        "title": "SOC Writing-Intensive Upper-Division Elective",
        "description": "Select one 3-unit upper-division writing-intensive SOC course.",
        "courses": [
            {"course_number": "SOC 3315", "title": "Global Race and Ethnic Relations",   "units": 3},
            {"course_number": "SOC 3321", "title": "Migration",                          "units": 3},
            {"course_number": "SOC 3326", "title": "Sociology of the Life Course",       "units": 3},
            {"course_number": "SOC 3343", "title": "Sociology of the Global South",      "units": 3},
        ],
    },
    "soc_cj_req_choice": {
        "title": "Criminal Justice Required Course Choice",
        "description": "Select one: Gender, Crime, and Violence or Contemporary Issues in Criminal Justice.",
        "courses": [
            {"course_number": "SOC 4402", "title": "Gender, Crime, and Violence",                    "units": 4},
            {"course_number": "SOC 4412", "title": "Contemporary Issues in Criminal Justice",         "units": 4},
        ],
    },
    "soc_cj_elective": {
        "title": "Criminal Justice Concentration Elective",
        "description": "Approved electives for the Criminal Justice concentration. Select SOC courses from the approved list.",
        "courses": [
            {"course_number": "SOC 3303", "title": "Social Work, Social Advocacy, and Social Service Agencies", "units": 4},
            {"course_number": "SOC 3395", "title": "Sociology of Complex Organizations",                         "units": 4},
            {"course_number": "SOC 4406", "title": "Juvenile Justice and Delinquency",                           "units": 4},
            {"course_number": "SOC 4414", "title": "Theories of Social Work in Counseling Agencies",             "units": 4},
            {"course_number": "SOC 4444", "title": "Incarceration and Society",                                  "units": 4},
        ],
    },
    "soc_org_core": {
        "title": "Organizations Core Course Choice",
        "description": "Select one: Sociology of Complex Organizations or Gender and Work.",
        "courses": [
            {"course_number": "SOC 3395", "title": "Sociology of Complex Organizations", "units": 4},
            {"course_number": "SOC 4423", "title": "Gender and Work",                    "units": 4},
        ],
    },
    "soc_org_method": {
        "title": "Organizations Method Course",
        "description": "Select one: SOC 3310, COMS 3320, or PSY 2252.",
        "courses": [
            {"course_number": "SOC 3310",  "title": "Self, Organizations, and Society", "units": 4},
            {"course_number": "COMS 3320", "title": "Organizational Communication",     "units": 4},
            {"course_number": "PSY 2252",  "title": "Social Psychology",                "units": 4},
        ],
    },
    "soc_sj_req": {
        "title": "Social Justice Required Course",
        "description": "Select from the approved Social Justice concentration required courses list.",
        "courses": [
            {"course_number": "SOC 3305", "title": "Social Movements",                      "units": 4},
            {"course_number": "SOC 3308", "title": "Sociology of the Environment",           "units": 4},
            {"course_number": "SOC 3315", "title": "Global Race and Ethnic Relations",       "units": 3},
            {"course_number": "SOC 3321", "title": "Migration",                              "units": 3},
            {"course_number": "SOC 3327", "title": "Social Change",                          "units": 4},
            {"course_number": "SOC 3343", "title": "Sociology of the Global South",          "units": 3},
            {"course_number": "SOC 4402", "title": "Gender, Crime, and Violence",            "units": 4},
            {"course_number": "SOC 4431", "title": "World Population Processes and Problems","units": 4},
            {"course_number": "SOC 4433", "title": "Global Climate Justice",                 "units": 4},
            {"course_number": "SOC 4435", "title": "Sociology of Health and Illness",        "units": 4},
            {"course_number": "SOC 4444", "title": "Incarceration and Society",              "units": 4},
        ],
    },
    "soc_ss_elective": {
        "title": "Social Services Concentration Elective",
        "description": "Approved electives for the Social Services concentration.",
        "courses": [
            {"course_number": "SOC 3305", "title": "Social Movements",                      "units": 4},
            {"course_number": "SOC 3308", "title": "Sociology of the Environment",           "units": 4},
            {"course_number": "SOC 3395", "title": "Sociology of Complex Organizations",     "units": 4},
            {"course_number": "SOC 4402", "title": "Gender, Crime, and Violence",            "units": 4},
            {"course_number": "SOC 4431", "title": "World Population Processes and Problems","units": 4},
            {"course_number": "SOC 4435", "title": "Sociology of Health and Illness",        "units": 4},
            {"course_number": "SOC 4440", "title": "Internship",                             "units": 4},
        ],
    },
    # Landscape Architecture (LA)
    "la_bio_choice": {
        "title": "Plant Biology Requirement",
        "description": "BIO 1114 or BOT 1121.",
        "courses": [
            {"course_number": "BIO 1114", "title": "Plant Diversity and Ecology", "units": 4},
            {"course_number": "BOT 1121", "title": "General Botany",              "units": 4},
        ],
    },
    "la_des_elec1": {
        "title": "Designated Elective Group 1",
        "description": "Approved courses for Designated Elective Group 1.",
        "courses": [
            {"course_number": "ARCH 1121", "title": "Equity, Social Justice, and Architecture",        "units": 3},
            {"course_number": "CRP 1222",  "title": "The Divided City: Urban Studies on Spatial Justice","units": 3},
            {"course_number": "DATA 1000", "title": "Statistical and Data Literacy",                   "units": 3},
            {"course_number": "SS 1120",   "title": "Introductory Soil Science",                       "units": 4},
            {"course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods",        "units": 4},
        ],
    },
    "la_des_elec2": {
        "title": "Designated Elective Group 2",
        "description": "Approved courses for Designated Elective Group 2.",
        "courses": [
            {"course_number": "BIO 2215",  "title": "Biodiversity of California",       "units": 4},
            {"course_number": "BIO 2217",  "title": "Wildlife Conservation Biology",    "units": 4},
            {"course_number": "CM 2239",   "title": "Construction Surveying",           "units": 3},
            {"course_number": "GEOL 2240", "title": "Physical Geology",                 "units": 4},
        ],
    },
    "la_des_elec3": {
        "title": "Designated Elective Group 3",
        "description": "Approved courses for Designated Elective Group 3.",
        "courses": [
            {"course_number": "BOT 3311",  "title": "Plants, People and Civilization",                 "units": 4},
            {"course_number": "BOT 3326",  "title": "Plant Ecology",                                   "units": 4},
            {"course_number": "BRAE 3340", "title": "Irrigation Water Management",                     "units": 3},
            {"course_number": "COMS 3316", "title": "Intercultural Communication",                     "units": 4},
            {"course_number": "ES 3360",   "title": "Indigeneity and the Land",                        "units": 4},
            {"course_number": "GEOG 3325", "title": "Climate and Humanity",                            "units": 4},
            {"course_number": "NR 3310",   "title": "Global Climate Change",                           "units": 4},
            {"course_number": "NR 3349",   "title": "Water for a Sustainable Society",                 "units": 4},
            {"course_number": "PLSC 3334", "title": "Advanced Plant Materials",                        "units": 4},
        ],
    },
    "la_caed_theory": {
        "title": "CAED Elective: Design Theory and History",
        "description": "CAED approved elective in design theory and history.",
        "courses": [
            {"course_number": "ARCE 2280", "title": "History of Structures",                 "units": 3},
            {"course_number": "CM 3318",   "title": "Housing and Communities",               "units": 3},
            {"course_number": "CRP 3303",  "title": "Smart Cities",                          "units": 4},
            {"course_number": "CRP 3334",  "title": "Cities in a Global World",              "units": 4},
            {"course_number": "CRP 4428",  "title": "International Planning and Development","units": 4},
            {"course_number": "CRP 4433",  "title": "Latino Urbanism",                       "units": 4},
            {"course_number": "CRP 4448",  "title": "Principles of Urban Design",            "units": 4},
        ],
    },
    "la_caed_finance": {
        "title": "CAED Elective: Finance, Legal, and Implementation",
        "description": "CAED approved elective in finance, legal, and implementation.",
        "courses": [
            {"course_number": "ARCH 4445", "title": "Topics in Architectural Technology and Practice","units": 3},
            {"course_number": "CM 3334",   "title": "Construction Law",                               "units": 3},
            {"course_number": "CM 4475",   "title": "Real Property Development Principles",           "units": 3},
            {"course_number": "CRP 3315",  "title": "Public and Private Real Estate Development",     "units": 4},
            {"course_number": "CRP 4420",  "title": "Land Use Law",                                   "units": 4},
            {"course_number": "CRP 4446",  "title": "Development Review and Entitlement",             "units": 4},
            {"course_number": "LA 5531",   "title": "Information Graphics for Landscape and Urban Studies","units": 3},
            {"course_number": "LA 5538",   "title": "Advanced GIS Application to Projects",           "units": 3},
        ],
    },
    "la_caed_sustain": {
        "title": "CAED Elective: Sustainability",
        "description": "CAED approved elective in sustainability.",
        "courses": [
            {"course_number": "CM 3317",   "title": "Sustainability and the Built Environment","units": 3},
            {"course_number": "CRP 4325",  "title": "Planning for Bicycling and Walking",      "units": 4},
            {"course_number": "CRP 4445",  "title": "Green Infrastructure",                    "units": 4},
            {"course_number": "EDES 3350", "title": "The Global Environment",                  "units": 4},
            {"course_number": "EDES 4406", "title": "Sustainable Environments",                "units": 4},
            {"course_number": "LA 5520",   "title": "Urban Design with Cultural Landscapes",   "units": 3},
            {"course_number": "LA 5521",   "title": "Ecological Urban Design",                 "units": 3},
        ],
    },
    "la_pro_topics": {
        "title": "Professional Topics Elective",
        "description": "LA Professional Topics elective.",
        "courses": [
            {"course_number": "LA 4414", "title": "Advanced Landscape Construction",                               "units": 3},
            {"course_number": "LA 4415", "title": "Advanced Landscape Representation",                             "units": 3},
            {"course_number": "LA 4416", "title": "Advanced Planting Design",                                      "units": 3},
            {"course_number": "LA 4417", "title": "Social and Behavioral Factors for Landscape Architecture",      "units": 3},
            {"course_number": "LA 4418", "title": "Contemporary Issues in Landscape Architecture",                 "units": 3},
        ],
    },
    "la_studio_choice": {
        "title": "Design Studio Choice",
        "description": "Interdisciplinary or Contemporary Issues design studio.",
        "courses": [
            {"course_number": "LA 4422", "title": "Interdisciplinary Design Studio",                               "units": 4},
            {"course_number": "LA 4424", "title": "Contemporary Issues in Landscape Architecture Design Studio",   "units": 4},
        ],
    },
    # Wine and Viticulture (WVIT)
    "wvit_math_choice": {
        "title": "Calculus Requirement",
        "description": "MATH 1261 (Calculus I, 4 units) or MATH 1267 (Business Calculus, 3 units).",
        "courses": [
            {"course_number": "MATH 1261", "title": "Calculus I",         "units": 4},
            {"course_number": "MATH 1267", "title": "Business Calculus",  "units": 3},
        ],
    },
    "wvit_accounting_choice": {
        "title": "Financial Accounting",
        "description": "AGB 2214 or BUS 2214.",
        "courses": [
            {"course_number": "AGB 2214", "title": "Agribusiness Accounting",  "units": 3},
            {"course_number": "BUS 2214", "title": "Financial Accounting",     "units": 3},
        ],
    },
    "wvit_wb_micro_choice": {
        "title": "Agricultural Economics or Microeconomics",
        "description": "AGB 2212 or ECON 2030 (Wine Business concentration).",
        "courses": [
            {"course_number": "AGB 2212", "title": "Agricultural Economics",  "units": 3},
            {"course_number": "ECON 2030", "title": "Microeconomics",         "units": 3},
        ],
    },
    "wvit_wb_hr_choice": {
        "title": "Personnel or Human Resources Management",
        "description": "AGB 3369 or BUS 3384 (Wine Business concentration).",
        "courses": [
            {"course_number": "AGB 3369", "title": "Agricultural Personnel Management",  "units": 3},
            {"course_number": "BUS 3384", "title": "Human Resources Management",         "units": 3},
        ],
    },
    "wvit_senior_project": {
        "title": "Senior Project",
        "description": "WVIT 4464 (Enology/Viticulture) or WVIT 4465 (Research Experience).",
        "courses": [
            {"course_number": "WVIT 4464", "title": "Senior Project - Enology/Viticulture",  "units": 3},
            {"course_number": "WVIT 4465", "title": "Senior Project - Research Experience",   "units": 3},
        ],
    },
    # ── Economics (ECON) ──────────────────────────────────────────────────────
    "econ_intro_choice": {
        "title": "Introductory Microeconomics or Survey of Economics",
        "description": "ECON 2001 (Survey of Economics) or ECON 2030 (Microeconomics). ECON 2030 is the standard path; ECON 2001 is the survey option.",
        "courses": [
            {"course_number": "ECON 2030", "title": "Microeconomics", "units": 3},
            {"course_number": "ECON 2001", "title": "Survey of Economics", "units": 3},
        ],
    },
    "econ_macro_choice": {
        "title": "Macroeconomics or Using Big Data",
        "description": "ECON 2040 (Macroeconomics) or ECON 2021 (Using Big Data for Economics).",
        "courses": [
            {"course_number": "ECON 2040", "title": "Macroeconomics", "units": 3},
            {"course_number": "ECON 2021", "title": "Using Big Data for Economics", "units": 3},
        ],
    },
    "econ_bus_choice": {
        "title": "Legal Responsibilities or Financial Accounting",
        "description": "BUS 2207 (Legal Responsibilities of Business) or BUS 2214 (Financial Accounting).",
        "courses": [
            {"course_number": "BUS 2207", "title": "Legal Responsibilities of Business", "units": 3},
            {"course_number": "BUS 2214", "title": "Financial Accounting", "units": 3},
        ],
    },
    "econ_accounting_elective": {
        "title": "Accounting Concentration Elective",
        "description": "Select from the approved accounting elective list: BUS 4424, 4425, 4426, 4427, or 4428.",
        "courses": [
            {"course_number": "BUS 4424", "title": "Advanced Auditing", "units": 3},
            {"course_number": "BUS 4425", "title": "Advanced Accounting", "units": 3},
            {"course_number": "BUS 4426", "title": "Accounting Information Systems", "units": 3},
            {"course_number": "BUS 4427", "title": "Governmental and Nonprofit Accounting", "units": 3},
            {"course_number": "BUS 4428", "title": "Cost Accounting", "units": 3},
        ],
    },
    "econ_info_sys_project": {
        "title": "Information Systems Project Course",
        "description": "Select one project or capstone course for the Information Systems and Analytics concentration.",
        "courses": [
            {"course_number": "BUS 4492", "title": "Project Management", "units": 3},
            {"course_number": "BUS 4497", "title": "Business Analytics", "units": 3},
        ],
    },
    "econ_mgmt_hr_project": {
        "title": "Management and HR Project Course",
        "description": "Select one project or consulting course for the Management and Human Resources concentration.",
        "courses": [
            {"course_number": "BUS 4477", "title": "Management Consulting, Change, and Development", "units": 3},
            {"course_number": "BUS 4489", "title": "Negotiation", "units": 3},
        ],
    },
    "eim_math_elective": {
        "title": "Mathematics Requirement",
        "description": "MATH 1004 (Stretch College Algebra), MATH 1006 (College Algebra), MATH 1007 (Precalculus), or MATH 1267 (Business Calculus). All satisfy GE Area 2.",
        "courses": [
            {"course_number": "MATH 1004", "title": "Stretch College Algebra", "units": 3},
            {"course_number": "MATH 1006", "title": "College Algebra", "units": 3},
            {"course_number": "MATH 1007", "title": "Precalculus", "units": 4},
            {"course_number": "MATH 1267", "title": "Business Calculus", "units": 4},
        ],
    },
    "eim_acct_choice": {
        "title": "Financial Accounting",
        "description": "BUS 2212 (Financial Accounting for Nonbusiness Majors) or AGB 2214 (Agricultural Business Accounting).",
        "courses": [
            {"course_number": "BUS 2212", "title": "Financial Accounting for Nonbusiness Majors", "units": 3},
            {"course_number": "AGB 2214", "title": "Agricultural Business Accounting", "units": 3},
        ],
    },
    "eim_stat_choice": {
        "title": "Statistics",
        "description": "STAT 1110 (Applied Statistical Concepts and Methods) or STAT 1210 (Business Statistics I).",
        "courses": [
            {"course_number": "STAT 1110", "title": "Applied Statistical Concepts and Methods", "units": 3},
            {"course_number": "STAT 1210", "title": "Business Statistics I", "units": 3},
        ],
    },
    "eim_mgmt_acct_choice": {
        "title": "Managerial Accounting",
        "description": "BUS 2215 (Managerial Accounting for Nonbusiness Majors) or AGB 3323 (Agricultural Business Finance).",
        "courses": [
            {"course_number": "BUS 2215", "title": "Managerial Accounting for Nonbusiness Majors", "units": 3},
            {"course_number": "AGB 3323", "title": "Agricultural Business Finance", "units": 3},
        ],
    },
    "eim_senior_project": {
        "title": "Senior Project",
        "description": "EIM 4460 (Senior Project: Community Engagement) or EIM 4461 (Senior Project: Industry Partner).",
        "courses": [
            {"course_number": "EIM 4460", "title": "Senior Project: Community Engagement", "units": 3},
            {"course_number": "EIM 4461", "title": "Senior Project: Industry Partner", "units": 3},
        ],
    },
    "eim_event_elective": {
        "title": "Event Planning and Management Concentration Elective",
        "description": "Select from approved Event Planning and Management concentration electives.",
        "courses": [
            {"course_number": "BUS 2207", "title": "Legal Responsibilities of Business", "units": 3},
            {"course_number": "COMS 2211", "title": "Interpersonal Communication", "units": 3},
            {"course_number": "COMS 3301", "title": "Business and Professional Communication", "units": 3},
            {"course_number": "COMS 3384", "title": "Media Effects", "units": 3},
            {"course_number": "EIM 2216", "title": "Resort and Lodging Operations", "units": 3},
            {"course_number": "EIM 3318", "title": "Destination and Hospitality Marketing and Management", "units": 3},
            {"course_number": "EIM 3321", "title": "Food and Beverage Experience Management", "units": 3},
            {"course_number": "EIM 3323", "title": "Sport Marketing and the Fan Experience", "units": 3},
            {"course_number": "EIM 4400", "title": "Special Topics in Experience Industry Management", "units": 3},
            {"course_number": "EIM 4412", "title": "Event Technology", "units": 3},
            {"course_number": "EIM 4450", "title": "Volunteer Management", "units": 3},
            {"course_number": "JOUR 3300", "title": "News Writing and Reporting", "units": 3},
            {"course_number": "JOUR 3342", "title": "Introduction to Public Relations", "units": 3},
        ],
    },
    "eim_sport_intro_choice": {
        "title": "Sport/Recreation Intro Course",
        "description": "EIM 1112 (Introduction to Parks and Outdoor Recreation) or EIM 1160 (Introduction to Sport Management).",
        "courses": [
            {"course_number": "EIM 1112", "title": "Introduction to Parks and Outdoor Recreation", "units": 3},
            {"course_number": "EIM 1160", "title": "Introduction to Sport Management", "units": 3},
        ],
    },
    "eim_sport_second_choice": {
        "title": "Sport/Recreation Community/Facilitation Course",
        "description": "EIM 2260 (Community Relations and Sports-Based Youth Development) or EIM 2275 (Facilitation and Teambuilding Experiences).",
        "courses": [
            {"course_number": "EIM 2260", "title": "Community Relations and Sports-Based Youth Development", "units": 3},
            {"course_number": "EIM 2275", "title": "Facilitation and Teambuilding Experiences", "units": 3},
        ],
    },
    "eim_sport_third_choice": {
        "title": "Sport/Recreation Upper-Division Course",
        "description": "EIM 3323 (Sport Marketing and the Fan Experience) or EIM 3325 (Leadership in Outdoor Experiences).",
        "courses": [
            {"course_number": "EIM 3323", "title": "Sport Marketing and the Fan Experience", "units": 3},
            {"course_number": "EIM 3325", "title": "Leadership in Outdoor Experiences", "units": 3},
        ],
    },
    "eim_sport_elective": {
        "title": "Sport and Recreation Management Concentration Elective",
        "description": "Select from approved Sport and Recreation Management concentration electives.",
        "courses": [
            {"course_number": "EIM 3317", "title": "Hospitality, Convention and Meeting Management", "units": 3},
            {"course_number": "EIM 3320", "title": "Strategic Event Planning", "units": 3},
            {"course_number": "EIM 3321", "title": "Food and Beverage Experience Management", "units": 3},
            {"course_number": "EIM 4400", "title": "Special Topics in Experience Industry Management", "units": 3},
            {"course_number": "EIM 4412", "title": "Event Technology", "units": 3},
            {"course_number": "KINE 1181", "title": "Physical Activity and Health", "units": 3},
        ],
    },
    "eim_tourism_elective": {
        "title": "Tourism, Hospitality, and Destination Management Concentration Elective",
        "description": "Select from approved Tourism, Hospitality, and Destination Management concentration electives.",
        "courses": [
            {"course_number": "EIM 3320", "title": "Strategic Event Planning", "units": 3},
            {"course_number": "EIM 3321", "title": "Food and Beverage Experience Management", "units": 3},
            {"course_number": "EIM 3323", "title": "Sport Marketing and the Fan Experience", "units": 3},
            {"course_number": "EIM 4400", "title": "Special Topics in Experience Industry Management", "units": 3},
            {"course_number": "EIM 4412", "title": "Event Technology", "units": 3},
            {"course_number": "EIM 4450", "title": "Volunteer Management", "units": 3},
            {"course_number": "WVIT 2121", "title": "Introduction to Wine", "units": 2},
        ],
    },
    "enve_ce_elective": {
        "title": "CE Technical Elective",
        "description": "Approved Civil Engineering technical elective courses for Environmental Engineering majors.",
        "courses": [
            {"course_number": "CE 3321", "title": "Fundamentals of Transportation Engineering", "units": 3},
            {"course_number": "CE 3352", "title": "Structural Analysis", "units": 3},
            {"course_number": "CE 3375", "title": "Fundamentals of Construction Engineering and Management", "units": 3},
            {"course_number": "CE 3381", "title": "Geotechnical Engineering", "units": 3},
            {"course_number": "CE 4413", "title": "Advanced Civil Computer-Aided Site Design", "units": 3},
            {"course_number": "CE 4433", "title": "Open Channel Hydraulics", "units": 3},
            {"course_number": "CE 4434", "title": "Groundwater Hydraulics and Hydrology", "units": 3},
            {"course_number": "CE 4435", "title": "Engineering Hydrology and Stormwater Management", "units": 3},
            {"course_number": "CE 4440", "title": "Hydraulic Systems Engineering", "units": 3},
            {"course_number": "CE 4474", "title": "Environmental Compliance and Permitting", "units": 3},
            {"course_number": "CE 4475", "title": "Mechanical, Electrical, and Energy Systems in Buildings", "units": 3},
            {"course_number": "CE 5536", "title": "Advanced Modeling in Water Resources", "units": 3},
            {"course_number": "CE 5537", "title": "Groundwater Contamination", "units": 3},
            {"course_number": "CE 5538", "title": "Urban Water Systems", "units": 3},
            {"course_number": "CE 5539", "title": "Environmental Hydraulics", "units": 3},
            {"course_number": "CE 5541", "title": "Extreme Events and Climate Change in Water Resources", "units": 3},
        ],
    },
    "grc_senior_project": {
        "title": "Senior Project",
        "description": "GRC 4461 (Senior Project I), GRC 4462 (Senior Project II), or GRC 4463 (Senior Project III).",
        "courses": [
            {"course_number": "GRC 4461", "title": "Senior Project I", "units": 3},
            {"course_number": "GRC 4462", "title": "Senior Project II", "units": 3},
            {"course_number": "GRC 4463", "title": "Senior Project III", "units": 3},
        ],
    },
    "grc_design_elective": {
        "title": "Design Reproduction Technology Concentration Elective",
        "description": "Select from approved Design Reproduction Technology concentration electives.",
        "courses": [
            {"course_number": "ART 1103", "title": "3D Design", "units": 3},
            {"course_number": "ART 2201", "title": "Drawing and Composition", "units": 3},
            {"course_number": "ART 2263", "title": "Figure Drawing", "units": 3},
            {"course_number": "ART 3351", "title": "Illustration", "units": 3},
            {"course_number": "ART 4433", "title": "The Art of Mixed Reality", "units": 3},
            {"course_number": "GRC 4400", "title": "Special Topics in Graphic Communication", "units": 3},
            {"course_number": "GRC 4451", "title": "Cooperative Education Experience I", "units": 3},
            {"course_number": "GRC 4452", "title": "Cooperative Education Experience II", "units": 3},
            {"course_number": "GRC 4453", "title": "Cooperative Education Experience III", "units": 3},
            {"course_number": "GRC 4485", "title": "Internship", "units": 3},
            {"course_number": "GRC 4495", "title": "Independent Study", "units": 3},
            {"course_number": "GRC 4550", "title": "Print Production Practicum", "units": 3},
        ],
    },
    "grc_mgmt_elective": {
        "title": "Graphic Communication Management Concentration Elective",
        "description": "Select from approved Graphic Communication Management concentration electives.",
        "courses": [
            {"course_number": "BUS 3310", "title": "Principles of Marketing", "units": 3},
            {"course_number": "BUS 3382", "title": "Organizational Behavior", "units": 3},
            {"course_number": "ENGL 3310", "title": "Technical Writing", "units": 4},
            {"course_number": "GRC 3270", "title": "Packaging Graphics Technology and Design", "units": 3},
            {"course_number": "GRC 4400", "title": "Special Topics in Graphic Communication", "units": 3},
            {"course_number": "GRC 4451", "title": "Cooperative Education Experience I", "units": 3},
            {"course_number": "GRC 4485", "title": "Internship", "units": 3},
            {"course_number": "GRC 4495", "title": "Independent Study", "units": 3},
        ],
    },
    "grc_packaging_elective": {
        "title": "Graphics for Packaging Concentration Elective",
        "description": "Select from approved Graphics for Packaging concentration electives.",
        "courses": [
            {"course_number": "GRC 4400", "title": "Special Topics in Graphic Communication", "units": 3},
            {"course_number": "GRC 4451", "title": "Cooperative Education Experience I", "units": 3},
            {"course_number": "GRC 4485", "title": "Internship", "units": 3},
            {"course_number": "GRC 4495", "title": "Independent Study", "units": 3},
            {"course_number": "ITP 3334", "title": "Package Engineering", "units": 3},
            {"course_number": "ITP 4408", "title": "Special Topics in Industrial Technology", "units": 3},
        ],
    },
    "grc_immersive_elective": {
        "title": "Immersive Experience Design Concentration Elective",
        "description": "Select from approved Immersive Experience Design concentration electives.",
        "courses": [
            {"course_number": "COMS 3384", "title": "Media Effects", "units": 3},
            {"course_number": "GRC 3990", "title": "Front-end Web Development", "units": 3},
            {"course_number": "GRC 4400", "title": "Special Topics in Graphic Communication", "units": 3},
            {"course_number": "GRC 4451", "title": "Cooperative Education Experience I", "units": 3},
            {"course_number": "GRC 4485", "title": "Internship", "units": 3},
            {"course_number": "GRC 4495", "title": "Independent Study", "units": 3},
            {"course_number": "GRC 4900", "title": "User Interface Innovations", "units": 3},
            {"course_number": "PSY 2201", "title": "Human-Computer Interaction", "units": 3},
        ],
    },
    "grc_uxui_elective": {
        "title": "User Experience/User Interface Concentration Elective",
        "description": "Select from approved UX/UI concentration electives.",
        "courses": [
            {"course_number": "COMS 3317", "title": "Technology and Human Communication", "units": 3},
            {"course_number": "COMS 4404", "title": "Video Games and Society", "units": 3},
            {"course_number": "GRC 4290", "title": "User Experience Research Methods", "units": 3},
            {"course_number": "GRC 4400", "title": "Special Topics in Graphic Communication", "units": 3},
            {"course_number": "GRC 4451", "title": "Cooperative Education Experience I", "units": 3},
            {"course_number": "GRC 4485", "title": "Internship", "units": 3},
            {"course_number": "GRC 4495", "title": "Independent Study", "units": 3},
            {"course_number": "PSY 2252", "title": "Organizational Psychology", "units": 4},
        ],
    },
    "coms_public_speaking": {
        "title": "Public Speaking",
        "description": "COMS 1101 (Public Speaking) or COMS 1102 (Public Speaking in Digital Spaces). Also satisfies GE Area 1C.",
        "courses": [
            {"course_number": "COMS 1101", "title": "Public Speaking", "units": 3},
            {"course_number": "COMS 1102", "title": "Public Speaking in Digital Spaces", "units": 3},
        ],
    },
    "coms_interp_choice": {
        "title": "Interpersonal/Organizational/Media/Group Communication",
        "description": "Select from COMS 2211, 2213, 2215, or 2217. Two separate courses from this list are required.",
        "courses": [
            {"course_number": "COMS 2211", "title": "Interpersonal Communication", "units": 3},
            {"course_number": "COMS 2213", "title": "Organizational Communication", "units": 3},
            {"course_number": "COMS 2215", "title": "Media Studies", "units": 3},
            {"course_number": "COMS 2217", "title": "Small Group Collaboration and Creativity", "units": 3},
        ],
    },
    "coms_advocacy_choice": {
        "title": "Advocacy or Performance",
        "description": "COMS 2250 (Building Advocacy Skills) or COMS 2208 (Performance, Literature, and Culture).",
        "courses": [
            {"course_number": "COMS 2250", "title": "Building Advocacy Skills", "units": 3},
            {"course_number": "COMS 2208", "title": "Performance, Literature, and Culture", "units": 3},
        ],
    },
    "coms_research_methods": {
        "title": "Quantitative or Qualitative Research Methods",
        "description": "COMS 3312 (Quantitative Research Methods) or COMS 3313 (Qualitative Research Methods).",
        "courses": [
            {"course_number": "COMS 3312", "title": "Quantitative Research Methods in Communication", "units": 3},
            {"course_number": "COMS 3313", "title": "Qualitative Research Methods in Communication", "units": 3},
        ],
    },
    "coms_criticism_choice": {
        "title": "Rhetorical or Media Criticism (GWR)",
        "description": "COMS 3332 (Rhetorical Criticism) or COMS 3385 (Media Criticism). Both satisfy the GWR requirement.",
        "courses": [
            {"course_number": "COMS 3332", "title": "Rhetorical Criticism", "units": 3},
            {"course_number": "COMS 3385", "title": "Media Criticism", "units": 3},
        ],
    },
    "coms_focus_culture": {
        "title": "Culture, Identity, and Power Focus Area Course",
        "description": "Select from approved Culture, Identity, and Power focus area courses.",
        "courses": [
            {"course_number": "COMS 3308", "title": "Group Performance of Literature", "units": 3},
            {"course_number": "COMS 3319", "title": "Critical Cultural Studies and Communication", "units": 3},
            {"course_number": "COMS 3320", "title": "Intergroup Communication", "units": 3},
            {"course_number": "COMS 3331", "title": "Contemporary Rhetorical Approaches", "units": 3},
            {"course_number": "COMS 3333", "title": "Race and Rhetoric", "units": 3},
            {"course_number": "COMS 3350", "title": "Advocacy Coaching and Consulting", "units": 3},
            {"course_number": "COMS 3351", "title": "Speech and Debate Team", "units": 3},
            {"course_number": "COMS 3352", "title": "Spanish-language Speech and Debate Team", "units": 3},
            {"course_number": "COMS 3387", "title": "Sports Communication", "units": 3},
            {"course_number": "COMS 4404", "title": "Video Games and Society", "units": 3},
            {"course_number": "COMS 4418", "title": "Health Communication", "units": 3},
            {"course_number": "COMS 4420", "title": "Nonverbal Communication", "units": 3},
            {"course_number": "COMS 4421", "title": "Gender and Communication", "units": 3},
            {"course_number": "COMS 4428", "title": "Family Communication", "units": 3},
            {"course_number": "COMS 4430", "title": "The Dark Side of Interpersonal Communication", "units": 3},
            {"course_number": "COMS 4435", "title": "Rhetoric and Social Change", "units": 3},
        ],
    },
    "coms_focus_media": {
        "title": "Media and Technology Focus Area Course",
        "description": "Select from approved Media and Technology focus area courses.",
        "courses": [
            {"course_number": "COMS 3317", "title": "Technology and Human Communication", "units": 3},
            {"course_number": "COMS 3384", "title": "Media Effects", "units": 3},
            {"course_number": "COMS 3386", "title": "Communication, Media, and Politics", "units": 3},
            {"course_number": "COMS 3387", "title": "Sports Communication", "units": 3},
            {"course_number": "COMS 3395", "title": "Science Communication", "units": 3},
            {"course_number": "COMS 4402", "title": "Rhetorics of Science, Technology, and Medicine", "units": 3},
            {"course_number": "COMS 4404", "title": "Video Games and Society", "units": 3},
            {"course_number": "COMS 4418", "title": "Health Communication", "units": 3},
            {"course_number": "COMS 4421", "title": "Gender and Communication", "units": 3},
            {"course_number": "COMS 4458", "title": "Solving Big World Challenges", "units": 3},
            {"course_number": "ISLA 3303", "title": "Values and Technology", "units": 3},
        ],
    },
    "coms_focus_persuasion": {
        "title": "Persuasion and Social Influence Focus Area Course",
        "description": "Select from approved Persuasion and Social Influence focus area courses.",
        "courses": [
            {"course_number": "COMS 2226", "title": "Applied Argumentation", "units": 3},
            {"course_number": "COMS 3301", "title": "Business and Professional Communication", "units": 3},
            {"course_number": "COMS 3302", "title": "Advanced Public Speaking", "units": 3},
            {"course_number": "COMS 3305", "title": "Persuasion", "units": 3},
            {"course_number": "COMS 3317", "title": "Technology and Human Communication", "units": 3},
            {"course_number": "COMS 3330", "title": "Classical Rhetoric", "units": 3},
            {"course_number": "COMS 3350", "title": "Advocacy Coaching and Consulting", "units": 3},
            {"course_number": "COMS 3351", "title": "Speech and Debate Team", "units": 3},
            {"course_number": "COMS 3352", "title": "Spanish-language Speech and Debate Team", "units": 3},
            {"course_number": "COMS 3384", "title": "Media Effects", "units": 3},
            {"course_number": "COMS 3386", "title": "Communication, Media, and Politics", "units": 3},
            {"course_number": "COMS 4418", "title": "Health Communication", "units": 3},
            {"course_number": "COMS 4420", "title": "Nonverbal Communication", "units": 3},
            {"course_number": "COMS 4435", "title": "Rhetoric and Social Change", "units": 3},
        ],
    },
    "coms_focus_politics": {
        "title": "Politics, Advocacy, and Civic Engagement Focus Area Course",
        "description": "Select from approved Politics, Advocacy, and Civic Engagement focus area courses.",
        "courses": [
            {"course_number": "COMS 2226", "title": "Applied Argumentation", "units": 3},
            {"course_number": "COMS 3302", "title": "Advanced Public Speaking", "units": 3},
            {"course_number": "COMS 3305", "title": "Persuasion", "units": 3},
            {"course_number": "COMS 3308", "title": "Group Performance of Literature", "units": 3},
            {"course_number": "COMS 3319", "title": "Critical Cultural Studies and Communication", "units": 3},
            {"course_number": "COMS 3330", "title": "Classical Rhetoric", "units": 3},
            {"course_number": "COMS 3331", "title": "Contemporary Rhetorical Approaches", "units": 3},
            {"course_number": "COMS 3350", "title": "Advocacy Coaching and Consulting", "units": 3},
            {"course_number": "COMS 3351", "title": "Speech and Debate Team", "units": 3},
            {"course_number": "COMS 3352", "title": "Spanish-language Speech and Debate Team", "units": 3},
            {"course_number": "COMS 3384", "title": "Media Effects", "units": 3},
            {"course_number": "COMS 3386", "title": "Communication, Media, and Politics", "units": 3},
            {"course_number": "COMS 3390", "title": "Environmental Communication", "units": 3},
            {"course_number": "COMS 4402", "title": "Rhetorics of Science, Technology, and Medicine", "units": 3},
            {"course_number": "COMS 4435", "title": "Rhetoric and Social Change", "units": 3},
        ],
    },
    "coms_focus_relationships": {
        "title": "Relationships, Organizations, and Socialization Focus Area Course",
        "description": "Select from approved Relationships, Organizations, and Socialization focus area courses.",
        "courses": [
            {"course_number": "COMS 3301", "title": "Business and Professional Communication", "units": 3},
            {"course_number": "COMS 3320", "title": "Intergroup Communication", "units": 3},
            {"course_number": "COMS 3333", "title": "Race and Rhetoric", "units": 3},
            {"course_number": "COMS 3387", "title": "Sports Communication", "units": 3},
            {"course_number": "COMS 4413", "title": "Training and Development", "units": 3},
            {"course_number": "COMS 4420", "title": "Nonverbal Communication", "units": 3},
            {"course_number": "COMS 4421", "title": "Gender and Communication", "units": 3},
            {"course_number": "COMS 4428", "title": "Family Communication", "units": 3},
            {"course_number": "COMS 4430", "title": "The Dark Side of Interpersonal Communication", "units": 3},
            {"course_number": "COMS 4458", "title": "Solving Big World Challenges", "units": 3},
        ],
    },
    "plsc_fruit_crop_elective": {
        "title": "Fruit and Crop Science Elective",
        "description": "Required or approved elective courses for the Fruit and Crop Science concentration. Includes fixed required courses and concentration-approved electives.",
        "courses": [
            {"course_number": "PLSC 1132", "title": "Introduction to Fruit Crop Production",        "units": 4},
            {"course_number": "PLSC 1150", "title": "California Row Crop Production",               "units": 4},
            {"course_number": "PLSC 1175", "title": "Introduction to Viticulture",                  "units": 3},
            {"course_number": "PLSC 2200", "title": "Principles of Agronomy",                       "units": 4},
            {"course_number": "PLSC 2205", "title": "Orchard Enterprise",                           "units": 2},
            {"course_number": "PLSC 2232", "title": "Introduction to Sustainable Viticulture",      "units": 2},
            {"course_number": "PLSC 2244", "title": "Precision Farming",                            "units": 3},
            {"course_number": "PLSC 3331", "title": "Soil-Plant Relationships",                     "units": 3},
            {"course_number": "PLSC 3333", "title": "Greenhouse Vegetable Production",              "units": 2},
            {"course_number": "PLSC 3337", "title": "Postharvest Handling of Horticultural Crops",  "units": 3},
            {"course_number": "PLSC 3339", "title": "Special Problems in Plant Sciences",           "units": 2},
            {"course_number": "PLSC 3360", "title": "Advanced Fruit Crop Production",               "units": 4},
            {"course_number": "PLSC 4400", "title": "Advanced Crop Production Systems",             "units": 3},
            {"course_number": "PLSC 4406", "title": "Advanced Weed Management",                     "units": 4},
            {"course_number": "PLSC 4420", "title": "Organic Crop Production Systems",              "units": 3},
            {"course_number": "PLSC 4421", "title": "Crop Improvement Seminar",                     "units": 1},
            {"course_number": "PLSC 4427", "title": "Disease and Pest Control for Ornamental Plants","units": 4},
            {"course_number": "PLSC 4428", "title": "Advanced Plant Pathology",                     "units": 3},
            {"course_number": "PLSC 4431", "title": "Integrated Pest Management for Insects",       "units": 3},
            {"course_number": "PLSC 4441", "title": "Biological Control for Pest Management",       "units": 3},
            {"course_number": "PLSC 4450", "title": "Plant Breeding Seminar",                       "units": 1},
            {"course_number": "WVIT 4414", "title": "Wine Quality Assessment",                      "units": 3},
        ],
    },
    "plsc_environ_hort_elective": {
        "title": "Environmental Horticultural Science Elective",
        "description": "Required or approved elective courses for the Environmental Horticultural Science concentration.",
        "courses": [
            {"course_number": "PLSC 1123", "title": "Introduction to Sustainable Site Horticulture","units": 3},
            {"course_number": "PLSC 2200", "title": "Principles of Agronomy",                       "units": 4},
            {"course_number": "PLSC 2212", "title": "Introduction to Floral Design",               "units": 3},
            {"course_number": "PLSC 2225", "title": "Landscape Plants",                             "units": 3},
            {"course_number": "PLSC 2234", "title": "Introduction to Plant Materials",              "units": 3},
            {"course_number": "PLSC 3301", "title": "Horticultural Production Techniques",          "units": 3},
            {"course_number": "PLSC 3332", "title": "Sustainable Site Design and Systems",          "units": 3},
            {"course_number": "PLSC 3333", "title": "Greenhouse Vegetable Production",              "units": 2},
            {"course_number": "PLSC 3334", "title": "Advanced Plant Materials",                     "units": 3},
            {"course_number": "PLSC 3339", "title": "Special Problems in Plant Sciences",           "units": 2},
            {"course_number": "PLSC 3340", "title": "Principles of Greenhouse Environments",        "units": 3},
            {"course_number": "PLSC 4400", "title": "Advanced Crop Production Systems",             "units": 3},
            {"course_number": "PLSC 4420", "title": "Organic Crop Production Systems",              "units": 3},
            {"course_number": "PLSC 4425", "title": "Arboriculture",                                "units": 3},
            {"course_number": "PLSC 4427", "title": "Disease and Pest Control for Ornamental Plants","units": 4},
            {"course_number": "PLSC 4428", "title": "Advanced Plant Pathology",                     "units": 3},
            {"course_number": "PLSC 4437", "title": "Turfgrass Management",                         "units": 3},
            {"course_number": "PLSC 4441", "title": "Biological Control for Pest Management",       "units": 3},
            {"course_number": "PLSC 4450", "title": "Plant Breeding Seminar",                       "units": 1},
        ],
    },
    "plsc_plant_protection_elective": {
        "title": "Plant Protection Science Elective",
        "description": "Required or approved elective courses for the Plant Protection Science concentration.",
        "courses": [
            {"course_number": "PLSC 1132", "title": "Introduction to Fruit Crop Production",        "units": 4},
            {"course_number": "PLSC 1150", "title": "California Row Crop Production",               "units": 4},
            {"course_number": "PLSC 1175", "title": "Introduction to Viticulture",                  "units": 3},
            {"course_number": "PLSC 2200", "title": "Principles of Agronomy",                       "units": 4},
            {"course_number": "PLSC 2205", "title": "Orchard Enterprise",                           "units": 2},
            {"course_number": "PLSC 2212", "title": "Introduction to Floral Design",               "units": 3},
            {"course_number": "PLSC 2244", "title": "Precision Farming",                            "units": 3},
            {"course_number": "PLSC 3331", "title": "Soil-Plant Relationships",                     "units": 3},
            {"course_number": "PLSC 3333", "title": "Greenhouse Vegetable Production",              "units": 2},
            {"course_number": "PLSC 3339", "title": "Special Problems in Plant Sciences",           "units": 2},
            {"course_number": "PLSC 3360", "title": "Advanced Fruit Crop Production",               "units": 4},
            {"course_number": "PLSC 4400", "title": "Advanced Crop Production Systems",             "units": 3},
            {"course_number": "PLSC 4406", "title": "Advanced Weed Management",                     "units": 4},
            {"course_number": "PLSC 4427", "title": "Disease and Pest Control for Ornamental Plants","units": 4},
            {"course_number": "PLSC 4428", "title": "Advanced Plant Pathology",                     "units": 3},
            {"course_number": "PLSC 4431", "title": "Integrated Pest Management for Insects",       "units": 3},
            {"course_number": "PLSC 4441", "title": "Biological Control for Pest Management",       "units": 3},
            {"course_number": "PLSC 4450", "title": "Plant Breeding Seminar",                       "units": 1},
            {"course_number": "WVIT 4414", "title": "Wine Quality Assessment",                      "units": 3},
        ],
    },
    "mcro_orga_choice": {
        "title": "Organic Chemistry",
        "description": "MCRO students take either the applied survey (CHEM 2240) or the traditional first-semester sequence (CHEM 2242). Confirm with your advisor.",
        "courses": [
            {"course_number": "CHEM 2240", "title": "Organic Chemistry: Fundamentals and Applications", "units": 4},
            {"course_number": "CHEM 2242", "title": "Organic Chemistry I", "units": 4},
        ],
    },
    "mcro_bioc_choice": {
        "title": "Biochemistry (GE UD2/5)",
        "description": "MCRO students take either the applied biochemistry course (CHEM 3350) or the rigorous full-sequence biochemistry (CHEM 3352). CHEM 3352 is recommended for graduate/professional school.",
        "courses": [
            {"course_number": "CHEM 3350", "title": "Biochemistry: Fundamentals and Applications", "units": 4},
            {"course_number": "CHEM 3352", "title": "Biochemistry", "units": 4},
        ],
    },
    "mcro_restricted_elective": {
        "title": "Microbiology Restricted Elective",
        "description": "Select from the approved restricted elective list. Verify eligibility with your advisor.",
        "courses": [
            {"course_number": "BIO 4429",  "title": "Parasitology",                          "units": 4},
            {"course_number": "BIO 4452",  "title": "Cell Biology",                          "units": 4},
            {"course_number": "BIO 4456",  "title": "Immunology",                            "units": 4},
            {"course_number": "BIO 4457",  "title": "Molecular Biology Laboratory",           "units": 2},
            {"course_number": "MCRO 4402", "title": "General Virology",                      "units": 4},
            {"course_number": "MCRO 4423", "title": "Medical Microbiology",                  "units": 4},
            {"course_number": "MCRO 4424", "title": "Microbial Physiology and Biochemistry", "units": 4},
            {"course_number": "MCRO 4433", "title": "Microbial Biotechnology",               "units": 4},
            {"course_number": "MCRO 4436", "title": "Microbial Ecology",                     "units": 4},
        ],
    },
    "mcro_senior_project": {
        "title": "Senior Project",
        "description": "MCRO students complete one of the three senior project options with their research advisor.",
        "courses": [
            {"course_number": "BIO 4461", "title": "Senior Project Research Proposal",      "units": 1},
            {"course_number": "BIO 4462", "title": "Senior Project Research Experience",    "units": 2},
            {"course_number": "BIO 4463", "title": "Senior Project Research Meta-analysis", "units": 3},
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
        "description": "ME general curriculum technical elective. The catalog requires 8-12 units from approved ME courses and allows 0-4 units from approved 3000-5000 level College of Engineering courses.",
        "depts": ["me", "aero", "bmed", "brae", "ce", "cpe", "csc", "ee", "engr", "enve", "ime", "mate", "se"],
        "min_level": 3000,
        "max_level": 5999,
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
    "asci_approved_elective": {
        "title": "Approved ASCI/DSCI Elective",
        "description": "Select any 3000-5000 level ASCI or DSCI course. The catalog limits ASCI 3339 and ASCI 4001-4015 to a combined maximum of 3 approved-elective units.",
        "depts": ["asci", "dsci"],
        "min_level": 3000,
        "max_level": 5999,
    },
    "antgeog_ant_elective": {
        "title": "Upper-Division Anthropology Elective",
        "description": "Select an upper-division ANT course approved for the Anthropology and Geography major.",
        "depts": ["ant"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "antgeog_geog_elective": {
        "title": "Upper-Division Geography Elective",
        "description": "Select an upper-division GEOG course approved for the Anthropology and Geography major.",
        "depts": ["geog"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "antgeog_ant_geog_soc_elective": {
        "title": "ANT, GEOG, or SOC Elective",
        "description": "Select an upper-division ANT, GEOG, or SOC elective.",
        "depts": ["ant", "geog", "soc"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "antgeog_concentration_elective": {
        "title": "Concentration Course or Elective",
        "description": "Select an upper-division course that fits the chosen concentration or advisor-approved elective plan.",
        "depts": ["ant", "geog", "ersc", "soc"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "antgeog_environmental_problems": {
        "title": "Environmental Problems, Issues, and Methods Elective",
        "description": "Select an upper-division environmental course approved for the Environmental Studies and Sustainability concentration.",
        "depts": ["ant", "geog", "ersc", "soc"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "antgeog_global_problems": {
        "title": "Global Problems, Issues, and Methods Elective",
        "description": "Select an upper-division global studies course approved for the Global Studies and International Development concentration.",
        "depts": ["ant", "geog", "soc"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "antgeog_human_ecology_elective": {
        "title": "Approved Human Ecology Elective",
        "description": "Select an upper-division ANT, GEOG, ERSC, or SOC course approved for the Human Ecology concentration.",
        "depts": ["ant", "geog", "ersc", "soc"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "arch_professional_elective": {
        "title": "Professional Elective",
        "description": "Select from ARCH, ARCE, ART, CM, CRP, EDES, or LA courses. At least 9 units must be 3000-4000 level.",
        "depts": ["arch", "arce", "art", "cm", "crp", "edes", "la"],
        "min_level": 1000,
        "max_level": 4999,
    },
    "arce_upper_division_elective": {
        "title": "ARCE Upper-Division Elective",
        "description": "Select any 3000-5000 level ARCE course approved for the ARCE elective requirement.",
        "depts": ["arce"],
        "min_level": 3000,
        "max_level": 5999,
    },
    "ad_art_advanced_elective": {
        "title": "3000-4000 Level Art Course",
        "description": "Art and Design students select an upper-division ART studio or design course (3000–4000 level).",
        "depts": ["art"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "pols_upper_div_elective": {
        "title": "3000-4000 Level POLS Elective",
        "description": "POLS students select any upper-division Political Science course (3000–4000 level).",
        "depts": ["pols"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "engl_lower_div_elective": {
        "title": "Lower-Division English Elective",
        "description": "English students select a lower-division English course (2000 level).",
        "depts": ["engl"],
        "min_level": 2000,
        "max_level": 2999,
    },
    "engl_intermediate_elective": {
        "title": "Intermediate English Elective",
        "description": "English students select an intermediate-level English course (3000 level).",
        "depts": ["engl"],
        "min_level": 3000,
        "max_level": 3999,
    },
    "engl_advanced_elective": {
        "title": "Advanced English Elective",
        "description": "English students select an advanced English course (4000 level).",
        "depts": ["engl"],
        "min_level": 4000,
        "max_level": 4999,
    },
    "mu_upper_div_elective": {
        "title": "Upper-Division Music Elective",
        "description": "Music students select an upper-division Music course (3000–4000 level).",
        "depts": ["mu"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "bus_tech_elective": {
        "title": "Technology Management Elective",
        "description": "BUS students select one technology or information systems elective from approved BUS or ITP courses (3000–4000 level).",
        "depts": ["bus", "itp"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "chem_advanced_elective": {
        "title": "Advanced Chemistry Elective",
        "description": "CHEM students select from all 4000-level Chemistry courses for their advanced elective slots.",
        "depts": ["chem"],
        "min_level": 4000,
        "max_level": 4999,
    },
    "cd_upper_div_elective": {
        "title": "CD Upper-Division Elective",
        "description": "CD students select from all 3000–4000 level Child Development courses for their upper-division elective slots.",
        "depts": ["cd"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "mate_technical_elective": {
        "title": "MATE Technical Elective",
        "description": "MATE students select from approved upper-division Materials Engineering courses for their technical elective slots.",
        "depts": ["mate"],
        "min_level": 4000,
        "max_level": 5999,
    },
    "mate_prof_dev_elective": {
        "title": "Professional Development Elective",
        "description": "MATE students select a professional development elective from the approved interdisciplinary list (BIO, BMED, BUS, CE, CHEM, COMS, ECON, ENVE, IME, ITP, MATE, MATH, ME, PHYS, and others).",
        "depts": ["mate", "ime", "bmed", "bus", "chem", "coms", "econ", "ce", "enve", "itp", "me"],
        "min_level": 2000,
        "max_level": 5999,
    },
    "ie_technical_elective": {
        "title": "IE Technical Elective",
        "description": "IE students select from approved upper-division Industrial Engineering courses for their technical elective slots.",
        "depts": ["ime"],
        "min_level": 3000,
        "max_level": 5999,
    },
    "ee_technical_elective": {
        "title": "EE Technical Elective",
        "description": "EE students select from approved upper-division and graduate Electrical Engineering courses (4000–5000 level) for their technical elective slots.",
        "depts": ["ee"],
        "min_level": 4000,
        "max_level": 5999,
    },
    "ee_lower_div_elective": {
        "title": "Lower-Division or Technical Elective",
        "description": "EE students may use this slot for additional EE technical electives or qualifying lower-division courses.",
        "depts": ["ee", "cpe", "csc", "me", "phys", "chem", "ime"],
        "min_level": 1000,
        "max_level": 5999,
    },
    "jour_elective": {
        "title": "Journalism Elective",
        "description": "Any JOUR course (1000–4999 level) not used to satisfy another requirement.",
        "depts": ["jour"],
        "min_level": 1000,
        "max_level": 4999,
    },
    "mfge_tech_elective": {
        "title": "Manufacturing Engineering Technical Elective",
        "description": "Upper-division IME course (3000–4999 level) approved as a technical elective by the Industrial and Manufacturing Engineering department.",
        "depts": ["ime"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "phys_tech_elective": {
        "title": "Physics Technical Elective",
        "description": "Upper-division PHYS or ASTR course (3000–4999 level) approved as a technical elective by the Physics department.",
        "depts": ["phys", "astr"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "cm_bus_elective": {
        "title": "Construction Management Business Elective",
        "description": "BUS 2215 (Managerial Accounting) or any 3000–4000 level BUS course.",
        "depts": ["bus"],
        "min_level": 2215,
        "max_level": 4999,
    },
    "soc_elective": {
        "title": "Sociology Elective",
        "description": "Any upper-division SOC course (3000–4999 level) not already used to satisfy another requirement.",
        "depts": ["soc"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "soc_ld_support": {
        "title": "Lower-Division Social Sciences Elective",
        "description": "Any lower-division (1000–2999) course from ANTH, ES, GEOG, SOC, POLS, PSY, or WGQS.",
        "depts": ["anth", "es", "geog", "soc", "pols", "psy", "wgqs"],
        "min_level": 1000,
        "max_level": 2999,
    },
    "econ_project_elective": {
        "title": "Economics & Project Elective",
        "description": "Any upper-division ECON lecture+lab course pair (3000–4000 level). Each elective is typically a 3-unit lecture paired with a 1-unit project lab (e.g., ECON 4010 + ECON 4010A).",
        "depts": ["econ"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "eim_concentration_elective": {
        "title": "Concentration Course",
        "description": "Any upper-division Experience Industry Management course (3000–4000 level). When a concentration is selected, specific required courses replace this slot.",
        "depts": ["eim"],
        "min_level": 1000,
        "max_level": 4999,
    },
    "grc_concentration_elective": {
        "title": "GRC Concentration/Individualized Elective",
        "description": "Any upper-division Graphic Communication course (3000–4000 level). For Individualized concentrations, minimum 6 units must have a GRC prefix.",
        "depts": ["grc"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "enve_tech_elective": {
        "title": "ENVE Technical Elective",
        "description": "Any upper-division Environmental Engineering course (3000–4000 level).",
        "depts": ["enve"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "coms_upper_div_elective": {
        "title": "COMS Upper-Division Elective",
        "description": "Any upper-division Communication Studies course (3000–4000 level).",
        "depts": ["coms"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "coms_focus_elective": {
        "title": "Focus Area Course",
        "description": "Any upper-division Communication Studies course (3000–4000 level). When a focus area is selected, this shows the approved course list for that focus area.",
        "depts": ["coms"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "plsc_concentration_elective": {
        "title": "Plant Sciences Concentration Elective",
        "description": "Approved concentration course for your Plant Sciences track. Select a concentration to see the approved course list.",
        "depts": ["plsc", "ss", "bot"],
        "min_level": 1000,
        "max_level": 4999,
    },
    "hist_ld_elective": {
        "title": "Lower Division History Elective",
        "description": "Any lower-division History course (2000-level). Select with your advisor's approval.",
        "depts": ["hist"],
        "min_level": 2000,
        "max_level": 2999,
    },
    "hist_ud_elective": {
        "title": "Upper Division History Elective",
        "description": "Any upper-division History course (3000–4000 level). Select with your advisor's approval.",
        "depts": ["hist"],
        "min_level": 3000,
        "max_level": 4999,
    },
    "hist_global_elective": {
        "title": "Global History Elective",
        "description": "Upper-division History course focused on global or non-US history (3000–4000 level). Verify global designation with your advisor.",
        "depts": ["hist"],
        "min_level": 3000,
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
    "PLSC_1120": "agc_plsc_pair",
    "AGS_BIO5B": "ags_life_science",
    "AGS_ASCI1102_1103": "ags_asci_pair",
    "AGS_PLSC1120": "agc_plsc_pair",
    "AGS_SS1120": "ags_soil_science",
    "AGS_DSCI_FSN": "ags_dairy_food_safety",
    "AGS_AGED_AGC": "ags_aged_agc_choice",
    "AGS_NR3308": "ags_nr_choice",
    "AGS_AGC4452": "ags_agc_ag_issues",
    "ASCI_ASCI2210_2211": "asci_meat_science_pair",
    "ASCI_MGMT1": "asci_animal_management",
    "ASCI_MGMT2": "asci_animal_management",
    "ASCI_ENTERPRISE": "asci_enterprise_elective",
    "ASCI_NUTRITION": "asci_nutrition_elective",
    "ASCI_PHYSIOLOGY": "asci_physiology_elective",
    "ASCI_SENIOR_PROJECT": "asci_senior_project",
    "ME_IME114X": "me_ime_mfg_selective",
    "ME_GE5B": "me_life_science",
    "ME_TE_SRF1": "me_tech_elective",
    "ME_TE_SRF2": "me_tech_elective",
    "ME_TE_SRS1": "me_tech_elective",
    "ME_TE_SRS2": "me_tech_elective",
    "ANTGEOG_PHYS_GEOG": "antgeog_physical_geography",
    "ANTGEOG_PROF_PREP": "antgeog_professional_preparation",
    "ANTGEOG_METHODS": "antgeog_methods_elective",
    "ANTGEOG_INTERNSHIP": "antgeog_internship",
    "ANTGEOG_REGIONAL": "antgeog_regional_geography",
    "ANTGEOG_RESEARCH_DESIGN": "antgeog_research_design",
    "ARCH_PROF_ELEC1": "arch_professional_elective",
    "ARCH_PROF_ELEC2": "arch_professional_elective",
    "ARCH_PROF_ELEC3": "arch_professional_elective",
    "ARCH_PROF_ELEC4": "arch_professional_elective",
    "ARCE_FE_TE1": "arce_fe_technical_elective",
    "ARCE_SURVEY": "arce_surveying_elective",
    "ARCE_FE_TE2": "arce_fe_technical_elective",
    "ARCE_CAED": "arce_caed_interdisciplinary_elective",
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
