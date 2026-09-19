import json
import asyncio
from pathlib import Path
from .base import LLMProvider

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

class MockProvider(LLMProvider):
    def __init__(self):
        self.provider_name = "mock"

    async def complete_json(self, prompt: str, timeout: int = 25) -> str:
        # In the mock provider, we expect the capability to be passed in a hacky way 
        # or we just parse the prompt for a keyword. 
        # For simplicity in this implementation, we will assume the caller injects a hint 
        # into the prompt like "CAPABILITY: analyze_idea", or we parse it.
        # Since this is a hackathon, we'll try to extract the capability from the prompt 
        # if injected, otherwise default to a fallback string.
        
        capability = "unknown"
        for line in prompt.split('\n'):
            if line.startswith("CAPABILITY_HINT:"):
                capability = line.split(":")[1].strip()
                break
        
        fixture_path = FIXTURES_DIR / f"{capability}.json"
        
        if not fixture_path.exists():
            return "{}"

        # Simulate small network delay
        await asyncio.sleep(0.5)

        with open(fixture_path, "r", encoding="utf-8") as f:
            data = f.read()
            
        return data
