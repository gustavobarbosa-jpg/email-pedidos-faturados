"""
Scheduler do Pipeline de Relatórios por Email
Executa o pipeline todos os dias às 09:00 AM
"""

import schedule
import time
import sys
import os
from datetime import datetime

# Adicionar o diretório raiz ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.orchestration.pipeline import PipelineOrchestrator
from src.utils.logger import pipeline_logger

def run_daily_pipeline():
    """Executa o pipeline diário para todas as equipes."""
    try:
        logger = pipeline_logger
        logger.info("=== INICIANDO PIPELINE AUTOMÁTICO DIÁRIO ===")
        logger.info(f"Horário de execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Inicializar pipeline
        orchestrator = PipelineOrchestrator()
        
        # Executar pipeline para todas as equipes (modo produção)
        results = orchestrator.run_pipeline()
        
        # Registrar resultados
        if results['success']:
            logger.info("=== PIPELINE AUTOMÁTICO CONCLUÍDO COM SUCESSO ===")
            stats = results['results']['statistics']
            logger.info(f"Gerentes processados: {results['results']['total_managers']}")
            logger.info(f"Registros totais: {stats['total_records']}")
            logger.info(f"Faturados: {stats['total_faturados']}")
            logger.info(f"Pendentes: {stats['total_pendentes']}")
        else:
            logger.error("=== PIPELINE AUTOMÁTICO FALHOU ===")
            logger.error(f"Erro: {results.get('error', 'Erro desconhecido')}")
            
    except Exception as e:
        logger.error("ERRO CRÍTICO NO PIPELINE AUTOMÁTICO", e)

def run_test_pipeline():
    """Executa o pipeline em modo de teste apenas para equipe 200."""
    try:
        logger = pipeline_logger
        logger.info("=== INICIANDO PIPELINE DE TESTE - EQUIPE 200 ===")
        logger.info(f"Horário de execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Inicializar pipeline
        orchestrator = PipelineOrchestrator()
        
        # Executar pipeline apenas para equipe 200 (modo produção)
        results = orchestrator.run_pipeline(team_codes=[200])
        
        # Registrar resultados
        if results['success']:
            logger.info("=== PIPELINE DE TESTE CONCLUÍDO COM SUCESSO ===")
            stats = results['results']['statistics']
            logger.info(f"Equipe 200 processada com sucesso")
            logger.info(f"Registros totais: {stats['total_records']}")
            logger.info(f"Faturados: {stats['total_faturados']}")
            logger.info(f"Pendentes: {stats['total_pendentes']}")
        else:
            logger.error("=== PIPELINE DE TESTE FALHOU ===")
            logger.error(f"Erro: {results.get('error', 'Erro desconhecido')}")
            
    except Exception as e:
        logger.error("ERRO CRÍTICO NO PIPELINE DE TESTE", e)

def main():
    """Função principal do scheduler."""
    print("🚀 INICIANDO SCHEDULER DO PIPELINE")
    print("⏰ Agendado para rodar todos os dias às 09:00")
    print("🧪 Para teste manual com equipe 200, use: python schedule_pipeline.py --test")
    print("=" * 50)
    
    # Agendar pipeline diário às 09:00
    schedule.every().day.at("09:00").do(run_daily_pipeline)
    
    # Verificar se modo de teste foi solicitado
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 MODO TESTE: Executando pipeline para equipe 200...")
        run_test_pipeline()
        return
    
    try:
        while True:
            # Verificar se próxima execução está em menos de 1 minuto
            next_run = schedule.next_run()
            if next_run:
                time_to_next = (next_run - datetime.now()).total_seconds()
                if time_to_next <= 60:
                    print(f"⏰ Próxima execução em: {next_run.strftime('%H:%M:%S')}")
            
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Scheduler interrompido pelo usuário")
        logger.info("Scheduler interrompido pelo usuário")

if __name__ == "__main__":
    main()
