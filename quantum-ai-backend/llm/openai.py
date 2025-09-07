import openai
from typing import AsyncGenerator, Optional
from .base import BaseLLMClient
from config.settings import settings

class OpenAIClient(BaseLLMClient):
    def __init__(self):
        super().__init__("openai")
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4"  # Use GPT-4 for best results
    
    async def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> Optional[str]:
        # Check cache first
        cached = await self.get_cached_response(prompt)
        if cached:
            return cached
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            result = response.choices[0].message.content
            
            # Cache the result
            await self.set_cached_response(prompt, result)
            
            return result
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    async def generate_stream(self, prompt: str, system_prompt: str = None, **kwargs) -> AsyncGenerator[str, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                **kwargs
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"OpenAI API streaming error: {e}")
            yield "I'm sorry, I encountered an error generating a response."

    async def generate_code(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        code_system_prompt = f"""
        {system_prompt or ''}
        
        You are an expert coding assistant. Please generate code that is:
        - Correct and efficient
        - Well-commented and documented
        - Follows best practices
        - Includes error handling where appropriate
        """
        
        return await self.generate(prompt, code_system_prompt, temperature=0.2)
