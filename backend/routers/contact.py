import os
import httpx

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

DEVELOPER_EMAIL = os.getenv("DEVELOPER_EMAIL", "fischerhewittdeveloper@gmail.com")

_CATEGORY_LABELS = {
    "bug": "Bug Report",
    "feature": "Feature Request",
    "question": "Question",
}

_RESEND_URL = "https://api.resend.com/emails"
_FROM_ADDRESS = "Mustang Blueprints <onboarding@resend.dev>"


class ContactRequest(BaseModel):
    name: str = ""
    email: str = ""
    category: str = "bug"
    custom_subject: str = ""
    message: str


@router.post("/send")
def send_contact(req: ContactRequest):
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="Email service not configured.")

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    category_label = (
        req.custom_subject.strip() or "Other"
        if req.category == "other"
        else _CATEGORY_LABELS.get(req.category, "Message")
    )
    subject = f"[Mustang Blueprints] {category_label} from {req.name.strip() or 'a user'}"
    reply_to = req.email.strip() or DEVELOPER_EMAIL

    body = (
        f"Name: {req.name.strip() or '(not provided)'}\n"
        f"Email: {req.email.strip() or '(not provided)'}\n"
        f"Category: {category_label}\n\n"
        f"{req.message.strip()}"
    )

    payload = {
        "from": _FROM_ADDRESS,
        "to": [DEVELOPER_EMAIL],
        "reply_to": reply_to,
        "subject": subject,
        "text": body,
    }

    try:
        res = httpx.post(
            _RESEND_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=10,
        )
        res.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Resend error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    return {"status": "sent"}
