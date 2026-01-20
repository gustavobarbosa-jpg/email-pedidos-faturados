"""
Validation utilities for the email reports pipeline.

This module provides:
- Semantic model update validation
- Business rule validation
- Pre-execution checks
- Alert notifications
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
import pytz

from src.delivery.email_service import EmailService
from src.utils.logger import pipeline_logger
from src.config.settings import EMAIL_CONFIG


class SemanticModelValidator:
    """Validates semantic model update status before pipeline execution."""
    
    def __init__(self):
        from src.extract.powerbi_extractor import PowerBIExtractor
        
        self.extractor = PowerBIExtractor()
        self.email_service = EmailService()
        self.logger = pipeline_logger
        self.timezone = pytz.timezone('America/Sao_Paulo')  # Brazil timezone
        
        # Alert configuration
        self.alert_recipient = "gustavo.barbosa@vilanova.com.br"
        self.date_table = "UltimaAtualizacao"
        self.date_column = "UltimaAtualizacao"
    
    def validate_semantic_model_update(self) -> Dict[str, Any]:
        """
        Validate if semantic model is updated with today's data.
        
        Returns:
            Dict with validation result and details
        """
        try:
            self.logger.log_step_start("Semantic Model Update Validation")
            
            # Extract update date from semantic model
            update_date = self._extract_update_date()
            
            if not update_date:
                return self._create_validation_result(
                    False, 
                    "Failed to extract update date from semantic model"
                )
            
            # Get today's date
            today = self._get_today_date()
            
            # Compare dates
            is_updated_today = self._compare_dates(update_date, today)
            
            result = self._create_validation_result(
                is_updated_today,
                "Semantic model validation completed",
                update_date=update_date,
                today_date=today
            )
            
            # Log validation result
            self._log_validation_result(result)
            
            # Send alert if not updated
            if not is_updated_today:
                self._send_alert_email(result)
            
            self.logger.log_step_end("Semantic Model Update Validation")
            
            return result
            
        except Exception as e:
            self.logger.error("Semantic model validation failed", e)
            return self._create_validation_result(
                False,
                f"Validation error: {str(e)}"
            )
    
    def _extract_update_date(self) -> Optional[date]:
        """
        Extract the last update date from semantic model.
        
        Returns:
            Date object or None if extraction fails
        """
        try:
            # DAX query to get the update date from UltimaAtualizacao table
            dax_query = """
            EVALUATE
            ROW(
                "UltimaAtualizacao", MAX('UltimaAtualizacao'[UltimaAtualizacao])
            )
            """
            
            self.logger.debug("Executing update date query", query=dax_query)
            
            result = self.extractor.execute_dax_query(dax_query)
            
            if not result:
                self.logger.error("No result returned from update date query")
                return None
            
            # Extract the date from response
            tables = result.get('results', [{}])[0].get('tables', [])
            if not tables:
                self.logger.error("No tables found in update date response")
                return None
            
            rows = tables[0].get('rows', [])
            if not rows:
                self.logger.error("No rows found in update date response - UltimaAtualizacao table is empty")
                return None
            
            # Debug: log the entire response
            self.logger.debug("Query response", 
                          tables_count=len(tables),
                          rows_count=len(rows),
                          first_row=rows[0] if rows else None,
                          all_keys=list(rows[0].keys()) if rows else [])
            
            # Check if the row is empty (no data)
            if not rows[0] or all(value is None or value == '' for value in rows[0].values()):
                self.logger.error("UltimaAtualizacao table exists but is empty - no update date available")
                return None
            
            # Extract date value - try different possible column names
            date_value = None
            possible_keys = ['UltimaAtualizacao', '[UltimaAtualizacao]']
            
            for key in possible_keys:
                if key in rows[0]:
                    date_value = rows[0][key]
                    self.logger.debug(f"Found date value with key: {key}", value=date_value)
                    break
            
            if not date_value:
                # If no specific key found, try to get the first non-null value
                for key, value in rows[0].items():
                    if value is not None and value != '':
                        date_value = value
                        self.logger.debug(f"Using first non-null value", key=key, value=date_value)
                        break
            
            if not date_value:
                self.logger.error("No date value found in response")
                return None
            
            # Parse date - handle different formats
            update_date = self._parse_date_value(date_value)
            
            self.logger.info("Update date extracted successfully", 
                          update_date=update_date,
                          raw_value=date_value)
            
            return update_date
            
        except Exception as e:
            self.logger.error("Failed to extract update date", e)
            return None
    
    def _parse_date_value(self, date_value: Any) -> Optional[date]:
        """
        Parse date value from various possible formats.
        
        Args:
            date_value: Date value from Power BI response
            
        Returns:
            Parsed date object or None
        """
        if isinstance(date_value, datetime):
            return date_value.date()
        elif isinstance(date_value, date):
            return date_value
        elif isinstance(date_value, str):
            # Try different date formats
            formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',  # ISO 8601 with microseconds
                '%Y-%m-%dT%H:%M:%S.%fZ',  # ISO 8601 with timezone
                '%Y-%m-%dT%H:%M:%S.%f%z',  # ISO 8601 with timezone offset
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',  # Power BI specific format without timezone
                'Y-%m-%dT%H:%M:%S.%f',  # Alternative Power BI format
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_value, fmt).date()
                except ValueError:
                    continue
        
        self.logger.error(f"Unable to parse date value: {date_value}")
        return None
    
    def _get_today_date(self) -> date:
        """
        Get today's date in the configured timezone.
        
        Returns:
            Today's date object
        """
        return datetime.now(self.timezone).date()
    
    def _compare_dates(self, update_date: date, today: date) -> bool:
        """
        Compare update date with today's date.
        
        Args:
            update_date: Last update date from semantic model
            today: Today's date
            
        Returns:
            True if dates are equal, False otherwise
        """
        return update_date == today
    
    def _create_validation_result(self, is_valid: bool, message: str, 
                               update_date: Optional[date] = None,
                               today_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Create validation result dictionary.
        
        Args:
            is_valid: Whether validation passed
            message: Validation message
            update_date: Update date from semantic model
            today_date: Today's date
            
        Returns:
            Validation result dictionary
        """
        return {
            'is_valid': is_valid,
            'message': message,
            'update_date': update_date,
            'today_date': today_date,
            'validation_time': datetime.now(self.timezone),
            'alert_sent': False
        }
    
    def _log_validation_result(self, result: Dict[str, Any]):
        """
        Log validation result with appropriate level.
        
        Args:
            result: Validation result dictionary
        """
        if result['is_valid']:
            self.logger.info(
                "Semantic model is up to date",
                update_date=result['update_date'],
                today_date=result['today_date']
            )
        else:
            self.logger.warning(
                f"Semantic model is NOT up to date - PIPELINE HALTED. Update date: {result.get('update_date')}, Today: {result.get('today_date')}"
            )
    
    def _send_alert_email(self, result: Dict[str, Any]):
        """
        Send alert email when semantic model is not updated.
        
        Args:
            result: Validation result dictionary
        """
        try:
            self.logger.log_step_start("Send Alert Email")
            
            # Compose alert email
            alert_message = self._compose_alert_email(result)
            
            # Create email message
            from email.message import EmailMessage
            import smtplib
            
            msg = EmailMessage()
            msg["From"] = EMAIL_CONFIG.sender_email
            msg["To"] = self.alert_recipient
            msg["Subject"] = "⚠️ ALERTA: Modelo Semântico Não Atualizado - Pipeline Interrompido"
            
            msg.set_content(alert_message)
            
            # Send email using existing infrastructure
            with smtplib.SMTP_SSL(
                EMAIL_CONFIG.smtp_server,
                EMAIL_CONFIG.smtp_port
            ) as smtp:
                smtp.login(EMAIL_CONFIG.sender_email, EMAIL_CONFIG.app_password)
                smtp.send_message(msg)
            
            # Update result to indicate alert was sent
            result['alert_sent'] = True
            
            self.logger.log_step_end("Send Alert Email")
            self.logger.warning(
                "Alert email sent successfully",
                recipient=self.alert_recipient,
                update_date=result['update_date'],
                today_date=result['today_date']
            )
            
        except Exception as e:
            self.logger.error("Failed to send alert email", e)
            # Don't re-raise - this is a secondary failure
            result['alert_sent'] = False
    
    def _compose_alert_email(self, result: Dict[str, Any]) -> str:
        """
        Compose alert email message.
        
        Args:
            result: Validation result dictionary
            
        Returns:
            Formatted email message
        """
        update_date = result['update_date']
        today_date = result['today_date']
        
        return f"""
⚠️ ALERTA CRÍTICO - PIPELINE INTERROMPIDO ⚠️

Data/Hora: {result['validation_time'].strftime('%d/%m/%Y %H:%M:%S')}

MOTIVO: A data de atualização do modelo semântico é diferente da data atual.

INFORMAÇÕES:
• Data encontrada no modelo semântico: {self._format_date(update_date) if update_date else 'TABELA VAZIA'}
• Data atual (hoje): {self._format_date(today_date) if today_date else 'N/A'}
• Status: MODELO DESATUALIZADO

ACESSO DIRETO AO MODELO SEMÂNTICO:
https://app.powerbi.com/groups/8078b761-84df-4800-8ee9-ddaada4a26f3/settings/datasets/38e5506b-bd07-4593-8d18-d90cb770cf2d?experience=power-bi

AÇÕES NECESSÁRIAS:
1. Verificar o processo de atualização do modelo semântico
2. Confirmar que os dados de hoje foram processados
3. Executar o pipeline manualmente após correção

IMPACTO:
• Nenhum relatório foi enviado aos gerentes hoje
• Pipeline foi interrompido preventivamente
• Alerta automático enviado para equipe responsável

---
Este é um alerta automático do Email Reports Pipeline.
Não responda a este e-mail.
""".strip()
    
    def _format_date(self, date_obj: date) -> str:
        """
        Format date object as DD/MM/YYYY.
        
        Args:
            date_obj: Date to format
            
        Returns:
            Formatted date string
        """
        return date_obj.strftime('%d/%m/%Y') if date_obj else 'N/A'
    
    def get_update_info_for_email(self) -> str:
        """
        Get formatted update information for inclusion in manager emails.
        
        Returns:
            Formatted string with update information
        """
        try:
            update_date = self._extract_update_date()
            if update_date:
                return f"Última atualização do modelo semântico: {self._format_date(update_date)}"
            else:
                return "Última atualização do modelo semântico: Não disponível"
        except Exception as e:
            self.logger.error("Failed to get update info for email", e)
            return "Última atualização do modelo semântico: Erro ao obter informação"
