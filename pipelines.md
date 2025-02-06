
# Pipelines: UI-Agnostic OpenAI API Plugin Framework

**Tip:** If you only need to add support for providers like Anthropic or basic filters, Open WebUI Functions are a better, built-in, and easier-to-configure solution.  Pipelines are designed for computationally heavy tasks (e.g., running large models or complex logic) that you want to offload from your main Open WebUI instance for improved performance and scalability.

Welcome to Pipelines, an Open WebUI initiative. Pipelines bring modular, customizable workflows to any UI client supporting OpenAI API specifications – and much more!  Extend functionalities, integrate unique logic, and create dynamic workflows with just a few lines of code.

---

## 🚀 Why Choose Pipelines?

*   **Limitless Possibilities:** Add custom logic and integrate Python libraries, ranging from AI agents to home automation APIs.
*   **Seamless Integration:** Compatible with any UI/client supporting OpenAI API specs. (Note: Only pipe-type pipelines are supported; filter types require clients with Pipelines support.)
*   **Custom Hooks:** Build and integrate custom pipelines.

---

## Examples of What You Can Achieve:

*   **Function Calling Pipeline:** Handle function calls and enhance applications with custom logic.
*   **Custom RAG Pipeline:** Implement sophisticated Retrieval-Augmented Generation pipelines tailored to your needs.
*   **Message Monitoring Using Langfuse:** Monitor and analyze message interactions in real-time using Langfuse.
*   **Rate Limit Filter:** Control the flow of requests to prevent exceeding rate limits.
*   **Real-Time Translation Filter with LibreTranslate:** Seamlessly integrate real-time translations into your LLM interactions.
*   **Toxic Message Filter:** Implement filters to detect and handle toxic messages effectively.
*   **And Much More!:**  The possibilities are vast with Pipelines and Python. Explore our scaffolds to kickstart your projects and streamline your development.

---

## 🔧 How It Works

Pipelines provide a workflow for integrating with any OpenAI API-compatible UI client.  Simply launch your Pipelines instance and set the OpenAI URL on your client to the Pipelines URL.  This allows you to leverage any Python library for your needs.

**Pipelines Workflow**

*(Image of Pipelines Workflow should be inserted here if available)*

---

## ⚡ Quick Start with Docker

**Warning:** Pipelines are a plugin system with arbitrary code execution.  Do not fetch pipelines from untrusted sources.

For a streamlined setup using Docker:

1.  **Run the Pipelines container:**

    ```bash
    docker run -d -p 9099:9099 --add-host=host.docker.internal:host-gateway -v pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main
    ```

2.  **Connect to Open WebUI:**
    *   Navigate to `Admin Panel > Settings > Connections` in Open WebUI.
    *   Click the `+` button to add a new connection.
    *   Set the `API URL` to `http://localhost:9099` and the `API key` to `0p3n-w3bu!`.
    *   After adding and verifying the connection, you'll see a "Pipelines" icon in the `API Base URL` field.

    **Info:** If Open WebUI is running in a Docker container, replace `localhost` with `host.docker.internal` in the API URL.

3.  **Manage Configurations:**
    *   Go to `Admin Panel > Settings > Pipelines`.
    *   Select your desired pipeline and modify the valve values directly from the WebUI.

**Tip:**  Connection issues are often related to Docker networking.  We encourage you to troubleshoot and share your solutions in the discussions forum.

To install a custom pipeline with additional dependencies:

```bash
docker run -d -p 9099:9099 --add-host=host.docker.internal:host-gateway -e PIPELINES_URLS="https://github.com/open-webui/pipelines/blob/main/examples/filters/detoxify_filter_pipeline.py" -v pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main
```

Alternatively, install pipelines directly from the admin settings by pasting the pipeline URL (if it doesn't have extra dependencies).

---

## 📦 Installation and Setup

Get started with Pipelines:

1.  **Ensure Python 3.11 is installed.**  This is the only officially supported version.

2.  **Clone the Pipelines repository:**

    ```bash
    git clone https://github.com/open-webui/pipelines.git
    cd pipelines
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the Pipelines server:**

    ```bash
    sh ./start.sh
    ```

After the server starts, set the OpenAI URL on your client to the Pipelines URL.

---

## 📂 Directory Structure and Examples

The `/pipelines` directory is the core of your setup. Add new modules, customize existing ones, and manage workflows here. All pipelines in this directory are automatically loaded at server launch.

You can change this directory using the `PIPELINES_DIR` environment variable.

**Integration Examples**

Find various integration examples in the [examples directory](https://github.com/open-webui/pipelines/blob/main/examples). These examples provide a foundation for building custom pipelines.

---
## 🎉 Work in Progress
We are continuously improving Pipelines! We welcome your feedback and suggestions for new hooks and features. Join the Open WebUI community and help us shape the future of this project.

Our vision is for Pipelines to become the ultimate plugin framework for Open WebUI, making it the "WordPress of AI interfaces."

---

## Filters

Filters perform actions on incoming user messages and outgoing assistant (LLM) messages.  Potential actions include:

*   Sending messages to monitoring platforms (e.g., Langfuse, DataDog).
*   Modifying message content.
*   Blocking toxic messages.
*   Translating messages.
*   Rate limiting messages.

A list of examples is maintained in the [Pipelines repo](link to repo). Filters can be executed as a Function or on a Pipelines server.

**Filter Workflow**

*(Image of Filter Workflow should be inserted here if available)*

When a filter pipeline is enabled, the incoming message ("inlet") is processed. The filter performs actions before requesting the chat completion from the LLM.  Finally, the filter post-processes the outgoing LLM message ("outlet") before sending it to the user.

---

## Pipes

Pipes are functions that perform actions *before* returning LLM messages to the user. Examples include:

*   Retrieval Augmented Generation (RAG).
*   Sending requests to non-OpenAI LLM providers (Anthropic, Azure OpenAI, Google).
*   Executing functions within the web UI.

Pipes can be hosted as a Function or on a Pipelines server. A list of examples is in the [Pipelines repo](link to repo).

**Pipe Workflow**

*(Image of Pipe Workflow should be inserted here if available)*

Pipes defined in your WebUI appear as new models with an "External" designation.

*(Image of example Pipe models should be inserted here if available)*
---

## Valves

Valves are input variables set *per pipeline*.  They are defined as a subclass of the `Pipeline` class and initialized in the `__init__` method.

When adding valves, ensure they can be reconfigured by admins in the web UI.  Options include:

1.  **Using `os.getenv()`:**

    ```python
    self.valves = self.Valves(
        **{
            "LLAMAINDEX_OLLAMA_BASE_URL": os.getenv("LLAMAINDEX_OLLAMA_BASE_URL", "http://localhost:11434"),
            "LLAMAINDEX_MODEL_NAME": os.getenv("LLAMAINDEX_MODEL_NAME", "llama3"),
            "LLAMAINDEX_EMBEDDING_MODEL_NAME": os.getenv("LLAMAINDEX_EMBEDDING_MODEL_NAME", "nomic-embed-text"),
        }
    )
    ```

2.  **Setting the valve to the `Optional` type:**

    ```python
    class Pipeline:
        class Valves(BaseModel):
            target_user_roles: List[str] = ["user"]
            max_turns: Optional[int] = None
    ```

Failure to provide a way to update valves in the UI will result in a `WARNING:root:No Pipeline class found in <pipeline name>` error in the Pipelines server log.

---

## FAQ

**What's the difference between Functions and Pipelines?**

Functions are executed directly on the Open WebUI server, while Pipelines run on a separate server, potentially reducing the load on your Open WebUI instance.
```