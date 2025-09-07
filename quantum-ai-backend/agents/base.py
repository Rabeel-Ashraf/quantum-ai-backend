from abc import ABC, abstractmethod
from typing import Optional, AsyncGenerator
from core.cache import cache
from core.prompts import get_agent_prompt

class BaseAgent(ABC):
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.system_prompt = get_agent_prompt(agent_type)
    
    @abstractmethod
    async def process(self, query: str, user_id: str) -> AsyncGenerator[str, None]:
        pass
    
    def get_cache_key(self, query: str, user_id: str) -> str:
        return f"agent:{self.agent_type}:{user_id}:{hash(query)}"
    
    async def get_cached_response(self, query: str, user_id: str) -> Optional[str]:
        key = self.get_cache_key(query, user_id)
        return cache.get(key)
    
    async def set_cached_response(self, query: str, user_id: str, response: str, ttl: int = 3600):
        key = self.get_cache_key(query, user_id)
        cache.set(key, response, ttl)
