
# GPT Researcher Documentation

## PIP Package

🌟 Exciting News! Now, you can integrate gpt-researcher with your apps seamlessly!

---

## Installation

Follow these easy steps to get started:

1.  **Pre-requisite:** Ensure Python 3.10+ is installed on your machine 💻
2.  **Install gpt-researcher:** Grab the official package from PyPi.

    ```bash
    pip install gpt-researcher
    ```

3.  **Environment Variables:** Create a `.env` file with your OpenAI API key or simply export it.

    ```bash
    export OPENAI_API_KEY={Your OpenAI API Key here}
    export TAVILY_API_KEY={Your Tavily API Key here}
    ```

4.  Start using GPT Researcher in your own codebase.

---

## Example Usage

```python
from gpt_researcher import GPTResearcher
import asyncio

async def get_report(query: str, report_type: str):
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    
    # Get additional information
    research_context = researcher.get_research_context()
    research_costs = researcher.get_costs()
    research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()
    
    return report, research_context, research_costs, research_images, research_sources

if __name__ == "__main__":
    query = "what team may win the NBA finals?"
    report_type = "research_report"

    report, context, costs, images, sources = asyncio.run(get_report(query, report_type))
    
    print("Report:")
    print(report)
    print("\nResearch Costs:")
    print(costs)
    print("\nNumber of Research Images:")
    print(len(images))
    print("\nNumber of Research Sources:")
    print(len(sources))
```

### Specific Examples

#### Example 1: Research Report

```python
query = "Latest developments in renewable energy technologies"
report_type = "research_report"
```

#### Example 2: Resource Report

```python
query = "List of top AI conferences in 2023"
report_type = "resource_report"
```

#### Example 3: Outline Report

```python
query = "Outline for an article on the impact of AI in education"
report_type = "outline_report"
```

---

## Integration with Web Frameworks

### FastAPI Example

```python
from fastapi import FastAPI
from gpt_researcher import GPTResearcher
import asyncio

app = FastAPI()

@app.get("/report/{report_type}")
async def get_report(query: str, report_type: str) -> dict:
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    
    source_urls = researcher.get_source_urls()
    research_costs = researcher.get_costs()
    research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()
    
    return {
        "report": report,
        "source_urls": source_urls,
        "research_costs": research_costs,
        "num_images": len(research_images),
        "num_sources": len(research_sources)
    }

# Run the server
# uvicorn main:app --reload
```

### Flask Example

**Pre-requisite:** Install flask with the async extra.

```bash
pip install 'flask[async]'
```

```python
from flask import Flask, request, jsonify
from gpt_researcher import GPTResearcher

app = Flask(__name__)

@app.route('/report/<report_type>', methods=['GET'])
async def get_report(report_type):
    query = request.args.get('query')
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    
    source_urls = researcher.get_source_urls()
    research_costs = researcher.get_costs()
    research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()
    
    return jsonify({
        "report": report,
        "source_urls": source_urls,
        "research_costs": research_costs,
        "num_images": len(research_images),
        "num_sources": len(research_sources)
    })

# Run the server
# flask run
```

Run the server

```
flask run
```
Example Request
```
curl -X GET "http://localhost:5000/report/research_report?query=what team may win the nba finals?"
```

---

## Getters and Setters

GPT Researcher provides several methods to retrieve additional information about the research process:

### Get Research Sources

Sources are the URLs that were used to gather information for the research.

```python
source_urls = researcher.get_source_urls()
```

### Get Research Context

Context is all the retrieved information from the research. It includes the sources and their corresponding content.

```python
research_context = researcher.get_research_context()
```

### Get Research Costs

Costs are the number of tokens consumed during the research process.

```python
research_costs = researcher.get_costs()
```

### Get Research Images

Retrieves a list of images found during the research process.

```python
research_images = researcher.get_research_images()
```
### Get Research Sources

Retrieves a list of research sources, including title, content, and images.

```python
research_sources = researcher.get_research_sources()
```

### Set Verbose

You can set the verbose mode to get more detailed logs.

```python
researcher.set_verbose(True)
```

### Add Costs

You can also add costs to the research process if you want to track the costs from external usage.

```python
researcher.add_costs(0.22)
```

---

## Advanced Usage

### Customizing the Research Process

You can customize various aspects of the research process by passing additional parameters when initializing the `GPTResearcher`:

```python
researcher = GPTResearcher(
    query="Your research query",
    report_type="research_report",
    report_format="APA",
    tone="formal and objective",
    max_subtopics=5,
    verbose=True
)
```

### Handling Research Results

After conducting research, you can process the results in various ways:

```python
# Conduct research
research_result = await researcher.conduct_research()

# Generate a report
report = await researcher.write_report()

# Generate a conclusion
conclusion = await researcher.write_report_conclusion(report)

# Get subtopics
subtopics = await researcher.get_subtopics()

# Get draft section titles for a subtopic
draft_titles = await researcher.get_draft_section_titles("Subtopic name")
```

