import json
import asyncio
from pathlib import Path
from typing import Any
from .base import SearchProvider

FIXTURES_DIR = Path(__file__).parent / "fixtures"

class CachedSearchProvider(SearchProvider):
    def __init__(self):
        self.provider_name = "cached"
        
    async def search(self, query: str, timeout: int = 6) -> list[dict[str, Any]]:
        # Simulate network latency
        await asyncio.sleep(0.5)
        
        fixture_path = FIXTURES_DIR / "search_cache.json"
        if not fixture_path.exists():
            return []
            
        with open(fixture_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
            
        # Very basic cache matching for demo purposes
        for cached_query, results in cache.items():
            if cached_query.lower() in query.lower():
                return results
                
        return []
