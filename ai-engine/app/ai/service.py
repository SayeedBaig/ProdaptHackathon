"""
AIService — The complete AI facade for PitchPilot AI.

Exposes all 13 capabilities as clean methods.
Each method:
  1. Projects the StartupProfile to a focused context string via ContextBuilder.
  2. Selects the prompt config from PROMPTS dict.
  3. Delegates to ai_runner.run() for retry/repair/fallback.
  4. Wraps the result in SuccessEnvelope with ResponseMeta.

Import:
    from app.ai.service import ai_service
"""
from __future__ import annotations

import time
from typing import Any

from app.ai.context import context_builder
from app.ai.prompts.prompts import PROMPTS
from app.ai.runner import ai_runner
from app.ai.schemas.common import (
    ResponseMeta,
    SuccessEnvelope,
    StartupProfile,
)
from app.ai.schemas.idea import IdeaAnalysis
from app.ai.schemas.clarification import ClarificationQuestion, ProfilePatch
from app.ai.schemas.value_prop import ValueProposition
from app.ai.schemas.competitors import CompetitorAnalysis
from app.ai.schemas.market import MarketAnalysis
from app.ai.schemas.business_model import BusinessModelAnalysis
from app.ai.schemas.pitch import Pitch
from app.ai.schemas.critique import PitchCritique
from app.ai.schemas.investor import InvestorQuestion
from app.ai.schemas.evaluation import AnswerEvaluation
from app.ai.schemas.narrative import ReadinessNarrative
from app.ai.schemas.feedback import FeedbackDraftList


