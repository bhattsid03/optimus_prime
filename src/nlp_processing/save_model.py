from transformers import GPTJForCausalLM, AutoTokenizer
import logging
import os

# Assuming you are using the setup_logging from your logging.py file
from src.utils.logging import setup_logging

# Set up logging
logger = setup_logging(log_file='save_model.log', log_level=logging.DEBUG)

def save_model_and_tokenizer(model_name='EleutherAI/gpt-j-6B', save_path='../../models/base_model'):
    """
    Load and save a pre-trained GPT-J model and tokenizer to the specified directory.
    
    :param model_name: Name of the pre-trained model to load
    :param save_path: Directory path to save the model and tokenizer
    """
    try:
        # Load pre-trained GPT-J model and tokenizer
        logger.info(f"Loading pre-trained model: {model_name}")
        model = GPTJForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Ensure the save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            logger.info(f"Created directory: {save_path}")

        # Save the model and tokenizer to the specified directory
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)
        
        logger.info(f"Model and tokenizer saved to {save_path}")
        print(f"GPT-J model and tokenizer saved to {save_path}")
    
    except Exception as e:
        logger.error(f"An error occurred while saving the model: {e}")
        raise