### Working with Research Context

You can use the research context for further processing or analysis:

```python
# Get the full research context
context = researcher.get_research_context()

# Get similar written contents based on draft section titles
similar_contents = await researcher.get_similar_written_contents_by_draft_section_titles(
    current_subtopic="Subtopic name",
    draft_section_titles=["Title 1", "Title 2"],
    written_contents=some_written_contents,
    max_results=10
)
```

This comprehensive documentation should help users understand and utilize the full capabilities of the GPT Researcher package.

---

## Configuration

The `config.py` enables you to customize GPT Researcher to your specific needs and preferences.

Thanks to our amazing community and contributions, GPT Researcher supports multiple LLMs and Retrievers.  In addition, GPT Researcher can be tailored to various report formats (such as APA), word count, research iterations depth, etc.

GPT Researcher defaults to our recommended suite of integrations: OpenAI for LLM calls and Tavily API for retrieving real-time web information.

As seen below, OpenAI still stands as the superior LLM. We assume it will stay this way for some time, and that prices will only continue to decrease, while performance and speed increase over time.

The default `config.py` file can be found in `/gpt_researcher/config/`. It supports various options for customizing GPT Researcher to your needs. You can also include your own external JSON file `config.json` by adding the path in the `config_file` param. Please follow the `config.py` file for additional future support.

Below is a list of current supported options:

