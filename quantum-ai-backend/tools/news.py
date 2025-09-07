import aiohttp
import json
from typing import Optional
from config.settings import settings
from core.cache import cache

class NewsTool:
    def __init__(self):
        self.api_key = settings.news_api_key
        self.base_url = "https://newsapi.org/v2"
    
    async def get_news(self, query: str) -> str:
        cache_key = f"news:{hash(query)}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        if not self.api_key:
            return "News API is not configured. Please contact support."
        
        url = f"{self.base_url}/everything?q={query}&apiKey={self.api_key}&pageSize=5"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])
                        
                        if not articles:
                            return f"No news articles found for '{query}'."
                        
                        result = f"Here are the latest news about '{query}':\n\n"
                        for i, article in enumerate(articles[:3], 1):
                            title = article.get("title", "No title")
                            description = article.get("description", "No description")
                            url = article.get("url", "#")
                            result += f"{i}. {title}\n   {description}\n   Source: {url}\n\n"
                        
                        cache.set(cache_key, result, 3600)  # Cache for 1 hour
                        return result
                    else:
                        return f"Failed to fetch news. API returned status {response.status}."
        except Exception as e:
            return f"Error fetching news: {str(e)}"
