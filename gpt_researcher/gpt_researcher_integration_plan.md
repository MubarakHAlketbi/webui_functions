# GPT Researcher Integration with Open WebUI via Pipelines

## Overview

This document outlines a plan to integrate GPT Researcher with Open WebUI using the Pipelines framework. This approach allows Open WebUI to leverage GPT Researcher's capabilities as an external LLM provider, offloading the computational workload to a separate server.

## Prerequisites

*   **Open WebUI:** A running instance of Open WebUI.
*   **Docker:** Docker installed and configured. This is the recommended method for setting up Pipelines.
*   **Python 3.10+:**  Required for GPT Researcher and Pipelines.  Pipelines officially supports 3.11.
*   **API Keys:**
    *   OpenAI API Key
    *   Tavily API Key (or another search provider's key if you choose a different retriever)
* **Pip Packages:**
    * gpt-researcher
    * pydantic
    * Any dependencies required by Pipelines (see `pipelines/requirements.txt` in the Pipelines repository)

## Pipeline Setup

1.  **Run the Pipelines Container:**

    Use the following Docker command to start the Pipelines server:

    ```bash
    docker run -d -p 9099:9099 --add-host=host.docker.internal:host-gateway -v pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main
    ```

    This command does the following:

    *   `-d`: Runs the container in detached mode (in the background).
    *   `-p 9099:9099`: Maps port 9099 on the host to port 9099 in the container.
    *   `--add-host=host.docker.internal:host-gateway`:  Allows the container to access services on the host machine.
    *   `-v pipelines:/app/pipelines`: Creates a Docker volume named `pipelines` and mounts it to `/app/pipelines` in the container. This is where your custom pipeline script will be placed.
    *   `--name pipelines`: Assigns the name "pipelines" to the container.
    *   `--restart always`:  Ensures the container automatically restarts if it fails.
    *   `ghcr.io/open-webui/pipelines:main`:  Specifies the Docker image to use.

2. **Create a directory for pipeline files:**

    Create a directory named `pipelines` in the current working directory. This will be used by the Docker volume.

## GPT Researcher Integration (Custom Pipeline Script)

1.  **Create `gpt_researcher_pipeline.py`:**

    Inside the `pipelines` directory you created, create a file named `gpt_researcher_pipeline.py`. This file will contain the custom pipeline script.

2.  **Write the Pipeline Code:**

    ```python
    from pydantic import BaseModel, Field
    from gpt_researcher import GPTResearcher
    import asyncio
    import os

    class Pipe:
        class Valves(BaseModel):
            openai_api_key: str = Field(default="", description="Your OpenAI API Key")
            tavily_api_key: str = Field(default="", description="Your Tavily API Key")
            report_type: str = Field(default="research_report", description="Type of report (research_report, resource_report, outline_report)")
            # Add other configurable settings here (e.g., report_format)

        def __init__(self):
            self.valves = self.Valves(
                **{
                    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
                    "tavily_api_key": os.getenv("TAVILY_API_KEY", ""),
                    "report_type": os.getenv("GPT_RESEARCHER_REPORT_TYPE", "research_report"),
                }
            )

        async def pipe(self, body: dict):
            try:
                query = body.get("messages", [])[-1].get("content", "")
                report_type = self.valves.report_type

                researcher = GPTResearcher(query=query, report_type=report_type, config={
                    "openai_api_key": self.valves.openai_api_key,
                    "tavily_api_key": self.valves.tavily_api_key,
                    # Add other config options as needed, potentially pulling from self.valves
                })

                research_result = await researcher.conduct_research()
                report = await researcher.write_report()

                return {"choices": [{"message": {"role": "assistant", "content": report}}]} # Format for OpenAI API compatibility

            except Exception as e:
                return {"choices": [{"message": {"role": "assistant", "content": f"Error: {str(e)}" }}]}
    ```

    **Explanation:**

    *   **Imports:** Imports necessary libraries (`pydantic`, `GPTResearcher`, `asyncio`, `os`).
    *   **`Pipe` Class:**  Defines the main pipeline class.
    *   **`Valves` Class:** Defines configuration options (API keys, report type) that can be set in the Open WebUI interface.  It uses `os.getenv()` to allow setting these via environment variables, with defaults.
    *   **`__init__` Method:** Initializes the `Valves` with values from environment variables or defaults.
    *   **`pipe` Method:**
        *   Extracts the user's query from the `body` (the input data from Open WebUI).
        *   Creates a `GPTResearcher` instance, using the query and configuration from `Valves`.
        *   Calls `conduct_research()` and `write_report()` to generate the report.
        *   Returns the report, formatted to be compatible with the OpenAI API response structure (important for Open WebUI).
        *   Includes basic error handling.

3. **Install Dependencies:**

    You'll need to ensure that the `gpt-researcher` package and its dependencies are installed within the Pipelines environment.  Since we're using Docker, the easiest way to do this is to create a `requirements.txt` file *inside the `pipelines` directory* with the following content:

    ```
    gpt-researcher
    pydantic
    ```
    Then, modify the docker run command to install the requirements:

```bash
docker run -d -p 9099:9099 --add-host=host.docker.internal:host-gateway -v pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main /bin/bash -c "pip install -r /app/pipelines/requirements.txt && python -m pipelines"
```
This command now executes a bash script inside the container that first installs requirements from `/app/pipelines/requirements.txt` and then starts the pipelines server.

## Open WebUI Configuration

1.  **Connect to Pipelines:**

    *   In Open WebUI, go to `Admin Panel > Settings > Connections`.
    *   Click the `+` button to add a new connection.
    *   Set the `API URL` to `http://localhost:9099` (or the appropriate address if your Pipelines server is running elsewhere, such as `host.docker.internal:9099` if Open WebUI is also in a Docker container).
    *   Set the `API key` to `0p3n-w3bu!`.
    *   Click "Save". You should see a "Pipelines" icon in the `API Base URL` field.

2.  **Manage Configurations (Valves):**

    *   Go to `Admin Panel > Settings > Pipelines`.
    *   You should see your `gpt_researcher_pipeline` listed.
    *   Click on it to access and modify the `Valves` (API keys, report type, etc.).

## Error Handling

The provided `gpt_researcher_pipeline.py` code includes basic error handling, returning an error message if an exception occurs.  For a production environment, you should implement more robust error handling, including:

*   **Specific Exception Handling:** Catch specific exceptions (e.g., network errors, API errors) and provide more informative error messages.
*   **Logging:**  Log errors to a file or monitoring system.
*   **Retries:** Implement retry mechanisms for transient errors.

## Future Enhancements

*   **Streaming Output:** Modify the `pipe` function to stream the research progress and report generation to Open WebUI, providing a better user experience.
*   **Multiple Report Types:**  Allow the user to select different report types (research report, resource report, outline report) through the Open WebUI interface, potentially using `UserValves`.
*   **Customizable Configuration:** Expose more GPT Researcher configuration options through `Valves`, allowing users to fine-tune the research process.
*   **Caching:** Implement caching to avoid redundant research requests.
*   **Integration with Open WebUI Features:** Explore integrating with other Open WebUI features, such as RAG and web browsing.