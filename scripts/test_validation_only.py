"""
Script de teste para verificar validação do modelo semântico
SEM ENVIAR EMAILS - APENAS VERIFICAÇÃO
"""

import sys
import os
# Adicionar o diretório raiz ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.validation import SemanticModelValidator
from datetime import date

def test_validation_only():
    """Testa validação sem enviar emails."""
    print("=" * 60)
    print("🔍 TESTE DE VALIDAÇÃO DO MODELO SEMÂNTICO")
    print("=" * 60)
    print(f"📅 Data atual: {date.today()}")
    print()
    
    # Criar validator
    validator = SemanticModelValidator()
    
    # Extrair data do modelo (sem enviar alerta)
    print("📊 Extraindo data do modelo semântico...")
    try:
        model_date = validator._extract_update_date()
        if model_date:
            print(f"✅ Data do modelo extraída: {model_date}")
        else:
            print("❌ Não foi possível extrair data do modelo")
            return False
    except Exception as e:
        print(f"❌ Erro ao extrair data: {e}")
        return False
    
    # Comparar com data atual
    print()
    print("🔍 Comparando datas...")
    today = date.today()
    
    if model_date == today:
        print("✅ SUCESSO: O modelo está atualizado com a data de hoje!")
        print(f"   📅 Modelo: {model_date}")
        print(f"   📅 Hoje: {today}")
        print()
        print("🎉 O pipeline pode executar normalmente!")
        return True
    else:
        print("❌ ATENÇÃO: O modelo NÃO está atualizado!")
        print(f"   📅 Modelo: {model_date}")
        print(f"   📅 Hoje: {today}")
        print(f"   📅 Diferença: {(today - model_date).days} dias")
        print()
        print("⚠️  O pipeline deveria enviar um alerta!")
        print("⚠️  NENHUM EMAIL SERÁ ENVIADO NESTE TESTE")
        return False

if __name__ == "__main__":
    print("⚠️  MODO DE TESTE SEGURO - NENHUM EMAIL SERÁ ENVIADO")
    print()
    
    success = test_validation_only()
    
    print()
    print("=" * 60)
    if success:
        print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO")
    else:
        print("❌ VALIDAÇÃO FALHOU")
    print("=" * 60)
