import asyncio
from typing import AsyncGenerator, List
from .base import BaseAgent
from llm.openai import OpenAIClient

class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__("reviewer")
        self.llm_client = OpenAIClient()  # Use most reliable model for review
    
    async def process(self, content: str, original_query: str, user_id: str) -> AsyncGenerator[str, None]:
        review_prompt = f"""
        Please review the following content for accuracy, clarity, and potential hallucinations.
        Original query: {original_query}
        
        Content to review:
        {content}
        
        Provide an improved version that:
        1. Fixes any inaccuracies or hallucinations
        2. Improves clarity and readability
        3. Maintains the original intent and information
        4. Is concise and professional
        """
        
        reviewed_content = await self.llm_client.generate(
            review_prompt, 
            self.system_prompt,
            temperature=0.1  # Low temperature for factual accuracy
        )
        
        yield reviewed_content or content  # Fallback to original if review fails
