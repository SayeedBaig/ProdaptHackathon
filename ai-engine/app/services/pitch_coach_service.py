from typing import Dict, Any, List
from app.schemas.common import StartupIdeaInput
from app.schemas.idea_analysis import IdeaAnalysisRequest, IdeaAnalysisResponse, RiskFactor
from app.schemas.clarification_questions import ClarificationQuestionsRequest, ClarificationQuestionsResponse, ClarificationQuestion
from app.schemas.value_prop import ValuePropRequest, ValuePropositionResponse, GeoffMooreTemplate, PainReliefItem
from app.schemas.market_analysis import MarketAnalysisRequest, MarketAnalysisResponse, MarketMetrics, Competitor
from app.schemas.pitch_deck import PitchGenerationRequest, PitchGenerationResponse, PitchSlide, PitchScriptSet
from app.schemas.pitch_critique import PitchCritiqueRequest, PitchCritiqueResponse, SlideCritique
from app.schemas.investor_questions import InvestorQuestionsRequest, InvestorQuestionsResponse, InvestorQuestion
from app.schemas.answer_evaluation import AnswerEvaluationRequest, AnswerEvaluationResponse
from app.schemas.readiness_report import ReadinessReportRequest, ReadinessReportResponse, DimensionScore
from app.schemas.full_pipeline import FullPipelineRequest, FullPipelineResponse
from app.services.llm_client import llm_client

