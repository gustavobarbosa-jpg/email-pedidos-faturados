"""
Integration tests for the email reports pipeline.

This module provides:
- End-to-end pipeline testing
- Component integration testing
- Mock data generation
- Validation testing
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List

from src.orchestration.pipeline import PipelineOrchestrator
from src.extract.powerbi_extractor import PowerBIExtractor
from src.extract.managers_extractor import ManagersExtractor
from src.transform.data_transformer import DataTransformer
from src.delivery.email_service import EmailService


class TestPipelineIntegration:
    """Integration tests for the complete pipeline."""
    
    @pytest.fixture
    def mock_managers_data(self):
        """Mock managers data for testing."""
        return [
            {
                'equipe': 200,
                'nome_gerente': 'Test Manager',
                'email_gerente': 'test@example.com'
            }
        ]
    
    @pytest.fixture
    def mock_orders_data(self):
        """Mock orders data from Power BI."""
        return [
            {
                'dEmpresas[Empresa]': 11,
                'dCalendario[Data]': '2024-01-15',
                'dEquipes[Nome da Equipe]': 'Test Team',
                'dVendedores[Nome Vendedor Completo]': 'Test Seller',
                'dClientes[Nome Completo do Cliente]': 'Test Client',
                'fPedidos[Nota Fiscal - Texto]': 'NF-001',
                'fPedidos[Pedido - Texto]': 'PED-001',
                'fPedidos[Legenda Situação]': 'Faturado',
                'Ingressado': 1000.50
            },
            {
                'dEmpresas[Empresa]': 11,
                'dCalendario[Data]': '2024-01-16',
                'dEquipes[Nome da Equipe]': 'Test Team',
                'dVendedores[Nome Vendedor Completo]': 'Test Seller 2',
                'dClientes[Nome Completo do Cliente]': 'Test Client 2',
                'fPedidos[Nota Fiscal - Texto]': 'NF-002',
                'fPedidos[Pedido - Texto]': 'PED-002',
                'fPedidos[Legenda Situação]': 'Pendente',
                'Ingressado': 2000.75
            }
        ]
    
    def test_managers_extractor_validation(self):
        """Test managers data extraction and validation."""
        extractor = ManagersExtractor()
        
        # Test with valid data
        valid_data = pd.DataFrame({
            'Equipe': [200, 300],
            'Nome da Equipe': ['Manager 1', 'Manager 2'],
            'Email': ['manager1@example.com', 'manager2@example.com']
        })
        
        with patch('pandas.read_excel', return_value=valid_data):
            result = extractor.extract_managers()
        
        assert len(result) == 2
        assert 'equipe' in result.columns
        assert 'nome_gerente' in result.columns
        assert 'email_gerente' in result.columns
        assert result['equipe'].dtype == 'int64'
    
    def test_data_transformation(self, mock_orders_data):
        """Test data transformation logic."""
        transformer = DataTransformer()
        
        result = transformer.transform_orders_data(mock_orders_data)
        
        assert 'PedidosFaturados' in result
        assert 'PedidosPendentes' in result
        assert len(result['PedidosFaturados']) == 1
        assert len(result['PedidosPendentes']) == 1
        
        # Check column mapping
        faturados_df = result['PedidosFaturados']
        assert 'Empresa' in faturados_df.columns
        assert 'Data' in faturados_df.columns
        assert 'Situação' in faturados_df.columns
        assert faturados_df['Situação'].iloc[0] == 'Faturado'
    
    @patch('src.delivery.email_service.smtplib.SMTP_SSL')
    def test_email_service(self, mock_smtp, mock_managers_data):
        """Test email service functionality."""
        # Setup mock
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        service = EmailService()
        
        # Mock report data
        report_data = {
            'PedidosFaturados': pd.DataFrame({'Test': ['Data']}),
            'PedidosPendentes': pd.DataFrame({'Test': ['Data']})
        }
        
        # Test email composition
        result = service.send_manager_report(mock_managers_data[0], report_data)
        
        assert result is True
        mock_smtp.assert_called_once()
    
    @patch('src.extract.powerbi_extractor.requests.post')
    def test_powerbi_extractor(self, mock_post, mock_orders_data):
        """Test Power BI data extraction."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [{
                'tables': [{
                    'rows': mock_orders_data
                }]
            }]
        }
        mock_post.return_value = mock_response
        
        extractor = PowerBIExtractor()
        
        with patch.object(extractor, 'get_access_token', return_value='mock_token'):
            result = extractor.extract_orders_by_team(200)
        
        assert len(result) == 2
        assert isinstance(result, list)
    
    def test_pipeline_validation_mode(self, mock_managers_data, mock_orders_data):
        """Test pipeline in validation mode."""
        orchestrator = PipelineOrchestrator()
        
        with patch.object(orchestrator.managers_extractor, 'get_managers_by_team', 
                       return_value=mock_managers_data), \
             patch.object(orchestrator.extractor, 'extract_orders_by_team', 
                       return_value=mock_orders_data), \
             patch.object(orchestrator.email_service, 'send_manager_report') as mock_email:
            
            result = orchestrator.run_validation_mode([200])
        
        assert result['success'] is True
        assert result['results']['total_managers'] == 1
        assert result['results']['successful'] == 1
        assert result['results']['failed'] == 0
        # Email should not be sent in validation mode
        mock_email.assert_not_called()


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_authentication_failure(self):
        """Test handling of authentication failures."""
        extractor = PowerBIExtractor()
        
        with patch('azure.identity.ClientSecretCredential') as mock_credential:
            mock_credential.side_effect = Exception("Authentication failed")
            
            with pytest.raises(Exception, match="Authentication failed"):
                extractor.get_access_token()
    
    def test_missing_managers_file(self):
        """Test handling of missing managers file."""
        extractor = ManagersExtractor()
        
        with pytest.raises(FileNotFoundError):
            extractor.extract_managers("nonexistent_file.xlsx")
    
    def test_invalid_email_configuration(self):
        """Test handling of invalid email configuration."""
        service = EmailService()
        
        # Mock invalid configuration
        service.config.sender_email = "invalid-email"
        
        assert service.validate_email_config() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
