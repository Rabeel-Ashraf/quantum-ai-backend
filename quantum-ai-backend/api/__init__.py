from fastapi import APIRouter
from .endpoints import chat, health, auth, subscriptions

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
