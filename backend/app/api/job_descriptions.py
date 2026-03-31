"""
Job Descriptions API
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional, Dict, Any
from uuid import UUID
import asyncpg

from app.core.database import get_db
from app.schemas import JobDescriptionResponse, JobDescriptionCreate, JDResumeMatch

router = APIRouter()


@router.post("/", response_model=JobDescriptionResponse)
async def create_job_description(
    title: str = Form(...),
    company: Optional[str] = Form(None),
    jd_text: str = Form(...),
    requirements: Optional[str] = Form(None),
    db=Depends(get_db)
):
    """Create a new job description"""
    import uuid
    import json

    jd_id = uuid.uuid4()
    req_dict = None

    if requirements:
        try:
            req_dict = json.loads(requirements)
        except json.JSONDecodeError:
            req_dict = {"raw": requirements}

    row = await db.fetchrow("""
        INSERT INTO job_descriptions (id, title, company, jd_text, requirements)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
    """, jd_id, title, company, jd_text, req_dict)

    return JobDescriptionResponse(**dict(row))


@router.get("/", response_model=List[JobDescriptionResponse])
async def list_job_descriptions(
    limit: int = 50,
    db=Depends(get_db)
):
    """List all job descriptions"""
    rows = await db.fetch("""
        SELECT * FROM job_descriptions
        ORDER BY created_at DESC
        LIMIT $1
    """, limit)

    return [JobDescriptionResponse(**dict(row)) for row in rows]


@router.get("/{jd_id}", response_model=JobDescriptionResponse)
async def get_job_description(jd_id: UUID, db=Depends(get_db)):
    """Get a specific job description"""
    row = await db.fetchrow("""
        SELECT * FROM job_descriptions WHERE id = $1
    """, jd_id)

    if not row:
        raise HTTPException(status_code=404, detail="Job description not found")

    return JobDescriptionResponse(**dict(row))


@router.post("/{jd_id}/parse")
async def parse_job_description(
    jd_id: UUID,
    db=Depends(get_db)
):
    """
    Parse job description to extract structured requirements.
    Uses LLM to analyze jd_text and populate requirements field.
    """
    from app.core.config import settings
    import httpx
    import json

    jd = await db.fetchrow("""
        SELECT * FROM job_descriptions WHERE id = $1
    """, jd_id)

    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(status_code=503, detail="LLM service not configured")

    prompt = f"""Analyze this job description and extract the following information in JSON format:

{{
    "required_skills": ["list of required technical skills"],
    "preferred_skills": ["list of preferred skills"],
    "experience_years": number or range,
    "education_requirements": "education requirements",
    "soft_skills": ["list of soft skills required"],
    "responsibilities": ["key responsibilities"],
    "domain_knowledge": ["industry/domain knowledge required"]
}}

Job Description:
{jd['jd_text']}

Respond with only the JSON, no other text."""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1000,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            if response.status_code == 200:
                result = response.json()
                requirements = json.loads(result["content"][0]["text"])

                await db.execute("""
                    UPDATE job_descriptions SET requirements = $2 WHERE id = $1
                """, jd_id, requirements)

                return {"message": "Requirements extracted", "requirements": requirements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing JD: {str(e)}")

    raise HTTPException(status_code=500, detail="Failed to parse job description")


@router.post("/{jd_id}/match/{candidate_id}", response_model=JDResumeMatch)
async def match_candidate_to_jd(
    jd_id: UUID,
    candidate_id: UUID,
    db=Depends(get_db)
):
    """
    Match a candidate's resume to a job description.
    Returns match score, matching skills, and gap analysis.
    """
    from app.core.config import settings
    import httpx

    # Get JD and candidate
    jd = await db.fetchrow("""
        SELECT * FROM job_descriptions WHERE id = $1
    """, jd_id)

    candidate = await db.fetchrow("""
        SELECT * FROM candidates WHERE id = $1
    """, candidate_id)

    if not jd or not candidate:
        raise HTTPException(status_code=404, detail="JD or candidate not found")

    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(status_code=503, detail="LLM service not configured")

    prompt = f"""Analyze the candidate's resume against the job description and provide:

1. A match score from 0-100
2. List of matching skills
3. List of gap skills (missing but required)
4. A brief analysis (2-3 sentences)

Job Description:
{jd['jd_text']}

Candidate Resume:
{candidate.get('resume_text', 'No resume text available')}

Respond in JSON format:
{{
    "match_score": 75,
    "matching_skills": ["skill1", "skill2"],
    "gap_skills": ["skill3", "skill4"],
    "analysis": "Brief analysis..."
}}"""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1000,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            if response.status_code == 200:
                result = response.json()
                match_data = httpx.Response(result["content"][0]["text"]).json()

                # Store in database
                import uuid
                match_id = uuid.uuid4()
                await db.execute("""
                    INSERT INTO jd_resume_matches (
                        id, candidate_id, job_description_id,
                        match_score, matching_skills, gap_skills, analysis
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """, match_id, candidate_id, jd_id,
                    match_data.get("match_score", 0),
                    match_data.get("matching_skills", []),
                    match_data.get("gap_skills", []),
                    match_data.get("analysis", ""))

                return JDResumeMatch(
                    candidate_id=candidate_id,
                    job_description_id=jd_id,
                    match_score=match_data.get("match_score", 0),
                    matching_skills=match_data.get("matching_skills", []),
                    gap_skills=match_data.get("gap_skills", []),
                    analysis=match_data.get("analysis", "")
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching: {str(e)}")

    raise HTTPException(status_code=500, detail="Failed to match candidate to JD")


@router.delete("/{jd_id}")
async def delete_job_description(jd_id: UUID, db=Depends(get_db)):
    """Delete a job description"""
    result = await db.execute("""
        DELETE FROM job_descriptions WHERE id = $1
    """, jd_id)

    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Job description not found")

    return {"message": "Job description deleted"}
