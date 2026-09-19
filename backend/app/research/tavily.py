import os
import aiohttp
from typing import Any
from .base import SearchProvider

class TavilySearchProvider(SearchProvider):
    def __init__(self):
        self.provider_name = "tavily"
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.url = "https://api.tavily.com/search"

    async def search(self, query: str, timeout: int = 6) -> list[dict[str, Any]]:
        if not self.api_key:
            return [] # Fallback to cached/empty if no key

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": False,
            "max_results": 3
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload, timeout=timeout) as resp:
                    if resp.status != 200:
                        # On failure, return empty list to trigger fallback logic in the service
                        return []
                    data = await resp.json()
                    
                    results = []
                    for item in data.get("results", []):
                        results.append({
                            "url": item.get("url", ""),
                            "title": item.get("title", ""),
                            "snippet": item.get("content", ""),
                            "provider": self.provider_name
                        })
                    return results
        except Exception:
            return []
