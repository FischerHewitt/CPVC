from functools import lru_cache
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "polyplanner" / "catalogs.json"
SOURCE_URL = "https://api.polyplanner.pro/catalogs"


@lru_cache(maxsize=1)
def load_catalogs() -> list[dict[str, Any]]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("Poly Planner catalog data must be a list of catalogs")
    return data


def _matches_key(value: Any, key: str) -> bool:
    return str(value).lower() == key.lower()


def _find_by_id_or_name(items: list[dict[str, Any]], key: str) -> dict[str, Any] | None:
    for item in items:
        if _matches_key(item.get("id"), key) or _matches_key(item.get("name"), key):
            return item
    return None


def _catalog_summary(catalog: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": catalog.get("id"),
        "name": catalog.get("name"),
        "termType": catalog.get("termType"),
        "published": catalog.get("published"),
        "lastEditDate": catalog.get("lastEditDate"),
        "lastEditName": catalog.get("lastEditName"),
        "degreeCount": len(catalog.get("degrees") or []),
        "courseCount": len(catalog.get("courses") or []),
        "generalEducationCount": len(catalog.get("generalEducations") or []),
    }


def _degree_summary(degree: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": degree.get("id"),
        "name": degree.get("name"),
        "published": degree.get("published"),
        "requirementCount": len(degree.get("requirements") or []),
        "technicalElectiveAreaCount": len(degree.get("technicalElectiveAreas") or []),
        "flowchartTemplateCount": len(degree.get("flowchartTemplates") or []),
        "courseMappingCount": len(degree.get("courseMappings") or []),
        "freeElectiveUnits": degree.get("freeElectiveUnits"),
    }


def catalog_summaries() -> list[dict[str, Any]]:
    return [_catalog_summary(catalog) for catalog in load_catalogs()]


def get_catalog(catalog_key: str) -> dict[str, Any] | None:
    return _find_by_id_or_name(load_catalogs(), catalog_key)


def degree_summaries(catalog_key: str) -> list[dict[str, Any]] | None:
    catalog = get_catalog(catalog_key)
    if not catalog:
        return None
    return [_degree_summary(degree) for degree in catalog.get("degrees") or []]


def get_degree(catalog_key: str, degree_key: str) -> dict[str, Any] | None:
    catalog = get_catalog(catalog_key)
    if not catalog:
        return None
    return _find_by_id_or_name(catalog.get("degrees") or [], degree_key)
