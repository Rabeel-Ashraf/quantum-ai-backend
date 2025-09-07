import aiohttp
import asyncio
from typing import AsyncGenerator
from .base import BaseAgent
from tools.news import NewsTool
from tools.weather import WeatherTool
from tools.search import SearchTool
from tools.scraper import WebScraper

class ScraperAgent(BaseAgent):
    def __init__(self):
        super().__init__("scraper")
        self.news_tool = NewsTool()
        self.weather_tool = WeatherTool()
        self.search_tool = SearchTool()
        self.web_scraper = WebScraper()
    
    async def process(self, query: str, user_id: str) -> AsyncGenerator[str, None]:
        # Check cache first
        cached = await self.get_cached_response(query, user_id)
        if cached:
            yield cached
            return
        
        # Determine which tool to use based on query
        if any(keyword in query.lower() for keyword in ["news", "headline", "article"]):
            result = await self.news_tool.get_news(query)
        elif any(keyword in query.lower() for keyword in ["weather", "temperature", "forecast"]):
            result = await self.weather_tool.get_weather(query)
        else:
            # Try web search as default
            result = await self.search_tool.search(query)
        
        # Cache the result
        await self.set_cached_response(query, user_id, result)
        
        yield result
