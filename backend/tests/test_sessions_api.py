from fastapi.testclient import TestClient

import routers.sessions as sessions_router
from main import app


client = TestClient(app)


def test_get_session_returns_backend_session(monkeypatch):
    def fake_get_session(session_id: str):
        assert session_id == "session-123"
        return {
            "session_id": session_id,
            "student_name": "Ada Lovelace",
            "major": "CS",
            "completed": ["CSC 1001"],
            "in_progress": ["MATH 1262"],
            "course_positions": {},
            "planned_ge_courses": {"GE 3B": "ENGL 2230"},
            "planned_ge_units": {"GE 3B": 3},
            "concentration": "ai_ml",
        }

    monkeypatch.setattr(sessions_router, "get_session", fake_get_session)

    response = client.get("/api/sessions/session-123")

    assert response.status_code == 200
    assert response.json()["student_name"] == "Ada Lovelace"
    assert response.json()["planned_ge_courses"] == {"GE 3B": "ENGL 2230"}
    assert response.json()["concentration"] == "ai_ml"


def test_get_session_returns_404_when_missing(monkeypatch):
    monkeypatch.setattr(sessions_router, "get_session", lambda _session_id: None)

    response = client.get("/api/sessions/missing-session")

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_patch_session_filters_to_allowed_fields(monkeypatch):
    captured = {}

    def fake_update_session(session_id: str, **updates):
        captured["session_id"] = session_id
        captured["updates"] = updates
        return {"session_id": session_id, **updates}

    monkeypatch.setattr(sessions_router, "update_session", fake_update_session)

    response = client.patch(
        "/api/sessions/session-123",
        json={
            "completed": ["CSC 1001"],
            "in_progress": ["MATH 1262"],
            "course_positions": {"CSC1001": {"grid_col": 1, "grid_row": 0}},
            "planned_ge_courses": {"GE 3B": "ENGL 2230"},
            "planned_ge_units": {"GE 3B": 3},
            "concentration": "ai_ml",
            "student_name": "Should Not Be Updated",
        },
    )

    assert response.status_code == 200
    assert captured == {
        "session_id": "session-123",
        "updates": {
            "completed": ["CSC 1001"],
            "in_progress": ["MATH 1262"],
            "course_positions": {"CSC1001": {"grid_col": 1, "grid_row": 0}},
            "planned_ge_courses": {"GE 3B": "ENGL 2230"},
            "planned_ge_units": {"GE 3B": 3},
            "concentration": "ai_ml",
        },
    }
    assert "student_name" not in response.json()


def test_patch_session_rejects_body_without_allowed_fields(monkeypatch):
    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("update_session should not be called")

    monkeypatch.setattr(sessions_router, "update_session", fail_if_called)

    response = client.patch("/api/sessions/session-123", json={"student_name": "Ada"})

    assert response.status_code == 400
    assert response.json()["detail"] == "No valid fields to update"


def test_patch_session_returns_404_when_update_fails(monkeypatch):
    def raise_not_found(*_args, **_kwargs):
        raise RuntimeError("missing")

    monkeypatch.setattr(sessions_router, "update_session", raise_not_found)

    response = client.patch("/api/sessions/missing-session", json={"completed": ["CSC 1001"]})

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"
