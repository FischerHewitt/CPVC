from dataclasses import dataclass

from fastapi.testclient import TestClient

from main import app
from services.polyratings import PolyRatingsCache, get_polyratings_cache


client = TestClient(app)


@dataclass
class FakeProfessor:
    name: str
    overall_score: float
    num_ratings: int
    polyratings_url: str


def test_professors_endpoint_returns_frontend_shape():
    class FakeCache(PolyRatingsCache):
        def get_professors_for_course(self, course_number: str):
            assert course_number == "CSC 101"
            return [
                FakeProfessor(
                    name="Grace Hopper",
                    overall_score=3.85,
                    num_ratings=42,
                    polyratings_url="https://polyratings.dev/professor/prof-1",
                )
            ]

    fake = FakeCache()
    app.dependency_overrides[get_polyratings_cache] = lambda: fake
    try:
        response = client.get("/api/professors/CSC%20101")
    finally:
        app.dependency_overrides.pop(get_polyratings_cache, None)

    assert response.status_code == 200
    assert response.json() == {
        "course_number": "CSC 101",
        "professors": [
            {
                "name": "Grace Hopper",
                "overall_score": 3.85,
                "num_ratings": 42,
                "polyratings_url": "https://polyratings.dev/professor/prof-1",
            }
        ],
    }


def test_professors_endpoint_preserves_slash_course_numbers():
    class EmptyCache(PolyRatingsCache):
        def get_professors_for_course(self, course_number: str):
            return []

    app.dependency_overrides[get_polyratings_cache] = lambda: EmptyCache()
    try:
        response = client.get("/api/professors/BIO%2FBOT")
    finally:
        app.dependency_overrides.pop(get_polyratings_cache, None)

    assert response.status_code == 200
    assert response.json() == {"course_number": "BIO/BOT", "professors": []}
