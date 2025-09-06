# Standard library imports
import logging
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure project-wide logger
logger = logging.getLogger("Project")
logger.setLevel(logging.INFO)

# Formatter for log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# File handler (writes to project.log)
file_handler = logging.FileHandler("logs/project.log")
file_handler.setFormatter(formatter)

# Console handler (prints to console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handlers to the logger (avoid duplicates)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
