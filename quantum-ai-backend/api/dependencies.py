# Update get_current_user to extract plan from token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        user_plan: str = payload.get("plan", "free")  # Extract plan from token
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id, user_plan  # Return both user_id and plan
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Update the rate limiter dependency
async def get_rate_limiter_with_plan(
    user_info: tuple = Depends(get_current_user)
):
    user_id, user_plan = user_info
    redis = get_redis()
    rate_limiter = RateLimiter(redis)
    return rate_limiter, user_id, user_plan
