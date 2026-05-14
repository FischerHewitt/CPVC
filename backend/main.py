from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import threading
import os

load_dotenv()

from routers import transcript, flowchart, professors
from services.polyratings import _ensure_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-warm PolyRatings cache in the background so first request is instant
    threading.Thread(target=_ensure_cache, daemon=True).start()
    yield


app = FastAPI(title="CPVC API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcript.router, prefix="/api/transcript", tags=["transcript"])
app.include_router(flowchart.router, prefix="/api/flowchart", tags=["flowchart"])
app.include_router(professors.router, prefix="/api/professors", tags=["professors"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
