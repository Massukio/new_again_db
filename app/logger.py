import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Create a rotating file handler for info level
info_handler = RotatingFileHandler("info.log", maxBytes=10*1024*1024, backupCount=5)
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
info_handler.setFormatter(info_formatter)

# Create a rotating file handler for debug level
debug_handler = RotatingFileHandler("debug.log", maxBytes=10*1024*1024, backupCount=5)
debug_handler.setLevel(logging.DEBUG)
debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
debug_handler.setFormatter(debug_formatter)

# Create a rotating file handler for error level
error_handler = RotatingFileHandler("error.log", maxBytes=10*1024*1024, backupCount=5)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

# Add the handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(debug_handler)
logger.addHandler(error_handler)
