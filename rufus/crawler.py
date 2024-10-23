"""
Web Crawler Module

This module implements a basic web crawler using multithreading to crawl web pages
up to a specified depth, extract content from them, and store the results in a
structured format. The crawler is designed to retry failed requests, log progress,
and respect the domain boundaries of the base URL.

Classes:
    Crawler: Implements the main crawling functionality, including recursive crawling,
    content extraction, and document synthesis.

Functions:
    extract_content: Extracts and organizes content from HTML pages.
    synthesize_document: Converts extracted content into a structured format.
    crawl: Initiates a crawl starting from the base URL and processes pages recursively.
    _crawl_recursive: Internal function that handles recursive crawling of pages.
    _is_same_domain: Checks if two URLs belong to the same domain.

Usage Example:
    crawler = Crawler(timeout=10, max_retries=3, max_workers=5)
    results = crawler.crawl(base_url="https://example.com", max_depth=3)
"""
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from .logging_config import get_logger

# Get a logger for the current module
logger = get_logger(__name__)

class Crawler:
    """
    A web crawler class that supports multithreaded crawling of web pages.

    Attributes:
        timeout (int): Timeout for HTTP requests in seconds.
        max_retries (int): Maximum number of retries for failed requests.
        max_workers (int): Maximum number of concurrent threads for crawling.
        visited_urls (set): A set to track URLs that have already been visited.
        executor (ThreadPoolExecutor): A thread pool executor to manage crawling threads.

    Methods:
        extract_content(html): Extracts title, headings, paragraphs, and links from the HTML.
        synthesize_document(url, content): Converts extracted content into a structured format.
        crawl(base_url, max_depth): Starts crawling from the base URL up to the specified depth.
        _crawl_recursive(base_url, url, depth, max_depth, pages): Recursively crawls URLs up to the specified depth.
        _is_same_domain(base_url, url): Checks if two URLs belong to the same domain.
    """
    def __init__(self, timeout=10, max_retries=3, max_workers=5):
        """
        Initializes the Crawler object with specified parameters.

        Args:
            timeout (int): Timeout for HTTP requests in seconds. Defaults to 10.
            max_retries (int): Maximum number of retries for failed requests. Defaults to 3.
            max_workers (int): Maximum number of concurrent threads for crawling. Defaults to 5.
        """
        self.visited_urls = set()
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        logger.debug("Crawler initialized with multithreading.")

    def extract_content(self, html):
        """
        Extracts title, headings, paragraphs, and links from the HTML content.

        Args:
            html (str): The HTML content of a web page.

        Returns:
            dict: A dictionary containing the page title, headings, paragraphs, and links.
        """
        logger.debug("Extracting content from HTML.")
        soup = BeautifulSoup(html, 'html.parser')
        content = {
            'title': soup.title.string.strip() if soup.title else '',
            'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
            'paragraph': [p.get_text(strip=True) for p in soup.find_all('p')],
            'links': [a['href'] for a in soup.find_all('a', href=True)],
        }
        logger.debug(f"Extracted content: {content}")
        return content
    
    def generate_doc(self, url, content):
        """
        Converts extracted content into a structured document format.

        Args:
            url (str): The URL of the page.
            content (dict): The extracted content from the page.

        Returns:
            dict: A structured document containing the URL, title, and paragraphs of the page.
        """
        logger.debug(f"Generating document for URL: {url}")
        document = {
            'url': url,
            'title': content.get('title', ''),
            'content': content.get('paragraph', []),
        }
        logger.debug(f"Generated document: {document}")
        return document
    
    def crawl(self, base_url, max_depth=3):
        """
        Initiates a crawl starting from the base URL and processes pages recursively up to the specified depth.

        Args:
            base_url (str): The starting URL for the crawl.
            max_depth (int): The maximum depth to crawl. Defaults to 3.

        Returns:
            dict: A dictionary mapping URLs to the HTML content of the crawled pages.
        """
        logger.info(f"Starting crawl at {base_url} with max depth {max_depth}.")
        pages = {}
        future_to_url = {}
        
        # Initial seed URL
        future_to_url[self.executor.submit(self._crawl_recursive, base_url, base_url, 0, max_depth, pages)] = base_url
        
        # Process futures as they complete
        for future in as_completed(future_to_url):
            try:
                future.result()  # Trigger any exceptions
            except Exception as e:
                logger.error(f"Error processing URL {future_to_url[future]}: {e}")
        
        self.executor.shutdown(wait=True)
        logger.info(f"Crawling complete. Visited {len(self.visited_urls)} URLs.")
        return pages
    
    def _crawl_recursive(self, base_url, url, depth, max_depth, pages):
        """
        Recursively crawls URLs up to the specified depth.

        Args:
            base_url (str): The starting URL for the crawl.
            url (str): The current URL being crawled.
            depth (int): The current depth of the crawl.
            max_depth (int): The maximum depth to crawl.
            pages (dict): A dictionary to store the HTML content of the crawled pages.
        """
        if depth > max_depth or url in self.visited_urls:
            logger.debug(f"Skipping URL {url} at depth {depth}.")
            return
        logger.debug(f"Crawling URL {url} at depth {depth}.")
        self.visited_urls.add(url)
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=self.timeout)
                if response.status_code == 404:
                    logger.warning(f"URL not found (404): {url}")
                    return
                response.raise_for_status()  # Raise exception for other 4xx/5xx errors
                html = response.text
                pages[url] = html
                soup = BeautifulSoup(html, 'html.parser')
                links = [urljoin(base_url, link['href']) for link in soup.find_all('a', href=True)]
                
                # Schedule next batch of URLs in the same domain
                for next_url in links:
                    if urlparse(base_url).netloc == urlparse(next_url).netloc: # avoid loops
                        self.executor.submit(self._crawl_recursive, base_url, next_url, depth + 1, max_depth, pages)
                return  # Break out after successful response
            except requests.exceptions.RequestException as e:
                logger.error(f"Attempt {attempt+1}/{self.max_retries} failed for {url}: {e}")
                time.sleep(1)  # Backoff before retrying
        logger.error(f"Failed to crawl {url} after {self.max_retries} attempts.")


if __name__ == "__main__":
    # test usage
    crawler = Crawler(timeout=10, max_retries=3, max_workers=5)
    base_url = "https://www.bu.edu/cs/masters/program/"
    results = crawler.crawl(base_url, max_depth=3)
    print(results.keys())
    print(f"Crawled {len(results)} pages.")
