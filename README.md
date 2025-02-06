# Open WebUI Functions Collection

A collection of custom functions for [Open WebUI](https://github.com/open-webui/open-webui) created by MubarakHAlketbi. These functions extend Open WebUI's capabilities by adding support for various AI model providers and enhancing functionality.

## What are Open WebUI Functions?

Functions are like plugins for Open WebUI that help extend its capabilities. They can:

-   Add support for new AI model providers
-   Modify how messages are processed
-   Add custom buttons to the interface
-   Create custom workflows

There are three types of functions:

1.  **Pipe Functions** - Create custom "agents/models" or integrations
2.  **Filter Functions** - Modify inputs and outputs
3.  **Action Functions** - Add custom buttons to the interface

## Available Functions

### OpenRouter API Integration

Location: `openrouter_api/openrouter.py`

A Pipe function that integrates OpenRouter's API into Open WebUI, providing access to 300+ AI models from various providers through a single unified API. Features include:

-   Access to all OpenRouter-supported models
-   Automatic model selection option
-   Configurable model allowlist
-   Comprehensive error handling
-   Support for streaming responses

[Learn more about the OpenRouter integration](openrouter_api/DESCRIPTION.md)

### GPT Researcher Integration

Location: `gpt_researcher/`

Integrates GPT Researcher as a Pipeline in Open WebUI, enabling autonomous web research capabilities. This allows Open WebUI to leverage GPT Researcher's ability to generate detailed, factual, and unbiased research reports.

[Learn more about the GPT Researcher integration](gpt_researcher/gpt_researcher_integration_plan.md)

## Installation

1.  Clone this repository:

    ```bash
    git clone https://github.com/MubarakHAlketbi/webui_functions.git
    ```
2.  For Functions: Copy the desired function folder into your Open WebUI functions directory.
3.  For Pipelines:
    - Set up a Pipelines instance (recommended using Docker, see `pipelines.md`).
    - Place the pipeline script (e.g., `gpt_researcher_pipeline.py`) in the Pipelines directory.
4.  Configure the function/pipeline through the Open WebUI interface:
    -   Navigate to Workspace => Functions (for Functions) or Admin Panel => Settings => Pipelines (for Pipelines)
    -   Enable the function/pipeline
    -   Configure any required settings (e.g., API keys)

## Contributing

Feel free to contribute by:

-   Reporting issues
-   Suggesting improvements
-   Creating pull requests with new functions

## Support the Project

If you find this project helpful, consider supporting its development:

-   **Donate**: [Support via Ziina](https://pay.ziina.com/MubarakHAlketbi)
-   **Star**: Give the project a star on GitHub
-   **Contribute**: Submit issues, suggestions, or pull requests

## License

This project is open source and available under the MIT License.