import logging
import sys

def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate logs if setup_logging is called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logging()
