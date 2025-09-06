import re
import asyncio
from typing import List, Dict, Any

def extract_urls(text: str) -> List[str]:
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&]*')
    return url_pattern.findall(text)

def sanitize_input(text: str) -> str:
    # Remove potentially harmful characters or patterns
    sanitized = re.sub(r'[<>{}`]', '', text)
    return sanitized[:1000]  # Limit length

async def async_retry(func, max_retries=3, delay=1, backoff=2, exceptions=(Exception,)):
    retries = 0
    while retries < max_retries:
        try:
            return await func()
        except exceptions as e:
            retries += 1
            if retries >= max_retries:
                raise e
            await asyncio.sleep(delay)
            delay *= backoff

def format_agent_response(agent_name: str, response: str) -> str:
    return f"[{agent_name.upper()}]: {response}"
