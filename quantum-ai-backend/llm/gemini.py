import google.generativeai as genai
from typing import AsyncGenerator, Optional
from .base import BaseLLMClient
from config.settings import settings

class GeminiClient(BaseLLMClient):
    def __init__(self):
        super().__init__("gemini")
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> Optional[str]:
        try:
            full_prompt = f"{system_prompt or ''}\n\n{prompt}" if system_prompt else prompt
            response = await self.model.generate_content_async(full_prompt, **kwargs)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
    
    async def generate_stream(self, prompt: str, system_prompt: str = None, **kwargs) -> AsyncGenerator[str, None]:
        try:
            full_prompt = f"{system_prompt or ''}\n\n{prompt}" if system_prompt else prompt
            response = await self.model.generate_content_async(full_prompt, stream=True, **kwargs)
            
            async for chunk in response:
                yield chunk.text
        except Exception as e:
            print(f"Gemini API streaming error: {e}")
            yield "I'm sorry, I encountered an error generating a response."
