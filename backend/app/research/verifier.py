import re
from typing import Any
from app.schemas.profile import Claim

def assign_provenance(claim: Claim, evidence_list: list[dict[str, Any]]) -> Claim:
    """
    Verifies if an AI-generated claim is actually supported by the provided evidence.
    Enforces strict rules:
    - If evidence_ids match and supporting_quote is found in the snippet -> source_backed
    - Otherwise -> ai_analysis
    - If ai_analysis contains unverified numbers -> strip numbers and mark 'Requires validation'
    """
    
    is_supported = False
    
    # Rule 1: Check if supporting quote exists in ANY of the cited evidence snippets
    if claim.supporting_quote and claim.evidence_ids:
        quote_lower = claim.supporting_quote.lower()
        
        for ev in evidence_list:
            if ev.get("id") in claim.evidence_ids:
                snippet = ev.get("snippet", "").lower()
                if quote_lower in snippet:
                    is_supported = True
                    break

    if is_supported:
        claim.provenance = "source_backed"
    else:
        # Rule 2: Downgrade to ai_analysis if quote is missing or fake
        if claim.provenance not in ["founder_assumption", "calculated"]:
            claim.provenance = "ai_analysis"
            
        # Rule 3: Strip unsupported numbers
        # Looks for digits, %, $, billion, million, etc.
        number_pattern = re.compile(r'\d+|%|\$|billion|million', re.IGNORECASE)
        if number_pattern.search(claim.text):
            claim.text = "Requires validation"
            claim.supporting_quote = None
            claim.evidence_ids = []
            
    return claim
