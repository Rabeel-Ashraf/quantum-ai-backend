import aiohttp
from bs4 import BeautifulSoup
from typing import Optional
from core.cache import cache

class WebScraper:
    async def scrape_url(self, url: str) -> Optional[str]:
        cache_key = f"scraped:{hash(url)}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Remove unwanted elements
                        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                            element.decompose()
                        
                        # Get text content
                        text = soup.get_text()
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        # Limit length
                        if len(text) > 2000:
                            text = text[:2000] + "..."
                        
                        cache.set(cache_key, text, 86400)  # Cache for 24 hours
                        return text
                    else:
                        return None
        except Exception as e:
            print(f"Scraping error: {e}")
            return None
