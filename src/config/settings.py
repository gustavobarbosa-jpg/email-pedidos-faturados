"""
Configuration settings for the email reports pipeline.

This module centralizes all configuration parameters including:
- Database and API connections
- Email settings
- File paths
- Business rules
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class PowerBIConfig:
    """Power BI API configuration."""
    tenant_id: str = os.getenv("TENANT_ID", "")
    client_id: str = os.getenv("CLIENT_ID", "")
    client_secret: str = os.getenv("CLIENT_SECRET", "")
    scope: str = os.getenv("POWER_BI_SCOPE", "https://analysis.windows.net/powerbi/api/.default")
    workspace_id: str = os.getenv("WORKSPACE_ID", "")
    semantic_model_id: str = os.getenv("SEMANTIC_MODEL_ID", "")


@dataclass
class EmailConfig:
    """Email service configuration."""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465
    sender_email: str = os.getenv("EMAIL", "gustavo.barbosa@vilanova.com.br")
    app_password: str = os.getenv("password_app", "")
    use_ssl: bool = True


@dataclass
class PathConfig:
    """File path configuration."""
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir: str = os.path.join(base_dir, "data")
    raw_data_dir: str = os.path.join(data_dir, "raw")
    processed_data_dir: str = os.path.join(data_dir, "processed")
    temp_data_dir: str = os.path.join(data_dir, "temp")
    logs_dir: str = os.path.join(base_dir, "logs")
    managers_file: str = os.path.join(data_dir, "raw", "dGerentes.xlsx")


@dataclass
class BusinessRules:
    """Business rules and filters."""
    valid_companies: List[int] = None
    current_month_filter: bool = True
    faturado_status: str = "Faturado"
    
    def __post_init__(self):
        if self.valid_companies is None:
            self.valid_companies = [1, 10, 11, 12, 14]


@dataclass
class DAXQueries:
    """DAX query templates."""
    
    @staticmethod
    def get_orders_by_team(team_code: int) -> str:
        """Get DAX query for orders filtered by team."""
        companies_str = ', '.join(map(str, BusinessRules().valid_companies))
        return f"""
        EVALUATE
        SUMMARIZECOLUMNS(
            'dEmpresas'[Empresa],
            'dCalendario'[Data],
            'dEquipes'[Nome da Equipe],
            'dVendedores'[Nome Vendedor Completo],
            'dClientes'[Nome Completo do Cliente],
            'fPedidos'[Nota Fiscal - Texto],
            'fPedidos'[Pedido - Texto],
            'fPedidos'[Legenda Situação],
            FILTER(
                VALUES('dCalendario'[MesAtual]),
                'dCalendario'[MesAtual] = TRUE()
            ),
            FILTER(
                VALUES('dEmpresas'[Empresa]),
                'dEmpresas'[Empresa] IN {{{companies_str}}}
            ),
            FILTER(
                VALUES('dEquipes'[Equipe]),
                'dEquipes'[Equipe] = {team_code}
            ),
            "Ingressado", 'Medidas'[Ingressado]
        )
        ORDER BY
            'dEmpresas'[Empresa],
            'dCalendario'[Data],
            'dEquipes'[Nome da Equipe],
            'dVendedores'[Nome Vendedor Completo],
            'dClientes'[Nome Completo do Cliente],
            'fPedidos'[Nota Fiscal - Texto],
            'fPedidos'[Pedido - Texto],
            'fPedidos'[Legenda Situação]
        """


@dataclass
class EmailTemplates:
    """Email message templates."""
    
    @staticmethod
    def manager_report_subject(team_code: int, manager_name: str) -> str:
        """Generate email subject for manager report."""
        return f"Relatório de Pedidos - Equipe {team_code} - {manager_name}"
    
    @staticmethod
    def manager_report_body(manager_name: str, team_code: int, 
                         total_faturados: int, total_pendentes: int) -> str:
        """Generate email body for manager report."""
        return f"""
        Prezado(a) {manager_name},
        
        Segue em anexo o relatório atualizado de pedidos para sua equipe (Equipe {team_code}).
        
        O arquivo Excel contém duas planilhas:
        - PedidosFaturados: {total_faturados} pedidos já faturados
        - PedidosPendentes: {total_pendentes} pedidos em andamento/outros status
        
        Este relatório contém apenas os dados da sua equipe, filtrados pelo mês atual.
        
        Atenciosamente,
        Sistema automático de Relatórios
        """


@dataclass
class LoggingConfig:
    """Logging configuration."""
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = os.path.join(PathConfig().logs_dir, "pipeline.log")
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


# Global configuration instances
POWER_BI_CONFIG = PowerBIConfig()
EMAIL_CONFIG = EmailConfig()
PATH_CONFIG = PathConfig()
BUSINESS_RULES = BusinessRules()
LOGGING_CONFIG = LoggingConfig()
