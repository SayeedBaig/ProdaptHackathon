from typing import Protocol

class LLMProvider(Protocol):
    async def complete_json(self, prompt: str, timeout: int = 25) -> str:
        """
        Calls the LLM provider and returns the raw response string, which should be JSON.
        Raises LLMUnavailable on network or timeout errors.
        """
        ...
