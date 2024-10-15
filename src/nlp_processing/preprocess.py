import pandas as pd
from transformers import AutoTokenizer
import logging
import os
from src.utils.logging import setup_logging

# Set up logging
logger = setup_logging(log_file='preprocess.log', log_level=logging.DEBUG)

def preprocess_chat_data(file_path):
    """
    Preprocess chat data for GPT-J training or inference.
    
    :param file_path: Path to the CSV file containing chat data
    :return: Tokenized inputs and responses
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        # Load the chat data
        data = pd.read_csv(file_path)
        
        if 'Input' not in data.columns or 'Response' not in data.columns:
            logger.error(f"CSV file must contain 'Input' and 'Response' columns.")
            raise ValueError("CSV file must contain 'Input' and 'Response' columns.")
        
        # Initialize GPT-J tokenizer
        tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-j-6B')
        
        # Tokenize inputs and responses
        inputs = tokenizer(
            list(data['Input']), 
            return_tensors='pt', 
            padding=True, 
            truncation=True, 
            max_length=1024  # Adjust max_length if needed
        )
        
        outputs = tokenizer(
            list(data['Response']), 
            return_tensors='pt', 
            padding=True, 
            truncation=True, 
            max_length=1024  # Adjust max_length if needed
        )
        
        logger.info("Tokenization completed successfully.")
        return inputs, outputs
    
    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        raise
    
    except ValueError as val_error:
        logger.error(val_error)
        raise
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise