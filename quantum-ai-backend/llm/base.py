from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional
from core.cache import cache

class BaseLLMClient(ABC):
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
    
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> Optional[str]:
        pass
    
    @abstractmethod
    async def generate_stream(self, prompt: str, system_prompt: str = None, **kwargs) -> AsyncGenerator[str, None]:
        pass
    
    def get_cache_key(self, prompt: str) -> str:
        return f"llm:{self.provider_name}:{hash(prompt)}"
    
    async def get_cached_response(self, prompt: str) -> Optional[str]:
        key = self.get_cache_key(prompt)
        return cache.get(key)
    
    async def set_cached_response(self, prompt: str, response: str, ttl: int = 3600):
        key = self.get_cache_key(prompt)
        cache.set(key, response, ttl)
