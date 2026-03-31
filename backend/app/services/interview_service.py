"""
Interview Service - Core business logic for interview management
"""
import uuid
import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
import asyncpg
import jwt
import json

from app.core.config import settings
from app.schemas import (
    InterviewSessionCreate,
    InterviewSessionResponse,
    InterviewStartResponse,
    InterviewEvaluation,
)


async def create_interview_session(
    conn: asyncpg.Connection,
    session_data: InterviewSessionCreate
) -> InterviewSessionResponse:
    """Create a new interview session"""
    session_id = uuid.uuid4()

    row = await conn.fetchrow("""
        INSERT INTO interview_sessions (
            id, candidate_id, job_description_id, language, status
        ) VALUES ($1, $2, $3, $4, 'scheduled')
        RETURNING *
    """, session_id, session_data.candidate_id, session_data.job_description_id, session_data.language)

    return InterviewSessionResponse(**dict(row))


async def get_interview_session(
    conn: asyncpg.Connection,
    session_id: UUID
) -> Optional[InterviewSessionResponse]:
    """Get a specific interview session by ID"""
    row = await conn.fetchrow("""
        SELECT * FROM interview_sessions WHERE id = $1
    """, session_id)

    if row:
        return InterviewSessionResponse(**dict(row))
    return None


async def get_interview_sessions(
    conn: asyncpg.Connection,
    status: Optional[str] = None,
    candidate_id: Optional[UUID] = None,
    limit: int = 50
) -> List[InterviewSessionResponse]:
    """List interview sessions with optional filters"""
    query = """
        SELECT * FROM interview_sessions
        WHERE 1=1
    """
    params = []
    param_count = 0

    if status:
        param_count += 1
        query += f" AND status = ${param_count}"
        params.append(status)

    if candidate_id:
        param_count += 1
        query += f" AND candidate_id = ${param_count}"
        params.append(candidate_id)

    query += f" ORDER BY created_at DESC LIMIT ${param_count + 1}"
    params.append(limit)

    rows = await conn.fetch(query, *params)
    return [InterviewSessionResponse(**dict(row)) for row in rows]


async def start_interview(
    conn: asyncpg.Connection,
    session_id: UUID
) -> InterviewStartResponse:
    """Start an interview session and generate LiveKit token"""
    # Update session status
    await conn.execute("""
        UPDATE interview_sessions
        SET status = 'in_progress', started_at = $2
        WHERE id = $1
    """, session_id, datetime.datetime.utcnow())

    # Generate LiveKit token
    room_name = f"interview_{session_id}"
    token = generate_livekit_token(room_name)

    return InterviewStartResponse(
        session_id=session_id,
        token=token,
        room_name=room_name
    )


def generate_livekit_token(room_name: str) -> str:
    """Generate a LiveKit access token for a room"""
    now = datetime.datetime.utcnow()
    payload = {
        "exp": int((now + datetime.timedelta(hours=2)).timestamp()),
        "iss": settings.LIVEKIT_API_KEY,
        "name": f"interviewer_{uuid.uuid4()}",
        "room": room_name,
        "room_join": True,
        "room_list": False,
        "room_record": True,
        "room_admin": True,
        "room_create": True
    }

    token = jwt.encode(
        payload,
        settings.LIVEKIT_API_SECRET,
        algorithm="HS256"
    )
    return token


async def complete_interview(
    conn: asyncpg.Connection,
    session_id: UUID
):
    """Mark an interview as completed"""
    await conn.execute("""
        UPDATE interview_sessions
        SET status = 'completed', completed_at = $2
        WHERE id = $1
    """, session_id, datetime.datetime.utcnow())


async def generate_evaluation(
    conn: asyncpg.Connection,
    session_id: UUID
) -> InterviewEvaluation:
    """Generate evaluation for a completed interview using LLM"""
    import httpx

    # Get interview data
    session = await conn.fetchrow("""
        SELECT * FROM interview_sessions WHERE id = $1
    """, session_id)

    if not session:
        raise ValueError("Interview session not found")

    # Get all responses for this interview
    responses = await conn.fetch("""
        SELECT cr.*, iq.question_text
        FROM candidate_responses cr
        JOIN interview_questions iq ON cr.interview_question_id = iq.id
        WHERE iq.interview_session_id = $1
        ORDER BY iq.question_order
    """, session_id)

    # Get scores
    scores = await conn.fetch("""
        SELECT sd.name, sd.category, isc.score, isc.max_score
        FROM interview_scores isc
        JOIN scoring_dimensions sd ON isc.dimension_id = sd.id
        WHERE isc.interview_session_id = $1
    """, session_id)

    # Build evaluation payload
    dimension_scores = {}
    for score in scores:
        category = score["category"]
        if category not in dimension_scores:
            dimension_scores[category] = {
                "score": 0,
                "max_score": 0,
                "breakdown": {}
            }
        dimension_scores[category]["breakdown"][score["name"]] = {
            "score": float(score["score"]),
            "max_score": float(score["max_score"])
        }
        dimension_scores[category]["score"] += float(score["score"])
        dimension_scores[category]["max_score"] += float(score["max_score"])

    # Calculate overall score
    total_score = sum(d["score"] for d in dimension_scores.values())
    total_max = sum(d["max_score"] for d in dimension_scores.values())
    overall_score = (total_score / total_max * 100) if total_max > 0 else 0

    # Determine hiring recommendation
    if overall_score >= 80:
        hiring_recommendation = "PROCEED"
    elif overall_score >= 60:
        hiring_recommendation = "HOLD"
    else:
        hiring_recommendation = "REJECT"

    # Generate recommendations using LLM
    recommendations = await generate_llm_recommendations(responses, dimension_scores)

    return InterviewEvaluation(
        interview_session_id=session_id,
        overall_score=overall_score,
        dimension_scores=dimension_scores,
        hiring_recommendation=hiring_recommendation,
        recommendations=recommendations,
        transcript=session.get("transcript"),
        recording_url=session.get("recording_url")
    )


async def generate_llm_recommendations(
    responses: List[Dict],
    dimension_scores: Dict
) -> List[str]:
    """Use LLM to generate personalized recommendations"""
    if not settings.ANTHROPIC_API_KEY:
        return ["Evaluation based on automated scoring"]

    # Build prompt
    prompt = f"""Based on the following interview assessment data, provide 3-5 concise, actionable recommendations for the hiring team:

Dimension Scores:
{json.dumps(dimension_scores, indent=2)}

The recommendations should:
1. Highlight key strengths
2. Note any areas of concern
3. Provide context for the hiring decision

Format as a bulleted list."""

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
                    "max_tokens": 500,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            if response.status_code == 200:
                result = response.json()
                content = result["content"][0]["text"]
                # Parse bullet points
                recommendations = [
                    line.strip().lstrip("-•*").strip()
                    for line in content.split("\n")
                    if line.strip() and line.strip()[0] in "-•*"
                ]
                return recommendations[:5]
    except Exception as e:
        print(f"Error generating LLM recommendations: {e}")

    return ["Review detailed scores for hiring decision"]
