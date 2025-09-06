from fastapi import APIRouter, Depends
from redis import Redis
from core.cache import get_redis

router = APIRouter()

@router.get("")
async def health_check(redis: Redis = Depends(get_redis)):
    try:
        # Test Redis connection
        redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "redis": "disconnected", "error": str(e)}
