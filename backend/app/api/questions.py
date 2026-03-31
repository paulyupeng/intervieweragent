"""
Questions API - Question bank management
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import UUID
import asyncpg
import yaml
import os

from app.core.database import get_db
from app.core.config import settings
from app.schemas import (
    QuestionBankResponse,
    QuestionBankWithQuestions,
    QuestionResponse,
    QuestionCreate,
)

router = APIRouter()

QUESTION_BANKS_PATH = "/question_banks"


@router.get("/banks", response_model=List[QuestionBankResponse])
async def list_question_banks(
    category: Optional[str] = None,
    language: str = "en",
    db=Depends(get_db)
):
    """List all question banks with optional filters"""
    query = """
        SELECT * FROM question_banks
        WHERE is_active = true
    """
    params = []

    if category:
        query += " AND category = $1"
        params.append(category)

    if language:
        query += " AND language = $1"
        params.append(language)

    rows = await db.fetch(query, *params)
    return [QuestionBankResponse(**dict(row)) for row in rows]


@router.get("/banks/{bank_id}", response_model=QuestionBankWithQuestions)
async def get_question_bank(bank_id: UUID, db=Depends(get_db)):
    """Get a question bank with all its questions"""
    bank = await db.fetchrow("""
        SELECT * FROM question_banks WHERE id = $1
    """, bank_id)

    if not bank:
        raise HTTPException(status_code=404, detail="Question bank not found")

    questions = await db.fetch("""
        SELECT * FROM questions WHERE question_bank_id = $1
        ORDER BY created_at
    """, bank_id)

    return QuestionBankWithQuestions(
        **dict(bank),
        questions=[QuestionResponse(**dict(q)) for q in questions]
    )


@router.get("/library", response_model=List[dict])
async def get_question_library(
    category: Optional[str] = None,
    language: str = "en"
):
    """
    Get questions from YAML files in the question_banks directory.
    This is useful for initial setup and admin UI.
    """
    questions = []

    if not os.path.exists(QUESTION_BANKS_PATH):
        return questions

    for filename in os.listdir(QUESTION_BANKS_PATH):
        if not filename.endswith(".yaml"):
            continue

        # Check language filter
        if language == "en" and filename.endswith("_zh.yaml"):
            continue
        if language == "zh" and not filename.endswith("_zh.yaml"):
            continue

        filepath = os.path.join(QUESTION_BANKS_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Check category filter
        metadata = data.get("metadata", {})
        file_category = metadata.get("name", filename.replace(".yaml", ""))

        if category and category.lower() not in file_category.lower():
            continue

        for q in data.get("questions", []):
            questions.append({
                "id": q.get("id"),
                "text": q.get("text") or q.get("text_zh"),
                "type": q.get("type"),
                "category": metadata.get("name", "Unknown"),
                "language": language,
                "expected_duration_seconds": q.get("expected_duration_seconds", 60),
                "evaluation_focus": q.get("evaluation_focus", []),
                "followups": q.get("followups", [])
            })

    return questions


@router.post("/banks", response_model=QuestionBankResponse)
async def create_question_bank(
    name: str,
    category: str,
    language: str = "en",
    db=Depends(get_db)
):
    """Create a new question bank"""
    bank_id = uuid.uuid4()
    row = await db.fetchrow("""
        INSERT INTO question_banks (id, name, category, language, is_active)
        VALUES ($1, $2, $3, $4, true)
        RETURNING *
    """, bank_id, name, category, language)

    return QuestionBankResponse(**dict(row))


@router.post("/", response_model=QuestionResponse)
async def create_question(
    question_data: QuestionCreate,
    db=Depends(get_db)
):
    """Create a new question in a question bank"""
    import uuid
    question_id = uuid.uuid4()

    row = await db.fetchrow("""
        INSERT INTO questions (
            id, question_bank_id, question_text, question_type,
            expected_duration_seconds, weight, metadata
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING *
    """, question_id, question_data.question_bank_id, question_data.question_text,
        question_data.question_type, question_data.expected_duration_seconds,
        question_data.weight, question_data.metadata)

    return QuestionResponse(**dict(row))


@router.delete("/banks/{bank_id}")
async def delete_question_bank(bank_id: UUID, db=Depends(get_db)):
    """Delete a question bank (cascades to questions)"""
    result = await db.execute("""
        DELETE FROM question_banks WHERE id = $1
    """, bank_id)

    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Question bank not found")

    return {"message": "Question bank deleted"}


@router.get("/suggest", response_model=List[dict])
async def suggest_questions(
    job_description: str,
    limit: int = 10,
    db=Depends(get_db)
):
    """
    Suggest relevant questions based on job description.
    Uses simple keyword matching - can be enhanced with LLM.
    """
    # Extract keywords from JD
    keywords = extract_jd_keywords(job_description)

    # Get questions that match keywords
    questions = await db.fetch("""
        SELECT q.*, qb.category
        FROM questions q
        JOIN question_banks qb ON q.question_bank_id = qb.id
        WHERE q.is_active = true
        LIMIT $1
    """, limit)

    # In a real implementation, you would:
    # 1. Use LLM to analyze JD requirements
    # 2. Match questions to required competencies
    # 3. Rank by relevance

    return [dict(q) for q in questions]


def extract_jd_keywords(jd_text: str) -> List[str]:
    """Extract key skills and requirements from JD text"""
    # Simple implementation - should use NLP/LLM in production
    common_skills = [
        "python", "javascript", "react", "node", "aws", "docker",
        "leadership", "communication", "teamwork", "problem solving",
        "agile", "scrum", "api", "database", "sql"
    ]

    jd_lower = jd_text.lower()
    return [skill for skill in common_skills if skill in jd_lower]
