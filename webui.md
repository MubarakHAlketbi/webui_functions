
# Open WebUI Documentation

👋 Welcome to the Open WebUI documentation!

---

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform designed to operate entirely offline.  It supports various LLM runners like Ollama and OpenAI-compatible APIs and includes a built-in inference engine for Retrieval-Augmented Generation (RAG), making it a powerful AI deployment solution.

## Key Features of Open WebUI ⭐

-   **🚀 Effortless Setup:**  Install seamlessly using Docker or Kubernetes (kubectl, kustomize, or helm) with support for both `:ollama` and `:cuda` tagged images.
-   **🤝 Ollama/OpenAI API Integration:** Integrate OpenAI-compatible APIs for versatile conversations alongside Ollama models. Customize the OpenAI API URL to link with LMStudio, GroqCloud, Mistral, OpenRouter, and more.
-   **🛡️ Granular Permissions and User Groups:** Administrators can create detailed user roles and permissions, ensuring a secure user environment and customized user experiences.
-   **📱 Responsive Design:** Enjoy a seamless experience across Desktop PC, Laptop, and Mobile devices.
-   **📱 Progressive Web App (PWA) for Mobile:**  A native app-like experience on mobile devices with offline access on localhost and a seamless user interface.
-   **✒️🔢 Full Markdown and LaTeX Support:** Comprehensive Markdown and LaTeX capabilities for enriched interaction.
-   **🎤📹 Hands-Free Voice/Video Call:** Integrated hands-free voice and video call features for a more dynamic and interactive chat environment.
-   **🛠️ Model Builder:** Easily create Ollama models via the Web UI. Create and add custom characters/agents, customize chat elements, and import models effortlessly through Open WebUI Community integration.
-   **🐍 Native Python Function Calling Tool:** Enhance LLMs with built-in code editor support in the tools workspace.  Bring Your Own Function (BYOF) by adding your pure Python functions.
-   **📚 Local RAG Integration:** Retrieval Augmented Generation (RAG) support, allowing seamless integration of document interactions into the chat experience. Load documents directly into the chat or add files to your document library, accessing them using the `#` command before a query.
-   **🔍 Web Search for RAG:** Perform web searches using providers like SearXNG, Google PSE, Brave Search, serpstack, serper, Serply, DuckDuckGo, TavilySearch, SearchApi, and Bing.  Inject results directly into your chat.
-   **🌐 Web Browsing Capability:** Integrate websites into your chat experience using the `#` command followed by a URL.
-   **🎨 Image Generation Integration:** Incorporate image generation using AUTOMATIC1111 API or ComfyUI (local), and OpenAI's DALL-E (external).
-   **⚙️ Many Models Conversations:** Engage with various models simultaneously, leveraging their unique strengths.
-   **🔐 Role-Based Access Control (RBAC):** Secure access with restricted permissions; only authorized individuals can access Ollama, and exclusive model creation/pulling rights are reserved for administrators.
-   **🌐🌍 Multilingual Support:**  Internationalization (i18n) support.  Contributions to expand supported languages are welcome!
-   **🧩 Pipelines, Open WebUI Plugin Support:** Integrate custom logic and Python libraries using the Pipelines Plugin Framework. Launch your Pipelines instance, set the OpenAI URL to the Pipelines URL. Examples include Function Calling, User Rate Limiting, Usage Monitoring (Langfuse), Live Translation (LibreTranslate), Toxic Message Filtering, and more.
-   **🌟 Continuous Updates:** Regular updates, fixes, and new features.

For a comprehensive overview of Open WebUI's features, please refer to the [Open WebUI documentation](link-to-documentation - *replace with actual link if available*).

## API Endpoints

This section details how to interact with Open WebUI's API endpoints.  This is an experimental setup and may be updated.

### Authentication

Authentication is required for secure API access 🛡️.  Use the Bearer Token mechanism. Obtain your API key from `Settings > Account` in the Open WebUI, or use a JWT (JSON Web Token).

### Notable API Endpoints

#### 📜 Retrieve All Models

-   **Endpoint:** `GET /api/models`
-   **Description:** Fetches all models created or added via Open WebUI.
-   **Example:**

    ```bash
    curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:3000/api/models
    ```

#### 💬 Chat Completions

-   **Endpoint:** `POST /api/chat/completions`
-   **Description:** OpenAI API compatible chat completion endpoint for models on Open WebUI (Ollama, OpenAI, and Open WebUI Function models).
-   **Example:**

    ```bash
    curl -X POST http://localhost:3000/api/chat/completions \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "llama3.1",
          "messages": [
            {
              "role": "user",
              "content": "Why is the sky blue?"
            }
          ]
        }'
    ```

### 🧩 Retrieval Augmented Generation (RAG)

RAG enhances responses by incorporating data from external sources.

#### Uploading Files

Upload files to use external data in RAG responses.  File content is automatically extracted and stored in a vector database.

