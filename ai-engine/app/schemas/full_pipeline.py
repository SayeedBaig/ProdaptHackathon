from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.common import StartupIdeaInput
from app.schemas.idea_analysis import IdeaAnalysisResponse
from app.schemas.clarification_questions import ClarificationQuestionsResponse
from app.schemas.value_prop import ValuePropositionResponse
from app.schemas.market_analysis import MarketAnalysisResponse
from app.schemas.pitch_deck import PitchGenerationResponse
from app.schemas.pitch_critique import PitchCritiqueResponse
from app.schemas.investor_questions import InvestorQuestionsResponse
from app.schemas.readiness_report import ReadinessReportResponse

class FullPipelineRequest(BaseModel):
    startup_info: StartupIdeaInput

class FullPipelineResponse(BaseModel):
    idea_analysis: IdeaAnalysisResponse
    clarification_questions: ClarificationQuestionsResponse
    value_proposition: ValuePropositionResponse
    market_analysis: MarketAnalysisResponse
    pitch_deck: PitchGenerationResponse
    pitch_critique: PitchCritiqueResponse
    investor_questions: InvestorQuestionsResponse
    readiness_report: ReadinessReportResponse
