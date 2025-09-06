from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any
from api.dependencies import get_current_user
from services.stripe_service import stripe_service
from models.plans import CreateCheckoutSessionRequest, SubscriptionUpdateRequest

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session(
    request: CreateCheckoutSessionRequest,
    user_id: str = Depends(get_current_user)
):
    try:
        session = await stripe_service.create_checkout_session(
            user_id, request.plan, request.success_url, request.cancel_url
        )
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/create-portal-session")
async def create_portal_session(
    user_id: str = Depends(get_current_user)
):
    # In a real implementation, you'd get the stripe_customer_id from your database
    # For now, we'll use a mock
    stripe_customer_id = "cus_mock_customer_id"
    
    try:
        session = await stripe_service.create_portal_session(stripe_customer_id)
        return session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/webhook")
async def webhook_received(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        return await stripe_service.handle_webhook(payload, sig_header)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/plans")
async def get_available_plans():
    from models.plans import PLAN_FEATURES, PlanName
    return {
        plan: features.dict() for plan, features in PLAN_FEATURES.items()
    }

@router.get("/subscription")
async def get_user_subscription(
    user_id: str = Depends(get_current_user)
):
    # In a real implementation, you'd get this from your database
    # For now, we'll return a mock response
    return {
        "plan": "free",
        "status": "active",
        "current_period_end": 1735689600,  # Unix timestamp
        "cancel_at_period_end": False
    }

@router.post("/cancel-subscription")
async def cancel_subscription(
    user_id: str = Depends(get_current_user)
):
    # In a real implementation, you'd get the subscription ID from your database
    stripe_subscription_id = "sub_mock_subscription_id"
    
    try:
        result = await stripe_service.cancel_subscription(stripe_subscription_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