class PitchCoachService:

    # 1. Idea Analysis
    def analyze_idea(self, req: IdeaAnalysisRequest) -> IdeaAnalysisResponse:
        info = req.startup_info

        def mock_fn() -> IdeaAnalysisResponse:
            return IdeaAnalysisResponse(
                title=info.title,
                problem_statement=f"Entrepreneurs and startup teams in {info.target_industry} face severe friction converting unrefined business concepts into compelling, investor-grade pitch collateral.",
                proposed_solution=f"{info.title} is an AI-native pitch coaching system providing automated idea refinement, real-time slide deck structuring, competitive benchmarking, and interactive investor Q&A simulation.",
                target_audience=f"Early-stage founders, hackathon participants, incubator teams, and startup accelerators in {info.location}.",
                novelty_score=88.5,
                clarity_score=85.0,
                key_strengths=[
                    "High problem relevance for early stage founders seeking venture capital",
                    "Automated structured outputs eliminates manual formatting and pitch deck writer costs",
                    "Integrated investor question simulator provides pitch defense preparation"
                ],
                potential_weaknesses=[
                    "Needs strong defensibility against generic LLM wrappers",
                    "Requires proprietary benchmark data for industry-specific market sizing validation"
                ],
                risk_factors=[
                    RiskFactor(
                        category="Execution",
                        risk="Founders relying solely on AI outputs without customizing real customer traction metrics.",
                        mitigation="Incorporate mandatory traction prompts and guidance notes during pitch generation."
                    ),
                    RiskFactor(
                        category="Market",
                        risk="Competitive pressure from established slide design tools adding basic AI plugins.",
                        mitigation="Position deeply as an AI Pitch Coach focused on investor readiness and defense rather than just aesthetics."
                    )
                ],
                summary=f"Strong startup concept with high market potential in {info.target_industry}. Focus on building proprietary pitch scoring and real-time VC Q&A practice to maximize founder value."
            )

        prompt = f"Analyze the following startup idea:\nTitle: {info.title}\nDescription: {info.raw_description}\nIndustry: {info.target_industry}\nStage: {info.stage}"
        system = "You are an elite Silicon Valley venture capitalist and startup incubator director. Analyze the startup idea and return structured JSON."
        return llm_client.generate_structured(prompt, IdeaAnalysisResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 2. Clarification Questions
    def generate_clarification_questions(self, req: ClarificationQuestionsRequest) -> ClarificationQuestionsResponse:
        info = req.startup_info

        def mock_fn() -> ClarificationQuestionsResponse:
            return ClarificationQuestionsResponse(
                questions=[
                    ClarificationQuestion(
                        id="CQ1",
                        category="Monetization",
                        question="What is your primary revenue model (e.g., monthly subscription per founder, pay-per-pitch deck, or accelerator licensing)?",
                        rationale="Investors need to verify customer lifetime value (LTV) and recurring revenue scalability.",
                        sample_answer_hint="Freemium model with $29/mo Founder Plan and $499/yr Enterprise License for accelerators."
                    ),
                    ClarificationQuestion(
                        id="CQ2",
                        category="Traction",
                        question="Do you have any pilot users, beta signups, or letter of intent (LOI) from incubator programs?",
                        rationale="Early validation metrics reduce execution risk for pre-seed investors.",
                        sample_answer_hint="We have 150 waitlist signups and a pilot agreement with 2 local startup incubators."
                    ),
                    ClarificationQuestion(
                        id="CQ3",
                        category="Defensibility",
                        question="What is your unfair advantage or proprietary moat against generic LLMs (e.g. ChatGPT / Claude)?",
                        rationale="VCs reject generic AI wrappers; they look for proprietary data loops or domain workflows.",
                        sample_answer_hint="Fine-tuned pitch evaluation model trained on 10,000+ successful YC/Techstars pitch decks and VC feedback."
                    )
                ],
                guidance_notes="Answering these clarification questions will convert your initial pitch draft into an investor-ready business case."
            )

        prompt = f"Generate 3-5 critical clarification questions for this startup:\nTitle: {info.title}\nDescription: {info.raw_description}"
        system = "You are a lead investor at a top seed fund. Identify missing details in the pitch."
        return llm_client.generate_structured(prompt, ClarificationQuestionsResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 3. Value Proposition
    def generate_value_proposition(self, req: ValuePropRequest) -> ValuePropositionResponse:
        info = req.startup_info

        def mock_fn() -> ValuePropositionResponse:
            return ValuePropositionResponse(
                headline=f"Transform Raw Startup Ideas into Investor-Ready Pitches with {info.title}",
                subheadline="The AI pitch coach that structures your deck, benchmarks your market, and trains you to pass VC grillings with confidence.",
                geoff_moore_template=GeoffMooreTemplate(
                    target_customer=f"Early-stage entrepreneurs and startup founders in {info.target_industry}",
                    statement_of_need="who struggle to structure compelling pitch decks and prepare for tough investor Q&A",
                    product_name=info.title,
                    product_category="AI-powered pitch coach and readiness service",
                    key_benefit="transforms rough concepts into structured VC decks, market analyses, and interactive pitch defense practice",
                    primary_competitor="static presentation templates or expensive pitch consultants",
                    our_differentiation="provides instant structured AI scoring, automated market benchmarking, and interactive VC question evaluation."
                ),
                elevator_pitch_30s=f"For early-stage founders, {info.title} is an AI startup pitch coach that converts unrefined ideas into winning business decks in minutes. Unlike generic slide templates, {info.title} evaluates your value proposition, analyzes market opportunities, and coaches you through tough investor Q&A before you step into the boardroom.",
                unique_selling_points=[
                    "End-to-end pitch deck & script generation in under 2 minutes",
                    "Interactive AI investor grill simulator with instant answer scoring",
                    "Automated TAM/SAM/SOM and competitive positioning benchmarking"
                ],
                pain_relief_matrix=[
                    PainReliefItem(
                        customer_pain="Uncertainty about what hard questions VCs will ask during pitch meetings",
                        product_feature="AI Investor Q&A Simulator",
                        relief_value="Identifies critical weak spots and trains founders with benchmark answers before actual pitch calls"
                    ),
                    PainReliefItem(
                        customer_pain="Hours wasted formatting slides and writing pitch script drafts",
                        product_feature="Instant Slide Deck Generator",
                        relief_value="Saves 20+ hours of prep time with structured, slide-by-slide speaker notes and visual layouts"
                    )
                ]
            )

        prompt = f"Generate structured value proposition for:\nTitle: {info.title}\nDescription: {info.raw_description}"
        system = "You are a expert marketing strategist and startup positioning master."
        return llm_client.generate_structured(prompt, ValuePropositionResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 4. Market Analysis
    def analyze_market(self, req: MarketAnalysisRequest) -> MarketAnalysisResponse:
        info = req.startup_info

        def mock_fn() -> MarketAnalysisResponse:
            return MarketAnalysisResponse(
                industry=info.target_industry or "B2B SaaS / AI Productivity Software",
                market_metrics=MarketMetrics(
                    tam="$15.4 Billion (Global Pitch & Presentation Software Market)",
                    sam="$2.2 Billion (Startup Founder Software & Accelerator Tools)",
                    som="$95 Million (Early-stage tech founders in NA & EU within 2 years)",
                    cagr="19.4% (2024 - 2030)"
                ),
                competitor_matrix=[
                    Competitor(
                        name="Slidebean / Pitch.com",
                        type="Direct",
                        strengths="Polished visual design templates and presentation collaboration.",
                        weaknesses="Limited AI-driven business model critique and no investor Q&A defense simulator.",
                        differentiation_angle="Deep focus on investor readiness, business logic critique, and interactive Q&A training."
                    ),
                    Competitor(
                        name="Generic LLMs (ChatGPT / Claude)",
                        type="Indirect",
                        strengths="High general intelligence and custom prompt flexibility.",
                        weaknesses="Unstructured output, lack of standardized pitch deck schemas, no visual slide mapping.",
                        differentiation_angle="Structured Pydantic JSON pipelines optimized specifically for startup fundraising workflows."
                    )
                ],
                key_market_trends=[
                    "Explosive growth in AI-native founder tools accelerating company creation",
                    "Shift towards micro-seed funding requiring faster pitch iteration cycles",
                    "Increased investor scrutiny on unit economics and defensibility over hype"
                ],
                barriers_to_entry=[
                    "Network effects from incubator & accelerator partnerships",
                    "Proprietary dataset of successful pitch decks for benchmarking algorithms"
                ],
                growth_drivers=[
                    "Rising number of global startup hackathons and incubator programs",
                    "Demand for automated business intelligence among solo founders"
                ]
            )

        prompt = f"Generate comprehensive market analysis for:\nTitle: {info.title}\nDescription: {info.raw_description}"
        system = "You are a senior market research analyst specializing in venture capital and SaaS technology trends."
        return llm_client.generate_structured(prompt, MarketAnalysisResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 5. Pitch Generation
    def generate_pitch(self, req: PitchGenerationRequest) -> PitchGenerationResponse:
        info = req.startup_info

        def mock_fn() -> PitchGenerationResponse:
            return PitchGenerationResponse(
                slides=[
                    PitchSlide(
                        slide_number=1,
                        title=f"{info.title}: AI Startup Pitch Coach",
                        key_bullets=[
                            "Empowering founders to turn ideas into venture-funded startups",
                            "AI-driven pitch deck generation, market benchmarking, and VC Q&A practice"
                        ],
                        visual_suggestion="Sleek dark mode title banner with glowing logo mark and key value tagline.",
                        speaker_notes=f"Hi everyone, I'm presenting {info.title}. We are solving the biggest bottleneck for early-stage entrepreneurs: turning raw business ideas into winning investor pitches."
                    ),
                    PitchSlide(
                        slide_number=2,
                        title="The Problem: Pitch Prep is Slow & Unpredictable",
                        key_bullets=[
                            "90% of early-stage pitches fail due to poor structure and weak market defense",
                            "Founders spend 40+ hours crafting decks or pay $3k+ to consultants",
                            "First-time founders are blind-sided by tough VC questions during meetings"
                        ],
                        visual_suggestion="Split-screen graphic showing stressed founder vs delayed timeline.",
                        speaker_notes="Most founders waste weeks guessing what investors want to hear, only to fail in pitch meetings when faced with unexpected questions."
                    ),
                    PitchSlide(
                        slide_number=3,
                        title=f"The Solution: {info.title}",
                        key_bullets=[
                            "Automated Idea Analysis & Value Proposition refinement",
                            "Instant slide deck content generation with timing & speaker notes",
                            "Interactive VC Grill Simulator with real-time answer evaluation"
                        ],
                        visual_suggestion="3-step workflow diagram: Input Idea -> AI Refinement -> Investor-Ready Pitch.",
                        speaker_notes=f"With {info.title}, founders input their raw concept and receive a complete, investor-vetted pitch package in minutes."
                    ),
                    PitchSlide(
                        slide_number=4,
                        title="Market Opportunity & TAM",
                        key_bullets=[
                            "TAM: $15.4B Global Pitch & Presentation Software market",
                            "SAM: $2.2B Early-Stage Founder Tools market",
                            "SOM: $95M Target market across tech incubators & solo founders"
                        ],
                        visual_suggestion="Concentric circle diagram for TAM/SAM/SOM breakdown.",
                        speaker_notes="We are targeting a massive $15B total addressable market, starting with early-stage founders and incubator cohorts."
                    ),
                    PitchSlide(
                        slide_number=5,
                        title="Business Model & Traction Roadmap",
                        key_bullets=[
                            "Freemium SaaS: $29/mo Founder tier, $199 Pitch Clinic tier",
                            "B2B Enterprise: Accelerator & Incubator bulk licensing",
                            "Roadmap: Integration with AI audio coaching and deck export"
                        ],
                        visual_suggestion="Tiered pricing grid and 4-quarter roadmap timeline.",
                        speaker_notes="Our business model leverages recurring SaaS subscriptions and enterprise licensing for accelerators."
                    )
                ],
                scripts=PitchScriptSet(
                    elevator_pitch_30s=f"Hi, I'm building {info.title}. Entrepreneurs struggle to turn raw ideas into convincing business pitches, wasting weeks and losing investor interest. {info.title} is an AI pitch coach that refines value propositions, generates structured slide decks, and trains founders through real-time VC Q&A simulations. We're opening up a $15B market opportunity to make every founder investor-ready.",
                    overview_pitch_2min=f"Good day. Every year, millions of entrepreneurs launch startups, but over 90% struggle to communicate their vision effectively to investors. Creating a great pitch deck and preparing for tough investor questions takes weeks of expensive trial and error. That's why we created {info.title}. Our platform uses structured AI models to analyze startup concepts, generate slide-by-slide deck content with speaker notes, calculate TAM/SAM/SOM market metrics, and simulate real-time investor grillings with instant feedback. We operate a freemium SaaS model targeting the $2.2B founder software market, partnering directly with startup incubators. We are seeking early partners and seed funding to scale our AI pitch engine globally.",
                    full_pitch_5min=f"Welcome investors. Today I'm thrilled to introduce {info.title}. Let's look at Slide 1: {info.title} is an AI Startup Pitch Coach designed to turn raw concepts into venture-backed companies. Moving to Slide 2: The core problem is that first-time founders lack fundraising experience. They spend 40+ hours writing decks or thousands of dollars on consultants, yet still get rejected because they haven't validated their market or prepared for hard VC questions. On Slide 3: Our solution automates the entire pitch creation workflow—from idea analysis and value prop mapping to interactive Q&A defense. Slide 4 shows our market validation: a $15.4B presentation software sector with an urgent need for domain-specific AI logic. Finally, Slide 5 highlights our monetization strategy: SaaS subscriptions starting at $29/mo and enterprise accelerator packages. Thank you, and we'd love to take your questions."
                )
            )

        prompt = f"Generate complete pitch deck slides and scripts for:\nTitle: {info.title}\nDescription: {info.raw_description}"
        system = "You are a master pitch coach and pitch deck designer for Y-Combinator startups."
        return llm_client.generate_structured(prompt, PitchGenerationResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 6. Pitch Critique
    def critique_pitch(self, req: PitchCritiqueRequest) -> PitchCritiqueResponse:
        def mock_fn() -> PitchCritiqueResponse:
            return PitchCritiqueResponse(
                overall_score=84.5,
                clarity_score=88.0,
                persuasion_score=81.0,
                slide_critiques=[
                    SlideCritique(
                        slide_number=1,
                        title="Title & Intro",
                        clarity_score=92.0,
                        persuasion_score=85.0,
                        feedback="Clear value statement and professional title framing.",
                        suggested_fix="Add a 1-sentence traction teaser right on the title slide (e.g. '150+ Beta Signups')."
                    ),
                    SlideCritique(
                        slide_number=2,
                        title="Problem Statement",
                        clarity_score=86.0,
                        persuasion_score=80.0,
                        feedback="Problem is relatable, but lacks quantitative dollar metrics on how much time/money is lost.",
                        suggested_fix="Quantify the cost: 'Founders waste 40+ hours and $3,000 per pitch deck prep.'"
                    )
                ],
                top_strengths=[
                    "Strong problem-solution alignment tailored to early-stage founders",
                    "Clear slide-by-slide structure following standard VC deck order",
                    "Compelling 30s elevator pitch script"
                ],
                critical_gaps=[
                    "Needs explicit unit economics details in the Business Model slide",
                    "Requires concrete competitive moat statement against generic AI platforms"
                ],
                actionable_recommendations=[
                    "Include 2 customer testimonials or pilot metrics on the solution slide",
                    "Add explicit CAC/LTV projection targets on the business model slide",
                    "Practice the 2-minute overview script to keep presentation time under strict limits"
                ]
            )

        prompt = "Critique the provided pitch deck slides and script."
        system = "You are a ruthless VC pitch reviewer providing candid, actionable critique."
        return llm_client.generate_structured(prompt, PitchCritiqueResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 7. Investor Questions
    def generate_investor_questions(self, req: InvestorQuestionsRequest) -> InvestorQuestionsResponse:
        info = req.startup_info

        def mock_fn() -> InvestorQuestionsResponse:
            return InvestorQuestionsResponse(
                questions=[
                    InvestorQuestion(
                        id="IQ1",
                        category="Financial",
                        question="What is your projected Customer Acquisition Cost (CAC) and how do you plan to achieve paybacks under 6 months?",
                        difficulty="Hard",
                        investor_intent="Testing financial literacy, go-to-market efficiency, and unit economics realism.",
                        key_points_to_include=[
                            "Target acquisition channels (organic founder communities, incubator partnerships)",
                            "Estimated CAC range ($40 - $70)",
                            "Expected payback window (3-5 months on monthly SaaS subscriptions)"
                        ]
                    ),
                    InvestorQuestion(
                        id="IQ2",
                        category="Technical",
                        question="How do you prevent users from bypassing your app and replicating your prompts directly in ChatGPT?",
                        difficulty="Brutal",
                        investor_intent="Probing for proprietary technology, data moats, and product defensibility.",
                        key_points_to_include=[
                            "Multi-agent evaluation pipeline with proprietary scoring rubrics",
                            "Fine-tuned investor feedback datasets",
                            "Integrated UI/UX for visual slide export and live voice Q&A practice"
                        ]
                    ),
                    InvestorQuestion(
                        id="IQ3",
                        category="Market",
                        question="Why hasn't pitch.com or slidebean already dominated this exact AI pitch coaching space?",
                        difficulty="Medium",
                        investor_intent="Evaluating market dynamics and competitive awareness.",
                        key_points_to_include=[
                            "Competitors focus on visual slide layout rather than business logic and pitch defense",
                            "Our focus is structured investor readiness scoring and active Q&A coaching"
                        ]
                    )
                ],
                preparation_advice="Always answer with numbers first, keep responses under 45 seconds, and avoid defensive language when challenged by VCs."
            )

        prompt = f"Generate top investor questions for:\nTitle: {info.title}\nDescription: {info.raw_description}"
        system = "You are a tough partner at a tier-1 VC fund conducting due diligence."
        return llm_client.generate_structured(prompt, InvestorQuestionsResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 8. Answer Evaluation
    def evaluate_answer(self, req: AnswerEvaluationRequest) -> AnswerEvaluationResponse:
        def mock_fn() -> AnswerEvaluationResponse:
            return AnswerEvaluationResponse(
                clarity_score=78.0,
                persuasiveness_score=72.0,
                completeness_score=68.0,
                overall_answer_score=72.7,
                strengths=[
                    "Acknowledged the question direction directly without hesitation"
                ],
                weaknesses=[
                    "Lacks concrete numerical metrics or data points",
                    "Did not specify distribution channels or conversion targets"
                ],
                missing_key_points=[
                    "Mentioning organic growth through incubator cohorts to lower initial CAC",
                    "Highlighting referral loops where founders share pitch scores"
                ],
                improved_answer=f"For our initial phase, our Customer Acquisition Cost is under $35 because we acquire founders organically through incubator partnerships and developer hackathons. As we scale paid channels, we target a CAC of $65 against an average annual customer value of $348, giving us a sub-3-month CAC payback period."
            )

        prompt = f"Evaluate founder's answer to investor question:\nQuestion: {req.question}\nAnswer: {req.user_answer}"
        system = "You are an AI communications coach grading pitch defense responses."
        return llm_client.generate_structured(prompt, AnswerEvaluationResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 9. Readiness Report
    def generate_readiness_report(self, req: ReadinessReportRequest) -> ReadinessReportResponse:
        info = req.startup_info

        def mock_fn() -> ReadinessReportResponse:
            return ReadinessReportResponse(
                overall_readiness_score=86.4,
                readiness_badge="Pitch Ready",
                dimension_scores=[
                    DimensionScore(dimension="Idea Clarity", score=88.0, summary="Clear problem statement and solution scope."),
                    DimensionScore(dimension="Market Viability", score=85.0, summary="Large TAM with favorable market growth trends."),
                    DimensionScore(dimension="Value Prop & Product", score=89.0, summary="Strong USPs and clear customer pain relief matrix."),
                    DimensionScore(dimension="Pitch Quality", score=84.0, summary="Well-structured 5-slide deck outline and timing scripts."),
                    DimensionScore(dimension="Investor Defense", score=86.0, summary="Prepared for core financial and technical questions.")
                ],
                key_highlights=[
                    "Targeting a growing $15.4B presentation software market",
                    "High problem relevance for early-stage startup founders",
                    "Clear freemium and enterprise accelerator monetization path"
                ],
                red_flags=[
                    "Need to secure early incubator pilots to prove low CAC assumptions",
                    "Must emphasize proprietary AI evaluation model against simple LLM wrappers"
                ],
                actionable_next_steps=[
                    "Finalize pilot agreements with 2 startup incubators",
                    "Conduct 10 practice Q&A sessions using the AI Investor Simulator",
                    "Add customer testimonial quotes to Slide 3 of the pitch deck"
                ]
            )

        prompt = f"Generate complete Investment Readiness Report for:\nTitle: {info.title}"
        system = "You are the Chairman of an Investment Committee issuing an investment readiness badge."
        return llm_client.generate_structured(prompt, ReadinessReportResponse, system_instruction=system, mock_generator_fn=mock_fn)

    # 10. Full End-to-End Orchestrator Pipeline
    def run_full_pipeline(self, req: FullPipelineRequest) -> FullPipelineResponse:
        idea_res = self.analyze_idea(IdeaAnalysisRequest(startup_info=req.startup_info))
        questions_res = self.generate_clarification_questions(ClarificationQuestionsRequest(startup_info=req.startup_info))
        vp_res = self.generate_value_proposition(ValuePropRequest(startup_info=req.startup_info))
        market_res = self.analyze_market(MarketAnalysisRequest(startup_info=req.startup_info))
        pitch_res = self.generate_pitch(PitchGenerationRequest(startup_info=req.startup_info, value_prop=vp_res, market_analysis=market_res))
        critique_res = self.critique_pitch(PitchCritiqueRequest(slides=pitch_res.slides, pitch_script=pitch_res.scripts.full_pitch_5min))
        investor_res = self.generate_investor_questions(InvestorQuestionsRequest(startup_info=req.startup_info))
        readiness_res = self.generate_readiness_report(ReadinessReportRequest(
            startup_info=req.startup_info,
            idea_analysis_score=idea_res.clarity_score,
            market_score=85.0,
            pitch_score=critique_res.overall_score,
            qna_score=86.0
        ))

        return FullPipelineResponse(
            idea_analysis=idea_res,
            clarification_questions=questions_res,
            value_proposition=vp_res,
            market_analysis=market_res,
            pitch_deck=pitch_res,
            pitch_critique=critique_res,
            investor_questions=investor_res,
            readiness_report=readiness_res
        )

pitch_coach_service = PitchCoachService()
