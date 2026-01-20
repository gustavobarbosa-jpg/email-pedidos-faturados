"""
Logging utilities for the email reports pipeline.

This module provides structured logging with:
- File and console handlers
- Log rotation
- Structured formatting
- Error tracking
"""

import logging
import logging.handlers
import os
import sys
from typing import Optional
from datetime import datetime

from src.config.settings import LOGGING_CONFIG


class PipelineLogger:
    """Centralized logging for the pipeline."""
    
    def __init__(self, name: str = "pipeline", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOGGING_CONFIG.log_level.upper()))
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers(log_file)
    
    def _setup_handlers(self, log_file: Optional[str] = None):
        """Setup file and console handlers."""
        
        # File handler with rotation
        file_path = log_file or LOGGING_CONFIG.log_file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=LOGGING_CONFIG.max_file_size,
            backupCount=LOGGING_CONFIG.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(LOGGING_CONFIG.log_format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message with optional context."""
        if kwargs:
            message = f"{message} | Context: {kwargs}"
        self.logger.info(message)
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error message with optional exception."""
        if kwargs:
            message = f"{message} | Context: {kwargs}"
        if exception:
            message = f"{message} | Exception: {str(exception)}"
        self.logger.error(message)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with optional context."""
        if kwargs:
            message = f"{message} | Context: {kwargs}"
        self.logger.warning(message)
    
    def debug(self, message: str, **kwargs):
        """Log debug message with optional context."""
        if kwargs:
            message = f"{message} | Context: {kwargs}"
        self.logger.debug(message)
    
    def log_pipeline_start(self, pipeline_name: str):
        """Log pipeline start."""
        self.info(f"Starting pipeline: {pipeline_name}")
    
    def log_pipeline_end(self, pipeline_name: str, duration: Optional[float] = None):
        """Log pipeline completion."""
        message = f"Completed pipeline: {pipeline_name}"
        if duration:
            message += f" | Duration: {duration:.2f}s"
        self.info(message)
    
    def log_step_start(self, step_name: str, **kwargs):
        """Log step start with optional context."""
        message = f"Starting step: {step_name}"
        if kwargs:
            message = f"{message} | Context: {kwargs}"
        self.logger.info(message)
    
    def log_step_end(self, step_name: str, record_count: Optional[int] = None):
        """Log step completion."""
        message = f"Completed step: {step_name}"
        if record_count is not None:
            message += f" | Records: {record_count}"
        self.info(message)


# Global logger instance
pipeline_logger = PipelineLogger()
