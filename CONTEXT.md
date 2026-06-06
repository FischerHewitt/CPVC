# Mustang Blueprints — Domain Glossary

## Concentration
A named track within a major that may customize elective slots, course overrides, or the entire flowchart. Every major exposes at least one concentration option in its picker.

**Default Concentration** (`id: "none"`): The base option for a major — labeled differently per major (e.g., "General Curriculum", "No Concentration Declared", "Individualized Course of Study"). Selecting it applies no slot overrides and uses the base major flowchart. Functionally identical to the major with no concentration filter applied.

A concentration with a `full_flowchart_key` serves an entirely separate flowchart instead of overlaying the base major flowchart.

## Elective Override
A selection made for an elective placeholder slot using a course that does not appear in the slot's predefined eligible-course list. Triggered via a "Can't find your course?" accordion at the bottom of the elective picker panel, which opens a full catalog search. If the student searches for and selects a course that IS in the eligible list, it is treated as a normal list selection (highlighted in place). If the course is novel, a docked summary card appears at the bottom of the panel with Plan/IP/Done status controls. Both paths write to the same `plannedGECourses[placeholder.course_number]` session field; no separate storage is used.

## Session
A persisted record (Supabase row + localStorage mirror) linking a student to their planned flowchart state: completed courses, in-progress courses, GE selections, elective selections, concentration choice, and course positions. Identified by a UUID (`session_id`).
