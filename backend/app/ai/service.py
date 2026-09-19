from typing import Any, Protocol
from .runner import run
from . import schemas

class AIService(Protocol):
    async def analyze_idea(self, ctx: Any) -> schemas.IdeaAnalysis: ...
    async def generate_clarification_question(self, ctx: Any) -> schemas.ClarificationQuestion: ...
    async def extract_profile_patch(self, ctx: Any, question: str, answer: str) -> schemas.ProfilePatch: ...
    async def generate_value_proposition(self, ctx: Any) -> schemas.ValueProposition: ...
    async def analyze_competitors(self, ctx: Any, evidence: Any) -> schemas.CompetitorAnalysis: ...
    async def analyze_market(self, ctx: Any, evidence: Any) -> schemas.MarketAnalysis: ...
    async def analyze_business_model(self, ctx: Any) -> schemas.BusinessModelAnalysis: ...
    async def generate_pitch(self, ctx: Any, prior_critique: Any = None) -> schemas.Pitch: ...
    async def critique_pitch(self, ctx: Any, pitch: Any) -> schemas.PitchCritique: ...
    async def generate_investor_question(self, ctx: Any, intent: str, topic: str, prev_turn: Any = None) -> schemas.InvestorQuestion: ...
    async def evaluate_answer(self, ctx: Any, turn: Any) -> schemas.AnswerEvaluation: ...
    async def generate_readiness_narrative(self, ctx: Any, turns: Any, computed_scores: Any) -> schemas.ReadinessNarrative: ...
    async def extract_feedback_patches(self, ctx: Any, report: Any) -> list[schemas.FeedbackItemDraft]: ...

class AIServiceImpl:
    async def analyze_idea(self, ctx: Any) -> schemas.IdeaAnalysis:
        return await run("analyze_idea", ctx, schemas.IdeaAnalysis)

    async def generate_clarification_question(self, ctx: Any) -> schemas.ClarificationQuestion:
        return await run("generate_clarification_question", ctx, schemas.ClarificationQuestion)

    async def extract_profile_patch(self, ctx: Any, question: str, answer: str) -> schemas.ProfilePatch:
        return await run("extract_profile_patch", ctx, schemas.ProfilePatch)

    async def generate_value_proposition(self, ctx: Any) -> schemas.ValueProposition:
        return await run("generate_value_proposition", ctx, schemas.ValueProposition)

    async def analyze_competitors(self, ctx: Any, evidence: Any) -> schemas.CompetitorAnalysis:
        return await run("analyze_competitors", ctx, schemas.CompetitorAnalysis)

    async def analyze_market(self, ctx: Any, evidence: Any) -> schemas.MarketAnalysis:
        return await run("analyze_market", ctx, schemas.MarketAnalysis)

    async def analyze_business_model(self, ctx: Any) -> schemas.BusinessModelAnalysis:
        return await run("analyze_business_model", ctx, schemas.BusinessModelAnalysis)

    async def generate_pitch(self, ctx: Any, prior_critique: Any = None) -> schemas.Pitch:
        return await run("generate_pitch", ctx, schemas.Pitch)

    async def critique_pitch(self, ctx: Any, pitch: Any) -> schemas.PitchCritique:
        return await run("critique_pitch", ctx, schemas.PitchCritique)

    async def generate_investor_question(self, ctx: Any, intent: str, topic: str, prev_turn: Any = None) -> schemas.InvestorQuestion:
        return await run("generate_investor_question", ctx, schemas.InvestorQuestion)

    async def evaluate_answer(self, ctx: Any, turn: Any) -> schemas.AnswerEvaluation:
        return await run("evaluate_answer", ctx, schemas.AnswerEvaluation)

    async def generate_readiness_narrative(self, ctx: Any, turns: Any, computed_scores: Any) -> schemas.ReadinessNarrative:
        return await run("generate_readiness_narrative", ctx, schemas.ReadinessNarrative)

    async def extract_feedback_patches(self, ctx: Any, report: Any) -> list[schemas.FeedbackItemDraft]:
        # Note: the schema defines returning a list. Run returns a single model usually.
        # We might need a wrapper model for a list of patches, but we'll adapt this later.
        pass

def get_ai_service() -> AIService:
    return AIServiceImpl()
