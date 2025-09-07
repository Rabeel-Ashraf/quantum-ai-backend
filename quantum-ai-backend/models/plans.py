from enum import Enum
from pydantic import BaseModel
from typing import Dict, List, Optional

class PlanName(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class PlanFeatures(BaseModel):
    rate_limit: int
    access_to_agents: List[str]
    max_concurrent_requests: int
    support_level: str
    custom_domains: bool
    sso: bool
    dedicated_support: bool
    uptime_guarantee: float

PLAN_FEATURES = {
    PlanName.FREE: PlanFeatures(
        rate_limit=50,
        access_to_agents=["reviewer", "composer"],
        max_concurrent_requests=1,
        support_level="community",
        custom_domains=False,
        sso=False,
        dedicated_support=False,
        uptime_guarantee=0.95
    ),
    PlanName.BASIC: PlanFeatures(
        rate_limit=100,
        access_to_agents=["reviewer", "composer", "scraper"],
        max_concurrent_requests=3,
        support_level="email",
        custom_domains=False,
        sso=False,
        dedicated_support=False,
        uptime_guarantee=0.99
    ),
    PlanName.PRO: PlanFeatures(
        rate_limit=500,
        access_to_agents=["reviewer", "composer", "scraper", "coder"],
        max_concurrent_requests=10,
        support_level="priority_email",
        custom_domains=True,
        sso=False,
        dedicated_support=False,
        uptime_guarantee=0.995
    ),
    PlanName.PREMIUM: PlanFeatures(
        rate_limit=2000,
        access_to_agents=["reviewer", "composer", "scraper", "coder"],
        max_concurrent_requests=25,
        support_level="priority",
        custom_domains=True,
        sso=True,
        dedicated_support=True,
        uptime_guarantee=0.999
    ),
    PlanName.ENTERPRISE: PlanFeatures(
        rate_limit=10000,
        access_to_agents=["reviewer", "composer", "scraper", "coder"],
        max_concurrent_requests=100,
        support_level="dedicated",
        custom_domains=True,
        sso=True,
        dedicated_support=True,
        uptime_guarantee=0.9999
    )
}

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"
    TRIALING = "trialing"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"

class UserSubscription(BaseModel):
    user_id: str
    plan: PlanName
    status: SubscriptionStatus
    current_period_start: int
    current_period_end: int
    cancel_at_period_end: bool
    stripe_customer_id: str
    stripe_subscription_id: str

class CreateCheckoutSessionRequest(BaseModel):
    plan: PlanName
    success_url: str
    cancel_url: str

class SubscriptionUpdateRequest(BaseModel):
    plan: PlanName