class AIService:
    """
    Single-entry-point facade for all AI capabilities.

    Usage:
        result = ai_service.analyze_idea(profile)
        # result.data  → IdeaAnalysis
        # result.meta  → ResponseMeta (ai_mode, model, ms, warnings…)
    """

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    def _call(
        self,
        capability: str,
        user_context: str,
        response_model,
    ) -> SuccessEnvelope:
        cfg = PROMPTS.get(capability, {"system": "", "temperature": 0.3})
        system: str = cfg["system"]
        temperature: float = cfg.get("temperature", 0.3)

        parsed, pr = ai_runner.run(
            capability=capability,
            system=system,
            user=user_context,
            response_model=response_model,
            temperature=temperature,
        )

        meta = ResponseMeta(
            ai_mode=pr.ai_mode,
            model=pr.model,
            degraded=pr.degraded,
            warnings=pr.warnings,
            processing_time_ms=pr.processing_time_ms,
        )
        return SuccessEnvelope(data=parsed, meta=meta)

    # ------------------------------------------------------------------
    # 1. Idea Analysis
    # ------------------------------------------------------------------

    def analyze_idea(self, profile: StartupProfile) -> SuccessEnvelope[IdeaAnalysis]:
        """
        Decompose a raw startup idea into problem, customer, solution,
        assumptions, risks, gaps, and a first follow-up question.
        """
        user = context_builder.project_for_idea_analysis(profile)
        return self._call("analyze_idea", user, IdeaAnalysis)

    # ------------------------------------------------------------------
    # 2. Clarification Question
    # ------------------------------------------------------------------

    def generate_clarification_question(
        self,
        profile: StartupProfile,
        previous_questions: list[str] | None = None,
    ) -> SuccessEnvelope[ClarificationQuestion]:
        """
        Generate one targeted clarification question for the highest
        severity open gap in the profile.
        """
        user = context_builder.project_for_clarification(profile, previous_questions)
        return self._call("generate_clarification_question", user, ClarificationQuestion)

    # ------------------------------------------------------------------
    # 3. Extract Profile Patch (from founder answer)
    # ------------------------------------------------------------------

    def extract_profile_patch(
        self,
        profile: StartupProfile,
        question: str,
        answer: str,
    ) -> SuccessEnvelope[ProfilePatch]:
        """
        Parse the founder's free-text answer and extract structured
        JSON patch operations to update the StartupProfile.
        """
        user = context_builder.project_for_patch_extraction(profile, question, answer)
        return self._call("extract_profile_patch", user, ProfilePatch)

    # ------------------------------------------------------------------
    # 4. Value Proposition
    # ------------------------------------------------------------------

    def generate_value_proposition(
        self, profile: StartupProfile
    ) -> SuccessEnvelope[ValueProposition]:
        """
        Generate a Geoff Moore value prop, 30-second elevator pitch,
        USP list, and pain-relief matrix.
        """
        user = context_builder.project_for_value_prop(profile)
        return self._call("generate_value_proposition", user, ValueProposition)

    # ------------------------------------------------------------------
    # 5. Competitor Analysis
    # ------------------------------------------------------------------

    def analyze_competitors(
        self,
        profile: StartupProfile,
        evidence_snippets: list[dict] | None = None,
    ) -> SuccessEnvelope[CompetitorAnalysis]:
        """
        Map direct/indirect competitors, their strengths, weaknesses,
        and differentiation angles — grounded in evidence snippets when available.
        """
        user = context_builder.project_for_competitors(profile, evidence_snippets)
        return self._call("analyze_competitors", user, CompetitorAnalysis)

    # ------------------------------------------------------------------
    # 6. Market Analysis
    # ------------------------------------------------------------------

    def analyze_market(
        self,
        profile: StartupProfile,
        evidence_snippets: list[dict] | None = None,
    ) -> SuccessEnvelope[MarketAnalysis]:
        """
        Derive TAM/SAM/SOM, market segments, opportunities, and threats
        from the profile and optional evidence.
        """
        user = context_builder.project_for_market(profile, evidence_snippets)
        return self._call("analyze_market", user, MarketAnalysis)

    # ------------------------------------------------------------------
    # 7. Business Model Analysis
    # ------------------------------------------------------------------

    def analyze_business_model(
        self, profile: StartupProfile
    ) -> SuccessEnvelope[BusinessModelAnalysis]:
        """
        Extract monetization model, pricing structure, cost drivers,
        GTM strategy, and missing unit-economic assumptions.
        """
        user = context_builder.project_for_business_model(profile)
        return self._call("analyze_business_model", user, BusinessModelAnalysis)

    # ------------------------------------------------------------------
    # 8. Pitch Generation
    # ------------------------------------------------------------------

    def generate_pitch(
        self,
        profile: StartupProfile,
        market_analysis: dict | None = None,
        competitor_analysis: dict | None = None,
    ) -> SuccessEnvelope[Pitch]:
        """
        Generate slide-by-slide pitch deck content (bullets, visual ideas,
        speaker notes) and 30s / 2min / 5min pitch scripts.
        """
        user = context_builder.project_for_pitch(profile, market_analysis, competitor_analysis)
        return self._call("generate_pitch", user, Pitch)

    # ------------------------------------------------------------------
    # 9. Pitch Critique
    # ------------------------------------------------------------------

    def critique_pitch(
        self,
        profile: StartupProfile,
        pitch: Pitch,
    ) -> SuccessEnvelope[PitchCritique]:
        """
        Critique the pitch for clarity, persuasion, investor objections,
        and return prioritised issues with recommendations.
        """
        pitch_json = pitch.model_dump_json(indent=2)
        user = f"Startup Profile:\n{context_builder.project_for_pitch(profile)}\n\nPitch JSON:\n{pitch_json}"
        return self._call("critique_pitch", user, PitchCritique)

    # ------------------------------------------------------------------
    # 10. Investor Question
    # ------------------------------------------------------------------

    def generate_investor_question(
        self,
        profile: StartupProfile,
        intent: str,
        topic: str,
        prev_turn: dict | None = None,
    ) -> SuccessEnvelope[InvestorQuestion]:
        """
        Act as a seasoned VC investor.
        Generate a sharp, realistic question for the assigned topic and intent.
        """
        user = context_builder.project_for_investor_question(profile, intent, topic, prev_turn)
        return self._call("generate_investor_question", user, InvestorQuestion)

    # ------------------------------------------------------------------
    # 11. Answer Evaluation
    # ------------------------------------------------------------------

    def evaluate_answer(
        self,
        profile: StartupProfile,
        question: str,
        user_answer: str,
    ) -> SuccessEnvelope[AnswerEvaluation]:
        """
        Grade the founder's answer across 6 criteria (0-10) and produce
        constructive feedback plus a model response.
        """
        user = context_builder.project_for_answer_eval(profile, question, user_answer)
        return self._call("evaluate_answer", user, AnswerEvaluation)

    # ------------------------------------------------------------------
    # 12. Readiness Narrative
    # ------------------------------------------------------------------

    def generate_readiness_narrative(
        self,
        profile: StartupProfile,
        dimension_scores: dict[str, float],
    ) -> SuccessEnvelope[ReadinessNarrative]:
        """
        Synthesise an executive readiness narrative explaining strengths
        and gaps based on dimension scores.
        """
        score_lines = "\n".join(
            f"- {dim}: {score}/10" for dim, score in dimension_scores.items()
        )
        user = (
            f"Startup: {profile.identity.startup_name}\n"
            f"Dimension Scores:\n{score_lines}\n"
            f"Problem: {profile.problem.statement or 'Not provided'}\n"
            f"Solution: {profile.solution.description or 'Not provided'}"
        )
        return self._call("generate_readiness_narrative", user, ReadinessNarrative)

    # ------------------------------------------------------------------
    # 13. Extract Feedback Patches
    # ------------------------------------------------------------------

    def extract_feedback_patches(
        self,
        profile: StartupProfile,
        narrative: ReadinessNarrative,
    ) -> SuccessEnvelope[FeedbackDraftList]:
        """
        Extract actionable feedback items with suggested profile patches
        from the readiness narrative.
        """
        user = (
            f"Startup: {profile.identity.startup_name}\n"
            f"Readiness Summary: {narrative.summary}\n"
            f"Top Gaps:\n" + "\n".join(f"- {g}" for g in narrative.top_gaps)
        )
        return self._call("extract_feedback_patches", user, FeedbackDraftList)


# Singleton — import this everywhere
ai_service = AIService()
