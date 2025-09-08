# Quantum AI Backend

A cutting-edge multi-agent AI platform with backend orchestration, multi-LLM integration, monetization support, and intelligent model selection.

## New Features in Version 2.0

### Intelligent Model Selection
The system now automatically selects the most appropriate LLM based on query type:
- **Code-related queries**: Prefers OpenAI Codex
- **Fact-checking queries**: Prefers Google Gemini
- **Conversational queries**: Prefers DeepSeek Qwen
- **General queries**: Uses configured default model

### Enhanced Orchestration
- Multi-agent coordination with intelligent routing
- Dynamic model selection based on query content
- Fallback mechanisms for rate-limited or unavailable models
- Real-time streaming of responses

### Improved Rate Limiting
- Token-bucket algorithm for smooth rate limiting
- Plan-based rate limits (Free, Basic, Pro, Premium, Enterprise)
- Model-specific rate limiting to prevent API overuse
- Graceful fallback to alternative models when limits are exceeded

## Setup Instructions

1. Run the setup script: `./setup.sh`
2. Update the `.env` file with your API keys and configuration
3. Start the server: `python main.py`

## Project Structure

- `config/`: Configuration settings and prompts
- `api/`: FastAPI endpoints and routes
- `core/`: Core functionality (orchestration, rate limiting, caching, security)
- `agents/`: Multi-agent system implementation
- `llm/`: LLM provider integrations
- `tools/`: External API integrations
- `models/`: Pydantic models and schemas
- `utils/`: Utility functions and helpers
- `services/`: External service integrations (Stripe)

## API Documentation

Once the server is running, access the API documentation at:
http://localhost:8000/docs

## Model Selection Configuration

The system uses the following environment variables for model selection:

- `DEFAULT_MODEL`: Default model for general queries (default: "openai")
- `CODE_MODEL`: Preferred model for code-related queries (default: "openai")
- `FACT_CHECK_MODEL`: Preferred model for fact-checking (default: "gemini")
- `CONVERSATIONAL_MODEL`: Preferred model for conversational queries (default: "deepseek")

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
- Model selection preferences
