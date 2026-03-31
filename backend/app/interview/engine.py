"""
Interview Engine - Core orchestration for voice interviews
Manages conversation flow, question selection, and real-time interaction
"""
import asyncio
import json
import uuid
import datetime
from typing import Optional, List, Dict, Any, Callable
from enum import Enum
import yaml
import os

from app.core.config import settings
from app.voice.pipeline import VoicePipeline, DeepgramSTT, ElevenLabsTTS


class InterviewState(Enum):
    """Interview state machine states"""
    INITIALIZED = "initialized"
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


class InterviewSection(Enum):
    """Interview sections for structured assessment"""
    OPENING = "opening"
    ENGLISH_PROFICIENCY = "english_proficiency"
    INDUSTRY_UNDERSTANDING = "industry_understanding"
    PROFESSIONAL_SKILLS = "professional_skills"
    SOFT_SKILLS = "soft_skills"
    CLOSING = "closing"


class InterviewEngine:
    """
    Core interview orchestration engine
    Manages the conversation flow, question selection, and real-time interaction
    """

    def __init__(
        self,
        session_id: uuid.UUID,
        language: str = "en",
        question_bank_path: str = "/question_banks"
    ):
        self.session_id = session_id
        self.language = language
        self.question_bank_path = question_bank_path

        # State management
        self.state = InterviewState.INITIALIZED
        self.current_section = InterviewSection.OPENING
        self.current_question_index = 0
        self.question_queue: List[Dict] = []
        self.asked_questions: List[Dict] = []
        self.responses: List[Dict] = []

        # Voice pipeline
        self.voice_pipeline = VoicePipeline()

        # Callbacks
        self._on_question_asked: Optional[Callable] = None
        self._on_response_received: Optional[Callable] = None
        self._on_section_complete: Optional[Callable] = None
        self._on_interview_complete: Optional[Callable] = None

        # Timing
        self.started_at: Optional[datetime.datetime] = None
        self.section_started_at: Optional[datetime.datetime] = None

        # Candidate context (for personalization)
        self.candidate_name: Optional[str] = None
        self.job_description: Optional[Dict] = None

    async def initialize(
        self,
        candidate_name: Optional[str] = None,
        job_description: Optional[Dict] = None
    ):
        """Initialize the interview with candidate context"""
        self.candidate_name = candidate_name
        self.job_description = job_description

        # Load question bank based on language
        await self._load_question_bank()

        self.state = InterviewState.STARTED
        self.started_at = datetime.datetime.utcnow()

    async def _load_question_bank(self):
        """Load questions from YAML files"""
        self.question_queue = []

        # Determine which question banks to load
        banks_to_load = [
            "english_proficiency",
            "industry_understanding",
            "professional_skills",
            "soft_skills"
        ]

        # Add language suffix if not English
        lang_suffix = f"_{self.language}" if self.language != "en" else ""

        for bank_name in banks_to_load:
            filename = f"{bank_name}{lang_suffix}.yaml"
            filepath = os.path.join(self.question_bank_path, filename)

            # Fallback to English if localized file doesn't exist
            if not os.path.exists(filepath) and lang_suffix:
                filepath = os.path.join(self.question_bank_path, f"{bank_name}.yaml")

            if not os.path.exists(filepath):
                print(f"Warning: Question bank not found: {filepath}")
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            # Add questions to queue with section info
            section = self._map_bank_to_section(bank_name)
            for question in data.get("questions", []):
                self.question_queue.append({
                    **question,
                    "section": section.value,
                    "bank_name": bank_name
                })

        # Shuffle questions within each section for variety
        self._shuffle_questions()

    def _map_bank_to_section(self, bank_name: str) -> InterviewSection:
        """Map question bank name to interview section"""
        mapping = {
            "english_proficiency": InterviewSection.ENGLISH_PROFICIENCY,
            "industry_understanding": InterviewSection.INDUSTRY_UNDERSTANDING,
            "professional_skills": InterviewSection.PROFESSIONAL_SKILLS,
            "soft_skills": InterviewSection.SOFT_SKILLS,
        }
        return mapping.get(bank_name, InterviewSection.OPENING)

    def _shuffle_questions(self):
        """Shuffle questions within each section"""
        import random

        # Group by section
        sections = {}
        for q in self.question_queue:
            section = q.get("section", "unknown")
            if section not in sections:
                sections[section] = []
            sections[section].append(q)

        # Shuffle each section
        for section in sections:
            random.shuffle(sections[section])

        # Rebuild queue maintaining section order
        section_order = [
            InterviewSection.OPENING.value,
            InterviewSection.ENGLISH_PROFICIENCY.value,
            InterviewSection.INDUSTRY_UNDERSTANDING.value,
            InterviewSection.PROFESSIONAL_SKILLS.value,
            InterviewSection.SOFT_SKILLS.value,
            InterviewSection.CLOSING.value
        ]

        self.question_queue = []
        for section in section_order:
            if section in sections:
                self.question_queue.extend(sections[section])

    async def start_interview(self) -> str:
        """Start the interview and return the opening question"""
        self.state = InterviewState.IN_PROGRESS
        self.section_started_at = datetime.datetime.utcnow()

        # Generate personalized opening
        opening = self._generate_opening()

        # Add to asked questions
        self.asked_questions.append({
            "id": "OPENING",
            "text": opening,
            "type": "opening",
            "asked_at": datetime.datetime.utcnow().isoformat()
        })

        if self._on_question_asked:
            await self._on_question_asked(opening)

        return opening

    def _generate_opening(self) -> str:
        """Generate a personalized opening message"""
        candidate_greeting = f"Hello{', ' + self.candidate_name if self.candidate_name else ''}!"

        return f"""{candidate_greeting} Welcome to today's interview.

I'll be asking you a series of questions to understand your background, skills, and experience. The interview will cover your English proficiency, industry knowledge, professional skills, and soft skills.

Each question will take about 1-2 minutes to answer. Please speak clearly and take your time to formulate your responses.

Are you ready to begin?"""

    async def process_response(
        self,
        transcript: str,
        audio_duration: Optional[float] = None
    ) -> Optional[str]:
        """
        Process a candidate's response and return the next question
        Returns None if interview is complete
        """
        # Store response
        response = {
            "transcript": transcript,
            "word_count": len(transcript.split()),
            "audio_duration": audio_duration,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.responses.append(response)

        if self._on_response_received:
            await self._on_response_received(response)

        # Get next question
        next_question = self._get_next_question(transcript)

        if next_question:
            self.asked_questions.append({
                **next_question,
                "asked_at": datetime.datetime.utcnow().isoformat()
            })

            if self._on_question_asked:
                await self._on_question_asked(next_question["text"])

            return next_question["text"]
        else:
            # Interview complete
            await self._complete_interview()
            return None

    def _get_next_question(self, last_response: str) -> Optional[Dict]:
        """
        Determine the next question based on conversation flow
        Optionally uses LLM for dynamic follow-up generation
        """
        if not self.question_queue:
            return None

        # Check if we should ask a follow-up
        last_question = self.asked_questions[-1] if self.asked_questions else None

        if last_question and last_question.get("followups"):
            # Simple follow-up logic - could be enhanced with LLM
            if len(last_response.split()) > 50:  # Substantial answer
                # Ask a follow-up from the list
                followup_text = last_question["followups"][0]
                return {
                    "id": f"FOLLOWUP_{last_question['id']}",
                    "text": followup_text,
                    "type": "followup",
                    "is_followup": True,
                    "parent_question_id": last_question["id"]
                }

        # Get next question from queue
        return self.question_queue.pop(0)

    async def _complete_interview(self):
        """Complete the interview and generate closing"""
        self.state = InterviewState.COMPLETED

        closing = """Thank you for taking the time to speak with me today.

Your responses have been recorded and will be evaluated. You should receive feedback within the next few days.

Do you have any questions for me before we conclude?"""

        if self._on_interview_complete:
            await self._on_interview_complete(closing)

    async def speak_question(self, question_text: str) -> bytes:
        """Convert question text to audio"""
        return await self.voice_pipeline.tts.synthesize(question_text)

    async def transcribe_response(self, audio_data: bytes) -> str:
        """Transcribe audio response"""
        return await self.voice_pipeline.stt.transcribe(audio_data)

    def get_interview_summary(self) -> Dict[str, Any]:
        """Get a summary of the interview progress"""
        return {
            "session_id": str(self.session_id),
            "state": self.state.value,
            "current_section": self.current_section.value,
            "questions_asked": len(self.asked_questions),
            "responses_received": len(self.responses),
            "questions_remaining": len(self.question_queue),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "duration_seconds": (
                (datetime.datetime.utcnow() - self.started_at).total_seconds()
                if self.started_at else 0
            )
        }

    def get_full_transcript(self) -> str:
        """Get the full interview transcript"""
        transcript_lines = []

        for i, question in enumerate(self.asked_questions):
            transcript_lines.append(f"Interviewer: {question['text']}")

            if i < len(self.responses):
                transcript_lines.append(f"Candidate: {self.responses[i]['transcript']}")

        return "\n\n".join(transcript_lines)

    # Callback setters
    def on_question_asked(self, callback: Callable):
        self._on_question_asked = callback

    def on_response_received(self, callback: Callable):
        self._on_response_received = callback

    def on_section_complete(self, callback: Callable):
        self._on_section_complete = callback

    def on_interview_complete(self, callback: Callable):
        self._on_interview_complete = callback


# Global registry of active interview engines
_active_interviews: Dict[uuid.UUID, InterviewEngine] = {}


def get_interview_engine(session_id: uuid.UUID) -> Optional[InterviewEngine]:
    """Get an active interview engine by session ID"""
    return _active_interviews.get(session_id)


def create_interview_engine(
    session_id: uuid.UUID,
    language: str = "en"
) -> InterviewEngine:
    """Create and register a new interview engine"""
    engine = InterviewEngine(session_id, language)
    _active_interviews[session_id] = engine
    return engine


def remove_interview_engine(session_id: uuid.UUID):
    """Remove an interview engine from the registry"""
    if session_id in _active_interviews:
        del _active_interviews[session_id]
