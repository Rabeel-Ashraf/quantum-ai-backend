import redis
from typing import Optional, Any
import json
from datetime import timedelta
from config.settings import settings

# Global Redis connection
_redis = None

def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            decode_responses=True
        )
    return _redis

class CacheManager:
    def __init__(self):
        self.redis = get_redis()
    
    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        serialized = json.dumps(value)
        return self.redis.setex(key, ttl, serialized)
    
    def delete(self, key: str) -> bool:
        return bool(self.redis.delete(key))
    
    def exists(self, key: str) -> bool:
        return bool(self.redis.exists(key))
    
    def increment(self, key: str) -> int:
        return self.redis.incr(key)
    
    def get_or_set(self, key: str, default_value: Any, ttl: int = 300) -> Any:
        value = self.get(key)
        if value is None:
            self.set(key, default_value, ttl)
            return default_value
        return value

# Global cache instance
cache = CacheManager()
