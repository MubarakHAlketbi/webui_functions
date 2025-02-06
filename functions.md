
# Open WebUI Functions Documentation

This document provides a comprehensive guide to Open WebUI Functions, explaining their types, usage, and implementation details.

---

## What Are Functions?

Functions are essentially plugins for OpenWebUI, extending its capabilities. They allow for:

*   Adding support for new AI model providers (e.g., Anthropic, Vertex AI).
*   Modifying message processing.
*   Introducing custom buttons to the interface.

Functions are built-in and run within the OpenWebUI environment, making them fast, modular, and independent of external dependencies. They are written in pure Python, offering high customizability.

---

## 🏗️ Types of Functions

OpenWebUI offers three types of Functions:

1.  **Pipe Function:** Creates custom "Agents/Models" or integrations, appearing as standalone models in the interface.
2.  **Filter Function:** Modifies inputs and outputs, acting as "hooks" in the workflow.
3.  **Action Function:** Adds custom buttons to the chat interface for interactive shortcuts.

### 1. Pipe Function – Create Custom "Agents/Models"

A Pipe Function allows you to create custom agents/models or integrations. These appear in the OpenWebUI interface as if they were standalone models.

**What does it do?**

*   Defines complex workflows.  For example, sending data to multiple models (Model A and Model B), processing their outputs, and combining the results.
*   Can interact with non-AI systems like search APIs, weather data providers, or systems like Home Assistant.

**Use case example:**

Querying Google Search directly from OpenWebUI:

1.  Takes the user's message as the search query.
2.  Sends the query to Google Search's API.
3.  Processes the response and returns it within the WebUI like a normal model response.

**Enabling:** When enabled, Pipe Functions appear as selectable models.

**Detailed Guide:** [Pipe Functions](#pipe-function-create-custom-agentsmodels) (See below)

### 2. Filter Function – Modify Inputs and Outputs

A Filter Function modifies data before it's sent to the AI model (input) or after it comes back (output).

**What does it do?**

*   **Inlet:** Adjusts the input sent to the model (e.g., adding instructions, keywords, or formatting).
*   **Outlet:** Modifies the output received from the model (e.g., cleaning up the response, adjusting tone, or formatting).

**Use case example:**

Ensuring precise formatting for a project:

1.  Transforms input into the required format.
2.  Cleans up the model's output before display.

**Enabling:** Filters can be linked to specific models or enabled globally for all models.

**Detailed Guide:** [Filter Functions](#filter-function-modify-inputs-and-outputs) (See below)

### 3. Action Function – Add Custom Buttons

An Action Function adds custom buttons to the chat interface, appearing beneath individual chat messages.

**What does it do?**

*   Defines interactive shortcuts that trigger specific functionality.

**Use case example:**

Adding a "Summarize" button:

1.  Adds a "Summarize" button under every incoming message.
2.  When clicked, triggers a custom function to process the message and return a summary.

**Detailed Guide:** [Action Functions](#action-function) (See below)

---

## 🛠️ How to Use Functions

1.  **Install Functions:** Install via the OpenWebUI interface or by importing manually.  Find community-created functions on the OpenWebUI Community Site.
    *   **⚠️ Caution:** Only install Functions from trusted sources due to security risks.

2.  **Enable Functions:** Functions must be explicitly enabled after installation.
    *   Pipe Functions become available as models.
    *   Filter and Action Functions need to be assigned to specific models or enabled globally.

3.  **Assign Filters or Actions to Models:**
    *   Navigate to `Workspace => Models` and assign the Function.
    *   Alternatively, enable globally via `Workspace => Functions`, select the "..." menu, and toggle the `Global` switch.

**Quick Summary:**

*   **Pipes:** Standalone models.
*   **Filters:** Modify inputs/outputs.
*   **Actions:** Add clickable buttons.

---

## ✅ Why Use Functions?

*   **Extend:** Add new models or integrate with external tools (APIs, databases, smart devices).
*   **Optimize:** Tweak inputs and outputs.
*   **Simplify:** Add buttons/shortcuts for an intuitive interface.

---

## Pipe Function: Create Custom "Agents/Models"

This section provides a detailed guide on creating Pipe Functions in Open WebUI.

### Introduction to Pipes

Pipes are analogous to plugins that introduce new data pathways and custom logic within Open WebUI.  They allow you to create custom models with specific behaviors.

### Understanding the Pipe Structure

A basic Pipe structure:

```python
from pydantic import BaseModel, Field

class Pipe:
    class Valves(BaseModel):
        MODEL_ID: str = Field(default="")

    def __init__(self):
        self.valves = self.Valves()

    def pipe(self, body: dict):
        # Logic goes here
        print(self.valves, body)  # Prints configuration and input
        return "Hello, World!"
```

**The `Pipe` Class:**

*   Defines the custom logic and acts as the blueprint for the plugin.

**`Valves` (Configuration):**

*   A nested class inheriting from `BaseModel`.
*   Contains configuration options (parameters) that persist across the Pipe's use.
*   Example: `MODEL_ID` is a configuration option.
*   Think of `Valves` as knobs controlling the data flow.

**The `__init__` Method:**

*   The constructor method.
*   Initializes the Pipe's state, primarily setting up `self.valves`.

**The `pipe` Function:**

*   The core function containing the custom logic.
*   `body`: A dictionary containing the input data.
*   Processes the input and returns the result.

**Note:**  The recommended structure is `Valves`, then `__init__`, then `pipe`.

### Creating Multiple Models with Pipes (Manifolds)

To create multiple models from a single Pipe, define a `pipes` function or variable within the `Pipe` class:

```python
from pydantic import BaseModel, Field

class Pipe:
    class Valves(BaseModel):
        MODEL_ID: str = Field(default="")

    def __init__(self):
        self.valves = self.Valves()

    def pipes(self):
        return [
            {"id": "model_id_1", "name": "model_1"},
            {"id": "model_id_2", "name": "model_2"},
            {"id": "model_id_3", "name": "model_3"},
        ]

    def pipe(self, body: dict):
        # Logic goes here
        print(self.valves, body)
        model = body.get("model", "")
        return f"{model}: Hello, World!"
```

**`pipes` Function:**

*   Returns a list of dictionaries, each representing a model with `id` and `name`.
*   These models appear individually in the OpenWebUI model selector.

**Updated `pipe` Function:**

*   Processes input based on the selected model.

### Example: OpenAI Proxy Pipe

This example creates a Pipe that proxies requests to the OpenAI API:

```python
from pydantic import BaseModel, Field
import requests

class Pipe:
    class Valves(BaseModel):
        NAME_PREFIX: str = Field(
            default="OPENAI/",
            description="Prefix to be added before model names.",
        )
        OPENAI_API_BASE_URL: str = Field(
            default="https://api.openai.com/v1",
            description="Base URL for accessing OpenAI API endpoints.",
        )
        OPENAI_API_KEY: str = Field(
            default="",
            description="API key for authenticating requests to the OpenAI API.",
        )

    def __init__(self):
        self.valves = self.Valves()

    def pipes(self):
        if self.valves.OPENAI_API_KEY:
            try:
                headers = {
                    "Authorization": f"Bearer {self.valves.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                }
                r = requests.get(
                    f"{self.valves.OPENAI_API_BASE_URL}/models", headers=headers
                )
                models = r.json()
                return [
                    {
                        "id": model["id"],
                        "name": f'{self.valves.NAME_PREFIX}{model.get("name", model["id"])}',
                    }
                    for model in models["data"]
                    if "gpt" in model["id"]
                ]
            except Exception as e:
                return [
                    {
                        "id": "error",
                        "name": "Error fetching models.  Check your API Key.",
                    },
                ]
        else:
            return [
                {
                    "id": "error",
                    "name": "API Key not provided.",
                },
            ]

    def pipe(self, body: dict, **user: dict):
        print(f"pipe:{__name__}")
        headers = {
            "Authorization": f"Bearer {self.valves.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        # Extract model id from the model name
        model_id = body["model"][body["model"].find(".") + 1 :]
        # Update the model id in the body
        payload = {**body, "model": model_id}
        try:
            r = requests.post(
                url=f"{self.valves.OPENAI_API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                stream=True,
            )
            r.raise_for_status()
            if body.get("stream", False):
                return r.iter_lines()
            else:
                return r.json()
        except Exception as e:
            return f"Error: {e}"
```

**Detailed Breakdown:**

*   **`Valves` Configuration:**  `NAME_PREFIX`, `OPENAI_API_BASE_URL`, `OPENAI_API_KEY`.
*   **`pipes` Function:** Fetches available OpenAI models, filters for models with "gpt" in their ID, and handles errors.
*   **`pipe` Function:** Handles requests to the selected OpenAI model, extracts the model ID, prepares the payload, makes the API request, and handles streaming.

### Extending the Proxy Pipe

This proxy Pipe can be modified to support other providers (Anthropic, Perplexity, etc.) by adjusting API endpoints, headers, and logic.

### Using Internal Open WebUI Functions

You can leverage internal Open WebUI functions:

```python
from pydantic import BaseModel, Field
from fastapi import Request
from open_webui.models.users import Users
from open_webui.utils.chat import generate_chat_completion

class Pipe:
    def __init__(self):
        pass

    async def pipe(
        self,
        body: dict,
        **user: dict,
        **request: Request,
    ) -> str:
        # Use the unified endpoint with the updated signature
        user = Users.get_user_by_id(user["id"])
        body["model"] = "llama3.2:latest"  # Example model
        return await generate_chat_completion(request, body, user)
```

**Explanation:**

*   Imports `Users` and `generate_chat_completion`.
*   The `pipe` function fetches the user object, sets the model, and calls `generate_chat_completion`.

**Important Notes:**

*   Refer to the latest Open WebUI codebase for accurate function signatures.
*   Handle exceptions and errors gracefully.

### Frequently Asked Questions (Pipe Functions)

*   **Q1: Why should I use Pipes in Open WebUI?**  To add new models with custom logic and processing.
*   **Q2: What are Valves, and why are they important?**  Configurable parameters of your Pipe.
*   **Q3: Can I create a Pipe without Valves?**  Yes, but `Valves` are good practice for flexibility.
*   **Q4: How do I ensure my Pipe is secure when using API keys?**  Use `Valves` to input and store API keys securely.
*   **Q5: What is the difference between the `pipe` and `pipes` functions?**  `pipe` handles logic for a single model; `pipes` allows representing multiple models.
*   **Q6: How can I handle errors in my Pipe?**  Use `try-except` blocks.
*   **Q7: Can I use external libraries in my Pipe?**  Yes.
*   **Q8: How do I test my Pipe?**  Run Open WebUI in a development environment and select your custom model.
*   **Q9: Are there any best practices for organizing my Pipe's code?**  Keep `Valves` at the top, initialize in `__init__`, and place `pipe` after `__init__`.
*   **Q10: Where can I find the latest Open WebUI documentation?**  Visit the official Open WebUI repository.

---

## Filter Function: Modify Inputs and Outputs

This section details Filter Functions in Open WebUI.

### 🌊 What Are Filters in Open WebUI?

Filters modify data flowing to and from models. They act as checkpoints for adjustments.

**Key Functions:**

*   **Modify User Inputs (`inlet` Function):** Tweak input data before it reaches the AI model.
*   **Modify Model Outputs (`outlet` Function):** Adjust the AI's response before showing it to the user.

**Key Concept:** Filters are *not* standalone models but tools to enhance data.

### 🗺️ Structure of a Filter Function: The Skeleton

```python
from pydantic import BaseModel
from typing import Optional

class Filter:
    # Valves: Configuration options for the filter
    class Valves(BaseModel):
        pass

    def __init__(self):
        # Initialize valves (optional configuration for the Filter)
        self.valves = self.Valves()

    def inlet(self, body: dict) -> dict:
        # This is where you manipulate user inputs.
        print(f"inlet called: {body}")
        return body

    def outlet(self, body: dict) -> None:
        # This is where you manipulate model outputs.
        print(f"outlet called: {body}")
        return body
```

**🎯 Key Components Explained:**

1.  **`Valves` Class (Optional Settings):**  Configuration options for the filter.

2.  **`inlet` Function (Input Pre-Processing):**
    *   **Input:** `body` (the raw input from OpenWebUI).
    *   **Task:** Modify and return the `body`.
    *   **Why Use `inlet`?**
        *   Adding Context: Append information to the user's input.
        *   Formatting Data: Transform input into a specific format (JSON, Markdown).
        *   Sanitizing Input: Remove unwanted characters.
        *   Streamlining User Input: Inject clarifying instructions.

    **Example 1: Adding System Context:**

    ```python
    def inlet(self, body: dict, **user: Optional[dict] = None) -> dict:
        context_message = {
            "role": "system",
            "content": "You are helping the user prepare an Italian meal."
        }
        body.setdefault("messages", []).insert(0, context_message)
        return body
    ```

    **Example 2: Cleaning Input:**

    ```python
    def inlet(self, body: dict, **user: Optional[dict] = None) -> dict:
        last_message = body["messages"][-1]["content"]
        body["messages"][-1]["content"] = last_message.replace("!!!", "").strip()
        return body
    ```

3.  **`outlet` Function (Output Post-Processing):**
    *   **Input:** `body` (all current messages in the chat).
    *   **Task:** Modify the `body`.
    *   **Best Practices:** Prefer logging over direct edits in the `outlet`.

    **Example: Strip out sensitive API responses:**
     ```python
    def outlet(self, body: dict, **user**: Optional[dict] = None) -> dict:
        for message in body["messages"]:
            message["content"] = message["content"].replace("<API_KEY>", "[REDACTED]")
        return body
     ```

### 🌟 Filters in Action: Building Practical Examples

**Example #1: Add Context to Every User Input:**

```python
class Filter:
    def inlet(self, body: dict, **user: Optional[dict] = None) -> dict:
        context_message = {
            "role": "system",
            "content": "You're a software troubleshooting assistant."
        }
        body.setdefault("messages", []).insert(0, context_message)
        return body
```

**Example #2: Highlight Outputs for Easy Reading:**

```python
class Filter:
    def outlet(self, body: dict, **user: Optional[dict] = None) -> dict:
        for message in body["messages"]:
            if message["role"] == "assistant":
                message["content"] = f"**{message['content']}**"
        return body
```

### 🚧 Potential Confusion: Clear FAQ (Filter Functions)

*   **Q: How Are Filters Different From Pipe Functions?** Filters modify data; Pipes integrate external APIs or significantly transform backend operations.
*   **Q: Can I Do Heavy Post-Processing Inside `outlet`?**  You can, but it's not best practice. Use a Pipe Function instead.

---

## Action Function

Action functions add custom buttons to the message toolbar.

### Action

Creates a button in the Message UI (underneath individual chat messages).

**Example:**

```python
async def action(
    self,
    body: dict,
    **user=None,
    __event_emitter__=None,
    __event_call__=None,
) -> Optional[dict]:
    print(f"action:{__name__}")
    response = await __event_call__(
        {
            "type": "input",
            "data": {
                "title": "write a message",
                "message": "here write a message to append",
                "placeholder": "enter your message",
            },
        }
    )
    print(response)

```
### Pipes (in context of Action Functions)
Pipes can perform actions before returning LLM messages, such as RAG, sending requests to non-OpenAI LLMs, or executing functions in the web UI.  Pipes can be hosted as a Function or on a Pipelines server.

**Pipe Workflow:** (Diagram is mentioned in the original documentation, but cannot be rendered here.  It would show the flow of data through a Pipe.)

Pipes defined in WebUI appear as new models with an "External" designation.

### Valves (in context of Action Functions)

Valves are input variables set *per pipeline*. They are set as a subclass of the `Pipeline` class and initialized in the `__init__` method.

**Options for configuring Valves:**

1.  Use `os.getenv()` to set an environment variable and a default value.

    ```python
    self.valves = self.Valves(
        **{
            "LLAMAINDEX_OLLAMA_BASE_URL": os.getenv("LLAMAINDEX_OLLAMA_BASE_URL", "http://localhost:11434"),
            "LLAMAINDEX_MODEL_NAME": os.getenv("LLAMAINDEX_MODEL_NAME", "llama3"),
            "LLAMAINDEX_EMBEDDING_MODEL_NAME": os.getenv("LLAMAINDEX_EMBEDDING_MODEL_NAME", "nomic-embed-text"),
        }
    )
    ```

2.  Set the valve to the `Optional` type.

    ```python
    class Pipeline:
        class Valves(BaseModel):
            target_user_roles: List[str] = ["user"]
            max_turns: Optional[int] = None
    ```

If valves cannot be updated in the web UI, you'll see a warning in the Pipelines server log.

### FAQ (Action Functions and related concepts)

*   **What's the difference between Functions and Pipelines?** Functions are executed on the Open WebUI server; Pipelines are executed on a separate server.

---

This reformatted documentation provides a structured and comprehensive guide to Open WebUI Functions, covering all the information from the original document in a clear and organized manner. It uses Markdown formatting for readability and includes detailed explanations, examples, and best practices.
```