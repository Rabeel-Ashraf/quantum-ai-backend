import asyncio
from typing import AsyncGenerator, List
from .base import BaseAgent
from llm.openai import OpenAIClient

class ComposerAgent(BaseAgent):
    def __init__(self):
        super().__init__("composer")
        self.llm_client = OpenAIClient()
    
    async def process(self, agent_responses: List[str], original_query: str, user_id: str) -> AsyncGenerator[str, None]:
        if len(agent_responses) == 1:
            # If only one response, just stream it
            for char in agent_responses[0]:
                yield char
                await asyncio.sleep(0.01)
            return
        
        # Compose multiple responses into one coherent response
        composition_prompt = f"""
        Combine the following responses into a single, coherent, and comprehensive answer.
        Original query: {original_query}
        
        Responses to combine:
        {chr(10).join([f'Response {i+1}: {r}' for i, r in enumerate(agent_responses)])}
        
        Please create a well-structured response that:
        1. Addresses all aspects of the original query
        2. Integrates information from all responses seamlessly
        3. Maintains a natural and engaging flow
        4. Is concise yet comprehensive
        """
        
        composed_response = await self.llm_client.generate_stream(
            composition_prompt, 
            self.system_prompt,
            temperature=0.3
        )
        
        async for chunk in composed_response:
            yield chunk
