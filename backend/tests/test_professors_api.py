from dataclasses import dataclass

from fastapi.testclient import TestClient

import routers.professors as professors_router
from main import app


client = TestClient(app)


@dataclass
class FakeProfessor:
    name: str
    overall_score: float
    num_ratings: int
    polyratings_url: str


def test_professors_endpoint_returns_frontend_shape(monkeypatch):
    def fake_get_professors_for_course(course_number: str):
        assert course_number == "CSC 101"
        return [
            FakeProfessor(
                name="Grace Hopper",
                overall_score=3.85,
                num_ratings=42,
                polyratings_url="https://polyratings.dev/professor/prof-1",
            )
        ]

    monkeypatch.setattr(
        professors_router,
        "get_professors_for_course",
        fake_get_professors_for_course,
    )

    response = client.get("/api/professors/CSC%20101")

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


def test_professors_endpoint_preserves_slash_course_numbers(monkeypatch):
    monkeypatch.setattr(professors_router, "get_professors_for_course", lambda course_number: [])

    response = client.get("/api/professors/BIO%2FBOT")

    assert response.status_code == 200
    assert response.json() == {"course_number": "BIO/BOT", "professors": []}
