"""
Pipeline orchestration layer.

This module handles:
- Pipeline coordination
- Workflow management
- Error handling and recovery
- Progress tracking
- Audit logging
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.extract.powerbi_extractor import PowerBIExtractor
from src.extract.managers_extractor import ManagersExtractor
from src.transform.data_transformer import DataTransformer
from src.delivery.email_service import EmailService
from src.utils.logger import pipeline_logger
from src.utils.validation import SemanticModelValidator
from src.config.settings import BUSINESS_RULES


class PipelineOrchestrator:
    """Orchestrates the entire email reports pipeline."""
    
    def __init__(self):
        self.logger = pipeline_logger
        self.extractor = PowerBIExtractor()
        self.managers_extractor = ManagersExtractor()
        self.transformer = DataTransformer()
        self.email_service = EmailService()
        self.validator = SemanticModelValidator()
        self.business_rules = BUSINESS_RULES
        
        # Pipeline state
        self.pipeline_start_time = None
        self.pipeline_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def run_pipeline(self, team_codes: Optional[List[int]] = None, 
                   validate_only: bool = False) -> Dict[str, Any]:
        """
        Run the complete pipeline.
        
        Args:
            team_codes: List of team codes to process (None for all)
            validate_only: If True, only validate without sending emails
            
        Returns:
            Dictionary with pipeline results and statistics
        """
        self.pipeline_start_time = time.time()
        
        try:
            self.logger.log_pipeline_start(self.pipeline_id)
            
            # CRITICAL: Validate semantic model update first
            if not self._validate_semantic_model():
                return self._create_early_exit_result("Semantic model validation failed")
            
            # Validation phase
            self._validate_prerequisites()
            
            # Extraction phase
            managers = self._extract_managers(team_codes)
            
            # Processing phase
            results = self._process_managers(managers, validate_only)
            
            # Completion phase
            duration = time.time() - self.pipeline_start_time
            self._log_pipeline_summary(results, duration)
            
            self.logger.log_pipeline_end(self.pipeline_id, duration)
            
            return {
                'pipeline_id': self.pipeline_id,
                'duration': duration,
                'results': results,
                'success': True
            }
            
        except Exception as e:
            duration = time.time() - self.pipeline_start_time if self.pipeline_start_time else 0
            self.logger.error(f"Pipeline {self.pipeline_id} failed", e, duration=duration)
            
            return {
                'pipeline_id': self.pipeline_id,
                'duration': duration,
                'error': str(e),
                'success': False
            }
    
    def _validate_prerequisites(self):
        """Validate all prerequisites before running pipeline."""
        self.logger.log_step_start("Validate prerequisites")
        
        # Validate Power BI connection
        if not self.extractor.validate_connection():
            raise Exception("Power BI connection validation failed")
        
        # Validate email configuration
        if not self.email_service.validate_email_config():
            raise Exception("Email configuration validation failed")
        
        # Test email connection
        if not self.email_service.test_connection():
            raise Exception("Email connection test failed")
        
        self.logger.log_step_end("Validate prerequisites")
    
    def _extract_managers(self, team_codes: Optional[List[int]]) -> List[Dict[str, Any]]:
        """Extract managers data."""
        try:
            managers = self.managers_extractor.get_managers_by_team(team_codes)
            
            if not managers:
                raise Exception("No managers found for processing")
            
            self.logger.info(f"Managers extracted successfully", 
                          count=len(managers),
                          team_filter=team_codes)
            
            return managers
            
        except Exception as e:
            self.logger.error("Failed to extract managers", e)
            raise
    
    def _process_managers(self, managers: List[Dict[str, Any]], 
                         validate_only: bool) -> Dict[str, Any]:
        """
        Process all managers and send reports.
        
        Args:
            managers: List of manager dictionaries
            validate_only: If True, only validate without sending
            
        Returns:
            Dictionary with processing results
        """
        results = {
            'total_managers': len(managers),
            'successful': 0,
            'failed': 0,
            'errors': [],
            'statistics': {
                'total_records': 0,
                'total_faturados': 0,
                'total_pendentes': 0,
                'total_ingressado': 0
            }
        }
        
        self.logger.info(f"Starting to process {len(managers)} managers")
        
        for i, manager in enumerate(managers, 1):
            try:
                self.logger.info(f"Processing manager {i}/{len(managers)}", 
                              team_code=manager['equipe'],
                              name=manager['nome_gerente'])
                
                # Extract orders data
                raw_orders = self.extractor.extract_orders_by_team(manager['equipe'])
                
                # Transform data
                transformed_data = self.transformer.transform_orders_data(raw_orders)
                
                # Update statistics
                stats = self.transformer.get_summary_stats(transformed_data)
                self._update_statistics(results['statistics'], stats)
                
                # Send email (unless validate_only)
                if not validate_only:
                    # Override recipient for team 200 to send to example email
                    if manager['equipe'] == 200:
                        original_email = manager['email_gerente']
                        manager['email_gerente'] = "admin@empresa.com.br"  # Email de exemplo
                        self.logger.info(f"Overriding email for team 200", 
                                      original_email=original_email,
                                      new_email=manager['email_gerente'])
                        
                        # Send to manager
                        self.email_service.send_manager_report(
                            manager, 
                            transformed_data
                        )
                        
                        # Send copy to admin@empresa.com.br
                        self.logger.info(f"Sending copy to admin@empresa.com.br for team 200")
                        
                        # Create copy email message
                        from email.message import EmailMessage
                        import smtplib
                        
                        copy_msg = EmailMessage()
                        copy_msg["From"] = "admin@empresa.com.br"
                        copy_msg["To"] = "admin@empresa.com.br"
                        copy_msg["Subject"] = f"📋 CÓPIA - Relatório Equipe 200 - {manager['nome_gerente']}"
                        
                        copy_body = f"""
