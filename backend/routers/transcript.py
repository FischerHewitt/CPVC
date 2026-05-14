from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.transcript_parser import parse_transcript, completed_course_numbers, in_progress_course_numbers

router = APIRouter()


class TranscriptResponse(BaseModel):
    student_name: str
    student_id: str
    major: str
    completed: list[str]
    in_progress: list[str]


@router.post("/parse", response_model=TranscriptResponse)
async def parse(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    contents = await file.read()
    import io
    result = parse_transcript(io.BytesIO(contents))

    return TranscriptResponse(
        student_name=result.student_name,
        student_id=result.student_id,
        major=result.major,
        completed=sorted(completed_course_numbers(result)),
        in_progress=sorted(in_progress_course_numbers(result)),
    )
