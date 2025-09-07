from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional, Tuple
from core.rate_limiter import RateLimiter
from core.cache import get_redis
from config.settings import settings

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Tuple[str, str]:
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        user_plan: str = payload.get("plan", "free")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id, user_plan
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_rate_limiter():
    redis = get_redis()
    return RateLimiter(redis)

async def get_rate_limiter_with_plan(
    user_info: Tuple[str, str] = Depends(get_current_user)
):
    user_id, user_plan = user_info
    redis = get_redis()
    rate_limiter = RateLimiter(redis)
    return rate_limiter, user_id, user_plan
