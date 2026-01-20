"""
Power BI data extraction layer.

This module handles:
- Authentication with Azure AD
- DAX query execution
- Data extraction from semantic models
- Error handling and retry logic
"""

import json
import requests
from typing import Dict, Any, Optional, List
from azure.identity import ClientSecretCredential

from src.config.settings import POWER_BI_CONFIG
from src.utils.logger import pipeline_logger


class PowerBIExtractor:
    """Extracts data from Power BI semantic models."""
    
    def __init__(self):
        self.config = POWER_BI_CONFIG
        self.logger = pipeline_logger
        self._access_token = None
    
    def get_access_token(self) -> str:
        """
        Obtain access token from Azure AD.
        
        Returns:
            str: Access token for Power BI API
            
        Raises:
            Exception: If authentication fails
        """
        try:
            self.logger.log_step_start("Azure AD Authentication")
            
            credential = ClientSecretCredential(
                tenant_id=self.config.tenant_id,
                client_id=self.config.client_id,
                client_secret=self.config.client_secret
            )
            
            token = credential.get_token(self.config.scope)
            self._access_token = token.token
            
            self.logger.log_step_end("Azure AD Authentication")
            return self._access_token
            
        except Exception as e:
            self.logger.error("Failed to obtain access token", e)
            raise Exception(f"Authentication failed: {str(e)}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        if not self._access_token:
            self.get_access_token()
        
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json"
        }
    
    def execute_dax_query(self, query: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Execute DAX query against semantic model.
        
        Args:
            query: DAX query string
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dict containing query results
            
        Raises:
            Exception: If query execution fails after retries
        """
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.config.workspace_id}/datasets/{self.config.semantic_model_id}/executeQueries"
        
        payload = {
            "queries": [
                {
                    "query": query
                }
            ]
        }
        
        headers = self._get_headers()
        
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"Executing DAX query (attempt {attempt + 1})", query_length=len(query))
                
                response = requests.post(url, headers=headers, json=payload, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.debug("DAX query executed successfully", 
                                   result_size=len(str(result)))
                    return result
                elif response.status_code == 401:
                    # Token expired, refresh and retry
                    self.logger.warning("Access token expired, refreshing...")
                    self._access_token = None
                    headers = self._get_headers()
                else:
                    self.logger.error(f"DAX query failed", 
                                   status_code=response.status_code,
                                   response_text=response.text[:500])
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request exception during DAX query", e, attempt=attempt + 1)
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to execute DAX query after {max_retries} attempts: {str(e)}")
        
        raise Exception(f"Failed to execute DAX query after {max_retries} attempts")
    
    def extract_orders_by_team(self, team_code: int) -> Optional[List[Dict[str, Any]]]:
        """
        Extract orders data for a specific team.
        
        Args:
            team_code: Team code to filter by
            
        Returns:
            List of order records
            
        Raises:
            Exception: If extraction fails
        """
        try:
            self.logger.log_step_start(f"Extract orders for team {team_code}")
            
            from src.config.settings import DAXQueries
            query = DAXQueries.get_orders_by_team(team_code)
            
            result = self.execute_dax_query(query)
            
            if not result:
                raise Exception(f"No results returned for team {team_code}")
            
            # Extract rows from response
            tables = result.get('results', [{}])[0].get('tables', [])
            if not tables:
                raise Exception(f"No tables found in response for team {team_code}")
            
            rows = tables[0].get('rows', [])
            record_count = len(rows)
            
            self.logger.log_step_end(f"Extract orders for team {team_code}", record_count)
            return rows
            
        except Exception as e:
            self.logger.error(f"Failed to extract orders for team {team_code}", e)
            raise
    
    def validate_connection(self) -> bool:
        """
        Validate connection to Power BI API.
        
        Returns:
            bool: True if connection is valid
        """
        try:
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.config.workspace_id}/datasets/{self.config.semantic_model_id}"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            self.logger.error("Connection validation failed", e)
            return False