-   **Endpoint:** `POST /api/v1/files/`
-   **Curl Example:**

    ```bash
    curl -X POST -H "Authorization: Bearer YOUR_API_KEY" -H "Accept: application/json" \
    -F "file=@/path/to/your/file" http://localhost:3000/api/v1/files/
    ```

-   **Python Example:**

    ```python
    import requests

    def upload_file(token, file_path):
        url = 'http://localhost:3000/api/v1/files/'
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, headers=headers, files=files)
        return response.json()
    ```

#### Adding Files to Knowledge Collections

Group uploaded files into knowledge collections or reference them individually.

-   **Endpoint:** `POST /api/v1/knowledge/{id}/file/add`
-   **Curl Example:**

    ```bash
    curl -X POST http://localhost:3000/api/v1/knowledge/{knowledge_id}/file/add \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"file_id": "your-file-id-here"}'
    ```

-   **Python Example:**

    ```python
    import requests

    def add_file_to_knowledge(token, knowledge_id, file_id):
        url = f'http://localhost:3000/api/v1/knowledge/{knowledge_id}/file/add'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        data = {'file_id': file_id}
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    ```

#### Using Files and Collections in Chat Completions

Reference individual files or entire collections in RAG queries.

##### Using an Individual File

Focus the chat model's response on a specific file.

-   **Endpoint:** `POST /api/chat/completions`
-   **Curl Example:**

    ```bash
    curl -X POST http://localhost:3000/api/chat/completions \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "gpt-4-turbo",
          "messages": [
            {"role": "user", "content": "Explain the concepts in this document."}
          ],
          "files": [
            {"type": "file", "id": "your-file-id-here"}
          ]
        }'
    ```

-   **Python Example:**

    ```python
    import requests

    def chat_with_file(token, model, query, file_id):
        url = 'http://localhost:3000/api/chat/completions'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': query}],
            'files': [{'type': 'file', 'id': file_id}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    ```

##### Using a Knowledge Collection

Leverage a knowledge collection for broader context or multiple documents.

-   **Endpoint:** `POST /api/chat/completions`
-   **Curl Example:**

    ```bash
    curl -X POST http://localhost:3000/api/chat/completions \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "gpt-4-turbo",
          "messages": [
            {"role": "user", "content": "Provide insights on the historical perspectives covered in the collection."}
          ],
          "files": [
            {"type": "collection", "id": "your-collection-id-here"}
          ]
        }'
    ```

-   **Python Example:**

    ```python
    import requests

    def chat_with_collection(token, model, query, collection_id):
        url = 'http://localhost:3000/api/chat/completions'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': query}],
            'files': [{'type': 'collection', 'id': collection_id}]
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    ```

### Advantages of Using Open WebUI as a Unified LLM Provider

-   **Unified Interface:**  Simplify interactions with different LLMs through a single platform.
-   **Ease of Implementation:** Quick start integration with comprehensive documentation and community support.

### Swagger Documentation Links

> **Important:** Set the `ENV` environment variable to `dev` to access Swagger documentation.

Access detailed API documentation for different services:

| Application | Documentation Path |
| ----------- | ------------------ |
| Main        | /docs              |

---

## FAQ

*Sponsored by Dave Waring*

[Dave Waring](Link to Dave Waring - *replace with actual link if available*)

*Follow along as I build my own AI powered digital brain.*

### 💡 Why Docker?

Docker is central to the project's design for consistency, dependency isolation, and simplified deployment.  Community-driven alternatives are encouraged for those seeking different deployment methods.

### 📜 Table of Contents

