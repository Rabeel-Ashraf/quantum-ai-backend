# Quantum AI Backend

A cutting-edge multi-agent AI platform with backend orchestration, multi-LLM integration, and monetization support.

## Setup Instructions

1. Run the setup script: `./setup.sh`
2. Update the `.env` file with your API keys and configuration
3. Start the server: `python main.py`

## Project Structure

- `config/`: Configuration settings and prompts
- `api/`: FastAPI endpoints and routes
- `core/`: Core functionality (rate limiting, caching, security)
- `agents/`: Multi-agent system implementation
- `llm/`: LLM provider integrations
- `tools/`: External API integrations
- `models/`: Pydantic models and schemas
- `utils/`: Utility functions and helpers
- `services/`: External service integrations (Stripe)

## API Documentation

Once the server is running, access the API documentation at:
http://localhost:8000/docs

## Monetization Plans

The system supports multiple subscription tiers:
- Free: 50 requests/hour, basic agents
- Basic: 100 requests/hour, all agents
- Pro: 500 requests/hour, priority support
- Premium: 2000 requests/hour, custom domains
- Enterprise: 10000 requests/hour, dedicated support

## Environment Variables

Update the `.env` file with your:
- API keys for LLM providers (OpenAI, Gemini, DeepSeek, etc.)
- External API keys (News, Weather, Search)
- Stripe credentials for payment processing
- Redis connection details
- Security settings
