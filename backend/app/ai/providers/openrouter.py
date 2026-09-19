import os
import json
import aiohttp
from .base import LLMProvider
from app.core.errors import LLMUnavailable

class OpenRouterProvider(LLMProvider):
    def __init__(self):
        self.provider_name = "openrouter"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v4-flash-0731:free")

    async def complete_json(self, prompt: str, timeout: int = 25) -> str:
        if not self.api_key:
            raise LLMUnavailable("OPENROUTER_API_KEY is not set.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5173", # Optional, for OpenRouter rankings
            "X-Title": "PitchPilot", # Optional, for OpenRouter rankings
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            # Note: Not all free OpenRouter models support strict JSON mode natively,
            # so we prompt it heavily or rely on our runner's extract_json & repair loop.
            # We can still pass response_format as a hint.
            "response_format": {"type": "json_object"}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=headers, json=payload, timeout=timeout) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        raise LLMUnavailable(f"OpenRouter API error: {resp.status} - {error_text}")
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise LLMUnavailable(f"OpenRouter request failed: {e}")
