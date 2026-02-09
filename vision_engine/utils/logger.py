"""
Logger Module: Logging utilities for the Vision Engine
"""

import logging
import sys
from datetime import datetime
from typing import Optional


class Logger:
    """
    Custom logger for the Vision Engine.
    
    Provides structured logging with different levels and output formats.
    """
    
    def __init__(self, name: str = "VisionEngine", level: int = logging.INFO):
        self.name = name
        self.level = level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Prevent adding handlers multiple times
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log a critical message."""
        self.logger.critical(message)
    
    def log_performance(self, operation: str, duration: float, details: Optional[dict] = None):
        """Log performance metrics for an operation."""
        perf_message = f"PERFORMANCE: {operation} took {duration:.4f}s"
        if details:
            perf_message += f" | Details: {details}"
        self.logger.info(perf_message)