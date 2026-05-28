import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data" / "polyplanner" / "catalogs.json"
OUTPUT_DIR = ROOT / "data" / "polyplanner" / "catalog-data"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unnamed"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def flowchart_filename(template: dict[str, Any], used_names: set[str]) -> str:
    year = template.get("startingYear") or template.get("id") or "unknown"
    base = f"{year}.json"
    if base not in used_names:
        used_names.add(base)
        return base

    fallback = f"{year}-{template.get('id')}.json"
    used_names.add(fallback)
    return fallback


def main() -> None:
    catalogs = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    for catalog in catalogs:
        catalog_dir = OUTPUT_DIR / catalog["name"]
        write_json(catalog_dir / "courses.json", catalog.get("courses", []))
        write_json(catalog_dir / "general-educations.json", catalog.get("generalEducations", []))

        for degree in catalog.get("degrees", []):
            degree_dir = catalog_dir / slugify(degree["name"])
            write_json(degree_dir / "major-requirements.json", degree.get("requirements", []))
            write_json(degree_dir / "technical-electives.json", degree.get("technicalElectiveAreas", []))
            write_json(degree_dir / "course-mappings.json", degree.get("courseMappings", []))

            (degree_dir / "flowchart-templates").mkdir(parents=True, exist_ok=True)
            used_flowchart_names: set[str] = set()
            for template in degree.get("flowchartTemplates", []):
                filename = flowchart_filename(template, used_flowchart_names)
                write_json(degree_dir / "flowchart-templates" / filename, template)

    print(f"Exported catalog-data to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
