"""
Scoring API
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from uuid import UUID
import asyncpg

from app.core.database import get_db
from app.schemas import (
    ScoringDimensionResponse,
    InterviewScoreResponse,
    InterviewScoreCreate,
    ScoringConfigResponse,
    ScoringConfigCreate,
)

router = APIRouter()


@router.get("/dimensions", response_model=List[ScoringDimensionResponse])
async def list_scoring_dimensions(
    category: Optional[str] = None,
    db=Depends(get_db)
):
    """List all scoring dimensions with optional category filter"""
    query = "SELECT * FROM scoring_dimensions WHERE 1=1"
    params = []

    if category:
        query += " AND category = $1"
        params.append(category)

    rows = await db.fetch(query, *params)
    return [ScoringDimensionResponse(**dict(row)) for row in rows]


@router.post("/dimensions", response_model=ScoringDimensionResponse)
async def create_scoring_dimension(
    dimension: ScoringDimensionResponse,
    db=Depends(get_db)
):
    """Create a new scoring dimension"""
    import uuid
    dim_id = uuid.uuid4()

    row = await db.fetchrow("""
        INSERT INTO scoring_dimensions (id, name, category, weight, description)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
    """, dim_id, dimension.name, dimension.category, dimension.weight, dimension.description)

    return ScoringDimensionResponse(**dict(row))


@router.post("/scores", response_model=InterviewScoreResponse)
async def create_interview_score(
    score: InterviewScoreCreate,
    db=Depends(get_db)
):
    """Create or update an interview score"""
    import uuid
    score_id = uuid.uuid4()

    # Check if score already exists for this session and dimension
    existing = await db.fetchrow("""
        SELECT * FROM interview_scores
        WHERE interview_session_id = $1 AND dimension_id = $2
    """, score.interview_session_id, score.dimension_id)

    if existing:
        # Update existing
        row = await db.fetchrow("""
            UPDATE interview_scores
            SET score = $3, max_score = $4, evaluator_type = $5, notes = $6
            WHERE id = $7
            RETURNING *
        """, score.score, score.max_score, score.evaluator_type, score.notes, existing["id"])
    else:
        # Create new
        row = await db.fetchrow("""
            INSERT INTO interview_scores (
                id, interview_session_id, dimension_id, score,
                max_score, evaluator_type, notes
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
        """, score_id, score.interview_session_id, score.dimension_id,
            score.score, score.max_score, score.evaluator_type, score.notes)

    return InterviewScoreResponse(**dict(row))


@router.get("/sessions/{session_id}/scores", response_model=List[InterviewScoreResponse])
async def get_interview_scores(
    session_id: UUID,
    db=Depends(get_db)
):
    """Get all scores for an interview session"""
    rows = await db.fetch("""
        SELECT * FROM interview_scores
        WHERE interview_session_id = $1
    """, session_id)

    return [InterviewScoreResponse(**dict(row)) for row in rows]


@router.post("/configs", response_model=ScoringConfigResponse)
async def create_scoring_config(
    config: ScoringConfigCreate,
    db=Depends(get_db)
):
    """Create a new scoring configuration"""
    import uuid
    config_id = uuid.uuid4()

    # If this is set as default, unset other defaults
    if config.is_default:
        await db.execute("""
            UPDATE scoring_configs SET is_default = false WHERE is_default = true
        """)

    row = await db.fetchrow("""
        INSERT INTO scoring_configs (id, name, config, is_default)
        VALUES ($1, $2, $3, $4)
        RETURNING *
    """, config_id, config.name, config.config, config.is_default)

    return ScoringConfigResponse(**dict(row))


@router.get("/configs", response_model=List[ScoringConfigResponse])
async def list_scoring_configs(db=Depends(get_db)):
    """List all scoring configurations"""
    rows = await db.fetch("""
        SELECT * FROM scoring_configs ORDER BY is_default DESC, created_at DESC
    """)

    return [ScoringConfigResponse(**dict(row)) for row in rows]


@router.get("/configs/default", response_model=ScoringConfigResponse)
async def get_default_scoring_config(db=Depends(get_db)):
    """Get the default scoring configuration"""
    row = await db.fetchrow("""
        SELECT * FROM scoring_configs WHERE is_default = true LIMIT 1
    """)

    if not row:
        raise HTTPException(status_code=404, detail="No default config found")

    return ScoringConfigResponse(**dict(row))


@router.put("/configs/{config_id}", response_model=ScoringConfigResponse)
async def update_scoring_config(
    config_id: UUID,
    name: Optional[str] = None,
    config: Optional[dict] = None,
    is_default: Optional[bool] = None,
    db=Depends(get_db)
):
    """Update a scoring configuration"""
    # If setting as default, unset others
    if is_default:
        await db.execute("""
            UPDATE scoring_configs SET is_default = false WHERE is_default = true
        """)

    updates = []
    params = [config_id]
    param_count = 1

    if name is not None:
        param_count += 1
        updates.append(f"name = ${param_count}")
        params.append(name)

    if config is not None:
        param_count += 1
        updates.append(f"config = ${param_count}")
        params.append(config)

    if is_default is not None:
        param_count += 1
        updates.append(f"is_default = ${param_count}")
        params.append(is_default)

    params.append(config_id)
    query = f"UPDATE scoring_configs SET {', '.join(updates)} WHERE id = ${param_count + 1} RETURNING *"

    row = await db.fetchrow(query, *params)

    if not row:
        raise HTTPException(status_code=404, detail="Config not found")

    return ScoringConfigResponse(**dict(row))
