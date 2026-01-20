"""
Email delivery service.

This module handles:
- Email composition and sending
- Attachment handling
- Retry logic
- Error handling
- Email validation
"""

import os
import smtplib
import time
from email.message import EmailMessage
from typing import Dict, List, Optional, Any
from pathlib import Path

import pandas as pd

from src.config.settings import EMAIL_CONFIG, PATH_CONFIG, EmailTemplates
from src.utils.logger import pipeline_logger


class EmailService:
    """Handles email delivery with retry logic and error handling."""
    
    def __init__(self):
        self.config = EMAIL_CONFIG
        self.path_config = PATH_CONFIG
        self.logger = pipeline_logger
        self.max_retries = 3
        self.retry_delay = 5  # seconds
    
    def send_manager_report(self, manager_info: Dict[str, Any], 
                         report_data: Dict[str, pd.DataFrame],
                         update_info: Optional[str] = None) -> bool:
        """
        Send personalized report to a manager.
        
        Args:
            manager_info: Dictionary with manager details (equipe, nome_gerente, email_gerente)
            report_data: Dictionary with DataFrames for each sheet
            update_info: Optional string with semantic model update information
            
        Returns:
            bool: True if email sent successfully
            
        Raises:
            Exception: If email sending fails after retries
        """
        try:
            self.logger.log_step_start(
                f"Send email to manager", 
                team_code=manager_info['equipe'],
                manager_name=manager_info['nome_gerente'],
                email=manager_info['email_gerente']
            )
            
            # Create Excel file
            excel_file = self._create_excel_file(manager_info, report_data)
            
            # Compose email
            email_message = self._compose_email(manager_info, report_data, excel_file, update_info)
            
            # Send email with retry logic
            success = self._send_with_retry(email_message, manager_info['email_gerente'])
            
            # Clean up temporary file
            self._cleanup_file(excel_file)
            
            if success:
                self.logger.log_step_end(
                    f"Send email to manager",
                    team_code=manager_info['equipe'],
                    email=manager_info['email_gerente']
                )
                return True
            else:
                raise Exception(f"Failed to send email after {self.max_retries} attempts")
                
        except Exception as e:
            self.logger.error(
                f"Failed to send manager email", 
                e,
                team_code=manager_info.get('equipe'),
                email=manager_info.get('email_gerente')
            )
            raise
    
    def _create_excel_file(self, manager_info: Dict[str, Any], 
                         report_data: Dict[str, pd.DataFrame]) -> str:
        """
        Create Excel file with multiple sheets.
        
        Args:
            manager_info: Manager information
            report_data: DataFrames for each sheet
            
        Returns:
            str: Path to created Excel file
        """
        try:
            # Ensure temp directory exists
            os.makedirs(self.path_config.temp_data_dir, exist_ok=True)
            
            # Generate filename
            team_code = manager_info['equipe']
            manager_name = manager_info['nome_gerente'].replace(" ", "_")
            filename = f'relatorio_equipe_{team_code}_{manager_name}.xlsx'
            file_path = os.path.join(self.path_config.temp_data_dir, filename)
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for sheet_name, df in report_data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            self.logger.debug(f"Excel file created", file_path=file_path)
            
            # Validate file was created
            if not Path(file_path).exists():
                raise Exception(f"Failed to create Excel file: {file_path}")
            
            return file_path
            
        except Exception as e:
            self.logger.error("Failed to create Excel file", e)
            raise
    
    def _compose_email(self, manager_info: Dict[str, Any], 
                     report_data: Dict[str, pd.DataFrame], 
                     excel_file: str,
                     update_info: Optional[str] = None) -> EmailMessage:
        """
        Compose email message.
        
        Args:
            manager_info: Manager information
            report_data: DataFrames for each sheet
            excel_file: Path to Excel attachment
            
        Returns:
            EmailMessage: Composed email message
        """
        try:
            # Calculate statistics
            total_faturados = len(report_data.get('PedidosFaturados', pd.DataFrame()))
            total_pendentes = len(report_data.get('PedidosPendentes', pd.DataFrame()))
            
            # Create email message
            msg = EmailMessage()
            msg["From"] = self.config.sender_email
            msg["To"] = manager_info['email_gerente']
            msg["Subject"] = EmailTemplates.manager_report_subject(
                manager_info['equipe'], 
                manager_info['nome_gerente']
            )
            
            # Email body
            body = EmailTemplates.manager_report_body(
                manager_info['nome_gerente'],
                manager_info['equipe'],
                total_faturados,
                total_pendentes
            )
            
            # Add update info if provided
            if update_info:
                body += f"\n\n{update_info}"
            
            msg.set_content(body)
            
            # Add attachment
            with open(excel_file, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    filename=os.path.basename(excel_file)
                )
            
            self.logger.debug(f"Email composed", 
                           recipients=manager_info['email_gerente'],
                           attachment_size=os.path.getsize(excel_file))
            
            return msg
            
        except Exception as e:
            self.logger.error("Failed to compose email", e)
            raise
    
    def _send_with_retry(self, email_message: EmailMessage, recipient: str) -> bool:
        """
        Send email with retry logic.
        
        Args:
            email_message: Email message to send
            recipient: Email recipient
            
        Returns:
            bool: True if sent successfully
        """
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(f"Sending email attempt {attempt + 1}", recipient=recipient)
                
                with smtplib.SMTP_SSL(
                    self.config.smtp_server, 
                    self.config.smtp_port
                ) as smtp:
                    smtp.login(self.config.sender_email, self.config.app_password)
                    smtp.send_message(email_message)
                
                self.logger.info(f"Email sent successfully", 
                              recipient=recipient,
                              attempt=attempt + 1)
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                self.logger.error(f"SMTP authentication failed", e, attempt=attempt + 1)
                # Don't retry authentication errors
                break
                
            except smtplib.SMTPException as e:
                self.logger.error(f"SMTP error occurred", e, attempt=attempt + 1)
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
            except Exception as e:
                self.logger.error(f"Unexpected error sending email", e, attempt=attempt + 1)
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return False
    
    def _cleanup_file(self, file_path: str):
        """
        Clean up temporary files.
        
        Args:
            file_path: Path to file to remove
        """
        try:
            if Path(file_path).exists():
                os.remove(file_path)
                self.logger.debug(f"Temporary file removed", file_path=file_path)
        except Exception as e:
            self.logger.warning(f"Failed to remove temporary file", e, file_path=file_path)
    
    def validate_email_config(self) -> bool:
        """
        Validate email configuration.
        
        Returns:
            bool: True if configuration is valid
        """
        try:
            required_fields = [
                self.config.sender_email,
                self.config.app_password,
                self.config.smtp_server,
                self.config.smtp_port
            ]
            
            if not all(required_fields):
                missing = [field for field in required_fields if not field]
                self.logger.error("Missing email configuration", missing_fields=missing)
                return False
            
            # Basic email validation
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(email_pattern, self.config.sender_email):
                self.logger.error("Invalid sender email format", 
                               email=self.config.sender_email)
                return False
            
            return True
            
        except Exception as e:
            self.logger.error("Email configuration validation failed", e)
            return False
    
    def test_connection(self) -> bool:
        """
        Test SMTP connection.
        
        Returns:
            bool: True if connection is successful
        """
        try:
            with smtplib.SMTP_SSL(
                self.config.smtp_server, 
                self.config.smtp_port
            ) as smtp:
                smtp.login(self.config.sender_email, self.config.app_password)
            
            self.logger.info("SMTP connection test successful")
            return True
            
        except Exception as e:
            self.logger.error("SMTP connection test failed", e)
            return False
