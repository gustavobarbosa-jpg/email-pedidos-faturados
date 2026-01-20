"""
Delivery layer.

This module handles report delivery:
- Email composition and sending
- Attachment handling
- Retry logic and error handling
- Delivery tracking
"""

from .email_service import EmailService

__all__ = ['EmailService']
