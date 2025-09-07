import logging
import sys
from config.settings import settings

def setup_logging():
    logging_level = logging.DEBUG if settings.debug else logging.INFO
    
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("quantum_ai.log")
        ]
    )
    
    # Set specific log levels for libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

logger = setup_logging()
