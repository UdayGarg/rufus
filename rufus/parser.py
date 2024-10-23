"""
Instruction Parser Module

This module provides the `InstructionParser` class, which uses OpenAI's gpt-4o API to:
- Parse user instructions and extract relevant keywords.
- Evaluate the relevance of content based on these extracted keywords.
- Handle content in manageable chunks to avoid exceeding token limits in the OpenAI API calls.

Classes:
    InstructionParser: Parses instructions for keyword extraction and checks content relevance using OpenAI's gpt-4o model.

Functions:
    parse_instructions: Extracts keywords from user-provided instructions.
    is_relevant: Evaluates whether the provided content is relevant based on the extracted keywords.
    _split_text: Splits a large text into smaller chunks to avoid exceeding token limits.
"""
import openai
from .logging_config import get_logger

# Get a logger for the current module
logger = get_logger(__name__)

class InstructionParser:
    """
    The InstructionParser class handles the parsing of user-provided instructions to extract
    relevant keywords and assesses the relevance of web content based on these keywords.

    This class leverages the OpenAI gpt-4o model for both keyword extraction and relevance assessment.

    Attributes:
        api_key (str): The OpenAI API key used to make requests to the gpt-4o model.

    Methods:
        parse_instructions(instructions): Extracts keywords from the user-provided instructions.
        is_relevant(content, keywords): Determines whether the extracted content is relevant to the given keywords.
        _split_text(text, max_tokens): Splits large text into smaller chunks to avoid exceeding API token limits.
    """
    def __init__(self, api_key, max_instruction_tokens=60, max_relevant_token = 5, temp = 0.0, max_split_token = 3000):
        """
        Initializes the InstructionParser with the provided OpenAI API key.

        :param api_key: The OpenAI API key for interacting with the gpt-4o model.
        """
        openai.api_key = api_key
        self.max_instruction_tokens = max_instruction_tokens
        self.temp = temp
        self.max_relevant_token = max_relevant_token
        self.max_split_token = max_split_token
        logger.debug("InstructionParser initialized with provided API key.")
    
    def parse_instructions(self, instructions):
        """
        Parses user-provided instructions and extracts relevant keywords using OpenAI's gpt-4o API.

        :param instructions: The instructions provided by the user for the content extraction task.
        :return: A string of keywords relevant to the user’s instructions.
        """
        logger.debug(f"Parsing instructions: {instructions}")
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "Your task is to extract only the most relevant keywords from the user's \
                        provided instructions. Return the keywords as a comma-separated list without additional text or explanations."},
                    {"role": "user",
                     "content": instructions}
                ],
                max_tokens=self.max_instruction_tokens,
                temperature=self.temp,
            )
            keywords = response.choices[0].message.content.strip()
            logger.debug(f"Extracted keywords: {keywords}")
            return keywords
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error during instruction parsing: {e}")
            return ""
    
    def is_relevant(self, content, keywords):
        """
        Determines whether the extracted content is relevant to the provided keywords by checking chunks of text.

        :param content: A dictionary containing the extracted content from a web page, including headings and paragraphs.
        :param keywords: A string of keywords extracted from the user's instructions.
        :return: A boolean indicating whether the content is relevant to the keywords.
        """
        text_content = ' '.join(content.get('headings', []) + content.get('paragraphs', []))
        chunks = self._split_text(text_content)
        relevance = False
        for chunk in chunks:
            prompt = f"Given the keywords: {keywords}\n\nDetermine if the following content is relevant. Answer 'Yes' or 'No'.\n\nContent:\n{chunk}"
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system",
                         "content": "Your task is to determine whether the provided content is relevant to the \
                            given keywords. Be flexible in your assessment, allowing content that fits \
                                the context"},
                        {"role": "user",
                            "content": prompt}
                        ],
                    max_tokens = self.max_relevant_token,
                    temperature = self.temp,
                )
                answer = response.choices[0].message.content.strip().lower()
                logger.debug(f"Relevance assessment result for chunk: {answer}")
                if 'yes' in answer:
                    relevance = True
                    break
            except openai.OpenAIError as e:
                logger.error(f"OpenAI API error during relevance assessment: {e}")
        return relevance

    def _split_text(self, text):
        """
        Splits large text into smaller chunks, each within the specified token limit, to avoid exceeding API limits.

        :param text: The large text content to be split.
        :param max_tokens: The maximum number of tokens allowed in each chunk. Defaults to 3000.
        :return: A list of text chunks, each within the token limit.
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        for word in words:
            current_length += len(word)
            current_chunk.append(word)
            if current_length >= self.max_split_token:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return chunks
    