from fastapi import APIRouter, HTTPException
from services.sessions import get_session, update_session

router = APIRouter()

ALLOWED_UPDATE_FIELDS = {"completed", "in_progress", "course_positions", "planned_ge_courses", "planned_ge_units"}


@router.get("/{session_id}")
def get(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.patch("/{session_id}")
def patch(session_id: str, body: dict):
    updates = {k: v for k, v in body.items() if k in ALLOWED_UPDATE_FIELDS}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    try:
        return update_session(session_id, **updates)
    except Exception:
        raise HTTPException(status_code=404, detail="Session not found")
