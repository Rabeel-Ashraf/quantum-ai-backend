import aiohttp
import json
from typing import Optional
from config.settings import settings
from core.cache import cache

class SearchTool:
    def __init__(self):
        self.api_key = settings.search_api_key
        self.base_url = "https://serpapi.com/search"
    
    async def search(self, query: str) -> str:
        cache_key = f"search:{hash(query)}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        if not self.api_key:
            return "Search API is not configured. Please contact support."
        
        url = f"{self.base_url}?q={query}&api_key={self.api_key}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        organic_results = data.get("organic_results", [])
                        
                        if not organic_results:
                            return f"No search results found for '{query}'."
                        
                        result = f"Search results for '{query}':\n\n"
                        for i, item in enumerate(organic_results[:3], 1):
                            title = item.get("title", "No title")
                            link = item.get("link", "#")
                            snippet = item.get("snippet", "No description")
                            result += f"{i}. {title}\n   {snippet}\n   Source: {link}\n\n"
                        
                        cache.set(cache_key, result, 3600)  # Cache for 1 hour
                        return result
                    else:
                        return f"Failed to search. API returned status {response.status}."
        except Exception as e:
            return f"Error performing search: {str(e)}"
