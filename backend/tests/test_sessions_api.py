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
            "planned_free_elective_courses": {
                "FREE1": {
                    "course_number": "MU 1010",
                    "title": "Introduction to Music",
                    "units": 3,
                    "status": "planned",
                },
            },
            "concentration": "ai_ml",
        }

    monkeypatch.setattr(sessions_router, "get_session", fake_get_session)

    response = client.get("/api/sessions/session-123")

    assert response.status_code == 200
    assert response.json()["student_name"] == "Ada Lovelace"
    assert response.json()["planned_ge_courses"] == {"GE 3B": "ENGL 2230"}
    assert response.json()["planned_free_elective_courses"]["FREE1"]["course_number"] == "MU 1010"
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
            "planned_free_elective_courses": {
                "FREE1": {
                    "course_number": "MU 1010",
                    "title": "Introduction to Music",
                    "units": 3,
                    "status": "completed",
                },
            },
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
            "planned_free_elective_courses": {
                "FREE1": {
                    "course_number": "MU 1010",
                    "title": "Introduction to Music",
                    "units": 3,
                    "status": "completed",
                },
            },
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


def test_patch_session_clears_concentration_with_none_sentinel(monkeypatch):
    """Sending concentration='none' must reach update_session — it must not be filtered."""
    captured = {}

    def fake_update_session(session_id: str, **updates):
        captured["updates"] = updates
        return {"session_id": session_id, **updates}

    monkeypatch.setattr(sessions_router, "update_session", fake_update_session)

    response = client.patch(
        "/api/sessions/session-123",
        json={"concentration": "none"},
    )

    assert response.status_code == 200
    assert captured["updates"] == {"concentration": "none"}


def test_patch_session_returns_404_when_session_key_missing(monkeypatch):
    def raise_key_error(*_args, **_kwargs):
        raise KeyError("missing-session")

    monkeypatch.setattr(sessions_router, "update_session", raise_key_error)

    response = client.patch("/api/sessions/missing-session", json={"completed": ["CSC 1001"]})

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_get_session_returns_planned_custom_courses(monkeypatch):
    def fake_get_session(session_id: str):
        return {
            "session_id": session_id,
            "student_name": "Ada Lovelace",
            "major": "MATH",
            "completed": [],
            "in_progress": [],
            "planned_custom_courses": {
                "custom-uuid-1": {
                    "course_number": "ACCT 221",
                    "title": "Accounting for Non-Business Majors",
                    "units": 4,
                    "grid_col": 1,
                    "status": "planned",
                }
            },
        }

    monkeypatch.setattr(sessions_router, "get_session", fake_get_session)

    response = client.get("/api/sessions/session-123")

    assert response.status_code == 200
    custom = response.json()["planned_custom_courses"]["custom-uuid-1"]
    assert custom["course_number"] == "ACCT 221"
    assert custom["status"] == "planned"
    assert custom["grid_col"] == 1


def test_patch_session_passes_through_planned_custom_courses(monkeypatch):
    captured = {}

    def fake_update_session(session_id: str, **updates):
        captured["updates"] = updates
        return {"session_id": session_id, **updates}

    monkeypatch.setattr(sessions_router, "update_session", fake_update_session)

    custom_course = {
        "course_number": "ACCT 221",
        "title": "Accounting for Non-Business Majors",
        "units": 4,
        "grid_col": 1,
        "status": "planned",
    }

    response = client.patch(
        "/api/sessions/session-123",
        json={"planned_custom_courses": {"custom-uuid-1": custom_course}},
    )

    assert response.status_code == 200
    assert "planned_custom_courses" in captured["updates"]
    assert captured["updates"]["planned_custom_courses"]["custom-uuid-1"]["course_number"] == "ACCT 221"


def test_patch_session_propagates_non_key_errors_as_500(monkeypatch):
    def raise_runtime_error(*_args, **_kwargs):
        raise RuntimeError("supabase unavailable")

    monkeypatch.setattr(sessions_router, "update_session", raise_runtime_error)

    # raise_server_exceptions=False lets starlette convert the unhandled exception
    # to an HTTP 500 response instead of re-raising it in the test process.
    error_client = TestClient(app, raise_server_exceptions=False)
    response = error_client.patch("/api/sessions/session-123", json={"completed": ["CSC 1001"]})

    assert response.status_code == 500
