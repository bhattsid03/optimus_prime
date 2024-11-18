import logging

def setup_logging(log_file='bot.log', log_level=logging.DEBUG):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.basicConfig(handlers=[file_handler, console_handler], level=log_level)
    logger.debug('Logging setup complete. Debugging messages will be logged.')

    return logger

logger = setup_logging()
