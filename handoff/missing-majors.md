# Majors: PDF Coverage and Gaps

## What the txt file covers

`FlowchartPdf/General Curriculum in Computer Science.txt` contains **168 flowchart grids
across 37 major programs**. These are the majors that can be validated/updated and
given per-concentration full flowcharts in the current migration.

---

## App majors WITH coverage in the txt (33 majors)

These majors are in the txt and can be fully migrated.
Two have name mismatches between the txt and the app (handled in the merge script).

| App Code | App Name | PDF Name (if different) |
|----------|----------|------------------------|
| AERO | Aerospace Engineering | |
| ANTGEOG | Anthropology and Geography | |
| AD | Art and Design | |
| BIOC | Biochemistry | |
| BIO | Biological Sciences | |
| BMED | Biomedical Engineering | |
| BUS | Business Administration | |
| CE | Civil Engineering | |
| CHEM | Chemistry | |
| CPE | Computer Engineering | |
| CS | Computer Science | |
| ECON | Economics | |
| EE | Electrical Engineering | |
| ENVM | Environmental Management and Protection | |
| CES | Environmental Earth and Soil Sciences | |
| EIM | Experience and Event Management | |
| FSN | Food Science and Nutrition | "Food Science" in txt |
| NR | Forest and Fire Sciences | |
| GEN | General Engineering | |
| GRC | Graphic Communication | |
| ITP | Industrial Technology and Packaging | |
| INTS | Interdisciplinary Studies | |
| JOUR | Journalism | |
| KINE | Kinesiology | |
| LAES | Liberal Arts and Engineering Studies | |
| LIBS | Liberal Studies | |
| ME | Mechanical Engineering | "Mechanical Engineering (San Luis Obispo Campus)" in txt |
| NUT | Nutrition | |
| PHIL | Philosophy | |
| PLSC | Plant Sciences | |
| POLS | Political Science | |
| PH | Public Health | |
| SOC | Sociology | |
| WVIT | Wine and Viticulture | |

---

## App majors WITHOUT coverage in the txt (32 majors)

These majors exist in the app (`FLOWCHARTS`) but have no matching section in the txt.
They cannot be validated or migrated from this source.
**Next step: obtain txt exports or catalog pages for these programs.**

| App Code | Major Name |
|----------|-----------|
| AGB | Agricultural Business |
| AGC | Agricultural Communication |
| AGS | Agricultural Science |
| ASM | Agricultural Systems Management |
| ASCI | Animal Science |
| ARCE | Architectural Engineering |
| ARCH | Architecture |
| BRAE | BioResource and Agricultural Engineering |
| CD | Child Development |
| CRP | City and Regional Planning |
| CM | Construction Management |
| COMS | Communication Studies |
| CES | Comparative Ethnic Studies |
| DSCI | Dairy Science |
| ENGL | English |
| ENVE | Environmental Engineering |
| HIST | History |
| IE | Industrial Engineering |
| LA | Landscape Architecture |
| MATE | Materials Engineering |
| MATH | Mathematics |
| MATH_TEACHING | Mathematics (Teaching) |
| MCRO | Microbiology |
| MFGE | Manufacturing Engineering |
| MSCI | Marine Sciences |
| MU | Music |
| PHYS | Physics |
| PSY | Psychology |
| SE | Software Engineering |
| SPAN | Spanish |
| STAT | Statistics |
| THEA | Theatre Arts |

---

## Programs in the txt NOT in the app (new majors to add later)

| PDF Name | Concentrations | Notes |
|----------|---------------|-------|
| Facilities Engineering Technology | Division 1 & 2, Division 3 & 4 | 3-term-per-year structure; likely Cal Maritime merger |
| Marine Engineering Technology | Division 1 & 2, Division 3 & 4 | 3-term-per-year structure; likely Cal Maritime merger |
| Marine Transportation | Division 1 & 2, Division 3 & 4 | 3-term-per-year structure; likely Cal Maritime merger |
| Plant Science | Plant Protection Science Concentration | One concentration only; may be a sub-program of PLSC |

---

## Name mappings required in the merge script

When matching PDF sections to app `FLOWCHARTS` entries, apply these overrides:

```python
PDF_TO_APP_MAJOR_NAME = {
    "Mechanical Engineering (San Luis Obispo Campus)": "Mechanical Engineering",
    "Food Science": "Food Science and Nutrition",
}
```
