from typing import Dict, Any, Optional
from app.ai.schemas.common import StartupProfile

class ContextBuilder:

    @staticmethod
    def project_for_idea_analysis(profile: StartupProfile) -> str:
        return f"""Startup Name: {profile.identity.startup_name}
Raw Idea: <founder_input>{profile.identity.raw_idea}</founder_input>
One Liner: {profile.identity.one_liner or 'Not provided'}"""

    @staticmethod
    def project_for_clarification(profile: StartupProfile, previous_questions: list = None) -> str:
        open_gaps = [f"- [{g.topic}] {g.text}" for g in profile.gaps if g.status == "open"]
        prev_q = previous_questions or []
        return f"""Startup Name: {profile.identity.startup_name}
Problem: {profile.problem.statement or 'Not provided'}
Target Customer: {profile.customer.primary_segment or 'Not provided'}
Solution: {profile.solution.description or 'Not provided'}
Open Gaps:
{chr(10).join(open_gaps) if open_gaps else 'None'}
Previously Asked Questions: {', '.join(prev_q) if prev_q else 'None'}"""

    @staticmethod
    def project_for_patch_extraction(profile: StartupProfile, question: str, answer: str) -> str:
        return f"""Question Asked: {question}
Founder Answer: <founder_input>{answer}</founder_input>
Allowed Profile Paths:
- problem.statement
- customer.primary_segment
- customer.persona
- solution.description
- value_proposition.one_line
- business_model.pricing
- business_model.revenue_source
- traction.interviews
- traction.interested
- traction.users
- traction.revenue"""

    @staticmethod
    def project_for_value_prop(profile: StartupProfile) -> str:
        return f"""Startup Name: {profile.identity.startup_name}
Problem: {profile.problem.statement}
Customer: {profile.customer.primary_segment}
Solution: {profile.solution.description}
Pain Points: {', '.join(profile.problem.pain_points)}"""

    @staticmethod
    def project_for_competitors(profile: StartupProfile, evidence_snippets: list = None) -> str:
        snippets = evidence_snippets or []
        formatted_snippets = "\n".join([f"[{e['id']}] {e['title']}: {e['snippet']}" for e in snippets])
        return f"""Startup Name: {profile.identity.startup_name}
Solution: {profile.solution.description}
Customer: {profile.customer.primary_segment}
Evidence Snippets:
{formatted_snippets if formatted_snippets else 'No external evidence available'}"""

    @staticmethod
    def project_for_market(profile: StartupProfile, evidence_snippets: list = None) -> str:
        snippets = evidence_snippets or []
        formatted_snippets = "\n".join([f"[{e['id']}] {e['title']}: {e['snippet']}" for e in snippets])
        return f"""Startup Name: {profile.identity.startup_name}
Customer: {profile.customer.primary_segment}
Market Size Inputs: Customers={profile.market.size_inputs.customers}, Price={profile.market.size_inputs.price}
Evidence Snippets:
{formatted_snippets if formatted_snippets else 'No external evidence available'}"""

    @staticmethod
    def project_for_business_model(profile: StartupProfile) -> str:
        return f"""Startup Name: {profile.identity.startup_name}
Customer: {profile.customer.primary_segment}
Solution: {profile.solution.description}
Existing Monetization Notes: {profile.business_model.revenue_source or 'None'}"""

    @staticmethod
    def project_for_pitch(profile: StartupProfile, market_analysis: dict = None, competitor_analysis: dict = None) -> str:
        return f"""Startup Name: {profile.identity.startup_name}
Problem: {profile.problem.statement}
Customer: {profile.customer.primary_segment}
Solution: {profile.solution.description}
Value Prop: {profile.value_proposition.one_line}
Business Model: {profile.business_model.type or 'Freemium SaaS'}
Traction: Revenue={profile.traction.revenue or 'Not provided'}, Users={profile.traction.users or 'Not provided'}"""

    @staticmethod
    def project_for_investor_question(profile: StartupProfile, intent: str, topic: str, prev_turn: dict = None) -> str:
        prev = f"Previous Question: {prev_turn['question']}\nPrevious Answer: {prev_turn['answer']}" if prev_turn else "None"
        return f"""Startup Name: {profile.identity.startup_name}
Topic Focus: {topic}
Intent: {intent}
{prev}"""

    @staticmethod
    def project_for_answer_eval(profile: StartupProfile, question: str, user_answer: str) -> str:
        return f"""Investor Question: {question}
Founder Answer: <founder_input>{user_answer}</founder_input>
Startup Profile:
- Problem: {profile.problem.statement}
- Solution: {profile.solution.description}
- Customer: {profile.customer.primary_segment}"""

context_builder = ContextBuilder()
