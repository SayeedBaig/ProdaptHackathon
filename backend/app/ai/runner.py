import re
from typing import Type, TypeVar, Any
from pydantic import BaseModel, ValidationError
from app.core.errors import LLMInvalidOutput, LLMUnavailable
import os
from app.ai.providers.mock import MockProvider
from app.ai.providers.openrouter import OpenRouterProvider

T = TypeVar('T', bound=BaseModel)

ai_mode = os.getenv("AI_MODE", "mock")
FALLBACK_CHAIN = []

if ai_mode == "live":
    # OpenRouter handles all our routing now!
    FALLBACK_CHAIN.append(OpenRouterProvider())

# Always append mock as the last resort fallback
FALLBACK_CHAIN.append(MockProvider())

def extract_json(raw: str) -> dict[str, Any]:
    """Strips markdown fences and parses JSON"""
    import json
    
    # Remove markdown code block fences if present
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        # Find the first newline to skip ```json
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline+1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
            
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise LLMInvalidOutput("Failed to decode JSON from LLM response.")

async def run(capability: str, ctx: Any, schema: Type[T]) -> T:
    """
    Core AI runner that handles execution, retries, and provider fallbacks.
    """
    # For now, we mock the prompt rendering. M2 owns the actual prompts.
    # We inject a hint for the mock provider to know which fixture to load.
    prompt = f"CAPABILITY_HINT: {capability}\nRendered prompt would go here."
    
    last_error = None
    
    for provider in FALLBACK_CHAIN:
        current_prompt = prompt
        
        for attempt in range(2):  # 1 initial try + 1 repair retry
            try:
                raw_response = await provider.complete_json(current_prompt, timeout=25)
                json_data = extract_json(raw_response)
                return schema.model_validate(json_data)
                
            except ValidationError as e:
                # Append repair instructions to prompt for the next attempt
                current_prompt = prompt + f"\n\nYour previous JSON failed validation:\n{e}\nPlease return only valid JSON matching the schema."
                last_error = e
                
            except Exception as e:
                # Network or other provider-level error, break to next provider
                last_error = e
                break
                
    if isinstance(last_error, ValidationError):
        raise LLMInvalidOutput(f"Validation failed after retries: {last_error}")
    else:
        raise LLMUnavailable(f"All LLM providers failed: {last_error}")
