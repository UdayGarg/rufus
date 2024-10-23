"""
This module implements the RufusClient, a tool for intelligent web data extraction aimed at preparing data 
for use in Retrieval-Augmented Generation (RAG) systems.

RufusClient uses AI to intelligently crawl websites and extract structured documents based on user-defined 
instructions. It includes the following core features:
- Crawl websites up to a specified depth to retrieve web content.
- Parse user instructions to extract relevant keywords using OpenAI's GPT-4o API.
- Selectively synthesize structured documents (JSON or dict) from the crawled data.
- Handle nested links and dynamically loaded content.
- Save or return structured data ready for downstream use in AI pipelines.

Classes:
- RufusClient: Main interface for scraping web content and synthesizing it into structured documents.
"""
import os

import json
from .crawler import Crawler
from .parser import InstructionParser
from .logging_config import get_logger

# Get a logger for the current module
logger = get_logger(__name__)

class RufusClient:
    """
    RufusClient is a tool for intelligent web data extraction aimed at preparing structured data for use in 
    Retrieval-Augmented Generation (RAG) systems.

    The RufusClient leverages a combination of web crawling and AI-driven instruction parsing to collect and 
    extract relevant data from web pages, synthesizing the results into structured formats (JSON or dictionaries). 
    The client is designed to handle nested links, dynamic content, and user-defined extraction instructions.

    Attributes:
        api_key (Optional[str]): The OpenAI API key used for parsing instructions and extracting keywords. If not provided, 
                                 it attempts to retrieve the key from the 'OPENAI_API_KEY' environment variable.
        parser (InstructionParser): A component responsible for parsing user instructions to extract keywords.
        crawler (Crawler): A multithreaded web crawler that extracts content from URLs up to a specified depth.

    Methods:
        scrape(url, instructions, max_depth, output_filename): Scrapes a website based on the given URL and instructions, 
                                                               and optionally saves the results to a JSON file or returns 
                                                               them as a list of structured documents.
    """
    def __init__(self, api_key = None):
        """
        Initialize the RufusClient with an API key.

        :param api_key: Optional OpenAI API key. If not provided, it will attempt to use
                        the environment variable 'OPENAI_API_KEY'.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.error("An OpenAI API key must be provided.")  # Log the error
            raise ValueError("An OpenAI API key must be provided.")
        logger.info("RufusClient initialized with API key.")  # Log successful initialization
        
        # Initialize components
        self.parser = InstructionParser(api_key=self.api_key)
        self.crawler = Crawler(timeout=10, max_retries=3, max_workers=5) 
    
    def scrape(self, url: str, instructions: str, max_depth: int = 3, output_filename = None):
        """
        Scrape the website based on the provided URL and user-defined instructions.

        :param url: The URL of the website to crawl.
        :param instructions: A brief prompt defining the data to be extracted.
        :param max_depth: Maximum depth of links to crawl. Default is 3.
        :param output_filename: Optional filename to save the scraped data in JSON format.
        :return: A list of structured documents as dictionaries, or None if output_filename is provided.
        """
        logger.info(f"Starting scrape on {url} with max depth {max_depth}")
        try:
            # Parse instructions
            keywords: str = self.parser.parse_instructions(instructions)
            logger.debug(f"Keywords extracted: {keywords}")

            # Crawl website
            pages = self.crawler.crawl(url, max_depth=max_depth)
            logger.info(f"Crawled {len(pages)} pages from {url}")

            # Extract content
            documents = []
            for page_url, html in pages.items():
                content = self.crawler.extract_content(html)
                logger.debug(f"Extracted content from {page_url}")
                if self.parser.is_relevant(content, keywords):
                    document = self.crawler.generate_doc(page_url, content) 
                    documents.append(document)
                    logger.debug(f"Document generated for {page_url}")
                else:
                    logger.debug(f"Irrelevant content skipped for {page_url}")

            logger.info(f"Scraping completed, {len(documents)} documents extracted.")
            if output_filename:
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(documents, f, ensure_ascii=False, indent=2)
            else:
                return documents

        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            raise