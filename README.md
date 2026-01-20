# Pipeline de Relatórios por Email

[![CI/CD](https://github.com/gustavobarbosa/email-pedidos-faturados/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/gustavobarbosa/email-pedidos-faturados/actions)
[![codecov](https://codecov.io/gh/gustavobarbosa/email-pedidos-faturados/branch/main/graph/badge.svg)](https://codecov.io/gh/gustavobarbosa/email-pedidos-faturados)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

## Visão Geral

Este é um pipeline profissional de Engenharia de Dados que extrai dados de modelos semânticos do Power BI, os transforma de acordo com regras de negócio e entrega relatórios personalizados para gerentes via email.

## Arquitetura

A solução segue um padrão de arquitetura em camadas:

```
├── src/
│   ├── extract/          # Camada de extração de dados
│   ├── transform/        # Camada de transformação de dados  
│   ├── delivery/         # Camada de entrega por email
│   ├── orchestration/    # Orquestração do pipeline
│   ├── config/          # Gerenciamento de configuração
│   └── utils/           # Utilitários comuns
├── data/               # Diretórios de dados
├── logs/               # Arquivos de log
├── tests/              # Testes unitários
└── docs/               # Documentação
```

## Funcionalidades

- **Separação de Responsabilidades**: Separação clara entre extração, transformação e entrega
- **Escalabilidade**: Pode lidar com múltiplos gerentes e equipes de forma eficiente
- **Observabilidade**: Logging abrangente e rastreamento de erros
- **Confiabilidade**: Lógica de retry e tratamento de erros em todo o sistema
- **Segurança**: Gerenciamento centralizado de credenciais
- **Manutenibilidade**: Código limpo e modular com documentação adequada

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente no `.env`:
   ```env
   TENANT_ID=seu_tenant_id
   CLIENT_ID=seu_client_id
   CLIENT_SECRET=seu_client_secret
   POWER_BI_SCOPE=https://analysis.windows.net/powerbi/api/.default
   WORKSPACE_ID=seu_workspace_id
   SEMANTIC_MODEL_ID=seu_semantic_model_id
   EMAIL=seu_email@gmail.com
   password_app=sua_senha_app
   ```

## Uso

### Uso Básico (Todos os Gerentes)
```bash
python main.py
```

### Equipes Específicas
```bash
python main.py --teams 200 300 400
```

### Modo Validação (Sem Envio de Email)
```bash
python main.py --validate
```

### Modo Validação para Equipes Específicas
```bash
python main.py --teams 200 --validate
```

### Logging Detalhado
```bash
python main.py --verbose
```

## Configuração

### Regras de Negócio
- **Empresas Válidas**: [1, 10, 11, 12, 14] (configurável em `src/config/settings.py`)
- **Filtro de Mês Atual**: Ativado por padrão
- **Status Faturado**: "Faturado" (usado para segmentação de dados)

### Templates de Email
Os templates de email são centralizados em `src/config/settings.py` e podem ser personalizados:
- Linhas de assunto
- Conteúdo do corpo
- Variáveis de personalização

### Consultas DAX
As consultas DAX são parametrizadas e configuráveis:
- Filtragem dinâmica de equipes
- Filtragem de empresas
- Filtragem de datas

## Fluxo de Dados

1. **Extrair**: 
   - Ler gerentes do arquivo Excel
   - Extrair pedidos do Power BI usando consultas DAX

2. **Transformar**:
   - Limpar e padronizar nomes de colunas
   - Aplicar regras de negócio e filtros
   - Segmentar dados por status (Faturados vs Pendentes)

3. **Entregar**:
   - Criar arquivos Excel com múltiplas abas
   - Compor emails personalizados
   - Enviar com lógica de retry

4. **Orquestrar**:
   - Coordenar todos os passos
   - Lidar com erros e retries
   - Registrar progresso e estatísticas

## Tratamento de Erros

O pipeline inclui tratamento abrangente de erros:
- Retentativas de conexão para API do Power BI
- Retentativas de envio de email
- Verificações de validação de dados
- Degradação graceful

## Logging

Logging estruturado com:
- Rotação de arquivos (10MB, 5 backups)
- Saída no console
- Informações de contexto
- Rastreamento de erros

## Desenvolvimento

### Executando Testes
```bash
pytest tests/ -v --cov=src
```

### Formatação de Código
```bash
black src/ tests/
```

### Verificação de Tipos
```bash
mypy src/
```

### Análise Estática
```bash
flake8 src/ tests/
```

## Monitoramento

### Métricas Chave
- Tempo de execução do pipeline
- Taxas de sucesso/falha
- Volumes de dados processados
- Padrões de erro

### Arquivos de Log
- Localização: `logs/pipeline.log`
- Rotação: Automática
- Formato: Estruturado com timestamps

## Segurança

- Credenciais armazenadas em variáveis de ambiente
- Nenhum segredo hardcoded no código
- Transmissão segura de email (SSL/TLS)
- Limpeza de arquivos temporários

## Considerações de Performance

- Capacidade de processamento paralelo (pronto para implementação)
- Manipulação eficiente de dados com pandas
- Operações de arquivo conscientes de memória
- Pool de conexões pronto

## Melhorias Futuras

1. **Processamento Paralelo**: Processar múltiplos gerentes concorrentemente
2. **Armazenamento em Banco**: Armazenar histórico e resultados de processamento
3. **Integração API**: API REST para gerenciamento do pipeline
4. **Dashboard**: Interface de monitoramento em tempo real
5. **Agendamento Avançado**: Automação baseada em cron
6. **Verificações de Qualidade de Dados**: Regras de validação aprimoradas

## Solução de Problemas

### Problemas Comuns

1. **Falhas de Autenticação**
   - Verifique as credenciais do Azure AD
   - Verifique as permissões da API
   - Certifique-se de que o tenant ID está correto

2. **Falhas no Envio de Email**
   - Verifique a senha do app Gmail
   - Verifique as configurações SMTP
   - Certifique-se de que SSL está ativado

3. **Problemas na Extração de Dados**
   - Valide a conexão com Power BI
   - Verifique o ID do modelo semântico
   - Verifique a sintaxe da consulta DAX

4. **Problemas de Acesso a Arquivos**
   - Verifique as permissões dos arquivos
   - Verifique se os caminhos existem
   - Certifique-se de que há espaço em disco

### Modo Debug
Execute com logging detalhado para solução de problemas detalhada:
```bash
python main.py --verbose --validate
```

## 📊 Repositório GitHub

### 🌐 Link do Projeto
- **Repositório**: https://github.com/gustavobarbosa/email-pedidos-faturados
- **Issues**: Reporte bugs e sugira melhorias
- **Wiki**: Documentação detalhada
- **Releases**: Versões estáveis

### 🤝 Como Contribuir
1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

### 📋 Status do Projeto
- ✅ **Produção**: Versão 1.0.0 estável
- 🔄 **CI/CD**: Testes automáticos
- 📊 **Cobertura**: Codecov integrado
- 🛡️ **Segurança**: Scans automáticos

### 📞 Suporte
- **Email**: gustavo.barbosa@vilanova.com.br
- **WhatsApp**: (35) 99825-3791
- **Issues**: GitHub Issues

---

## Suporte

Para problemas e dúvidas:
1. Verifique os logs em `logs/pipeline.log`
2. Execute o modo de validação primeiro
3. Revise as configurações
4. Verifique o status da API do Power BI
