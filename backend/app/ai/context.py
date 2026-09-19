from app.schemas.profile import Profile
from typing import Any

def build_context(capability: str, profile: Profile, **kwargs) -> dict[str, Any]:
    """
    Builds a focused projection of the profile for a specific AI capability.
    This prevents the LLM from being overwhelmed by the entire document.
    """
    ctx = {}
    
    if capability == "analyze_idea":
        ctx["identity"] = profile.identity.model_dump()
        
    elif capability == "generate_clarification_question":
        ctx["profile"] = profile.model_dump()
        ctx["open_gaps"] = [g.model_dump() for g in profile.gaps if g.status == "open"]
        ctx["previous_questions"] = kwargs.get("previous_questions", [])
        
    elif capability == "extract_profile_patch":
        ctx["profile"] = profile.model_dump()
        ctx["question"] = kwargs.get("question", "")
        ctx["founder_answer"] = kwargs.get("answer", "")
        
    elif capability == "generate_value_proposition":
        ctx["problem"] = profile.problem.model_dump()
        ctx["customer"] = profile.customer.model_dump()
        ctx["solution"] = profile.solution.model_dump()
        ctx["competitors"] = [c.model_dump() for c in profile.competitor_summary]
        ctx["traction"] = profile.traction.model_dump()
        
    elif capability in ("analyze_market", "analyze_competitors"):
        ctx["customer"] = profile.customer.model_dump()
        ctx["problem"] = profile.problem.model_dump()
        ctx["solution"] = profile.solution.model_dump()
        ctx["market_size_inputs"] = profile.market.size_inputs.model_dump()
        ctx["evidence"] = kwargs.get("evidence", [])
        
    elif capability == "analyze_business_model":
        ctx["customer"] = profile.customer.model_dump()
        ctx["solution"] = profile.solution.model_dump()
        ctx["business_model"] = profile.business_model.model_dump()
        ctx["traction"] = profile.traction.model_dump()
        
    elif capability == "generate_pitch":
        full_dump = profile.model_dump()
        # Remove gaps so they don't leak into the pitch blindly
        full_dump.pop("gaps", None)
        ctx["profile"] = full_dump
        if kwargs.get("prior_critique"):
            ctx["prior_critique"] = kwargs.get("prior_critique")
            
    elif capability == "critique_pitch":
        ctx["pitch_slides"] = kwargs.get("pitch_slides", [])
        ctx["profile"] = profile.model_dump()
        
    elif capability in ("generate_investor_question", "evaluate_answer"):
        ctx["profile"] = profile.model_dump()
        ctx["open_gaps"] = [g.model_dump() for g in profile.gaps if g.status == "open"]
        ctx["topic"] = kwargs.get("topic")
        ctx["last_turn"] = kwargs.get("last_turn")
        
    elif capability == "generate_readiness_narrative":
        ctx["open_gaps"] = [g.model_dump() for g in profile.gaps if g.status == "open"]
        ctx["computed_scores"] = kwargs.get("computed_scores")
        ctx["turns"] = kwargs.get("turns", [])
        
    return ctx
