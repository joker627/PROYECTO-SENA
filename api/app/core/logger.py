"""Configuración del sistema de logging de la aplicación.

Proporciona un logger configurado con formato estructurado para
facilitar debugging y monitoreo en producción.
"""

import logging
import sys
from typing import Optional


def setup_logger(name: str = "signtechnology", level: int = logging.INFO) -> logging.Logger:
    """Configura y retorna un logger con formato estructurado.
    
    Args:
        name: Nombre del logger.
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        
    Returns:
        Logger configurado.
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya está configurado
    if logger.handlers:
        return logger
        
    logger.setLevel(level)
    
    # Handler para stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Formato estructurado con timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


# Logger global de la aplicación
logger = setup_logger()