*   **RETRIEVER:** Web search engine used for retrieving sources. Defaults to `tavily`. Options: `duckduckgo`, `bing`, `google`, `searchapi`, `serper`, `searx`.  [Check here for supported retrievers](https://tavily.com/)
*   **EMBEDDING:** Embedding model. Defaults to `openai:text-embedding-3-small`. Options: `ollama`, `huggingface`, `azure_openai`, `custom`.
*   **FAST_LLM:** Model name for fast LLM operations such summaries. Defaults to `openai:gpt-4o-mini`.
*   **SMART_LLM:** Model name for smart operations like generating research reports and reasoning. Defaults to `openai:gpt-4o`.
*   **STRATEGIC_LLM:** Model name for strategic operations like generating research plans and strategies. Defaults to `openai:o1-preview`.
*   **LANGUAGE:** Language to be used for the final research report. Defaults to `english`.
*   **CURATE_SOURCES:** Whether to curate sources for research. This step adds an LLM run which may increase costs and total run time but improves quality of source selection. Defaults to `True`.
*   **FAST_TOKEN_LIMIT:** Maximum token limit for fast LLM responses. Defaults to `2000`.
*   **SMART_TOKEN_LIMIT:** Maximum token limit for smart LLM responses. Defaults to `4000`.
*   **STRATEGIC_TOKEN_LIMIT:** Maximum token limit for strategic LLM responses. Defaults to `4000`.
*   **BROWSE_CHUNK_MAX_LENGTH:** Maximum length of text chunks to browse in web sources. Defaults to `8192`.
*   **SUMMARY_TOKEN_LIMIT:** Maximum token limit for generating summaries. Defaults to `700`.
*   **TEMPERATURE:** Sampling temperature for LLM responses, typically between 0 and 1. A higher value results in more randomness and creativity, while a lower value results in more focused and deterministic responses. Defaults to `0.55`.
*   **TOTAL_WORDS:** Total word count limit for document generation or processing tasks. Defaults to `800`.
*   **REPORT_FORMAT:** Preferred format for report generation. Defaults to `APA`. Consider formats like `MLA`, `CMS`, `Harvard style`, `IEEE`, etc.
*   **MAX_ITERATIONS:** Maximum number of iterations for processes like query expansion or search refinement. Defaults to `3`.
*   **AGENT_ROLE:** Role of the agent. This might be used to customize the behavior of the agent based on its assigned roles. No default value.
*   **MAX_SUBTOPICS:** Maximum number of subtopics to generate or consider. Defaults to `3`.
*   **SCRAPER:** Web scraper to use for gathering information. Defaults to `bs` (BeautifulSoup). You can also use `newspaper`.
*   **DOC_PATH:** Path to read and research local documents. Defaults to an empty string indicating no path specified.
*   **USER_AGENT:** Custom User-Agent string for web crawling and web requests.
*   **MEMORY_BACKEND:** Backend used for memory operations, such as local storage of temporary data. Defaults to `local`.

To change the default configurations, you can simply add env variables to your `.env` file as named above or export manually in your local project directory.

For example, to manually change the search engine and report format:

```bash
export RETRIEVER=bing
export REPORT_FORMAT=IEEE
```

Please note that you might need to export additional env vars and obtain API keys for other supported search retrievers and LLM providers. Please follow your console logs for further assistance. To learn more about additional LLM support you can check out the [docs here](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/modules.html).

You can also include your own external JSON file `config.json` by adding the path in the `config_file` param.

---

## Scraping Options

GPT Researcher now offers various methods for web scraping: static scraping with BeautifulSoup, dynamic scraping with Selenium, and High scale scraping with Tavily Extract. This document explains how to switch between these methods and the benefits of each approach.

### Configuring Scraping Method

You can choose your preferred scraping method by setting the `SCRAPER` environment variable:

*   For BeautifulSoup (static scraping):

    ```bash
    export SCRAPER="bs"
    ```

*   For Selenium (dynamic browser scraping):

    ```bash
    export SCRAPER="browser"
    ```

*   For production use cases, you can set the Scraper to `tavily_extract`. Tavily allows you to scrape sites at scale without the hassle of setting up proxies, managing cookies, or dealing with CAPTCHAs. Please note that you need to have a Tavily account and API key to use this option. To learn more about Tavily Extract see [here](https://tavily.com/).  Make sure to first install the pip package `tavily-python`. Then:

    ```bash
    export SCRAPER="tavily_extract"
    ```

**Note:** If not set, GPT Researcher will default to BeautifulSoup for scraping.

### Scraping Methods Explained

#### BeautifulSoup (Static Scraping)

When `SCRAPER="bs"`, GPT Researcher uses BeautifulSoup for static scraping. This method:

*   Sends a single HTTP request to fetch the page content
*   Parses the static HTML content
*   Extracts text and data from the parsed HTML

**Benefits:**

*   Faster and more lightweight
*   Doesn't require additional setup
*   Works well for simple, static websites

**Limitations:**

*   Cannot handle dynamic content loaded by JavaScript
*   May miss content that requires user interaction to display

#### Selenium (Browser Scraping)

When `SCRAPER="browser"`, GPT Researcher uses Selenium for dynamic scraping.  This method:

*   Opens a real browser instance (Chrome by default)
*   Loads the page and executes JavaScript
*   Waits for dynamic content to load
*   Extracts text and data from the fully rendered page

**Benefits:**

*   Can scrape dynamically loaded content
*   Simulates real user interactions (scrolling, clicking, etc.)
*   Works well for complex, JavaScript-heavy websites

**Limitations:**

*   Slower than static scraping
*   Requires more system resources
*   Requires additional setup (Selenium and WebDriver installation)

#### Tavily Extract (Recommended for Production)

When `SCRAPER="tavily_extract"`, GPT Researcher uses Tavily's Extract API for web scraping. This method:

*   Uses Tavily's robust infrastructure to handle web scraping at scale
*   Automatically handles CAPTCHAs, JavaScript rendering, and anti-bot measures
*   Provides clean, structured content extraction

**Benefits:**

*   Production-ready and highly reliable
*   No need to manage proxies or handle rate limiting
*   Excellent success rate on most websites
*   Handles both static and dynamic content
*   Built-in content cleaning and formatting
*   Fast response times through Tavily's distributed infrastructure

**Setup:**

1.  Create a Tavily account at [app.tavily.com](https://app.tavily.com/)
2.  Get your API key from the dashboard
3.  Install the Tavily Python SDK:

    ```bash
    pip install tavily-python
    ```

4.  Set your Tavily API key:

    ```bash
    export TAVILY_API_KEY="your-api-key"
    ```

**Usage Considerations:**

*   Requires a Tavily API key and account
*   API calls are metered based on your Tavily plan
*   Best for production environments where reliability is crucial
*   Ideal for businesses and applications that need consistent scraping results

### Additional Setup for Selenium

If you choose to use Selenium (`SCRAPER="browser"`), you'll need to:

1.  Install the Selenium package:

    ```bash
    pip install selenium
    ```

2.  Download the appropriate WebDriver for your browser:
    *   For Chrome: [ChromeDriver](https://chromedriver.chromium.org/downloads)
    *   For Firefox: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
    *   For Safari: Built-in, no download required

3.  Ensure the WebDriver is in your system's PATH.

### Choosing the Right Method

*   **Use BeautifulSoup (static) for:**
    *   Simple websites with mostly static content
    *   Scenarios where speed is a priority
    *   When you don't need to interact with the page

*   **Use Selenium (dynamic) for:**
    *   Websites with content loaded via JavaScript
    *   Sites that require scrolling or clicking to load more content
    *   When you need to simulate user interactions
*   **Use Tavily Extract for:**
    * Production environments
    * High reliability and scalability

### Troubleshooting

*   If Selenium fails to start, ensure you have the correct WebDriver installed and it's in your system's PATH.
*   If you encounter an `ImportError` related to Selenium, make sure you've installed the Selenium package.
*   If the scraper misses expected content, try switching between static and dynamic scraping to see which works better for your target website.

Remember, the choice between static and dynamic scraping can significantly impact the quality and completeness of the data GPT Researcher can gather. Choose the method that best suits your research needs and the websites you're targeting.

---

## Querying the Backend

### Introduction

In this section, we will discuss how to query the GPTR backend server. The GPTR backend server is a Python server that runs the GPTR Python package. The server listens for WebSocket connections and processes incoming messages to generate reports, streaming back logs and results to the client.

An example WebSocket client is implemented in the `gptr-webhook.js` file below.

This function sends a Webhook Message to the GPTR Python backend running on `localhost:8000`, but this example can also be modified to query a GPTR Server hosted on Linux.

```javascript
// gptr-webhook.js

const WebSocket = require('ws');

let socket = null;
let responseCallback = null;

async function initializeWebSocket() {
  if (!socket) {
    const host = 'localhost:8000';
    const ws_uri = `ws://${host}/ws`;

    socket = new WebSocket(ws_uri);

    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('WebSocket data received:', data);

      if (data.content === 'dev_team_result'
          && data.output.rubber_ducker_thoughts != undefined
          && data.output.tech_lead_review != undefined) {
        if (responseCallback) {
          responseCallback(data.output);
          responseCallback = null; // Clear callback after use
        }
      } else {
        console.log('Received data:', data);
      }
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
      socket = null;
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }
}

async function sendWebhookMessage(message) {
  return new Promise((resolve, reject) => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      initializeWebSocket();
    }

    const data = {
      task: message,
      report_type: 'dev_team',
      report_source: 'web',
      tone: 'Objective',
      headers: {},
      repo_name: 'elishakay/gpt-researcher'
    };

    const payload = "start " + JSON.stringify(data);

    responseCallback = (response) => {
      resolve(response); // Resolve the promise with the WebSocket response
    };

    if (socket.readyState === WebSocket.OPEN) {
      socket.send(payload);
      console.log('Message sent:', payload);
    } else {
      socket.onopen = () => {
        socket.send(payload);
        console.log('Message sent after connection:', payload);
      };
    }
  });
}

