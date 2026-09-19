from typing import Protocol, Any

class SearchProvider(Protocol):
    async def search(self, query: str, timeout: int = 6) -> list[dict[str, Any]]:
        """
        Executes a search query and returns a list of evidence dictionaries.
        Each dictionary should contain: {'url', 'title', 'snippet', 'provider'}
        """
        ...
