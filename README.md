# Open WebUI Functions Collection

A collection of custom functions for [Open WebUI](https://github.com/open-webui/open-webui) created by MubarakHAlketbi. These functions extend Open WebUI's capabilities by adding support for various AI model providers and enhancing functionality.

## What are Open WebUI Functions?

Functions are like plugins for Open WebUI that help extend its capabilities. They can:
- Add support for new AI model providers
- Modify how messages are processed
- Add custom buttons to the interface
- Create custom workflows

There are three types of functions:
1. **Pipe Functions** - Create custom "agents/models" or integrations
2. **Filter Functions** - Modify inputs and outputs
3. **Action Functions** - Add custom buttons to the interface

## Available Functions

### OpenRouter API Integration
Location: `openrouter_api/openrouter.py`

A Pipe function that integrates OpenRouter's API into Open WebUI, providing access to 300+ AI models from various providers through a single unified API. Features include:
- Access to all OpenRouter-supported models
- Automatic model selection option
- Configurable model allowlist
- Comprehensive error handling
- Support for streaming responses

[Learn more about the OpenRouter integration](openrouter_api/DESCRIPTION.md)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MubarakHAlketbi/webui_functions.git
```

2. Copy the desired function folder into your Open WebUI functions directory.

3. Configure the function through the Open WebUI interface:
   - Navigate to Workspace => Functions
   - Enable the function
   - Configure any required settings (e.g., API keys)

## Contributing

Feel free to contribute by:
- Reporting issues
- Suggesting improvements
- Creating pull requests with new functions

## License

This project is open source and available under the MIT License.