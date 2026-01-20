"""
Data transformation layer.

This module handles:
- Data cleaning and standardization
- Column mapping and renaming
- Business rule application
- Data segmentation
"""

import pandas as pd
from typing import Dict, List, Tuple, Any
from datetime import datetime

from src.config.settings import BUSINESS_RULES
from src.utils.logger import pipeline_logger


class DataTransformer:
    """Transforms raw data into business-ready format."""
    
    def __init__(self):
        self.logger = pipeline_logger
        self.business_rules = BUSINESS_RULES
        
        # Column mapping from Power BI to business format
        self.column_mapping = {
            'Empresa': 'Empresa',
            'Data': 'Data',
            'Nome da Equipe': 'Equipe',
            'Nome Vendedor Completo': 'Vendedor',
            'Nome Completo do Cliente': 'Cliente',
            'Nota Fiscal - Texto': 'Nota Filsca',
            'Pedido - Texto': 'Pedido',
            'Legenda Situação': 'Situação',
            'Ingressado': 'Ingressado'
        }
        
        # Desired column order
        self.column_order = [
            'Empresa', 'Data', 'Equipe', 'Vendedor', 
            'Cliente', 'Nota Filsca', 'Pedido', 'Situação', 'Ingressado'
        ]
    
    def transform_orders_data(self, raw_data: List[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
        """
        Transform raw orders data into segmented DataFrames.
        
        Args:
            raw_data: List of raw order records from Power BI
            
        Returns:
            Dictionary with 'PedidosFaturados' and 'PedidosPendentes' DataFrames
        """
        try:
            self.logger.log_step_start("Transform orders data", 
                                   raw_records=len(raw_data))
            
            # Create DataFrame from raw data
            df = pd.DataFrame(raw_data)
            
            if df.empty:
                self.logger.warning("No data to transform")
                return {
                    'PedidosFaturados': pd.DataFrame(columns=self.column_order),
                    'PedidosPendentes': pd.DataFrame(columns=self.column_order)
                }
            
            # Apply transformations
            df = self._clean_column_names(df)
            df = self._map_columns(df)
            df = self._apply_business_rules(df)
            df = self._validate_data(df)
            df = self._order_columns(df)
            
            # Segment by status
            segmented_data = self._segment_by_status(df)
            
            # Log transformation summary
            self._log_transformation_summary(segmented_data)
            
            self.logger.log_step_end("Transform orders data")
            
            return segmented_data
            
        except Exception as e:
            self.logger.error("Failed to transform orders data", e)
            raise
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean column names from Power BI format.
        
        Args:
            df: DataFrame with raw column names
            
        Returns:
            DataFrame with cleaned column names
        """
        # Remove table references and brackets
        df.columns = [
            col.split('[')[-1].replace(']', '') if '[' in col else col 
            for col in df.columns
        ]
        
        self.logger.debug("Column names cleaned", 
                        original_columns=list(df.columns))
        
        return df
    
    def _map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map columns to business standard names.
        
        Args:
            df: DataFrame with raw column names
            
        Returns:
            DataFrame with mapped column names
        """
        # Only map columns that exist
        available_mapping = {
            old: new for old, new in self.column_mapping.items() 
            if old in df.columns
        }
        
        df = df.rename(columns=available_mapping)
        
        self.logger.debug("Columns mapped", 
                        mapping=available_mapping)
        
        return df
    
    def _apply_business_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply business rules to the data.
        
        Args:
            df: DataFrame to apply rules to
            
        Returns:
            DataFrame with business rules applied
        """
        initial_count = len(df)
        
        # Convert data types
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        
        if 'Ingressado' in df.columns:
            df['Ingressado'] = pd.to_numeric(df['Ingressado'], errors='coerce')
        
        # Remove rows with invalid dates
        if 'Data' in df.columns:
            df = df.dropna(subset=['Data'])
        
        # Apply company filter (additional validation)
        if 'Empresa' in df.columns:
            valid_companies = self.business_rules.valid_companies
            df = df[df['Empresa'].isin(valid_companies)]
        
        # Standardize status values
        if 'Situação' in df.columns:
            df['Situação'] = df['Situação'].str.strip()
        
        final_count = len(df)
        filtered_count = initial_count - final_count
        
        if filtered_count > 0:
            self.logger.info(f"Applied business rules", 
                          records_filtered=filtered_count,
                          final_records=final_count)
        
        return df
    
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate data quality and consistency.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Validated DataFrame
        """
        # Check for required columns
        required_columns = ['Empresa', 'Data', 'Equipe']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns after transformation: {missing_columns}")
        
        # Check for null values in critical fields
        null_counts = df[required_columns].isnull().sum()
        if null_counts.any():
            self.logger.warning("Found null values in critical fields", 
                             null_counts=null_counts.to_dict())
        
        return df
    
    def _order_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Order columns according to business standard.
        
        Args:
            df: DataFrame to reorder
            
        Returns:
            DataFrame with ordered columns
        """
        # Only include columns that exist
        available_columns = [col for col in self.column_order if col in df.columns]
        
        # Add any additional columns at the end
        additional_columns = [col for col in df.columns if col not in available_columns]
        final_order = available_columns + additional_columns
        
        return df[final_order]
    
    def _segment_by_status(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Segment data by order status.
        
        Args:
            df: DataFrame to segment
            
        Returns:
            Dictionary with segmented DataFrames
        """
        faturado_status = self.business_rules.faturado_status
        
        # Create segments
        df_faturados = df[df['Situação'] == faturado_status].copy()
        df_pendentes = df[df['Situação'] != faturado_status].copy()
        
        return {
            'PedidosFaturados': df_faturados,
            'PedidosPendentes': df_pendentes
        }
    
    def _log_transformation_summary(self, segmented_data: Dict[str, pd.DataFrame]):
        """
        Log transformation summary statistics.
        
        Args:
            segmented_data: Dictionary with segmented DataFrames
        """
        total_records = sum(len(df) for df in segmented_data.values())
        
        summary = {
            'total_records': total_records,
            'segments': {}
        }
        
        for segment_name, df in segmented_data.items():
            record_count = len(df)
            summary['segments'][segment_name] = record_count
            
            # Additional statistics for each segment
            if not df.empty and 'Empresa' in df.columns:
                companies = df['Empresa'].nunique()
                summary['segments'][f'{segment_name}_companies'] = companies
            
            if not df.empty and 'Ingressado' in df.columns:
                total_ingressado = df['Ingressado'].sum()
                summary['segments'][f'{segment_name}_total_ingressado'] = total_ingressado
        
        self.logger.info("Data transformation completed", **summary)
    
    def get_summary_stats(self, segmented_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Get summary statistics for the transformed data.
        
        Args:
            segmented_data: Dictionary with segmented DataFrames
            
        Returns:
            Dictionary with summary statistics
        """
        stats = {
            'total_records': 0,
            'faturados_count': 0,
            'pendentes_count': 0,
            'total_ingressado': 0,
            'faturados_ingressado': 0,
            'pendentes_ingressado': 0
        }
        
        for segment_name, df in segmented_data.items():
            record_count = len(df)
            stats['total_records'] += record_count
            
            if 'PedidosFaturados' in segment_name:
                stats['faturados_count'] = record_count
                if 'Ingressado' in df.columns:
                    stats['faturados_ingressado'] = df['Ingressado'].sum()
            else:
                stats['pendentes_count'] = record_count
                if 'Ingressado' in df.columns:
                    stats['pendentes_ingressado'] = df['Ingressado'].sum()
        
        stats['total_ingressado'] = stats['faturados_ingressado'] + stats['pendentes_ingressado']
        
        return stats
