from pydantic import BaseModel
from typing import Optional, List

class StreamingResponseChunk(BaseModel):
    content: str
    type: str  # 'chunk' or 'complete'

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    sources: Optional[List[str]] = None

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    redis: str
    details: Optional[dict] = None
