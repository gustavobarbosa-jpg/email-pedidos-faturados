# Pipeline de Relatórios de Pedidos Faturados

[![CI/CD](https://github.com/gustavobarbosa-jpg/email-pedidos-faturados/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/gustavobarbosa-jpg/email-pedidos-faturados/actions)
[![codecov](https://codecov.io/gh/gustavobarbosa-jpg/email-pedidos-faturados/branch/main/graph/badge.svg)](https://codecov.io/gh/gustavobarbosa-jpg/email-pedidos-faturados)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

## 🎯 Objetivo Principal

Este pipeline automatiza completamente o processo de extração, transformação e envio de relatórios de pedidos faturados para gerentes de equipes, eliminando trabalho manual e garantindo entregas consistentes e pontuais.

### 📊 Problema Resolvido

- **Manual**: Gerentes precisavam acessar sistemas manualmente para ver seus pedidos
- **Demorado**: Processo manual levava horas para compilar dados
- **Inconsistente**: Dados podiam variar dependendo de quando eram extraídos
- **Custo**: Tempo gasto pelos gerentes e equipe de TI

### 🚀 Solução Implementada

- **Automático**: Executa todos os dias às 09:00 AM sem intervenção humana
- **Consistente**: Todos os gerentes recebem dados do mesmo momento
- **Completo**: Inui pedidos faturados e pendentes com análise detalhada
- **Seguro**: Validação do modelo semântico antes de executar

---

## 🔍 Como o Pipeline Funciona

### 📋 Etapa 1: Validação do Modelo Semântico

**O que faz**: Verifica se o modelo semântico do Power BI foi atualizado hoje

**Por que é importante**: Garante que estamos trabalhando com dados frescos

**Como funciona**:
1. Conecta-se à API do Power BI usando Azure AD
2. Executa consulta DAX na tabela `UltimaAtualizacao`
3. Compara a data extraída com a data atual
4. **Se datas coincidirem** → Pipeline continua
5. **Se datas não coincidirem** → Envia alerta e para execução

**Regras impostas**:
- ✅ Modelo deve ser atualizado no mesmo dia
- ⚠️ Se não estiver atualizado, envia email para gustavo.barbosa@vilanova.com.br e milena.danziger@vilanova.com.br
- 🛑 Pipeline não executa com dados desatualizados

---

### 📋 Etapa 2: Extração de Dados dos Gerentes

**O que faz**: Lê a lista de gerentes e suas equipes do arquivo Excel

**Fonte de dados**: `data/raw/dGerentes.xlsx`

**Informações extraídas**:
- Nome do gerente
- Código da equipe
- Email do gerente
- Outros dados de configuração

**Regras impostas**:
- ✅ Arquivo deve existir e estar acessível
- ✅ Estrutura deve conter colunas obrigatórias
- ✅ Email deve ser válido para envio

---

### 📋 Etapa 3: Extração de Pedidos do Power BI

**O que faz**: Busca todos os pedidos para cada equipe no Power BI

**Como funciona**:
1. Para cada gerente/equipe:
   - Conecta-se ao Power BI via API
   - Executa consulta DAX complexa
   - Filtra por equipe específica
   - Aplica filtros de negócio

**Consulta DAX utilizada**:
```dax
EVALUATE
SUMMARIZECOLUMNS(
    'fPedidos'[Empresa],
    'dCalendario'[MesAtual],
    'dEmpresas'[Empresa],
    KEEPFILTERS(FILTER('dEmpresas', 'dEmpresas'[Empresa] IN {1, 10, 11, 12, 14}))
)
```

**Regras de negócio impostas**:
- ✅ **Empresas válidas**: Apenas {1, 10, 11, 12, 14}
- ✅ **Mês atual**: Apenas pedidos do mês corrente
- ✅ **Filtro por equipe**: Cada gerente vê apenas sua equipe
- ✅ **Colunas obrigatórias**: Empresa, Data, Status, Valor, etc.

---

### 📋 Etapa 4: Transformação e Limpeza de Dados

**O que faz**: Processa e organiza os dados brutos do Power BI

**Transformações aplicadas**:

1. **Limpeza de colunas**:
   - Padronização de nomes (snake_case)
   - Remoção de espaços e caracteres especiais
   - Conversão de tipos de dados

2. **Aplicação de regras de negócio**:
   - Filtro por empresas válidas
   - Filtro por mês atual
   - Cálculo de campos derivados

3. **Segmentação inteligente**:
   - **Pedidos Faturados**: Status = "Faturado"
   - **Pedidos Pendentes**: Status ≠ "Faturado"

4. **Cálculos automáticos**:
   - Total de registros
   - Valor total ingressado
   - Quantidade por status
   - Estatísticas por empresa

**Regras impostas**:
- ✅ Dados devem estar limpos e padronizados
- ✅ Segregação clara entre faturados e pendentes
- ✅ Cálculos precisos de valores
- ✅ Validação de integridade dos dados

---

### 📋 Etapa 5: Geração de Relatórios Excel

**O que faz**: Cria arquivos Excel profissionais com múltiplas abas

**Estrutura do Excel**:

**Aba 1: PedidosFaturados**
- Todos os pedidos com status "Faturado"
- Colunas: Empresa, Data, Pedido, Cliente, Valor, etc.
- Formatação profissional com cabeçalhos
- Filtros automáticos para fácil análise

**Aba 2: PedidosPendentes**
- Todos os pedidos com status diferente de "Faturado"
- Mesmas colunas da aba de faturados
- Destaque visual para status diferentes

**Estatísticas incluídas**:
- Total de registros por aba
- Valor total ingressado
- Quantidade de empresas únicas
- Data/hora de geração

**Regras impostas**:
- ✅ Formato .xlsx padrão
- ✅ Múltiplas abas organizadas
- ✅ Cabeçalhos claros e formatados
- ✅ Filtros automáticos habilitados
- ✅ Arquivo temporário (apagado após envio)

---

### 📋 Etapa 6: Envio Automático de Emails

**O que faz**: Envia emails personalizados para cada gerente

**Processo de envio**:

1. **Para cada gerente**:
   - Compor email personalizado
   - Anexar arquivo Excel gerado
   - Enviar via SMTP (Gmail)
   - Registrar log de envio

2. **Conteúdo do email**:
   - **Assunto**: "📋 Relatório Equipe [XXX] - [Nome Gerente]"
   - **Corpo**: Resumo estatístico e informações
   - **Anexo**: Arquivo Excel completo
   - **Personalização**: Nome e equipe do gerente

3. **Especial para Equipe 200**:
   - Email enviado para admin@empresa.com.br
   - Cópia automática também enviada
   - Aviso de não responder no corpo

**Regras impostas**:
- ✅ Email personalizado para cada gerente
- ✅ Anexo obrigatório com dados completos
- ✅ Formatação profissional do corpo
- ✅ Tratamento de erros de envio
- ✅ Logs detalhados de todas as tentativas

---

### 📋 Etapa 7: Orquestração e Monitoramento

**O que faz**: Coordena todas as etapas e monitora a execução

**Coordenação**:
- Execução sequencial de todas as etapas
- Tratamento de erros em cada fase
- Continuação mesmo se um gerente falhar
- Registro completo de estatísticas

**Monitoramento**:
- Logs estruturados com timestamps
- Métricas de performance
- Taxa de sucesso/fracasso
- Tempo total de execução

**Estatísticas finais**:
- Gerentes processados
- Registros totais
- Faturados vs Pendentes
- Valor total ingressado
- Taxa de sucesso

---

## 🎛️ Regras de Negócio e Validações

### 📊 Regras de Dados

1. **Empresas Válidas**
   - Apenas empresas: {1, 10, 11, 12, 14}
   - Outras empresas são ignoradas

2. **Período Temporal**
   - Apenas mês corrente
   - Data de hoje como referência

3. **Segmentação**
   - Faturados: Status = "Faturado"
   - Pendentes: Qualquer outro status

### 🔐 Regras de Segurança

1. **Autenticação**
   - Azure AD para Power BI
   - App Password para Gmail
   - Credenciais em variáveis de ambiente

2. **Validação**
   - Modelo semântico deve estar atualizado
   - Arquivos de configuração devem existir
   - Emails devem ser válidos

### ⚡ Regras de Performance

1. **Limites**
   - Timeout de 30 segundos por requisição
   - Máximo de 3 tentativas de envio
   - Limpeza automática de arquivos temporários

2. **Logging**
   - Todos os passos registrados
   - Erros com stack trace completo
   - Contexto em todas as mensagens

---

## 📈 Benefícios e Impactos

### 🎯 Para os Gerentes

- **Economia de tempo**: Não precisam mais buscar dados manualmente
- **Consistência**: Todos recebem dados do mesmo momento
- **Completude**: Informações detalhadas e organizadas
- **Pontualidade**: Recebem sempre no mesmo horário

### 🏢 Para a Empresa

- **Eficiência**: Redução drástica de trabalho manual
- **Confiabilidade**: Processo automatizado e validado
- **Escalabilidade**: Fácil adicionar novas equipes
- **Compliance**: Logs completos para auditoria

### 🔧 Para a TI

- **Manutenção**: Código limpo e documentado
- **Monitoramento**: Logs detalhados e métricas
- **Flexibilidade**: Fácil ajuste de regras
- **Segurança**: Sem senhas no código

---

## 🚀 Instalação e Configuração

### 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Azure AD com permissões Power BI
- Conta Gmail com App Password
- Arquivo dGerentes.xlsx com dados dos gerentes

### 🔧 Configuração

1. **Clonar repositório**:
   ```bash
   git clone https://github.com/gustavobarbosa-jpg/email-pedidos-faturados.git
   cd email-pedidos-faturados
   ```

2. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar ambiente**:
   ```bash
   cp config/.env.example .env
   # Editar .env com suas credenciais
   ```

4. **Validar configuração**:
   ```bash
   python main.py --validate
   ```

### 🚀 Execução

**Modo de teste (equipe 200)**:
```bash
python main.py --teams 200
```

**Modo de produção (todas as equipes)**:
```bash
python main.py
```

**Scheduler automático**:
```bash
python scripts/schedule_pipeline.py
```

**Serviço Windows**:
```bash
scripts/install_service.bat    # Executar como Administrador
```

---

## 📁 Estrutura do Projeto

```
├── main.py              # Ponto de entrada principal
├── requirements.txt     # Dependências Python
├── src/                 # Código fonte do pipeline
│   ├── extract/          # Extração de dados (Power BI, Excel)
│   ├── transform/        # Transformação e limpeza
│   ├── delivery/         # Envio de emails
│   ├── orchestration/    # Orquestração do pipeline
│   ├── config/          # Configurações e constantes
│   └── utils/           # Utilitários (logging, validação)
├── scripts/             # Scripts de automação
├── config/              # Arquivos de configuração
├── docs/                # Documentação completa
├── data/                # Diretórios de dados
│   ├── raw/             # Arquivos de entrada
│   ├── temp/            # Arquivos temporários
│   └── processed/       # Arquivos processados
├── logs/                # Logs de execução
└── tests/               # Testes automatizados
```

---

## 🔄 Fluxo de Dados

```
Power BI → Extração → Transformação → Excel → Email → Gerente
    ↑           ↓           ↓        ↓       ↓
Validação ← Orquestração ← Logs ← Monitoramento ← Estatísticas
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Power BI API**: Extração de dados
- **Azure AD**: Autenticação
- **Pandas**: Manipulação de dados
- **OpenPyXL**: Geração de Excel
- **SMTPlib**: Envio de emails
- **Schedule**: Agendamento
- **StructLog**: Logging estruturado

---

## 📝 Logs e Monitoramento

### 📋 Estrutura de Logs

```
2026-01-20 09:00:00,123 - pipeline - INFO - Starting pipeline: pipeline_20260120_090000
2026-01-20 09:00:01,456 - pipeline - INFO - Semantic model validation passed
2026-01-20 09:00:02,789 - pipeline - INFO - Processing manager 1/19 | Context: {'team_code': 200}
2026-01-20 09:00:05,012 - pipeline - INFO - Email sent successfully | Context: {'recipient': 'gerente@empresa.com'}
```

### 📊 Métricas Disponíveis

- Tempo total de execução
- Gerentes processados com sucesso
- Taxa de erro por etapa
- Volume de dados processados
- Performance do Power BI API

---

## 🔄 Manutenção e Operação

### 📅 Tarefas Semanais

- [ ] Executar teste com equipe 200
- [ ] Verificar logs de erros
- [ ] Validar espaço em disco
- [ ] Backup do arquivo dGerentes.xlsx

### 📅 Tarefas Mensais

- [ ] Atualizar dependências Python
- [ ] Revisar regras de negócio
- [ ] Analisar métricas de performance
- [ ] Documentar novas funcionalidades

### 🚨 Alertas e Incidentes

- **Modelo desatualizado**: Email automático para suporte
- **Falha de envio**: Tentativas automáticas com retry
- **Erro crítico**: Pipeline para e registra erro completo

---

## 📊 Repositório GitHub

### 🌐 Link do Projeto
- **Repositório**: https://github.com/gustavobarbosa-jpg/email-pedidos-faturados
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
- **Email**: admin@empresa.com.br
- **WhatsApp**: (35) 99825-3791
- **Issues**: GitHub Issues

---

## Suporte

Para problemas e dúvidas:
1. Verifique os logs em `logs/pipeline.log`
2. Execute o modo de validação primeiro
3. Revise as configurações no arquivo .env
4. Verifique o status da API do Power BI
5. Contacte o suporte técnico

---

**Este pipeline representa uma solução completa e profissional para automação de relatórios, eliminando trabalho manual e garantindo entregas consistentes e pontuais para todos os gerentes da organização.**
