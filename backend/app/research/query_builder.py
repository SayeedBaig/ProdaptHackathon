from app.schemas.profile import Profile

def build_queries(profile: Profile) -> list[str]:
    """
    Generates 3-5 targeted search queries based on the startup profile.
    """
    queries = []
    
    # 1. Competitor discovery
    target = profile.customer.primary_segment or "target customers"
    solution = profile.solution.description or profile.identity.raw_idea
    queries.append(f"{target} {solution} alternative competitor")
    
    # 2. Known competitors pricing/features
    for comp in profile.competitor_summary[:2]:
        queries.append(f"{comp.name} pricing target market weaknesses")
        
    # 3. Market size / trends
    queries.append(f"{target} market size growth trend {solution}")
    
    # Cap to avoid hitting API limits
    return queries[:4]
