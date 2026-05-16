import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

SUPPORT_EMAIL = os.getenv("SMTP_EMAIL", "fischerhewittdeveloper@gmail.com")
DEVELOPER_EMAIL = os.getenv("DEVELOPER_EMAIL", "fihewitt@calpoly.edu")

_CATEGORY_LABELS = {
    "bug": "Bug Report",
    "feature": "Feature Request",
    "question": "Question",
}


class ContactRequest(BaseModel):
    name: str = ""
    email: str = ""
    category: str = "bug"
    custom_subject: str = ""
    message: str


@router.post("/send")
def send_contact(req: ContactRequest):
    smtp_password = os.getenv("SMTP_PASSWORD")
    if not smtp_password:
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

    msg = MIMEMultipart()
    msg["From"] = SUPPORT_EMAIL
    msg["To"] = SUPPORT_EMAIL
    msg["Reply-To"] = reply_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SUPPORT_EMAIL, smtp_password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=503, detail="Email authentication failed. Check SMTP credentials.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    return {"status": "sent"}