-   [Q: Why am I asked to sign up? Where are my data being sent to?](#q-why-am-i-asked-to-sign-up-where-are-my-data-being-sent-to)
-   [Q: Why can't my Docker container connect to services on the host using localhost?](#q-why-cant-my-docker-container-connect-to-services-on-the-host-using-localhost)
-   [Q: How do I make my host's services accessible to Docker containers?](#q-how-do-i-make-my-hosts-services-accessible-to-docker-containers)
-   [Q: Why isn't my Open WebUI updating? I've re-pulled/restarted the container, and nothing changed.](#q-why-isnt-my-open-webui-updating-ive-re-pulledrestarted-the-container-and-nothing-changed)
-   [Q: Wait, why would I delete my container? Won't I lose my data?](#q-wait-why-would-i-delete-my-container-wont-i-lose-my-data)
-   [Q: Should I use the distro-packaged Docker or the official Docker package?](#q-should-i-use-the-distro-packaged-docker-or-the-official-docker-package)
-   [Q: Is GPU support available in Docker?](#q-is-gpu-support-available-in-docker)
-   [Q: Why does Open WebUI emphasize the use of Docker?](#q-why-does-open-webui-emphasize-the-use-of-docker)
-   [Q: Why doesn't Speech-to-Text (STT) and Text-to-Speech (TTS) work in my deployment?](#q-why-doesnt-speech-to-text-stt-and-text-to-speech-tts-work-in-my-deployment)
-   [Q: Why doesn't Open WebUI include built-in HTTPS support?](#q-why-doesnt-open-webui-include-built-in-https-support)
-   [Q: I updated/restarted/installed some new software and now Open WebUI isn't working anymore!](#q-i-updatedrestartedinstalled-some-new-software-and-now-open-webui-isnt-working-anymore)
-   [Q: I updated/restarted and now my login isn't working anymore, I had to create a new account and all my chats are gone.](#q-i-updatedrestarted-and-now-my-login-isnt-working-anymore-i-had-to-create-a-new-account-and-all-my-chats-are-gone)
-   [Q: I tried to login and couldn't, made a new account and now I'm being told my account needs to be activated by an admin.](#q-i-tried-to-login-and-couldnt-made-a-new-account-and-now-im-being-told-my-account-needs-to-be-activated-by-an-admin)
-   [Q: Why can't Open WebUI start with an SSL error?](#q-why-cant-open-webui-start-with-an-ssl-error)
-    [Need Further Assistance?](#need-further-assistance)

### Q: Why am I asked to sign up? Where are my data being sent to?

A:  Sign-up creates an admin user for enhanced security.  All data is kept *local*.  No data is collected.  Information stays within your server.

### Q: Why can't my Docker container connect to services on the host using localhost?

A: Inside a Docker container, `localhost` refers to the *container* itself.  Use the DNS name `host.docker.internal` to connect to services on the host.

### Q: How do I make my host's services accessible to Docker containers?

A: Configure services to listen on all network interfaces (`0.0.0.0`) instead of `127.0.0.1` (localhost only).  Be aware of security implications and implement appropriate measures (firewalls, authentication).

### Q: Why isn't my Open WebUI updating? I've re-pulled/restarted the container, and nothing changed.

A: Updating requires more than pulling the new image.  Docker volumes persist data.  To apply the update:

1.  Remove the existing container (this does *not* delete the volume).
2.  Create a new container with the updated image and the existing volume attached.

### Q: Wait, why would I delete my container? Won't I lose my data?

A: Deleting a container doesn't delete data stored in Docker *volumes*.  Data persists as long as the volume is not explicitly deleted (e.g., `docker volume rm`).  The correct update process (described above) preserves data.

### Q: Should I use the distro-packaged Docker or the official Docker package?

A: Use the *official* Docker package.  It's frequently updated with the latest features, bug fixes, and security patches, and supports functionalities like `host.docker.internal`.  Refer to the [Install Docker Engine](Link to Docker install guide - *replace with actual link*) guide.

### Q: Is GPU support available in Docker?

A: GPU support varies by platform.  Officially supported on Docker for Windows and Docker Engine on Linux.  *Not* currently supported on Docker Desktop for Linux and MacOS.

### Q: Why does Open WebUI emphasize the use of Docker?

A: Docker ensures consistency, isolates dependencies, and simplifies deployment.  It's a strategic choice by the project maintainers. Community alternatives are welcome.

### Q: Why doesn't Speech-to-Text (STT) and Text-to-Speech (TTS) work in my deployment?

A: STT and TTS may require HTTPS.  Modern browsers restrict these features to secure connections.  Ensure your deployment uses HTTPS.

### Q: Why doesn't Open WebUI include built-in HTTPS support?

A:  HTTPS implementation is left to the user for greater flexibility and customization.  Community members may provide guidance.

### Q: I updated/restarted/installed some new software and now Open WebUI isn't working anymore!

A: This is likely due to a direct installation without a virtual environment.  Use a virtual environment to manage `requirements.txt` dependencies.

### Q: I updated/restarted and now my login isn't working anymore, I had to create a new account and all my chats are gone.

A: This happens when a container is created *without* mounting a volume for `/app/backend/data` or if the Open WebUI volume was deleted.  Ensure your `docker run` command includes the correct volume mount.

### Q: I tried to login and couldn't, made a new account and now I'm being told my account needs to be activated by an admin.

A: This occurs when the initial admin account password is forgotten.  The first account is automatically the admin.  See the [Resetting the Admin Password](Link to password reset guide - *replace with actual link if available*) guide.

### Q: Why can't Open WebUI start with an SSL error?

A: This is likely due to missing SSL certificates or incorrect Hugging Face configuration.  Set up a mirror (e.g., `hf-mirror.com`) and specify it as the endpoint:

```bash
docker run -d -p 3000:8080 -e HF_ENDPOINT=https://hf-mirror.com/ --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```
### Need Further Assistance?
If you have any further questions or concerns, please reach out to our [GitHub Issues](Link to GitHub Issues - *replace with actual link*) page or our [Discord](Link to Discord - *replace with actual link*) channel for more help and information.
