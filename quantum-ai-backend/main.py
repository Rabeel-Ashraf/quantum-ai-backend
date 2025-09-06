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

    yield

    # Shutdown
    logger.info("Shutting down Quantum AI Backend")
    redis.close()

app = FastAPI(
    title="Quantum AI Backend",
    description="A cutting-edge multi-agent AI platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )
