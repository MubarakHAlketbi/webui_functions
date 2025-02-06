```markdown
# Open WebUI Tools Documentation

This document provides a comprehensive guide to understanding, using, installing, and creating custom tools within the Open WebUI framework.

---

## What are Tools?

Tools are Python scripts that extend the functionality of Large Language Models (LLMs) within Open WebUI. They allow LLMs to perform actions and receive additional context, enabling use cases like:

*   Web searching
*   Web scraping
*   API interactions (e.g., image generation, voice synthesis)

**Key Requirement:** Your chosen LLM must support function calling for tools to be used reliably.

Many pre-built tools are available on the [Community Website](https://openwebui.com/tools/) and can be easily imported into your Open WebUI instance.

---

## How to Use Tools

1.  **Assign Tools to a Model:**
    *   Navigate to `Workspace` => `Models`.
    *   Select the model you want to configure.
    *   Click the pencil icon to edit the model settings.
    *   Scroll down to the `Tools` section.
    *   Check the boxes next to the tools you want to enable for that model.
    *   Click `Save`.

2.  **Using Tools in Chat:**
    *   When chatting with an LLM that has tools enabled, click the "+" icon.
    *   Select the desired tool from the list.

**Important Note:** Enabling a tool doesn't force its use; it gives the LLM the *option* to call that tool.

3.  **AutoTool Filter (Optional):**
    *   The [AutoTool Filter](https://openwebui.com/f/hub/autotool_filter/) on the community site allows LLMs to automatically select tools without manual enabling in the "+" menu.
    *   **Note:** You still need to enable the tools per model (as described in step 1) even when using the AutoTool Filter.

---

## How to Install Tools

There are two methods for importing tools:

### 1. Manual Download and Import

1.  Go to the [Community Website](https://openwebui.com/tools/).
2.  Click on the tool you want to import.
3.  Click the blue "Get" button (top right corner).
4.  Click "Download as JSON export".
5.  In Open WebUI, navigate to `Workspace` => `Tools`.
6.  Click "Import Tools" and upload the downloaded JSON file.

### 2. Import via Open WebUI URL

1.  Go to the [Community Website](https://openwebui.com/tools/).
2.  Click on the tool you want to import.
3.  Click the blue "Get" button (top right corner).
4.  Enter the IP address of your Open WebUI instance.
5.  Click "Import to WebUI". This will automatically open your instance and initiate the import process.

**Security Warning:**  You can install custom tools or tools not listed on the community site using the manual import method.  Exercise extreme caution when importing tools from untrusted sources. Running unknown code is *always* a security risk.  Only import tools you understand and trust.

---

## What Sorts of Things Can Tools Do?

Tools enable a wide range of functionalities, including but not limited to:

*   **Web Search:** Fetch real-time information from the web.
*   **Image Generation:** Create images based on user prompts.
*   **External Voice Synthesis:** Integrate with services like ElevenLabs to generate audio from LLM output.
*   Other API interactions

---

## Writing A Custom Toolkit

This section details how to create your own custom tools for Open WebUI.

### Toolkit Structure

Toolkits are defined within a single Python file.  The file must contain:

1.  **Top-Level Docstring (Metadata):** Provides information about the tool.
2.  **`Tools` Class:** Contains the tool's methods.

### Example Top-Level Docstring

```python
"""
title: String Inverse
author: Your Name
author_url: https://website.com
git_url: https://github.com/username/string-reverse.git
description: This tool calculates the inverse of a string
required_open_webui_version: 0.4.0
requirements: langchain-openai, langgraph, ollama, langchain_ollama
version: 0.4.0
licence: MIT
"""
```

*   **`title`:**  The name of the tool.
*   **`author`:** Your name.
*   **`author_url`:**  (Optional) Your website.
*   **`git_url`:** (Optional)  Link to the tool's Git repository.
*   **`description`:** A brief explanation of the tool's function.
*   **`required_open_webui_version`:**  The minimum Open WebUI version required.
*   **`requirements`:**  Comma-separated list of Python package dependencies.
*   **`version`:** The tool's version number.
*   **`licence`:** The license under which the tool is distributed (e.g., MIT, GPL).

### Tools Class

All tool logic must be defined as methods within a class named `Tools`.

```python
class Tools:
    def __init__(self):
        """Initialize the Tool."""
        self.valves = self.Valves()

    class Valves(BaseModel):
        api_key: str = Field("", description="Your API key here")

    def reverse_string(self, string: str) -> str:
        """
        Reverses the input string.
        :param string: The string to reverse
        """
        # example usage of valves
        if self.valves.api_key != "42":
            return "Wrong API key"
        return string[::-1]
```

*   **`__init__`:**  (Optional)  The constructor for the `Tools` class.  This is a good place to initialize any resources or load configurations. The example shows how to initialize `Valves`.
*   **`Valves` (Inner Class):**  (Optional, but highly recommended) Defines configuration options that administrators can set. See the "Valves and UserValves" section below.
*   **Tool Methods (e.g., `reverse_string`):**  Each function within the `Tools` class represents a specific tool action.
    *   **Docstrings:**  Each tool method *must* have a docstring explaining its purpose and parameters.  This is used to generate the tool's description in the Open WebUI interface.
    *   **Type Hints:** Each tool method *must* have type hints for all arguments and the return value.  This is crucial for generating the JSON schema used by the LLM.  As of OpenWebUI version 0.4.3, nested types are supported (e.g., `list[tuple[str, int]]`).

### Valves and UserValves (Optional, but HIGHLY encouraged)

`Valves` and `UserValves` provide a mechanism for users and administrators to configure tool settings.  They create input fields or toggles in the Open WebUI interface.

*   **`Valves`:**  Configuration options that only administrators can modify.
*   **`UserValves`:** Configuration options that any user can modify.

Both `Valves` and `UserValves` are defined as inner classes within the `Tools` class, inheriting from `pydantic.BaseModel`.  Use `pydantic.Field` to define each configuration option.

```python
class Tools:
    # Define any Valves
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        test_valve: int = Field(
            default=4, description="A valve controlling a numberical value"
        )
        pass

    # Define any UserValves
    class UserValves(BaseModel):
        test_user_valve: bool = Field(
            default=False, description="A user valve controlling a True/False (on/off) switch"
        )
        pass

    def __init__(self):
        self.valves = self.Valves()
        # You can also initialize UserValves here if needed.

    # ... rest of your Tools class ...

```

*   **`default`:**  The default value for the configuration option.
*   **`description`:**  A description of the configuration option, displayed in the Open WebUI interface.

### Optional Arguments

Tool methods can accept several optional arguments:

*   **`__event_emitter__`:**  Used to emit events (e.g., status updates, additional messages).
*   **`__event_call__`:** Similar to `__event_emitter__`, but specifically for user interactions.
*   **`__user__`:**  A dictionary containing user information.
*   **`__metadata__`:** A dictionary containing chat metadata.
*   **`__messages__`:**  A list of previous messages in the conversation.
*   **`__files__`:**  Attached files.
*   **`__model__`:**  The name of the LLM model.

### Event Emitters

Event emitters allow tools to add information to the chat interface dynamically.

#### 1. Status Events

Used to display status updates above the message content.  Useful for long-running processes or tools that process large amounts of data.

```python
async def test_function(
        self, prompt: str, __user__: dict, __event_emitter__=None
    ) -> str:
        """
        This is a demo

        :param test: this is a test parameter
        """

        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": "Message that shows up in the chat", "done": False, "hidden": False},
            }
        )

        # ... some processing logic ...

        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": "Completed a task message", "done": True, "hidden": False},
            }
        )

        # ... more logic ...

    except Exception as e:
        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": f"An error occured: {e}", "done": True},
            }
        )
        return f"Tell the user: {e}"
```

*   **`type`:**  Must be set to `"status"`.
*   **`data`:**  A dictionary containing:
    *   **`description`:** The status message to display.
    *   **`done`:**  `True` if this is the final status update, `False` otherwise.
    *   **`hidden`:** `True` to remove the status message once the tool returns, `False` to keep it visible.

#### 2. Message Events

Used to append messages to the chat at any point during the tool's execution.  This allows you to add content, embed images, or render web pages before, during, or after the LLM's response.

```python
async def test_function(
        self, prompt: str, __user__: dict, __event_emitter__=None
    ) -> str:
        """
        This is a demo

        :param test: this is a test parameter
        """

        await __event_emitter__(
            {
                "type": "message",
                "data": {"content": "This message will be appended to the chat."},
            }
        )

        # ... some processing logic ...
    except Exception as e:
        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": f"An error occured: {e}", "done": True},
            }
        )
        return f"Tell the user: {e}"
```

*   **`type`:** Must be set to `"message"`.
*   **`data`:**  A dictionary containing:
    *   **`content`:**  The message content to append.  This can be plain text, Markdown, or HTML.
    *   Other message properties as needed.

**Key Differences between `status` and `message` events:**

*   `status` events are for displaying temporary status updates *above* the main message.  `message` events append new messages to the chat history.
*   `status` events require a `done` flag to indicate completion. `message` events do not.
*   `status` can be hidden.

This comprehensive guide covers all aspects of Open WebUI tools, from basic usage to advanced custom tool development. Remember to prioritize security when using or creating tools.
