import json
import os
import uuid
from typing import Any
from app.ai.schemas.capabilities import (
    IdeaAnalysis,
    ClarificationQuestion,
    ProfilePatch,
    ProfilePatchOp,
    SlideContent,
    Pitch,
    PitchCritique,
    InvestorQuestion,
    AnswerEvaluation,
)
from app.core.config import settings

FIXTURES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "ai", "fixtures"))

def load_fixture(capability_name: str) -> dict[str, Any]:
    file_path = os.path.join(FIXTURES_DIR, f"{capability_name}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data and isinstance(data, dict) and len(data) > 0:
                    return data
        except Exception:
            pass
    return {}

class MockAIService:
    """Mock AI Service that satisfies all 13 capabilities with high quality fixtures.
    Allows backend and frontend development in parallel without blocking on external LLM APIs.
    """

    async def analyze_idea(self, ctx: dict[str, Any]) -> IdeaAnalysis:
        fixture = load_fixture("analyze_idea")
        if fixture:
            return IdeaAnalysis.model_validate(fixture)
        
        name = ctx.get("identity", {}).get("startup_name", "NutriNest")
        idea = ctx.get("identity", {}).get("raw_idea", "Affordable healthy meals for students")
        return IdeaAnalysis(
            problem="College students struggle to find affordable, healthy meal options near campus.",
            target_customer="Hostel-dwelling college students",
            solution="A student-focused platform aggregating verified healthy meal prep providers with flexible subscriptions.",
            pain_points=[
                "Hostel mess food is low quality and repetitive",
                "Swiggy/Zomato orders are too expensive for daily student budgets",
                "Lack of nutritional information on street food options",
            ],
            assumptions=[
                "Students are willing to switch from irregular ordering to a meal subscription",
                "Local kitchens can maintain quality at low price points",
            ],
            risks=[
                "Incumbent food delivery platforms can introduce student discounts or healthy food tags",
                "High churn during semester breaks",
            ],
            missing_information=[
                "Specific target price per meal",
                "Evidence of student willingness to pay",
                "Kitchen onboarding pipeline",
            ],
            first_question={
                "id": str(uuid.uuid4()),
                "text": "Which specific student segment are you targeting initially, and what is their daily food budget?",
                "target_field": "customer.primary_segment",
            },
        )

    async def generate_clarification_question(self, ctx: dict[str, Any]) -> ClarificationQuestion:
        fixture = load_fixture("generate_clarification_question")
        if fixture:
            return ClarificationQuestion.model_validate(fixture)

        # Check what fields are missing in ctx
        customer = ctx.get("customer", {}).get("primary_segment")
        problem = ctx.get("problem", {}).get("statement")
        
        if not customer:
            return ClarificationQuestion(
                id=str(uuid.uuid4()),
                text="Which specific student demographic (e.g. hostellers, off-campus renters) will you launch with?",
                target_field="customer.primary_segment",
            )
        elif not problem:
            return ClarificationQuestion(
                id=str(uuid.uuid4()),
                text="What is the single biggest pain point hostellers face with current food alternatives?",
                target_field="problem.statement",
            )
        else:
            return ClarificationQuestion(
                id=str(uuid.uuid4()),
                text="How do you plan to keep the unit meal cost under 80 INR while maintaining kitchen margins?",
                target_field="business_model.pricing",
            )

    async def extract_profile_patch(self, ctx: dict[str, Any], question: str, answer: str) -> ProfilePatch:
        fixture = load_fixture("extract_profile_patch")
        if fixture:
            return ProfilePatch.model_validate(fixture)

        lower_ans = answer.lower()
        ops = []
        if "hostel" in lower_ans or "student" in lower_ans:
            ops.append(ProfilePatchOp(
                op="set",
                path="customer.primary_segment",
                value="Hostel-dwelling undergraduate students",
                reason="Extracted from founder clarification answer",
            ))
        if "cook" in lower_ans or "expensive" in lower_ans or "unhealthy" in lower_ans:
            ops.append(ProfilePatchOp(
                op="set",
                path="problem.statement",
                value=answer,
                reason="Extracted from founder clarification answer",
            ))
        if not ops:
            ops.append(ProfilePatchOp(
                op="set",
                path="problem.statement",
                value=answer,
                reason="Founder clarification input",
            ))
        return ProfilePatch(ops=ops)

    async def generate_value_proposition(self, ctx: dict[str, Any]) -> dict[str, Any]:
        fixture = load_fixture("generate_value_proposition")
        if fixture:
            return fixture

        return {
            "one_line": "Guaranteed healthy, student-budget meal subscriptions tailored for hostel living.",
            "elevator": "For hostel students tired of repetitive mess food and expensive delivery apps, NutriNest offers verified, nutritionist-approved daily meal plans under ₹79/meal delivered right to campus.",
            "pain_points": [
                "Unhealthy campus dining",
                "High Swiggy/Zomato delivery fees",
                "Zero nutritional visibility",
            ],
            "differentiators": [
                "Strict sub-₹80 pricing model",
                "Direct campus hostel batch deliveries (zero delivery charge)",
                "Nutrient tracking synced with student lifestyle",
            ],
            "competitive_advantage": "Batch delivery routing to designated hostel pickup points cuts logistics costs by 65%.",
        }

    async def analyze_competitors(self, ctx: dict[str, Any], evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        fixture = load_fixture("analyze_competitors")
        if fixture:
            return fixture

        return {
            "competitors": [
                {
                    "name": "Swiggy / Zomato",
                    "description": "General food delivery aggregator giants.",
                    "differentiation": "Massive variety, but exorbitant delivery fees and minimum order values make daily meals unaffordable for students.",
                    "strengths": ["Brand dominance", "Restaurant coverage", "Fast delivery"],
                    "weaknesses": ["High per-order commission", "Expensive for daily use", "No healthy student focus"],
                    "provenance": "source_backed",
                },
                {
                    "name": "Hostel Mess Facilities",
                    "description": "On-campus institutional food services.",
                    "differentiation": "Included in hostel fees, but notorious for poor nutritional quality and repetitive menus.",
                    "strengths": ["Convenient location", "Extremely low apparent cost"],
                    "weaknesses": ["Low quality ingredients", "Fixed timings", "Zero student customization"],
                    "provenance": "founder_assumption",
                },
            ]
        }

    async def analyze_market(self, ctx: dict[str, Any], evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        fixture = load_fixture("analyze_market")
        if fixture:
            return fixture

        return {
            "research_status": "ok",
            "segments": [
                {"name": "Hostel undergraduate students", "provenance": "founder_assumption"},
                {"name": "Private PG college residents", "provenance": "ai_analysis"},
            ],
            "competitors": [
                {"name": "Swiggy Daily (discontinued)", "difference": "Focused on corporate offices rather than campus clusters", "provenance": "source_backed"},
            ],
            "opportunities": [
                {"text": "High student density in campus hubs allows scheduled batch drop-offs", "provenance": "ai_analysis"}
            ],
            "threats": [
                {"text": "Aggregators introducing dedicated student meal discounts", "provenance": "ai_analysis"}
            ],
            "market_size": {
                "tam": None,
                "sam": None,
                "som": None,
                "status": "Requires validation",
                "calculation": None,
            },
            "evidence": [
                {
                    "id": "e1",
                    "title": "Indian Higher Education Student Housing & Food Survey",
                    "url": "https://example.com/student-housing-report",
                    "snippet": "Over 4 million college students in Tier 1 & 2 cities reside in hostels and rely on third-party dining alternatives.",
                }
            ],
        }

    async def analyze_business_model(self, ctx: dict[str, Any]) -> dict[str, Any]:
        fixture = load_fixture("analyze_business_model")
        if fixture:
            return fixture

        return {
            "type": "B2C Subscription & Marketplace Commission",
            "customer": "Hostel students seeking daily dinner/lunch",
            "payer": "Student / Parents",
            "revenue_source": "15% platform commission on meal subscriptions + premium nutrition add-ons",
            "pricing": "Requires validation (suggested: ₹1,800 - ₹2,400 monthly subscription for 30 meals)",
            "costs": "Requires validation (partner kitchen acquisition, campus ambassador stipends, customer support)",
            "go_to_market": "Campus ambassador network and hostel orientation partnerships",
            "missing_assumptions": [
                "Kitchen margin acceptance at sub-₹70 vendor payout",
                "Student renewal rate after month 1",
            ],
        }

    async def generate_pitch(self, ctx: dict[str, Any], prior_critique: dict[str, Any] | None = None) -> Pitch:
        fixture = load_fixture("generate_pitch")
        if fixture:
            return Pitch.model_validate(fixture)

        return Pitch(
            slides=[
                SlideContent(
                    key="problem",
                    title="The Campus Food Crisis",
                    bullets=[
                        "Hostel mess food fails on nutrition, hygiene, and taste.",
                        "Commercial delivery apps charge ₹150+ per meal with delivery overheads.",
                        "4M+ hostel students compromise their health daily due to budget constraints.",
                    ],
                    status="complete",
                ),
                SlideContent(
                    key="solution",
                    title="NutriNest: Smart Student Meal Subscriptions",
                    bullets=[
                        "Curated healthy meals prepared by certified local cloud kitchens.",
                        "Strict sub-₹79 pricing per meal with zero individual delivery fees.",
                        "Batch delivery directly to campus hostel gates twice daily.",
                    ],
                    status="complete",
                ),
                SlideContent(
                    key="target_market",
                    title="Target Market",
                    bullets=[
                        "Initial target: 45,000 hostel students across 12 university campuses in Pune/Bangalore.",
                        "Secondary expansion: Off-campus PG clusters and junior colleges.",
                        "Total Addressable Market requires on-ground validation.",
                    ],
                    status="complete",
                ),
                SlideContent(
                    key="traction",
                    title="Early Validation & Traction",
                    bullets=[
                        "Not provided — requires validation",
                    ],
                    status="needs_input",
                ),
                SlideContent(
                    key="ask",
                    title="Funding & Next Milestones",
                    bullets=[
                        "Not provided — requires validation",
                    ],
                    status="needs_input",
                ),
            ]
        )

    async def critique_pitch(self, ctx: dict[str, Any], pitch: dict[str, Any]) -> PitchCritique:
        fixture = load_fixture("critique_pitch")
        if fixture:
            return PitchCritique.model_validate(fixture)

        return PitchCritique(
            issues=[
                {
                    "topic": "differentiation",
                    "severity": "high",
                    "text": "Existing food delivery apps can easily replicate healthy tags or subsidized delivery zones.",
                    "recommendation": "Articulate defensibility via exclusive cloud kitchen contracts or on-campus distribution partnerships.",
                },
                {
                    "topic": "validation",
                    "severity": "high",
                    "text": "Zero traction numbers or user interviews documented in the profile.",
                    "recommendation": "Interview at least 30-50 target students to confirm willingness to commit to prepaid weekly subscriptions.",
                },
            ],
            investor_objections=[
                "Why won't Swiggy or Zomato crush you by launching student-discounted meal boxes?",
                "How will you maintain food quality and hygiene across decentralized partner kitchens?",
            ],
            top_priorities=[
                "Validate student willingness to pay upfront",
                "Establish kitchen unit economics and hygiene checks",
            ],
        )

    async def generate_investor_question(
        self,
        ctx: dict[str, Any],
        intent: str,
        topic: str,
        prev_turn: dict[str, Any] | None = None,
    ) -> InvestorQuestion:
        fixture = load_fixture("generate_investor_question")
        if fixture:
            return InvestorQuestion.model_validate(fixture)

        if intent == "follow_up" and prev_turn:
            return InvestorQuestion(
                id=str(uuid.uuid4()),
                intent=intent,
                topic=topic,
                text=f"Regarding your earlier point: you mentioned your pricing is lower, but what concrete evidence or customer interview data proves students will commit to an upfront subscription rather than order ad-hoc?",
            )
        elif topic == "differentiation":
            return InvestorQuestion(
                id=str(uuid.uuid4()),
                intent=intent,
                topic=topic,
                text="What prevents Swiggy or Zomato from introducing a student filter with clustered batch delivery to your campus next month?",
            )
        else:
            return InvestorQuestion(
                id=str(uuid.uuid4()),
                intent=intent,
                topic=topic,
                text="Walk me through your kitchen unit economics: at ₹79 per meal, what is the food cost, delivery cost, and platform margin?",
            )

    async def evaluate_answer(self, ctx: dict[str, Any], turn: dict[str, Any]) -> AnswerEvaluation:
        fixture = load_fixture("evaluate_answer")
        if fixture:
            return AnswerEvaluation.model_validate(fixture)

        ans = turn.get("answer", "")
        # Score realistically based on detail
        has_numbers = any(char.isdigit() for char in ans)
        has_evidence = "interview" in ans.lower() or "tested" in ans.lower() or "spoke" in ans.lower()

        scores = {
            "clarity": 8 if len(ans) > 20 else 5,
            "specificity": 7 if has_numbers else 4,
            "evidence": 8 if has_evidence else 3,
            "business_reasoning": 6,
            "differentiation": 5,
            "scalability": 6,
        }

        return AnswerEvaluation(
            scores=scores,
            explanation="The answer demonstrates a clear understanding of the customer problem, but lacks hard validation data and defensibility mechanisms.",
            strengths=[
                "Direct address of the student budget constraint",
                "Clear recognition of the hostel convenience factor",
            ],
            weaknesses=[
                "No empirical evidence or pilot data presented",
                "Weak barrier to entry against large aggregators",
            ],
            recommended_improvement="Cite specific pilot feedback, number of students surveyed, or secured kitchen agreements to prove demand.",
            weakest_criterion="evidence" if not has_evidence else "differentiation",
            claims_made=[ans],
            follow_up_question="Do you have any customer waitlist or pilot order numbers to substantiate this?",
        )

    async def generate_readiness_narrative(
        self,
        ctx: dict[str, Any],
        turns: list[dict[str, Any]],
        computed_scores: dict[str, Any],
    ) -> dict[str, Any]:
        fixture = load_fixture("generate_readiness_narrative")
        if fixture:
            return fixture

        return {
            "summary": "NutriNest exhibits strong problem clarity and an intuitive value proposition, but requires immediate empirical customer validation and margin stress-testing.",
            "why": {
                "customer_validation": "Willingness to prepay for subscriptions remains unverified by empirical pilot data.",
                "differentiation": "Defensibility against incumbent aggregators relies heavily on execution rather than proprietary moats.",
            },
            "top_gaps": [
                "Unvalidated unit economics per meal",
                "Absence of recorded student customer interviews",
            ],
            "disclaimer": "Coaching metrics designed for iterative improvement; not a prediction of venture success.",
        }

    async def extract_feedback_patches(self, ctx: dict[str, Any], report: dict[str, Any]) -> list[dict[str, Any]]:
        fixture = load_fixture("extract_feedback_patches")
        if fixture and isinstance(fixture, list):
            return fixture

        return [
            {
                "topic": "validation",
                "title": "Conduct Student Demand Interviews",
                "recommendation": "Interview at least 30-50 hostel students to validate price ceiling and subscription commitment.",
                "suggested_patch": [
                    {"op": "set", "path": "traction.interviews", "value": "50 students interviewed"},
                    {"op": "set", "path": "traction.interested", "value": "35 willing to prepay"},
                ],
            },
            {
                "topic": "business_model",
                "title": "Lock Partner Kitchen Unit Economics",
                "recommendation": "Secure pilot contracts with 2 cloud kitchens agreeing to ₹55 production cost per meal.",
                "suggested_patch": [
                    {"op": "set", "path": "business_model.costs", "value": "₹55 food prep + ₹8 campus batch distribution"},
                    {"op": "set", "path": "business_model.pricing", "value": "₹79 per meal subscription"},
                ],
            },
        ]

_ai_service_instance = MockAIService()

def get_ai_service() -> MockAIService:
    return _ai_service_instance
