
# Rufus: Intelligent Web Data Extraction Tool for LLMs (Retrieval-Augmented Generation)

## Overview

**Rufus** is a tool designed to perform web crawling, content extraction, and synthesis of data into structured documents. The primary purpose of Rufus is to retrieve relevant information from websites and present it in a structured, easily usable format for LLM-based Retrieval-Augmented Generation (RAG) systems. Rufus can handle nested links and extract content from HTML pages, synthesizing the extracted data into JSON or plain text formats.

---

## Key Features

- **Crawling Websites:** Rufus crawls websites based on user-defined prompts and traverses links up to a configurable depth to extract relevant data.
- **Content Extraction:** Rufus extracts structured content such as page titles, headings, paragraphs, and links using BeautifulSoup.
- **Nested Links Handling:** Rufus can follow and crawl nested links within the same domain up to a specified depth.
- **Structured Output:** The extracted data is synthesized into structured documents, such as JSON, which can be saved locally or returned as Python dictionaries.
- **Error Handling:** Rufus includes error handling mechanisms to retry failed requests and handle page access issues.

---

## Project Structure

The repository is organized into several key components:

```
.
├── README.md               # This file
├── demo.py                 # Demo script to showcase Rufus in action
├── logs/                   # Logs directory for client, crawler, and parser logs
│   ├── rufus.client.log
│   ├── rufus.crawler.log
│   └── rufus.parser.log
├── requirements.txt        # Python dependencies
├── rufus/                  # Rufus package
│   ├── __init__.py
│   ├── client.py           # RufusClient class (main entry point)
│   ├── crawler.py          # Web crawling functionality
│   ├── logging_config.py   # Configurations for logging
│   └── parser.py           # Instruction parser for AI-based content extraction
└── test_crawler.py         # Test cases for the web crawler
```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/UdayGarg/rufus.git
   cd rufus
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### RufusClient

The `RufusClient` class is the main interface for interacting with Rufus. It provides the `scrape` method to crawl a website and extract relevant content based on user-defined instructions.

#### Basic Example:

```python
from rufus import RufusClient
import os

# Initialize the client with your OpenAI API key
client = RufusClient(api_key=os.getenv('OPENAI_API_KEY'))

# Scrape a website with instructions
documents = client.scrape(
    url="https://www.example.com", 
    instructions="Find information about product features and customer FAQs.",
    max_depth=3  # Set the depth to crawl
)

# Print the structured output
print(documents)
```

### Crawling Custom Websites

To crawl a custom website, you can use a prompt-based approach to define what kind of data Rufus should extract.

#### Example:

```python
instructions = "Retrieve application guidelines and contact information."
documents = client.scrape("https://www.sfgov.com", max_depth=2)
```

This will prompt Rufus to crawl the specified URL, extract application guidelines and contact information, and synthesize it into a structured document.

---

## Rufus Components

### 1. Web Crawler (`crawler.py`)

The crawler is responsible for navigating through web pages, collecting raw HTML content, and extracting relevant information (titles, headings, paragraphs, links). It can handle nested links within the same domain, ensuring comprehensive crawling of a website.

- **`extract_content(html)`**: Extracts content (headings, paragraphs, and links) from a given HTML page.
- **`generate_doc(url, content)`**: Converts the extracted content into a structured document format.

### 2. Instruction Parser (`parser.py`)

The instruction parser uses OpenAI’s GPT-4 API to extract relevant keywords from user-provided instructions. It evaluates whether the crawled content is relevant to those keywords before synthesizing it into a document.

- **`parse_instructions(instructions)`**: Extracts keywords from user instructions.
- **`is_relevant(content, keywords)`**: Determines if the extracted content is relevant based on the parsed keywords.

### 3. Logging Configuration (`logging_config.py`)

Logging is configured to track the operation of Rufus, including crawling progress, keyword extraction, and any errors encountered during scraping. Logs are saved in the `logs/` directory.

---

## Handling Edge Cases

- **Retry Mechanism**: Rufus includes a retry mechanism for failed requests (e.g., network issues, HTTP errors) to ensure robust crawling.
- **Handling Nested Links**: Rufus can follow and crawl nested links within the same domain up to a specified depth.
- **No Support for JavaScript-Rendered Pages**: Rufus does not handle dynamic content rendered by JavaScript. It works with static HTML content only.

---

## Challenges and Solutions

### Challenge 1: Extracting Relevant Content Based on User Prompts

Extracting only the relevant content (as defined by user prompts) was a challenge. Rufus uses GPT-4-based instruction parsing to intelligently extract keywords and match them against the extracted content.

### Challenge 2: Handling Deeply Nested Links

Rufus is capable of handling deeply nested links up to a configurable depth, ensuring comprehensive coverage of the target website.

---

## Future Improvements

1. **Support for JavaScript-rendered Content**: Adding support for JavaScript execution to handle dynamic content and single-page applications.
2. **Customizable Link Filtering**: Allow users to specify custom rules for link crawling (e.g., filtering out specific domains or link patterns).
3. **Better Error Handling for Specific Domains**: Implement specific error handling mechanisms for common website structures like captchas or login-required pages.

---

Thank you for using Rufus!