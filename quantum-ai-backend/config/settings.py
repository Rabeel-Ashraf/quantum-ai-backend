import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "default-secret-key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Redis
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    
    # LLM APIs
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    
    # External APIs
    news_api_key: str = os.getenv("NEWS_API_KEY", "")
    weather_api_key: str = os.getenv("WEATHER_API_KEY", "")
    search_api_key: str = os.getenv("SEARCH_API_KEY", "")
    
    # Vector Database
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "")
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", 6333))
    
    # Rate Limiting
    default_rate_limit: int = int(os.getenv("DEFAULT_RATE_LIMIT", 60))
    premium_rate_limit: int = int(os.getenv("PREMIUM_RATE_LIMIT", 300))
    agent_rate_limit: int = int(os.getenv("AGENT_RATE_LIMIT", 1000))
    basic_rate_limit: int = int(os.getenv("BASIC_RATE_LIMIT", 100))
    pro_rate_limit: int = int(os.getenv("PRO_RATE_LIMIT", 500))
    premium_rate_limit: int = int(os.getenv("PREMIUM_RATE_LIMIT", 2000))
    enterprise_rate_limit: int = int(os.getenv("ENTERPRISE_RATE_LIMIT", 10000))
    
    # Stripe
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    stripe_price_basic: str = os.getenv("STRIPE_PRICE_BASIC", "")
    stripe_price_pro: str = os.getenv("STRIPE_PRICE_PRO", "")
    stripe_price_premium: str = os.getenv("STRIPE_PRICE_PREMIUM", "")
    stripe_price_enterprise: str = os.getenv("STRIPE_PRICE_ENTERPRISE", "")
    
    class Config:
        env_file = ".env"

settings = Settings()
