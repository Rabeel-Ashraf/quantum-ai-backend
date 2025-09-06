import asyncio
from typing import AsyncGenerator
from .base import BaseAgent
from llm.openai import OpenAIClient
from llm.gemini import GeminiClient
from llm.deepseek import DeepSeekClient

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("coder")
        self.llm_clients = [
            OpenAIClient(),
            GeminiClient(),
            DeepSeekClient()
        ]
    
    async def process(self, query: str, user_id: str) -> AsyncGenerator[str, None]:
        # Check cache first
        cached = await self.get_cached_response(query, user_id)
        if cached:
            yield cached
            return
        
        # Try each LLM client until we get a response
        response = None
        for client in self.llm_clients:
            try:
                response = await client.generate_code(query, self.system_prompt)
                if response:
                    break
            except Exception as e:
                print(f"Error with {client.__class__.__name__}: {e}")
                continue
        
        if not response:
            response = "I apologize, but I'm currently unable to generate code. Please try again later."
        
        # Cache the result
        await self.set_cached_response(query, user_id, response)
        
        yield response
