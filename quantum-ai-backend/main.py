from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api import api_router
from core.cache import get_redis
from config.settings import settings
from utils.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Quantum AI Backend")
    redis = get_redis()
    try:
        redis.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
    
    # Initialize Stripe (if configured)
    if settings.stripe_secret_key:
        try:
            import stripe
            stripe.api_key = settings.stripe_secret_key
            logger.info("Stripe initialized successfully")
        except Exception as e:
            logger.error(f"Stripe initialization failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Quantum AI Backend")
    redis.close()

app = FastAPI(
    title="Quantum AI Backend",
    description="A cutting-edge multi-agent AI platform with monetization support",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Quantum AI Backend is running",
        "version": "1.0.0",
        "docs": "/docs",
        "subscription_plans": "/api/v1/subscriptions/plans"
    }

@app.get("/health")
async def health_check():
    redis = get_redis()
    try:
        redis.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"disconnected: {str(e)}"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "stripe": "configured" if settings.stripe_secret_key else "not_configured"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )
