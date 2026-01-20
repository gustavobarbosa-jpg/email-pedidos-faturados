"""
Data extraction layer.

This module handles data extraction from various sources:
- Power BI semantic models via DAX queries
- Excel files with manager information
- Data validation and cleaning
"""

from .powerbi_extractor import PowerBIExtractor
from .managers_extractor import ManagersExtractor

__all__ = ['PowerBIExtractor', 'ManagersExtractor']
