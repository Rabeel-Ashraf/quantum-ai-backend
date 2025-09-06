# Update the chat endpoint to use the new rate limiter dependency
@router.post("")
async def chat_endpoint(
    request: ChatRequest,
    user_info: tuple = Depends(get_current_user),
    rate_limiter_info: tuple = Depends(get_rate_limiter_with_plan)
):
    user_id, user_plan = user_info
    rate_limiter, _, _ = rate_limiter_info
    
    # Check rate limits with user's plan
    if not await rate_limiter.is_allowed(user_id, user_plan):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    
    # Check if user has access to requested agents
    from models.plans import PLAN_FEATURES, PlanName
    user_features = PLAN_FEATURES.get(PlanName(user_plan), PLAN_FEATURES[PlanName.FREE])
    
    agents_to_use = determine_agents(request.message)
    for agent in agents_to_use:
        if agent not in user_features.access_to_agents:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Your current plan ({user_plan}) does not include access to the {agent} agent."
            )
    
    # ... rest of the function remains the same
