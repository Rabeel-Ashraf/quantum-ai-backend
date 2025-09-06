# Add to the Settings class in config/settings.py
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Stripe
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    stripe_price_basic: str = os.getenv("STRIPE_PRICE_BASIC", "")
    stripe_price_pro: str = os.getenv("STRIPE_PRICE_PRO", "")
    stripe_price_premium: str = os.getenv("STRIPE_PRICE_PREMIUM", "")
    stripe_price_enterprise: str = os.getenv("STRIPE_PRICE_ENTERPRISE", "")
    
    # Plan configurations
    basic_rate_limit: int = int(os.getenv("BASIC_RATE_LIMIT", 100))
    pro_rate_limit: int = int(os.getenv("PRO_RATE_LIMIT", 500))
    premium_rate_limit: int = int(os.getenv("PREMIUM_RATE_LIMIT", 2000))
    enterprise_rate_limit: int = int(os.getenv("ENTERPRISE_RATE_LIMIT", 10000))
    
    # ... rest of the class ...
