from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from core.cache import get_redis
from config.settings import settings
import stripe
from models.plans import PLAN_FEATURES

router = APIRouter()

@router.get("")
async def health_check(redis: Redis = Depends(get_redis)):
    try:
        # Test Redis connection
        redis.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"disconnected: {str(e)}"
    
    # Test Stripe connection if configured
    stripe_status = "not_configured"
    if settings.stripe_secret_key:
        try:
            stripe.api_key = settings.stripe_secret_key
            # Make a simple API call to test connection
            stripe.Product.list(limit=1)
            stripe_status = "connected"
        except Exception as e:
            stripe_status = f"error: {str(e)}"
    
    # Check if all required API keys are configured
    api_keys_status = {}
    required_keys = {
        "OPENAI_API_KEY": settings.openai_api_key,
        "GEMINI_API_KEY": settings.gemini_api_key,
        "DEEPSEEK_API_KEY": settings.deepseek_api_key,
        "STRIPE_SECRET_KEY": settings.stripe_secret_key,
        "REDIS_HOST": settings.redis_host
    }
    
    for key_name, key_value in required_keys.items():
        api_keys_status[key_name] = "configured" if key_value else "missing"
    
    # Get system information
    system_info = {
        "version": "1.0.0",
        "debug_mode": settings.debug,
        "host": settings.host,
        "port": settings.port,
        "available_plans": list(PLAN_FEATURES.keys())
    }
    
    # Determine overall status
    overall_status = "healthy"
    if redis_status != "connected" or stripe_status not in ["connected", "not_configured"]:
        overall_status = "degraded"
    if any(status == "missing" for status in api_keys_status.values()):
        overall_status = "degraded"
    
    return {
        "status": overall_status,
        "components": {
            "redis": redis_status,
            "stripe": stripe_status,
            "api_keys": api_keys_status
        },
        "system": system_info
    }

@router.get("/detailed")
async def detailed_health_check(redis: Redis = Depends(get_redis)):
    # Get basic health info
    basic_health = await health_check(redis)
    
    # Add more detailed information
    detailed_info = {
        **basic_health,
        "rate_limits": {
            "basic": settings.basic_rate_limit,
            "pro": settings.pro_rate_limit,
            "premium": settings.premium_rate_limit,
            "enterprise": settings.enterprise_rate_limit
        },
        "plan_features": {plan: features.dict() for plan, features in PLAN_FEATURES.items()}
    }
    
    return detailed_info
