"""
Pydantic Schemas for API Request/Response
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ============= Auth Schemas =============
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[UUID] = None


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    role: str = "interviewer"


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    role: str

    class Config:
        from_attributes = True


# ============= Candidate Schemas =============
class CandidateBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateWithResume(CandidateBase):
    resume_text: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: UUID
    resume_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Job Description Schemas =============
class JobDescriptionBase(BaseModel):
    title: str
    company: Optional[str] = None
    jd_text: str


class JobDescriptionCreate(JobDescriptionBase):
    requirements: Optional[Dict[str, Any]] = None


class JobDescriptionResponse(JobDescriptionBase):
    id: UUID
    jd_url: Optional[str] = None
    requirements: Optional[Dict[str, Any]] = None
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Interview Session Schemas =============
class InterviewSessionBase(BaseModel):
    candidate_id: UUID
    job_description_id: Optional[UUID] = None
    language: str = "en"


class InterviewSessionCreate(InterviewSessionBase):
    pass


class InterviewSessionResponse(InterviewSessionBase):
    id: UUID
    status: str
    interviewer_id: Optional[UUID] = None
    recording_url: Optional[str] = None
    transcript: Optional[str] = None
    overall_score: Optional[float] = None
    hiring_recommendation: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewStartResponse(BaseModel):
    session_id: UUID
    token: str
    room_name: str


# ============= Question Schemas =============
class QuestionBase(BaseModel):
    question_text: str
    question_type: str = "open"
    expected_duration_seconds: int = 60
    weight: float = 1.0
    metadata: Optional[Dict[str, Any]] = None


class QuestionCreate(QuestionBase):
    question_bank_id: UUID


class QuestionResponse(QuestionBase):
    id: UUID
    question_bank_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionBankBase(BaseModel):
    name: str
    category: str
    language: str = "en"


class QuestionBankCreate(QuestionBankBase):
    pass


class QuestionBankResponse(QuestionBankBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionBankWithQuestions(QuestionBankResponse):
    questions: List[QuestionResponse] = []


# ============= Interview Question Schemas =============
class InterviewQuestionCreate(BaseModel):
    interview_session_id: UUID
    question_id: Optional[UUID] = None
    question_text: str
    question_order: int
    is_followup: bool = False
    parent_question_id: Optional[UUID] = None


class InterviewQuestionResponse(BaseModel):
    id: UUID
    interview_session_id: UUID
    question_id: Optional[UUID] = None
    question_text: str
    question_order: int
    is_followup: bool
    parent_question_id: Optional[UUID] = None
    asked_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============= Candidate Response Schemas =============
class CandidateResponseCreate(BaseModel):
    interview_question_id: UUID
    transcript: str
    audio_url: Optional[str] = None
    duration_seconds: Optional[int] = None


class CandidateResponseMetrics(BaseModel):
    word_count: Optional[int] = None
    speaking_rate: Optional[float] = None
    pause_count: Optional[int] = None
    filler_word_count: Optional[int] = None


class CandidateResponseResponse(CandidateResponseCreate):
    id: UUID
    metrics: Optional[CandidateResponseMetrics] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Scoring Schemas =============
class ScoringDimensionBase(BaseModel):
    name: str
    category: str
    weight: float = 1.0
    description: Optional[str] = None


class ScoringDimensionCreate(ScoringDimensionBase):
    pass


class ScoringDimensionResponse(ScoringDimensionBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewScoreCreate(BaseModel):
    interview_session_id: UUID
    dimension_id: UUID
    score: float
    max_score: float = 10.0
    evaluator_type: str = "automated"
    notes: Optional[str] = None


class InterviewScoreResponse(BaseModel):
    id: UUID
    interview_session_id: UUID
    dimension_id: UUID
    score: float
    max_score: float
    evaluator_type: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewEvaluation(BaseModel):
    """Complete evaluation result for an interview"""
    interview_session_id: UUID
    overall_score: float
    dimension_scores: Dict[str, Dict[str, Any]]
    hiring_recommendation: str
    recommendations: List[str]
    transcript: Optional[str] = None
    recording_url: Optional[str] = None


# ============= JD-Resume Match Schemas =============
class JDResumeMatch(BaseModel):
    candidate_id: UUID
    job_description_id: UUID
    match_score: float
    matching_skills: List[str]
    gap_skills: List[str]
    analysis: str


# ============= Scoring Config Schemas =============
class ScoringConfigBase(BaseModel):
    name: str
    config: Dict[str, Any]


class ScoringConfigCreate(ScoringConfigBase):
    is_default: bool = False


class ScoringConfigResponse(ScoringConfigBase):
    id: UUID
    is_default: bool
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============= API Response Wrappers =============
class MessageResponse(BaseModel):
    message: str


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
