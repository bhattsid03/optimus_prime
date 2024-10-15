import logging

def setup_logging(log_file='bot.log', log_level=logging.DEBUG):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Create a file handler and set its level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Optionally, add a console handler for real-time logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # You can set a different level for console output
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # You can also log a message right after setting up logging
    logger.debug('Logging setup complete. Debugging messages will be logged.')

    return logger  # Return the logger for further use if needed

logger = setup_logging()
