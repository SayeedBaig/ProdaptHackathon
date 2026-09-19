import time
from fastapi import APIRouter, HTTPException, status
from app.schemas.common import BaseAIResponse
from app.schemas.idea_analysis import IdeaAnalysisRequest, IdeaAnalysisResponse
from app.schemas.clarification_questions import ClarificationQuestionsRequest, ClarificationQuestionsResponse
from app.schemas.value_prop import ValuePropRequest, ValuePropositionResponse
from app.schemas.market_analysis import MarketAnalysisRequest, MarketAnalysisResponse
from app.schemas.pitch_deck import PitchGenerationRequest, PitchGenerationResponse
from app.schemas.pitch_critique import PitchCritiqueRequest, PitchCritiqueResponse
from app.schemas.investor_questions import InvestorQuestionsRequest, InvestorQuestionsResponse
from app.schemas.answer_evaluation import AnswerEvaluationRequest, AnswerEvaluationResponse
from app.schemas.readiness_report import ReadinessReportRequest, ReadinessReportResponse
from app.schemas.full_pipeline import FullPipelineRequest, FullPipelineResponse
from app.services.pitch_coach_service import pitch_coach_service

router = APIRouter(prefix="/api/v1", tags=["AI Startup Pitch Coach Engine"])

@router.post("/idea-analysis", response_model=BaseAIResponse[IdeaAnalysisResponse])
async def analyze_idea_endpoint(req: IdeaAnalysisRequest):
    t0 = time.time()
    res = pitch_coach_service.analyze_idea(req)
    t1 = time.time()
    return BaseAIResponse(module="Idea Analysis", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/clarification-questions", response_model=BaseAIResponse[ClarificationQuestionsResponse])
async def clarification_questions_endpoint(req: ClarificationQuestionsRequest):
    t0 = time.time()
    res = pitch_coach_service.generate_clarification_questions(req)
    t1 = time.time()
    return BaseAIResponse(module="Clarification Questions", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/value-proposition", response_model=BaseAIResponse[ValuePropositionResponse])
async def value_proposition_endpoint(req: ValuePropRequest):
    t0 = time.time()
    res = pitch_coach_service.generate_value_proposition(req)
    t1 = time.time()
    return BaseAIResponse(module="Value Proposition", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/market-analysis", response_model=BaseAIResponse[MarketAnalysisResponse])
async def market_analysis_endpoint(req: MarketAnalysisRequest):
    t0 = time.time()
    res = pitch_coach_service.analyze_market(req)
    t1 = time.time()
    return BaseAIResponse(module="Market Analysis", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/pitch-generation", response_model=BaseAIResponse[PitchGenerationResponse])
async def pitch_generation_endpoint(req: PitchGenerationRequest):
    t0 = time.time()
    res = pitch_coach_service.generate_pitch(req)
    t1 = time.time()
    return BaseAIResponse(module="Pitch Generation", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/pitch-critique", response_model=BaseAIResponse[PitchCritiqueResponse])
async def pitch_critique_endpoint(req: PitchCritiqueRequest):
    t0 = time.time()
    res = pitch_coach_service.critique_pitch(req)
    t1 = time.time()
    return BaseAIResponse(module="Pitch Critique", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/investor-questions", response_model=BaseAIResponse[InvestorQuestionsResponse])
async def investor_questions_endpoint(req: InvestorQuestionsRequest):
    t0 = time.time()
    res = pitch_coach_service.generate_investor_questions(req)
    t1 = time.time()
    return BaseAIResponse(module="Investor Questions", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/answer-evaluation", response_model=BaseAIResponse[AnswerEvaluationResponse])
async def answer_evaluation_endpoint(req: AnswerEvaluationRequest):
    t0 = time.time()
    res = pitch_coach_service.evaluate_answer(req)
    t1 = time.time()
    return BaseAIResponse(module="Answer Evaluation", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/readiness-report", response_model=BaseAIResponse[ReadinessReportResponse])
async def readiness_report_endpoint(req: ReadinessReportRequest):
    t0 = time.time()
    res = pitch_coach_service.generate_readiness_report(req)
    t1 = time.time()
    return BaseAIResponse(module="Readiness Report", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)

@router.post("/full-pipeline", response_model=BaseAIResponse[FullPipelineResponse])
async def full_pipeline_endpoint(req: FullPipelineRequest):
    t0 = time.time()
    res = pitch_coach_service.run_full_pipeline(req)
    t1 = time.time()
    return BaseAIResponse(module="Full Coaching Pipeline", processing_time_ms=round((t1 - t0) * 1000, 2), data=res)
