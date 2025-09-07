from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Optional
import asyncio
import json

from api.dependencies import get_current_user, get_rate_limiter_with_plan
from core.rate_limiter import RateLimiter
from agents.scraper import ScraperAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from agents.composer import ComposerAgent
from models.schemas import ChatRequest
from models.responses import StreamingResponseChunk
from models.plans import PLAN_FEATURES, PlanName

router = APIRouter()

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
    user_features = PLAN_FEATURES.get(PlanName(user_plan), PLAN_FEATURES[PlanName.FREE])
    
    agents_to_use = determine_agents(request.message)
    for agent in agents_to_use:
        if agent not in user_features.access_to_agents:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Your current plan ({user_plan}) does not include access to the {agent} agent."
            )
    
    async def generate_stream():
        # Initialize agents
        scraper = ScraperAgent() if "scraper" in agents_to_use else None
        coder = CoderAgent() if "coder" in agents_to_use else None
        reviewer = ReviewerAgent()
        composer = ComposerAgent()
        
        # Execute agents in parallel
        tasks = []
        if scraper:
            tasks.append(scraper.process(request.message, user_id))
        if coder:
            tasks.append(coder.process(request.message, user_id))
        
        # Wait for all agent tasks to complete
        agent_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = []
        for result in agent_results:
            if not isinstance(result, Exception):
                valid_results.append(result)
        
        # Review results
        reviewed_results = []
        for result in valid_results:
            reviewed = await reviewer.process(result, request.message, user_id)
            reviewed_results.append(reviewed)
        
        # Compose final response
        final_response = await composer.process(reviewed_results, request.message, user_id)
        
        # Stream the response
        for chunk in final_response:
            yield f"data: {json.dumps({'content': chunk, 'type': 'chunk'})}\n\n"
            await asyncio.sleep(0.01)  # Small delay to simulate streaming
        
        yield f"data: {json.dumps({'content': '', 'type': 'complete'})}\n\n"
    
    return StreamingResponse(
        generate_stream(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering for nginx
        }
    )

def determine_agents(query: str) -> list:
    query_lower = query.lower()
    agents = []
    
    # Check if we need scraper agent (for real-time information)
    if any(keyword in query_lower for keyword in [
        "news", "weather", "latest", "current", "today", "recent", "update"
    ]):
        agents.append("scraper")
    
    # Check if we need coder agent (for code-related queries)
    if any(keyword in query_lower for keyword in [
        "code", "program", "function", "algorithm", "python", "javascript", 
        "java", "c++", "html", "css", "sql", "debug", "fix", "error"
    ]):
        agents.append("coder")
    
    # Always use reviewer and composer
    agents.extend(["reviewer", "composer"])
    
    return list(set(agents))  # Remove duplicates
