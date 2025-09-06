# Update the RateLimiter class to consider user plans
class RateLimiter:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.memory_limiter = Limiter(MemoryStorage())
    
    def get_user_rate_limit(self, user_plan: str) -> int:
        from models.plans import PlanName
        from config.settings import settings
        
        plan_limits = {
            PlanName.FREE: 50,
            PlanName.BASIC: settings.basic_rate_limit,
            PlanName.PRO: settings.pro_rate_limit,
            PlanName.PREMIUM: settings.premium_rate_limit,
            PlanName.ENTERPRISE: settings.enterprise_rate_limit
        }
        
        return plan_limits.get(user_plan, 50)  # Default to free plan
    
    async def is_allowed(self, user_id: str, user_plan: str) -> bool:
        rate_limit = self.get_user_rate_limit(user_plan)
        key = f"rate_limit:{user_id}"
        
        # Get current count
        current = self.redis.get(key)
        if current is None:
            # Set initial value with expiration
            self.redis.setex(key, 60, 1)
            return True
        
        current_count = int(current)
        if current_count >= rate_limit:
            return False
        
        # Increment count
        self.redis.incr(key)
        return True
    
    def get_remaining_requests(self, user_id: str, user_plan: str) -> int:
        rate_limit = self.get_user_rate_limit(user_plan)
        key = f"rate_limit:{user_id}"
        
        current = self.redis.get(key)
        if current is None:
            return rate_limit
        
        current_count = int(current)
        return max(0, rate_limit - current_count)
