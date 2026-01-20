# Instruções do Scheduler do Pipeline

## 🚀 Como Usar

### Opção 1: Execução Manual (Recomendado para Testes)

**Para testar com equipe 200:**
```bash
# Execute o arquivo batch
test_team_200.bat

# Ou execute diretamente
python schedule_pipeline.py --test
```

### Opção 2: Scheduler Manual

**Para iniciar o scheduler diário:**
```bash
# Execute o arquivo batch
start_scheduler.bat

# Ou execute diretamente
python schedule_pipeline.py
```

### Opção 3: Serviço Automático do Windows (Recomendado para Produção)

**Para instalar serviço automático:**
```bash
# Execute como Administrador
install_service.bat
```

**Para remover serviço automático:**
```bash
# Execute como Administrador
uninstall_service.bat
```

**Para verificar tarefas agendadas:**
```bash
taskschd.msc
```

## ⏰ Agendamento

- **Horário**: Todos os dias às 09:00 AM
- **Modo**: Produção (todas as equipes)
- **Logs**: Registrados em `logs/pipeline.log`

### Para Teste (Equipe 200)
Use o modo de teste para validação:
```bash
python schedule_pipeline.py --test
```

## 📋 Arquivos Criados

| Arquivo | Função |
|----------|----------|
| `schedule_pipeline.py` | Script principal do scheduler |
| `start_scheduler.bat` | Inicia scheduler manualmente |
| `test_team_200.bat` | Testa apenas equipe 200 |
| `install_service.bat` | Instala serviço automático do Windows |
| `uninstall_service.bat` | Remove serviço automático do Windows |

## 🔧 Configuração

O scheduler usa as mesmas configurações do pipeline:
- Validação do modelo semântico
- Regras de negócio
- Configurações de email
- Logs estruturados

## 📊 Resultados

### Modo Teste
- Processa apenas equipe 200
- Envia email para gustavo.barbosa@vilanova.com.br
- Gera logs detalhados

### Modo Automático
- Processa todas as equipes
- Envia emails para todos os gerentes
- Gera estatísticas completas

## 🛑 Como Parar

- **Scheduler**: Feche a janela do terminal ou pressione Ctrl+C
- **Teste**: O teste termina automaticamente após execução

## 📝 Logs

Todos os logs são salvos em:
- **Arquivo**: `logs/pipeline.log`
- **Rotação**: Automática (10MB, 5 backups)
- **Formato**: Estruturado com timestamps

## ⚠️ Importante

1. **Primeira execução**: Execute o modo teste primeiro
2. **Validação**: O scheduler valida o modelo semântico antes de executar
3. **Erros**: Em caso de erro, o scheduler continua agendado
4. **Reinício**: Se precisar reiniciar, execute o `start_scheduler.bat` novamente

## 🔄 Recomendações

- **Teste semanal**: Execute `test_team_200.bat` para verificar funcionamento
- **Monitoramento**: Verifique os logs regularmente
- **Backup**: Mantenha backup do arquivo `dGerentes.xlsx`
- **Atualização**: Mantenha o requirements.txt atualizado
