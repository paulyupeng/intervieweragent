"""
Interviewer Agent Backend - FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import interviews, questions, candidates, job_descriptions, scoring, auth
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Interviewer Agent API",
    description="Voice-based interview system for candidate assessment",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "Interviewer Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["Interviews"])
app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
app.include_router(candidates.router, prefix="/api/candidates", tags=["Candidates"])
app.include_router(job_descriptions.router, prefix="/api/jobs", tags=["Job Descriptions"])
app.include_router(scoring.router, prefix="/api/scoring", tags=["Scoring"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
