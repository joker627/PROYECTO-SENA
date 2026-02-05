"""Sistema de logging con formato estructurado."""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "signtechnology", level: int = logging.ERROR) -> logging.Logger:
    """Configura logger con formato estructurado."""
    logger = logging.getLogger(name)
    
    # Clear existing handlers to allow reconfiguration
    logger.handlers.clear()
        
    logger.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Stream handler (console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # Rotating file handler (mejor opción: rotación automática)
    log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5  # Mantener 5 archivos de respaldo
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()
