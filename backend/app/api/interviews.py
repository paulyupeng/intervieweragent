"""
Interview Sessions API
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from uuid import UUID
import asyncpg

from app.core.database import get_db
from app.schemas import (
    InterviewSessionCreate,
    InterviewSessionResponse,
    InterviewStartResponse,
    InterviewEvaluation,
)
from app.services.interview_service import (
    create_interview_session,
    get_interview_session,
    get_interview_sessions,
    start_interview,
    complete_interview,
    generate_evaluation,
)

router = APIRouter()


@router.post("/", response_model=InterviewSessionResponse)
async def create_session(
    session_data: InterviewSessionCreate,
    db=Depends(get_db)
):
    """Create a new interview session"""
    return await create_interview_session(db, session_data)


@router.get("/", response_model=List[InterviewSessionResponse])
async def list_sessions(
    status: Optional[str] = None,
    candidate_id: Optional[UUID] = None,
    limit: int = 50,
    db=Depends(get_db)
):
    """List interview sessions with optional filters"""
    return await get_interview_sessions(db, status, candidate_id, limit)


@router.get("/{session_id}", response_model=InterviewSessionResponse)
async def get_session(session_id: UUID, db=Depends(get_db)):
    """Get a specific interview session"""
    session = await get_interview_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    return session


@router.post("/{session_id}/start", response_model=InterviewStartResponse)
async def start_session(session_id: UUID, db=Depends(get_db)):
    """Start an interview session - returns LiveKit token"""
    return await start_interview(db, session_id)


@router.post("/{session_id}/complete")
async def complete_session(
    session_id: UUID,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    """Complete an interview session and trigger evaluation"""
    await complete_interview(db, session_id)
    # Generate evaluation in background
    background_tasks.add_task(generate_evaluation_wrapper, session_id)
    return {"message": "Interview completed, evaluation being generated"}


async def generate_evaluation_wrapper(session_id: UUID):
    """Wrapper to generate evaluation in background"""
    from app.core.database import get_db
    async for db in get_db():
        await generate_evaluation(db, session_id)
        break


@router.get("/{session_id}/evaluation", response_model=InterviewEvaluation)
async def get_evaluation(session_id: UUID, db=Depends(get_db)):
    """Get the evaluation result for a completed interview"""
    # This would fetch the pre-generated evaluation
    # For now, regenerate if not exists
    evaluation = await generate_evaluation(db, session_id)
    return evaluation
