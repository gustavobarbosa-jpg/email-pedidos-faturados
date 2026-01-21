# 🚀 Guia de Deploy para Produção

## 📋 Pré-Deploy Checklist

- [x] **Ambiente virtual**: Criado e funcionando
- [x] **Dependências**: Todas instaladas
- [x] **Código**: Testado e validado
- [x] **Mensagem WhatsApp**: Adicionada ao corpo do email
- [x] **Scripts**: Criados para automação
- [x] **Scheduler**: Configurado para 09:00 AM
- [x] **Serviço Windows**: Pronto para instalação

## 🎯 Modo Produção

O sistema está configurado para rodar automaticamente todos os dias às 09:00 AM sem intervenção humana.

### 📁 Arquivos de Produção

#### **Execução Manual**
```bash
# Script principal (sem pausa)
run_pipeline.bat

# Scheduler direto
scripts\schedule_pipeline.py

# Validação
run_pipeline.bat --validate
```

#### **Serviço Windows**
```bash
# Instalar serviço (executar como Administrador)
scripts\install_service.bat

# Remover serviço (executar como Administrador)
scripts\uninstall_service.bat
```

## ⚙️ Configuração do Scheduler

O scheduler está configurado para:
- **Horário**: 09:00 AM todos os dias
- **Modo**: Produção (todas as equipes)
- **Logs**: Registrados em `logs/pipeline.log`
- **Sem pausa**: Execução contínua sem intervenção

## 🧪 Modo Teste

Para testes, use:
```bash
# Teste com equipe 200
run_pipeline.bat --teams 200

# Validação (sem envio de emails)
run_pipeline.bat --validate
```

## 📊 Monitoramento

### Logs de Execução
- **Local**: `logs/pipeline.log`
- **Estrutura**: Timestamp, nível, contexto
- **Rotação**: 10MB, 5 backups

### Métricas Disponíveis
- Gerentes processados
- Taxa de sucesso
- Volume de dados
- Tempo de execução

## 🧹 Manutenção

### Tarefas Semanais
- [ ] Verificar logs de erros
- [ ] Executar teste com equipe 200
- [ ] Validar espaço em disco
- [ ] Backup do arquivo dGerentes.xlsx

### Tarefas Mensais
- [ ] Atualizar dependências Python
- [ ] Revisar regras de negócio
- [ ] Analisar métricas de performance

## 🚨 Procedimentos de Emergência

### Falha de Execução
1. Verificar logs em `logs/pipeline.log`
2. Identificar etapa com erro
3. Verificar configurações no arquivo `.env`
4. Executar modo de validação para diagnóstico

### Falha de Envio de Email
1. Verificar configurações SMTP no `.env`
2. Validar credenciais do Gmail
3. Testar conexão com servidor SMTP
4. Verificar se emails estão sendo bloqueados

### Falha de Conexão Power BI
1. Verificar credenciais Azure AD
2. Validar permissões no Power BI
3. Testar conexão manualmente
4. Verificar se modelo semântico está atualizado

## 📞 Contatos de Suporte

- **Email**: admin@empresa.com.br
- **WhatsApp**: (35) 99825-3791
- **Horário de atendimento**: 08:00 - 18:00

## 🎉 Deploy Concluído

O sistema está pronto para operação em produção com:
- ✅ Execução automática às 09:00 AM
- ✅ Monitoramento completo
- ✅ Logs detalhados
- ✅ Procedimentos de emergência
- ✅ Contato de suporte disponível

---

**O pipeline está oficialmente em produção!** 🚀
