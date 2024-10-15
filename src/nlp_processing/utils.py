import re
import logging
from transformers import GPT2TokenizerFast

# Initialize logger
logger = logging.getLogger(__name__)

def clean_text(text):
    """Cleans input text by removing unwanted characters, spaces, and URLs."""
    try:
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove special characters and extra whitespace
        text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        logger.error(f"Error cleaning text: {e}")
        raise

def tokenize_text(text_list, tokenizer=None, max_length=512):
    """Tokenizes a list of texts using a provided tokenizer or GPT-2 tokenizer as default."""
    try:
        if tokenizer is None:
            tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')  # Default tokenizer if not provided
        return tokenizer(text_list, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    except Exception as e:
        logger.error(f"Error tokenizing text: {e}")
        raise

def load_excel(file_path):
    """Loads an Excel file and returns it as a pandas DataFrame."""
    import pandas as pd
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        logger.error(f"Excel file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        raise

def save_tokenized_data(tokenized_data, file_path):
    """Saves tokenized data to disk."""
    try:
        tokenized_data.save_to_disk(file_path)
        logger.info(f"Tokenized data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving tokenized data: {e}")
        raise
