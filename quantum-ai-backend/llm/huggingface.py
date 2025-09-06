import aiohttp
import json
from typing import AsyncGenerator, Optional
from .base import BaseLLMClient
from config.settings import settings

class HuggingFaceClient(BaseLLMClient):
    def __init__(self, model_name: str = "google/flan-t5-xxl"):
        super().__init__("huggingface")
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.model_name = model_name
    
    async def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.huggingface_api_key}",
            "Content-Type": "application/json"
        }
        
        full_prompt = f"{system_prompt or ''}\n\n{prompt}" if system_prompt else prompt
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": kwargs.get("max_tokens", 200),
                "temperature": kwargs.get("temperature", 0.7),
                "return_full_text": False
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if isinstance(data, list) and len(data) > 0:
                            return data[0].get("generated_text", "")
                    else:
                        print(f"HuggingFace API error: {response.status}")
                        return None
        except Exception as e:
            print(f"HuggingFace API exception: {e}")
            return None
    
    async def generate_stream(self, prompt: str, system_prompt: str = None, **kwargs) -> AsyncGenerator[str, None]:
        # Hugging Face doesn't support streaming for all models, so we simulate it
        response = await self.generate(prompt, system_prompt, **kwargs)
        if response:
            for word in response.split():
                yield word + " "
                await asyncio.sleep(0.05)
