from fastapi import APIRouter, HTTPException

from services.polyplanner_catalog import (
    SOURCE_URL,
    catalog_summaries,
    degree_summaries,
    get_catalog,
    get_degree,
)


router = APIRouter()


@router.get("")
def list_polyplanner_catalogs():
    return {
        "source": SOURCE_URL,
        "catalogs": catalog_summaries(),
    }


@router.get("/{catalog_key}/degrees")
def list_polyplanner_degrees(catalog_key: str):
    degrees = degree_summaries(catalog_key)
    if degrees is None:
        raise HTTPException(status_code=404, detail=f"No imported catalog for {catalog_key}")
    return {"catalog": catalog_key, "degrees": degrees}


@router.get("/{catalog_key}/degrees/{degree_key}")
def polyplanner_degree(catalog_key: str, degree_key: str):
    catalog = get_catalog(catalog_key)
    if not catalog:
        raise HTTPException(status_code=404, detail=f"No imported catalog for {catalog_key}")

    degree = get_degree(catalog_key, degree_key)
    if not degree:
        raise HTTPException(status_code=404, detail=f"No imported degree for {degree_key}")

    return {
        "catalog": {
            "id": catalog.get("id"),
            "name": catalog.get("name"),
            "termType": catalog.get("termType"),
        },
        "degree": degree,
    }
