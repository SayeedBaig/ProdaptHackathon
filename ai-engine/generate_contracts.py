import os
import json
from app.schemas.common import StartupIdeaInput
from app.schemas.idea_analysis import IdeaAnalysisRequest
from app.schemas.clarification_questions import ClarificationQuestionsRequest
from app.schemas.value_prop import ValuePropRequest
from app.schemas.market_analysis import MarketAnalysisRequest
from app.schemas.pitch_deck import PitchGenerationRequest
from app.schemas.pitch_critique import PitchCritiqueRequest
from app.schemas.investor_questions import InvestorQuestionsRequest
from app.schemas.answer_evaluation import AnswerEvaluationRequest
from app.schemas.readiness_report import ReadinessReportRequest
from app.schemas.full_pipeline import FullPipelineRequest
from app.services.pitch_coach_service import pitch_coach_service

OUTPUT_DIR = "contracts"

def export_contracts():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    sample_idea = StartupIdeaInput(
        title="PitchCoach AI",
        raw_description="An AI startup coach that helps users refine ideas, generate pitch decks, define value propositions, analyze market opportunities, and practice investor Q&A.",
        target_industry="AI & Enterprise SaaS",
        stage="Pre-Seed",
        location="Global"
    )

    contracts = {
        "idea_analysis_sample.json": pitch_coach_service.analyze_idea(IdeaAnalysisRequest(startup_info=sample_idea)).model_dump(),
        "clarification_questions_sample.json": pitch_coach_service.generate_clarification_questions(ClarificationQuestionsRequest(startup_info=sample_idea)).model_dump(),
        "value_proposition_sample.json": pitch_coach_service.generate_value_proposition(ValuePropRequest(startup_info=sample_idea)).model_dump(),
        "market_analysis_sample.json": pitch_coach_service.analyze_market(MarketAnalysisRequest(startup_info=sample_idea)).model_dump(),
        "pitch_generation_sample.json": pitch_coach_service.generate_pitch(PitchGenerationRequest(startup_info=sample_idea)).model_dump(),
        "pitch_critique_sample.json": pitch_coach_service.critique_pitch(PitchCritiqueRequest()).model_dump(),
        "investor_questions_sample.json": pitch_coach_service.generate_investor_questions(InvestorQuestionsRequest(startup_info=sample_idea)).model_dump(),
        "answer_evaluation_sample.json": pitch_coach_service.evaluate_answer(AnswerEvaluationRequest(
            question="What is your projected CAC and payback window?",
            user_answer="We don't know CAC yet, but we will run social ads."
        )).model_dump(),
        "readiness_report_sample.json": pitch_coach_service.generate_readiness_report(ReadinessReportRequest(startup_info=sample_idea)).model_dump(),
        "full_pipeline_sample.json": pitch_coach_service.run_full_pipeline(FullPipelineRequest(startup_info=sample_idea)).model_dump(),
    }

    for filename, data in contracts.items():
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Generated contract sample: {filepath}")

if __name__ == "__main__":
    export_contracts()
