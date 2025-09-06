import stripe
from typing import Dict, Optional
from fastapi import HTTPException, status
from config.settings import settings
from models.plans import PlanName, UserSubscription, SubscriptionStatus

stripe.api_key = settings.stripe_secret_key

class StripeService:
    def __init__(self):
        self.webhook_secret = settings.stripe_webhook_secret
    
    def get_price_id(self, plan: PlanName) -> str:
        price_map = {
            PlanName.BASIC: settings.stripe_price_basic,
            PlanName.PRO: settings.stripe_price_pro,
            PlanName.PREMIUM: settings.stripe_price_premium,
            PlanName.ENTERPRISE: settings.stripe_price_enterprise
        }
        return price_map.get(plan)
    
    async def create_checkout_session(self, user_id: str, plan: PlanName, 
                                    success_url: str, cancel_url: str) -> Dict:
        try:
            price_id = self.get_price_id(plan)
            if not price_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Price not configured for plan {plan}"
                )
            
            # Create a new Stripe customer
            customer = stripe.Customer.create(
                metadata={"user_id": user_id}
            )
            
            session = stripe.checkout.Session.create(
                customer=customer.id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "user_id": user_id,
                    "plan": plan
                }
            )
            
            return {"session_id": session.id, "session_url": session.url}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create checkout session: {str(e)}"
            )
    
    async def create_portal_session(self, stripe_customer_id: str) -> Dict:
        try:
            session = stripe.billing_portal.Session.create(
                customer=stripe_customer_id,
                return_url="https://your-domain.com/account"
            )
            return {"url": session.url}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create portal session: {str(e)}"
            )
    
    async def handle_webhook(self, payload: bytes, sig_header: str):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid payload: {str(e)}"
            )
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid signature: {str(e)}"
            )
        
        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            await self.handle_checkout_session(session)
        elif event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']
            await self.handle_subscription_updated(subscription)
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            await self.handle_subscription_deleted(subscription)
        
        return {"status": "success"}
    
    async def handle_checkout_session(self, session):
        user_id = session.metadata.get('user_id')
        plan = session.metadata.get('plan')
        stripe_customer_id = session.customer
        stripe_subscription_id = session.subscription
        
        # Here you would save this to your database
        # For now, we'll just print
        print(f"User {user_id} subscribed to {plan} plan")
    
    async def handle_subscription_updated(self, subscription):
        stripe_customer_id = subscription.customer
        stripe_subscription_id = subscription.id
        status = subscription.status
        
        # Update user subscription in database
        print(f"Subscription {stripe_subscription_id} updated to status {status}")
    
    async def handle_subscription_deleted(self, subscription):
        stripe_customer_id = subscription.customer
        stripe_subscription_id = subscription.id
        
        # Update user subscription in database
        print(f"Subscription {stripe_subscription_id} deleted")
    
    async def cancel_subscription(self, stripe_subscription_id: str):
        try:
            deleted_subscription = stripe.Subscription.delete(stripe_subscription_id)
            return {"status": "canceled", "subscription": deleted_subscription.id}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel subscription: {str(e)}"
            )

# Global instance
stripe_service = StripeService()
