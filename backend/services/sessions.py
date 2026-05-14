"""
Backend session persistence using Supabase.
The sessions table stores parsed transcript data so sessions survive
across devices and browser clears.
"""

import os
from supabase import create_client, Client


def _client() -> Client:
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_KEY", "")
    return create_client(url, key)


def create_session(
    student_name: str,
    student_id: str,
    major: str,
    completed: list[str],
    in_progress: list[str],
) -> str:
    """Insert a new session row and return the generated UUID."""
    result = (
        _client()
        .table("sessions")
        .insert(
            {
                "student_name": student_name,
                "student_id": student_id,
                "major": major,
                "completed": completed,
                "in_progress": in_progress,
                "course_positions": {},
            }
        )
        .execute()
    )
    return str(result.data[0]["session_id"])


def get_session(session_id: str) -> dict | None:
    """Return a session row or None if not found."""
    result = (
        _client()
        .table("sessions")
        .select("*")
        .eq("session_id", session_id)
        .maybe_single()
        .execute()
    )
    return result.data


def update_session(session_id: str, **updates) -> dict:
    """Partially update a session (completed, in_progress, course_positions)."""
    result = (
        _client()
        .table("sessions")
        .update(updates)
        .eq("session_id", session_id)
        .execute()
    )
    return result.data[0]
