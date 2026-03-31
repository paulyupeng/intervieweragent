"""
Scoring Service - Automated and LLM-based evaluation
"""
import asyncio
import json
from typing import Dict, List, Any, Optional
from uuid import UUID
import re

from app.core.config import settings


class ScoringService:
    """
    Evaluates candidate responses using multiple methods:
    1. Automated metrics (word count, speaking rate, etc.)
    2. Grammar and vocabulary analysis
    3. LLM-based holistic evaluation
    """

    def __init__(self):
        self.grammar_patterns = self._load_grammar_patterns()

    def _load_grammar_patterns(self) -> Dict[str, re.Pattern]:
        """Load common grammar error patterns"""
        return {
            "subject_verb_agreement": re.compile(r'\b(he|she|it)\s+(\w+)s?\b'),
            "tense_consistency": re.compile(r'\b(was|were)\s+(\w+)ing\b'),
            "article_usage": re.compile(r'\b(a|an|the)\s+(\w+)\b'),
        }

    async def evaluate_response(
        self,
        question: Dict[str, Any],
        transcript: str,
        audio_duration: Optional[float] = None,
        evaluation_focus: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a single candidate response
        Returns scores for each evaluation dimension
        """
        scores = {}

        # Automated metrics
        metrics = self._calculate_automated_metrics(
            transcript, audio_duration
        )
        scores["automated"] = metrics

        # Grammar analysis
        grammar_score = self._analyze_grammar(transcript)
        scores["grammar"] = grammar_score

        # Vocabulary analysis
        vocabulary_score = self._analyze_vocabulary(transcript)
        scores["vocabulary"] = vocabulary_score

        # LLM evaluation (if enabled and requested)
        if settings.ANTHROPIC_API_KEY and evaluation_focus:
            llm_scores = await self._llm_evaluate(
                question, transcript, evaluation_focus
            )
            scores["llm"] = llm_scores

        # Calculate weighted average
        overall_score = self._calculate_overall_score(scores, evaluation_focus)

        return {
            "overall_score": overall_score,
            "dimension_scores": scores,
            "metrics": metrics
        }

    def _calculate_automated_metrics(
        self,
        transcript: str,
        audio_duration: Optional[float] = None
    ) -> Dict[str, Any]:
        """Calculate automated speech metrics"""
        words = transcript.split()
        word_count = len(words)

        # Speaking rate (words per minute)
        speaking_rate = 0
        if audio_duration and audio_duration > 0:
            speaking_rate = (word_count / audio_duration) * 60

        # Unique words (lexical diversity)
        unique_words = set(w.lower() for w in words)
        lexical_diversity = len(unique_words) / word_count if word_count > 0 else 0

        # Average word length (vocabulary sophistication proxy)
        avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0

        # Sentence count (proxy for structured response)
        sentence_count = len(re.split(r'[.!?]+', transcript))

        return {
            "word_count": word_count,
            "speaking_rate_wpm": round(speaking_rate, 2),
            "lexical_diversity": round(lexical_diversity, 3),
            "avg_word_length": round(avg_word_length, 2),
            "sentence_count": sentence_count,
            "avg_sentence_length": round(word_count / sentence_count, 1) if sentence_count > 0 else 0
        }

    def _analyze_grammar(self, transcript: str) -> Dict[str, Any]:
        """Analyze grammar quality"""
        # Count potential grammar issues
        issues = {
            "repeated_words": len(re.findall(r'\b(\w+)\s+\1\b', transcript.lower())),
            "filler_words": len(re.findall(
                r'\b(um|uh|like|you know|sort of|kind of|i mean)\b',
                transcript.lower()
            )),
            "incomplete_sentences": transcript.count("\n")  # Rough proxy
        }

        total_words = len(transcript.split())
        error_rate = sum(issues.values()) / total_words if total_words > 0 else 0

        # Score: 10 - error_rate * 10 (higher is better)
        score = max(0, 10 - error_rate * 20)

        return {
            "score": round(score, 2),
            "error_rate": round(error_rate, 4),
            "issues": issues
        }

    def _analyze_vocabulary(self, transcript: str) -> Dict[str, Any]:
        """Analyze vocabulary usage"""
        words = transcript.split()
        unique_words = set(w.lower() for w in words)

        # Word frequency distribution
        word_freq = {}
        for w in words:
            w_lower = w.lower()
            word_freq[w_lower] = word_freq.get(w_lower, 0) + 1

        # Find sophisticated words (longer, less common)
        sophisticated_words = [
            w for w in unique_words
            if len(w) > 8 and word_freq.get(w.lower(), 0) == 1
        ]

        # Score based on lexical diversity and sophisticated word usage
        diversity_score = len(unique_words) / len(words) if words else 0
        sophistication_score = len(sophisticated_words) / len(words) if words else 0

        combined_score = (diversity_score * 0.6 + sophistication_score * 0.4) * 10

        return {
            "score": round(min(10, combined_score), 2),
            "unique_word_count": len(unique_words),
            "sophisticated_words": sophisticated_words[:10],  # Top 10
            "lexical_diversity": round(diversity_score, 3)
        }

    async def _llm_evaluate(
        self,
        question: Dict[str, Any],
        transcript: str,
        evaluation_focus: List[str]
    ) -> Dict[str, float]:
        """Use LLM to evaluate response holistically"""
        import httpx

        # Build evaluation prompt
        focus_str = ", ".join(evaluation_focus)
        prompt = f"""Evaluate the following interview response on these dimensions: {focus_str}

Question: {question.get('text', 'N/A')}
Expected Focus: {focus_str}

Candidate Response:
{transcript}

Rate each dimension on a scale of 0-10, where:
- 0-3: Poor - Does not meet expectations
- 4-6: Adequate - Meets basic expectations
- 7-8: Good - Exceeds expectations
- 9-10: Excellent - Significantly exceeds expectations

Respond with ONLY a JSON object in this format:
{{
    "dimension_name": score,
    ...
}}

Example: {{"fluency": 7.5, "vocabulary": 8.0, "grammar": 6.5}}"""

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
                        "max_tokens": 200,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    content = result["content"][0]["text"]

                    # Parse JSON from response
                    try:
                        # Extract JSON from response (may have markdown formatting)
                        json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
                        if json_match:
                            scores = json.loads(json_match.group())
                            return {k: float(v) for k, v in scores.items()}
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            print(f"LLM evaluation error: {e}")

        # Fallback: return None for LLM scores
        return {}

    def _calculate_overall_score(
        self,
        scores: Dict[str, Any],
        evaluation_focus: Optional[List[str]] = None
    ) -> float:
        """Calculate weighted overall score"""
        weights = {
            "automated": 0.2,
            "grammar": 0.25,
            "vocabulary": 0.25,
            "llm": 0.3
        }

        total = 0
        total_weight = 0

        # Automated metrics score (normalize to 0-10)
        automated = scores.get("automated", {})
        if automated:
            # Score based on speaking rate and lexical diversity
            rate_score = min(10, automated.get("speaking_rate_wpm", 0) / 15)  # Target 150 wpm
            diversity_score = automated.get("lexical_diversity", 0) * 10
            auto_score = (rate_score + diversity_score) / 2
            total += auto_score * weights["automated"]
            total_weight += weights["automated"]

        # Grammar score
        grammar = scores.get("grammar", {})
        if grammar:
            total += grammar.get("score", 0) * weights["grammar"]
            total_weight += weights["grammar"]

        # Vocabulary score
        vocabulary = scores.get("vocabulary", {})
        if vocabulary:
            total += vocabulary.get("score", 0) * weights["vocabulary"]
            total_weight += weights["vocabulary"]

        # LLM score
        llm = scores.get("llm", {})
        if llm:
            llm_avg = sum(llm.values()) / len(llm) if llm else 0
            total += llm_avg * weights["llm"]
            total_weight += weights["llm"]

        return round(total / total_weight, 2) if total_weight > 0 else 0

    async def evaluate_interview_session(
        self,
        questions: List[Dict[str, Any]],
        responses: List[Dict[str, Any]],
        dimension_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate an entire interview session
        Aggregates individual response scores into dimension scores
        """
        dimension_totals = {
            "english_proficiency": {"scores": [], "weights": []},
            "industry_understanding": {"scores": [], "weights": []},
            "professional_skills": {"scores": [], "weights": []},
            "soft_skills": {"scores": [], "weights": []}
        }

        # Evaluate each response
        for i, response in enumerate(responses):
            if i >= len(questions):
                break

            question = questions[i]
            evaluation = await self.evaluate_response(
                question=question,
                transcript=response.get("transcript", ""),
                audio_duration=response.get("audio_duration"),
                evaluation_focus=question.get("evaluation_focus", [])
            )

            # Categorize by question type/section
            question_type = question.get("type", "")
            section = self._map_question_type_to_dimension(question_type)

            if section in dimension_totals:
                dimension_totals[section]["scores"].append(evaluation["overall_score"])
                dimension_totals[section]["weights"].append(question.get("weight", 1.0))

        # Calculate dimension averages
        dimension_scores = {}
        for dimension, data in dimension_totals.items():
            if data["scores"]:
                weighted_sum = sum(s * w for s, w in zip(data["scores"], data["weights"]))
                total_weight = sum(data["weights"])
                dimension_scores[dimension] = round(weighted_sum / total_weight, 2) if total_weight > 0 else 0
            else:
                dimension_scores[dimension] = 0

        # Calculate overall score
        overall = sum(dimension_scores.values()) / len(dimension_scores) if dimension_scores else 0

        return {
            "overall_score": round(overall, 2),
            "dimension_scores": dimension_scores,
            "total_questions": len(responses),
            "evaluated_questions": len([r for r in responses if r.get("transcript")])
        }

    def _map_question_type_to_dimension(self, question_type: str) -> str:
        """Map question type to evaluation dimension"""
        mapping = {
            "fluency": "english_proficiency",
            "vocabulary": "english_proficiency",
            "grammar": "english_proficiency",
            "comprehension": "english_proficiency",
            "scenario": "english_proficiency",
            "market_knowledge": "industry_understanding",
            "competitor_awareness": "industry_understanding",
            "regulatory_knowledge": "industry_understanding",
            "innovation_awareness": "industry_understanding",
            "technical_competency": "professional_skills",
            "problem_solving": "professional_skills",
            "domain_expertise": "professional_skills",
            "tool_proficiency": "professional_skills",
            "communication": "soft_skills",
            "teamwork": "soft_skills",
            "leadership": "soft_skills",
            "adaptability": "soft_skills",
            "emotional_intelligence": "soft_skills"
        }
        return mapping.get(question_type, "english_proficiency")


# Global scoring service instance
scoring_service = ScoringService()
