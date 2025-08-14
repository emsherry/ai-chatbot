"""Logging configuration for the application."""

import logging
import sys
from pathlib import Path
from typing import Optional

from loguru import logger as loguru_logger


def setup_logger(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True
) -> "loguru_logger":
    """Setup application logger with file and console handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        enable_console: Whether to enable console logging
        
    Returns:
        Configured logger instance
    """
    # Remove default handler
    loguru_logger.remove()
    
    # Set log level
    level = log_level.upper()
    
    # Console handler
    if enable_console:
        loguru_logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=level,
            colorize=True
        )
    
    # File handler
    if log_file:
        log_file_path = Path(log_file)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        loguru_logger.add(
            log_file_path,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            rotation="10 MB",
            retention="30 days",
            compression="zip"
        )
    
    return loguru_logger


# Configure root logger for compatibility
def configure_root_logger(level: str = "INFO") -> None:
    """Configure Python's root logger for compatibility."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


# Global logger instance
logger = setup_logger()
