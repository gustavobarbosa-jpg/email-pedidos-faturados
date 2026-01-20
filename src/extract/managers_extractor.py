"""
Managers data extraction layer.

This module handles:
- Reading managers from Excel files
- Data validation and cleaning
- Type conversion
- Error handling
"""

import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

from src.config.settings import PATH_CONFIG
from src.utils.logger import pipeline_logger


class ManagersExtractor:
    """Extracts and validates managers data from Excel files."""
    
    def __init__(self):
        self.config = PATH_CONFIG
        self.logger = pipeline_logger
        self.required_columns = ['Equipe', 'Nome da Equipe', 'Email']
        self.column_mapping = {
            'Equipe': 'equipe',
            'Nome da Equipe': 'nome_gerente',
            'Email': 'email_gerente'
        }
    
    def extract_managers(self, file_path: str = None) -> pd.DataFrame:
        """
        Extract managers data from Excel file.
        
        Args:
            file_path: Path to managers Excel file
            
        Returns:
            DataFrame with validated managers data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing
            Exception: For other processing errors
        """
        try:
            file_path = file_path or self.config.managers_file
            self.logger.log_step_start("Extract managers data", file_path=file_path)
            
            # Check if file exists
            if not Path(file_path).exists():
                raise FileNotFoundError(f"Managers file not found: {file_path}")
            
            # Read Excel file
            df = pd.read_excel(file_path)
            self.logger.debug(f"Raw managers data loaded", shape=df.shape, columns=list(df.columns))
            
            # Validate required columns
            self._validate_columns(df)
            
            # Clean and transform data
            df = self._clean_data(df)
            
            record_count = len(df)
            self.logger.log_step_end("Extract managers data", record_count)
            
            return df
            
        except Exception as e:
            self.logger.error("Failed to extract managers data", e, file_path=file_path)
            raise
    
    def _validate_columns(self, df: pd.DataFrame):
        """
        Validate that all required columns are present.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValueError: If required columns are missing
        """
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform managers data.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Remove rows with null values in critical columns
        initial_count = len(df)
        df = df.dropna(subset=self.required_columns)
        nulls_removed = initial_count - len(df)
        
        if nulls_removed > 0:
            self.logger.warning(f"Removed {nulls_removed} rows with null values")
        
        # Rename columns
        df = df.rename(columns=self.column_mapping)
        
        # Convert team code to integer
        df['equipe'] = pd.to_numeric(df['equipe'], errors='coerce')
        df = df.dropna(subset=['equipe'])
        df['equipe'] = df['equipe'].astype(int)
        
        # Clean email addresses
        df['email_gerente'] = df['email_gerente'].str.strip().str.lower()
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['equipe', 'email_gerente'])
        duplicates_removed = initial_count - len(df)
        
        if duplicates_removed > 0:
            self.logger.warning(f"Removed {duplicates_removed} duplicate records")
        
        # Validate email format
        df = self._validate_emails(df)
        
        self.logger.debug(f"Data cleaning completed", 
                        final_shape=df.shape,
                        nulls_removed=nulls_removed,
                        duplicates_removed=duplicates_removed)
        
        return df
    
    def _validate_emails(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate email format.
        
        Args:
            df: DataFrame with email column
            
        Returns:
            DataFrame with invalid emails removed
        """
        import re
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Filter valid emails
        valid_emails = df['email_gerente'].str.match(email_pattern, na=False)
        invalid_count = len(df) - valid_emails.sum()
        
        if invalid_count > 0:
            self.logger.warning(f"Found {invalid_count} invalid email addresses")
            invalid_emails = df[~valid_emails]['email_gerente'].tolist()
            self.logger.debug("Invalid emails", invalid_emails=invalid_emails[:5])  # Log first 5
        
        return df[valid_emails]
    
    def get_managers_by_team(self, team_codes: List[int] = None) -> List[Dict[str, Any]]:
        """
        Get managers filtered by team codes.
        
        Args:
            team_codes: List of team codes to filter by
            
        Returns:
            List of manager dictionaries
        """
        try:
            df = self.extract_managers()
            
            if team_codes:
                df = df[df['equipe'].isin(team_codes)]
            
            # Convert to list of dictionaries
            managers = df.to_dict('records')
            
            self.logger.info(f"Retrieved {len(managers)} managers", 
                          team_filter=team_codes)
            
            return managers
            
        except Exception as e:
            self.logger.error("Failed to get managers by team", e, team_codes=team_codes)
            raise