📋 CÓPIA AUTOMÁTICA - RELATÓRIO EQUIPE 200

Gerente: {manager['nome_gerente']}
Equipe: {manager['equipe']}
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

RESUMO DO RELATÓRIO:
• Total de Registros: {len(transformed_data.get('PedidosFaturados', pd.DataFrame())) + len(transformed_data.get('PedidosPendentes', pd.DataFrame()))}
• Pedidos Faturados: {len(transformed_data.get('PedidosFaturados', pd.DataFrame()))}
• Pedidos Pendentes: {len(transformed_data.get('PedidosPendentes', pd.DataFrame()))}

INFORMAÇÕES:
• Este é uma cópia automática do relatório enviado ao gerente
• O relatório original também foi enviado para: {original_email}
• Anexo: Planilha Excel com dados completos

⚠️ IMPORTANTE: Este é um email automático e não deve ser respondido.
• Caso tenha dúvidas, entre em contato com o suporte técnico.

---
Este é um alerta automático do Email Reports Pipeline.
Não responda a este e-mail.
""".strip()
                        
                        copy_msg.set_content(copy_body)
                        
                        # Send copy
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                            smtp.login("admin@empresa.com.br", "senha_app_exemplo")  # Usar variáveis de ambiente
                            smtp.send_message(copy_msg)
                        
                        self.logger.info(f"Copy sent successfully to admin@empresa.com.br")
                    else:
                        self.email_service.send_manager_report(
                            manager, 
                            transformed_data
                        )
                
                results['successful'] += 1
                
                self.logger.info(f"Manager processed successfully", 
                              team_code=manager['equipe'],
                              faturados=stats['faturados_count'],
                              pendentes=stats['pendentes_count'])
                
            except Exception as e:
                error_info = {
                    'manager': manager,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                results['errors'].append(error_info)
                results['failed'] += 1
                
                self.logger.error(f"Failed to process manager", e,
                               team_code=manager.get('equipe'),
                               name=manager.get('nome_gerente'))
        
        return results
    
    def _update_statistics(self, current_stats: Dict[str, Any], 
                        new_stats: Dict[str, Any]):
        """Update cumulative statistics."""
        current_stats['total_records'] += new_stats['total_records']
        current_stats['total_faturados'] += new_stats['faturados_count']
        current_stats['total_pendentes'] += new_stats['pendentes_count']
        current_stats['total_ingressado'] += new_stats['total_ingressado']
    
    def _log_pipeline_summary(self, results: Dict[str, Any], duration: float):
        """Log pipeline execution summary."""
        stats = results['statistics']
        
        summary = {
            'duration_seconds': round(duration, 2),
            'duration_minutes': round(duration / 60, 2),
            'managers_processed': results['total_managers'],
            'successful': results['successful'],
            'failed': results['failed'],
            'success_rate': round(results['successful'] / results['total_managers'] * 100, 2),
            'total_records': stats['total_records'],
            'total_faturados': stats['total_faturados'],
            'total_pendentes': stats['total_pendentes'],
            'total_ingressado': stats['total_ingressado']
        }
        
        self.logger.info("Pipeline execution completed", **summary)
        
        # Log errors if any
        if results['errors']:
            self.logger.warning(f"Pipeline completed with {len(results['errors'])} errors")
            for error in results['errors'][:5]:  # Log first 5 errors
                self.logger.error("Manager processing error", 
                               error=error['error'],
                               team_code=error['manager'].get('equipe'))
    
    def run_validation_mode(self, team_codes: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Run pipeline in validation mode (no email sending).
        
        Args:
            team_codes: List of team codes to validate
            
        Returns:
            Dictionary with validation results
        """
        self.logger.info("Running pipeline in validation mode")
        return self.run_pipeline(team_codes, validate_only=True)
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get current pipeline status.
        
        Returns:
            Dictionary with pipeline status information
        """
        return {
            'pipeline_id': self.pipeline_id,
            'is_running': self.pipeline_start_time is not None,
            'start_time': self.pipeline_start_time,
            'business_rules': {
                'valid_companies': self.business_rules.valid_companies,
                'current_month_filter': self.business_rules.current_month_filter,
                'faturado_status': self.business_rules.faturado_status
            }
        }
    
    def _validate_semantic_model(self) -> bool:
        """
        Validate semantic model update status.
        
        Returns:
            True if model is updated, False otherwise
        """
        try:
            validation_result = self.validator.validate_semantic_model_update()
            
            if not validation_result['is_valid']:
                self.logger.error(
                    "Pipeline halted: Semantic model not updated",
                    update_date=validation_result.get('update_date'),
                    today_date=validation_result.get('today_date'),
                    alert_sent=validation_result.get('alert_sent', False)
                )
                return False
            
            self.logger.info("Semantic model validation passed")
            return True
            
        except Exception as e:
            self.logger.error("Semantic model validation failed with exception", e)
            return False
    
    def _create_early_exit_result(self, reason: str) -> Dict[str, Any]:
        """
        Create result dictionary for early pipeline exit.
        
        Args:
            reason: Reason for early exit
            
        Returns:
            Result dictionary
        """
        duration = time.time() - self.pipeline_start_time if self.pipeline_start_time else 0
        
        return {
            'pipeline_id': self.pipeline_id,
            'duration': duration,
            'early_exit': True,
            'early_exit_reason': reason,
            'success': False,
            'results': {
                'total_managers': 0,
                'successful': 0,
                'failed': 0,
                'errors': [],
                'statistics': {
                    'total_records': 0,
                    'total_faturados': 0,
                    'total_pendentes': 0,
                    'total_ingressado': 0
                }
            }
        }
