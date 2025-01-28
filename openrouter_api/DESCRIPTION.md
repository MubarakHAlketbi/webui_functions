# OpenRouter API Integration for Open WebUI

A Pipe function that integrates OpenRouter's API into Open WebUI, providing access to 300+ AI models from various providers through a single unified API.

## Features

- Access to all OpenRouter-supported models (300+ models)
- Automatic model selection using OpenRouter's NotDiamond algorithm
- Configurable model allowlist
- Support for streaming responses
- Comprehensive error handling
- Provider preferences support (routing, fallbacks, data privacy)

## Configuration

The function uses the following configuration options (Valves):

| Option | Description | Default |
|--------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | `""` |
| `ALLOWED_MODELS` | Space-separated list of allowed model IDs | `""` (all models allowed) |
| `DEFAULT_MODEL` | Default model to use if none specified | `"openai/gpt-3.5-turbo"` |

## How It Works

### Model Discovery

The function automatically fetches available models from OpenRouter and presents them in Open WebUI with the following features:

1. Always includes an "Auto" model option that uses OpenRouter's automatic model selection
2. Prefixes all model IDs with "openrouter." for internal routing
3. Respects the configured allowlist if specified
4. Handles API errors gracefully with informative messages

### Request Processing

When processing chat completion requests:

1. Validates the API key and model permissions
2. Handles both regular and streaming responses
3. Supports provider preferences for custom routing
4. Provides detailed error messages for common issues:
   - Rate limiting
   - API quota exceeded
   - Invalid API key
   - Content moderation
   - Context length exceeded
   - Provider availability
   - Request timeouts

## Usage Examples

### Basic Usage

```python
# Configuration in Open WebUI
OPENROUTER_API_KEY = "your-api-key"
ALLOWED_MODELS = ""  # Allow all models
DEFAULT_MODEL = "openai/gpt-3.5-turbo"
```

### Restricting Models

To restrict available models to specific ones:

```python
# Configuration in Open WebUI
ALLOWED_MODELS = "openai/gpt-3.5-turbo anthropic/claude-3-opus-20240229"
```

### Using Provider Preferences

The function supports OpenRouter's provider preferences for custom routing:

```python
# Example body with provider preferences
{
    "model": "openrouter.mistralai/mixtral-8x7b-instruct",
    "messages": [...],
    "provider": {
        "order": ["Together", "DeepInfra"],
        "allow_fallbacks": false,
        "data_collection": "deny"
    }
}
```

## Error Handling

The function provides detailed error messages for common scenarios:

- Rate limiting: "Rate limit exceeded. Please wait a moment before trying again."
- Quota exceeded: "API quota exceeded. Please check your OpenRouter account."
- Invalid API key: "Invalid API key. Please check your OpenRouter API key."
- Content moderation: "Content was flagged by moderation. Please revise your input."
- Context length: "Input exceeds model's context length. Please reduce the input size."
- Provider unavailable: "Provider service is currently unavailable. Please try again later."
- Request timeout: "Request timed out. The model may be overloaded, please try again."

## Implementation Details

The function is implemented as a Pipe class with three main components:

1. **Valves**: Configuration options for API key, allowed models, and default model
2. **pipes()**: Model discovery and listing
3. **pipe()**: Request processing and response handling

Key features of the implementation:

- Clean separation of concerns
- Comprehensive error handling
- Support for both streaming and regular responses
- Efficient model ID handling and validation
- Flexible provider preference support

## Dependencies

- `requests`: For making HTTP requests to OpenRouter API
- `pydantic`: For configuration management
- Standard Python libraries: `typing`

## Best Practices

1. Always store your API key securely
2. Use the allowlist feature in production to restrict available models
3. Implement proper error handling in your applications
4. Consider using the Auto model for optimal model selection
5. Monitor your API usage through OpenRouter's dashboard

## Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [API Status Page](https://status.openrouter.ai/)