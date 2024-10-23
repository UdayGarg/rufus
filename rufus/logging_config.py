"""
logging_config.py

This module provides a utility function to create and configure loggers with console and file handlers.
The log files are saved in a "logs" directory, and the log level for the console is set to INFO while
the log level for the file is set to DEBUG. If the "logs" directory does not exist, it will be created
automatically.

Usage:
    Import the module and call `get_logger` with a logger name to get a pre-configured logger.

Example:
    from logging_config import get_logger
    logger = get_logger('my_module')
    logger.info("This is an info message")
    logger.debug("This is a debug message")
"""
import os
import logging

# Ensure the logs directory exists
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name):
    """
    Creates and configures a logger with both console and file handlers.

    The logger is configured with:
    - A StreamHandler for console output at the INFO level.
    - A FileHandler that writes logs to a file in the "logs" directory at the DEBUG level.
    - A common log format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    If the logger already has handlers, no additional handlers are added to avoid duplicate logging.

    Args:
        name (str): The name of the logger, typically the name of the module using the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)  # Create a logger for the given module
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create handlers
    console_handler = logging.StreamHandler()  # Console output
    console_handler.setLevel(logging.INFO)  # Set handler level for console logging
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, f'{name}.log'))  # Log to a file
    file_handler.setLevel(logging.DEBUG)  # Set handler level for file logging

    # Create a formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger if not already added
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger