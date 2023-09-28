# logger_config.py

import logging
import os
if not os.path.exists('logs'):
    os.mkdir('logs')
def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler('logs/server_log.log')
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Console handler (optional)
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger
logger = setup_logger()
