import requests
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Generator, Union

class Pipe:
    """OpenRouter API integration for open-webui."""
    
    class Valves(BaseModel):
        OPENROUTER_API_KEY: str = Field(
            default="",
            description="API key for authenticating requests to OpenRouter"
        )
        ALLOWED_MODELS: str = Field(
            default="",
            description="Space-separated list of allowed model IDs. Leave empty to allow all models."
        )
        DEFAULT_MODEL: str = Field(
            default="openai/gpt-3.5-turbo",
            description="Default model ID to use if none specified"
        )

    def __init__(self):
        self.valves = self.Valves()
        self.base_url = "https://openrouter.ai/api/v1"

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers for OpenRouter API."""
        return {
            "Authorization": f"Bearer {self.valves.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

    def _get_allowed_models(self) -> List[str]:
        """Get list of allowed models from space-separated string."""
        if not self.valves.ALLOWED_MODELS:
            return []
        return [m.strip() for m in self.valves.ALLOWED_MODELS.split() if m.strip()]

    def pipes(self) -> List[Dict[str, str]]:
        """Return available models from OpenRouter.
        
        Always includes the Auto model as the first option, which uses OpenRouter's
        automatic model selection based on the prompt content. The Auto model chooses
        between high-quality models using NotDiamond's selection algorithm.
        """
        if not self.valves.OPENROUTER_API_KEY:
            return [{"id": "openrouter.error", "name": "API Key not provided"}]
        
        try:
            # Get allowed models list
            allowed = self._get_allowed_models()
            
            # Fetch models from OpenRouter
            response = requests.get(
                f"{self.base_url}/models",
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            # Start with auto model (always available)
            models = [{
                "id": "openrouter.auto",
                "name": "Auto (Selects best model for your prompt)"
            }]
            
            # Add available models
            for model in response.json().get("data", []):
                model_id = model.get("id")
                if not model_id:
                    continue
                    
                # Skip if not in allowed models (when allowed models is specified)
                if allowed and model_id not in allowed:
                    continue
                
                # Add openrouter prefix to model ID
                prefixed_id = f"openrouter.{model_id}"
                
                models.append({
                    "id": prefixed_id,
                    "name": model.get("name", model_id)
                })
            
            return models

        except Exception as e:
            return [{"id": "openrouter.error", "name": f"Error fetching models: {str(e)}"}]

    def pipe(self, body: dict) -> Union[str, Generator[str, None, None]]:
        """Process chat completion requests through OpenRouter API.
        
        Handles both regular models and the Auto model. When using Auto,
        OpenRouter will automatically select the most appropriate model
        based on your prompt content using NotDiamond's selection algorithm.
        """
        if not self.valves.OPENROUTER_API_KEY:
            return "Error: OpenRouter API key not provided"

        try:
            # Get and format model ID
            model = body.get("model", self.valves.DEFAULT_MODEL)
            
            # Handle model ID formatting
            if model.startswith("openrouter."):
                model = model[len("openrouter."):]
            
            # Convert dot to slash for auto model
            if model == "auto":
                model = "openrouter/auto"
            
            # Check if model is allowed (skip check for auto model)
            allowed = self._get_allowed_models()
            if allowed and model != "openrouter/auto" and model not in allowed:
                return f"Error: Model {model} is not allowed"

            # Prepare request
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": model,
                "messages": body.get("messages", []),
                "stream": body.get("stream", False)
            }

            # Add any provider config if specified
            if "provider" in body:
                payload["provider"] = body["provider"]

            # Make request
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                stream=payload["stream"]
            )
            response.raise_for_status()

            # Handle streaming response
            if payload["stream"]:
                def generate():
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith('data: '):
                                line = line[6:]
                                if line == '[DONE]':
                                    break
                                try:
                                    data = requests.json.loads(line)
                                    content = data.get('choices', [{}])[0].get('delta', {}).get('content')
                                    if content:
                                        yield content
                                except requests.json.JSONDecodeError:
                                    continue
                return generate()

            # Handle regular response
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("error", {}).get("message", str(e))
                    
                    if e.response.status_code == 429:
                        return "Rate limit exceeded. Please wait a moment before trying again."
                    elif e.response.status_code == 402:
                        return "API quota exceeded. Please check your OpenRouter account."
                    elif e.response.status_code == 401:
                        return "Invalid API key. Please check your OpenRouter API key."
                    elif e.response.status_code == 400:
                        if "moderation" in error_msg.lower():
                            return "Content was flagged by moderation. Please revise your input."
                        elif "context_length" in error_msg.lower():
                            return "Input exceeds model's context length. Please reduce the input size."
                    elif e.response.status_code == 502:
                        return "Provider service is currently unavailable. Please try again later."
                    elif e.response.status_code == 504:
                        return "Request timed out. The model may be overloaded, please try again."
                    
                    return f"Error: {error_msg}"
                except:
                    return f"Error: {str(e)}"
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error: Unexpected error occurred - {str(e)}"