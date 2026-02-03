"""Sistema de logging con formato estructurado."""

import logging
import sys

def setup_logger(name: str = "signtechnology", level: int = logging.INFO) -> logging.Logger:
    """Configura logger con formato estructurado."""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
        
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logger()