module.exports = {
  sendWebhookMessage
};
```
And here's how you can leverage this helper function:

```javascript
const { sendWebhookMessage } = require('./gptr-webhook');

async function main() {
  const message = 'How do I get started with GPT-Researcher Websockets?';
  const response = await sendWebhookMessage(message);
  console.log('Response:', response);
}

```
---
## Troubleshooting

We're constantly working to provide a more stable version. If you're running into any issues, please first check out the [resolved issues](https://github.com/assafelovic/gpt-researcher/issues?q=is%3Aissue+is%3Aclosed) or ask us via our [Discord community](https://discord.gg/MK2EYjphZh).

### `model: gpt-4 does not exist`

This relates to not having permission to use gpt-4 yet. Based on OpenAI, it will be widely available for all by end of July.

### `cannot load library 'gobject-2.0-0'`

The issue relates to the library WeasyPrint (which is used to generate PDFs from the research report). Please follow [this guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) to resolve it:

Or you can install this package manually

In case of MacOS you can install this lib using `brew install glib pango` If you face an issue with linking afterward, you can try running `brew link glib`

In case of Linux you can install this lib using `sudo apt install libglib2.0-dev`

### `cannot load library 'pango'`

In case of MacOS you can install this lib using `brew install pango`

In case of Linux you can install this lib using `sudo apt install libpango-1.0-0`

### Workaround for Mac M chip users

If the above solutions don't work, you can try the following:

1.  Install a fresh version of Python 3.11 pointed to brew: `brew install python@3.11`
2.  Install the required libraries: `brew install pango glib gobject-introspection`
3.  Install the required GPT Researcher Python packages: `pip3.11 install -r requirements.txt`
4.  Run the app with Python 3.11 (using brew): `python3.11 -m uvicorn main:app --reload`

### Error processing the url

We're using Selenium for site scraping. Some sites fail to be scraped. In these cases, restart and try running again.

### Chrome version issues

Many users have an issue with their chromedriver because the latest chrome browser version doesn't have a compatible chrome driver yet.

To downgrade your Chrome web browser using slimjet, follow [these steps](https://www.slimjet.com/chrome/google-chrome-old-version.php). First, visit the website and scroll down to find the list of available older Chrome versions. Choose the version you wish to install making sure it's compatible with your operating system. Once you've selected the desired version, click on the corresponding link to download the installer. Before proceeding with the installation, it's crucial to uninstall your current version of Chrome to avoid conflicts.

It's important to check if the version you downgrade to, has a chromedriver available in the official [chrome driver website](https://chromedriver.chromium.org/downloads)

If none of the above work, you can try out our [hosted beta](https://app.tavily.com/)
