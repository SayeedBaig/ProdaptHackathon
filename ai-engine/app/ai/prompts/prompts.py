from app.ai.prompts.common import COMMON_RULES

PROMPTS = {
    "analyze_idea": {
        "system": COMMON_RULES + "\nAnalyze the raw startup idea and extract structured problem, customer, solution, assumptions, risks, and first question.",
        "temperature": 0.2
    },
    "generate_clarification_question": {
        "system": COMMON_RULES + "\nGenerate a targeted clarification question for the highest severity profile gap.",
        "temperature": 0.7
    },
    "extract_profile_patch": {
        "system": COMMON_RULES + "\nExtract JSON patch operations from the founder's answer against whitelisted profile fields.",
        "temperature": 0.1
    },
    "generate_value_proposition": {
        "system": COMMON_RULES + "\nFormulate Geoff Moore value proposition, 30s elevator pitch, and pain-relief matrix.",
        "temperature": 0.3
    },
    "analyze_competitors": {
        "system": COMMON_RULES + "\nAnalyze market evidence to map competitors, strengths, weaknesses, and differentiation with evidence citations.",
        "temperature": 0.2
    },
    "analyze_market": {
        "system": COMMON_RULES + "\nAnalyze market evidence to calculate TAM/SAM/SOM inputs, opportunities, and threats with evidence citations.",
        "temperature": 0.2
    },
    "analyze_business_model": {
        "system": COMMON_RULES + "\nExtract business model structure, pricing model, cost drivers, and missing unit economic assumptions.",
        "temperature": 0.2
    },
    "generate_pitch": {
        "system": COMMON_RULES + "\nGenerate 5-slide pitch deck content (bullets, visual ideas, speaker notes) and timed pitch scripts.",
        "temperature": 0.4
    },
    "critique_pitch": {
        "system": COMMON_RULES + "\nCritique the pitch deck for clarity, persuasion, and objections. Highlight weak slides and priorities.",
        "temperature": 0.3
    },
    "generate_investor_question": {
        "system": COMMON_RULES + "\nAct as a seasoned VC investor. Generate a sharp, realistic investor question for the assigned topic and intent.",
        "temperature": 0.7
    },
    "evaluate_answer": {
        "system": COMMON_RULES + "\nGrade the founder's answer across the 6 criteria (0-10), provide constructive feedback and a model response.",
        "temperature": 0.2
    },
    "generate_readiness_narrative": {
        "system": COMMON_RULES + "\nSynthesize an executive readiness report narrative explaining strengths and gaps without changing numerical scores.",
        "temperature": 0.3
    },
    "extract_feedback_patches": {
        "system": COMMON_RULES + "\nExtract actionable feedback items with suggested profile patches from the readiness report.",
        "temperature": 0.2
    }
}
