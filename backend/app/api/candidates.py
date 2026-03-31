"""
Candidates API
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
from uuid import UUID
import asyncpg

from app.core.database import get_db
from app.schemas import CandidateResponse, CandidateCreate

router = APIRouter()


@router.post("/", response_model=CandidateResponse)
async def create_candidate(
    name: str = Form(...),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None),
    db=Depends(get_db)
):
    """Create a new candidate with optional resume upload"""
    import uuid
    import os

    candidate_id = uuid.uuid4()
    resume_url = None

    # Handle resume upload
    if resume:
        from app.core.config import settings
        resume_dir = os.path.join(settings.STORAGE_LOCAL_PATH, "resumes")
        os.makedirs(resume_dir, exist_ok=True)

        resume_url = f"/resumes/{candidate_id}_{resume.filename}"
        resume_path = os.path.join(resume_dir, f"{candidate_id}_{resume.filename}")

        with open(resume_path, "wb") as f:
            content = await resume.read()
            f.write(content)

    row = await db.fetchrow("""
        INSERT INTO candidates (id, name, email, phone, resume_url)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
    """, candidate_id, name, email, phone, resume_url)

    return CandidateResponse(**dict(row))


@router.get("/", response_model=List[CandidateResponse])
async def list_candidates(
    limit: int = 50,
    db=Depends(get_db)
):
    """List all candidates"""
    rows = await db.fetch("""
        SELECT * FROM candidates
        ORDER BY created_at DESC
        LIMIT $1
    """, limit)

    return [CandidateResponse(**dict(row)) for row in rows]


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: UUID, db=Depends(get_db)):
    """Get a specific candidate"""
    row = await db.fetchrow("""
        SELECT * FROM candidates WHERE id = $1
    """, candidate_id)

    if not row:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return CandidateResponse(**dict(row))


@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: UUID, db=Depends(get_db)):
    """Delete a candidate"""
    result = await db.execute("""
        DELETE FROM candidates WHERE id = $1
    """, candidate_id)

    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Candidate not found")

    return {"message": "Candidate deleted"}


@router.post("/{candidate_id}/resume")
async def upload_resume(
    candidate_id: UUID,
    resume: UploadFile = File(...),
    db=Depends(get_db)
):
    """Upload or update resume for a candidate"""
    import os
    from app.core.config import settings

    resume_dir = os.path.join(settings.STORAGE_LOCAL_PATH, "resumes")
    os.makedirs(resume_dir, exist_ok=True)

    resume_url = f"/resumes/{candidate_id}_{resume.filename}"
    resume_path = os.path.join(resume_dir, f"{candidate_id}_{resume.filename}")

    with open(resume_path, "wb") as f:
        content = await resume.read()
        f.write(content)

    await db.execute("""
        UPDATE candidates SET resume_url = $2 WHERE id = $1
    """, candidate_id, resume_url)

    return {"message": "Resume uploaded", "resume_url": resume_url}
