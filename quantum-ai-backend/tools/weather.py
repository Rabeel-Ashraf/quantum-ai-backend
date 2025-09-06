import aiohttp
import json
from typing import Optional
from config.settings import settings
from core.cache import cache

class WeatherTool:
    def __init__(self):
        self.api_key = settings.weather_api_key
        self.base_url = "http://api.weatherapi.com/v1"
    
    async def get_weather(self, query: str) -> str:
        cache_key = f"weather:{hash(query)}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        if not self.api_key:
            return "Weather API is not configured. Please contact support."
        
        url = f"{self.base_url}/current.json?key={self.api_key}&q={query}&aqi=no"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        location = data.get("location", {})
                        current = data.get("current", {})
                        
                        location_name = location.get("name", "Unknown location")
                        country = location.get("country", "Unknown country")
                        temp_c = current.get("temp_c", "Unknown")
                        condition = current.get("condition", {}).get("text", "Unknown conditions")
                        humidity = current.get("humidity", "Unknown")
                        wind_kph = current.get("wind_kph", "Unknown")
                        
                        result = f"Weather in {location_name}, {country}:\n"
                        result += f"Temperature: {temp_c}°C\n"
                        result += f"Conditions: {condition}\n"
                        result += f"Humidity: {humidity}%\n"
                        result += f"Wind: {wind_kph} km/h\n"
                        
                        cache.set(cache_key, result, 1800)  # Cache for 30 minutes
                        return result
                    else:
                        return f"Failed to fetch weather. API returned status {response.status}."
        except Exception as e:
            return f"Error fetching weather: {str(e)}"
