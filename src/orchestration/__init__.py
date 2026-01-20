"""
Orchestration layer.

This module handles pipeline coordination:
- Workflow management
- Error handling and recovery
- Progress tracking
- Audit logging
"""

from .pipeline import PipelineOrchestrator

__all__ = ['PipelineOrchestrator']
