from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import threading
import os

load_dotenv()

from routers import transcript, flowchart, professors, ge, sessions, courses, electives, contact
from services.polyratings import warm_cache


def _allowed_frontend_origins() -> list[str]:
    raw_origins = os.getenv("FRONTEND_URLS") or os.getenv("FRONTEND_URL") or "http://localhost:3000"
    return [origin.strip().rstrip("/") for origin in raw_origins.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-warm PolyRatings cache in the background so first request is instant
    threading.Thread(target=warm_cache, daemon=True).start()
    yield


app = FastAPI(title="CPVC API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_frontend_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcript.router, prefix="/api/transcript", tags=["transcript"])
app.include_router(flowchart.router, prefix="/api/flowchart", tags=["flowchart"])
app.include_router(professors.router, prefix="/api/professors", tags=["professors"])
app.include_router(ge.router, prefix="/api/ge", tags=["ge"])
app.include_router(electives.router, prefix="/api/electives", tags=["electives"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
app.include_router(contact.router, prefix="/api/contact", tags=["contact"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
