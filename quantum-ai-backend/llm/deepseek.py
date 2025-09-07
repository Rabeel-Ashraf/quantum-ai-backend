import aiohttp
import json
from typing import AsyncGenerator, Optional
from .base import BaseLLMClient
from config.settings import settings

class DeepSeekClient(BaseLLMClient):
    def __init__(self):
        super().__init__("deepseek")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
    
    async def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000)
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        print(f"DeepSeek API error: {response.status}")
                        return None
        except Exception as e:
            print(f"DeepSeek API exception: {e}")
            return None
    
    async def generate_stream(self, prompt: str, system_prompt: str = None, **kwargs) -> AsyncGenerator[str, None]:
        headers = {
            "Authorization": f"Bearer {settings.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000)
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line.startswith(b"data: "):
                                data = line[6:].strip()
                                if data != b"[DONE]":
                                    try:
                                        chunk = json.loads(data)
                                        if "choices" in chunk and chunk["choices"]:
                                            delta = chunk["choices"][0].get("delta", {})
                                            if "content" in delta:
                                                yield delta["content"]
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        yield "I'm sorry, I encountered an error generating a response."
        except Exception as e:
            print(f"DeepSeek API streaming exception: {e}")
            yield "I'm sorry, I encountered an error generating a response."
