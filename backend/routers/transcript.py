import io
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from services.transcript_parser import parse_transcript, parse_csv_transcript, completed_course_numbers, in_progress_course_numbers
from services.sessions import create_session

router = APIRouter()


class TranscriptResponse(BaseModel):
    session_id: str
    student_name: str
    student_id: str
    major: str
    completed: list[str]
    in_progress: list[str]


@router.post("/parse", response_model=TranscriptResponse)
async def parse(
    file: UploadFile = File(...),
    major: str = Form("CS"),
):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    contents = await file.read()
    result = parse_transcript(io.BytesIO(contents))

    completed   = sorted(completed_course_numbers(result))
    in_progress = sorted(in_progress_course_numbers(result))

    session_id = create_session(
        student_name=result.student_name,
        student_id=result.student_id,
        major=major,
        completed=completed,
        in_progress=in_progress,
    )

    return TranscriptResponse(
        session_id=session_id,
        student_name=result.student_name,
        student_id=result.student_id,
        major=major,
        completed=completed,
        in_progress=in_progress,
    )


@router.post("/parse-csv", response_model=TranscriptResponse)
async def parse_csv(
    file: UploadFile = File(...),
    major: str = Form("CS"),
):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    contents = await file.read()
    result = parse_csv_transcript(io.BytesIO(contents))

    completed   = sorted(completed_course_numbers(result))
    in_progress = sorted(in_progress_course_numbers(result))

    session_id = create_session(
        student_name="",
        student_id="",
        major=major,
        completed=completed,
        in_progress=in_progress,
    )

    return TranscriptResponse(
        session_id=session_id,
        student_name="",
        student_id="",
        major=major,
        completed=completed,
        in_progress=in_progress,
    )
