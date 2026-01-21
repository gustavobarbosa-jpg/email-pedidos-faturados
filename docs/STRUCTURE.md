# 📁 Estrutura do Projeto

## 🗂️ Organização de Pastas

```
email-pedidos-faturados/
├── 📄 main.py                    # Ponto de entrada principal
├── 📄 requirements.txt           # Dependências Python
├── 📄 .env                       # Variáveis de ambiente (não versionado)
├── 📄 .gitignore                # Arquivos ignorados pelo Git
│
├── 📁 src/                      # Código fonte do pipeline
│   ├── extract/                 # Extração de dados
│   ├── transform/               # Transformação de dados
│   ├── delivery/                # Envio de emails
│   ├── orchestration/           # Orquestração do pipeline
│   ├── config/                  # Configurações
│   └── utils/                   # Utilitários
│
├── 📁 scripts/                  # Scripts de automação
│   ├── schedule_pipeline.py     # Scheduler automático
│   ├── test_validation_only.py  # Teste de validação
│   ├── install_service.bat      # Instala serviço Windows
│   ├── uninstall_service.bat    # Remove serviço Windows
│   ├── start_scheduler.bat      # Inicia scheduler manual
│   └── test_team_200.bat        # Teste equipe 200
│
├── 📁 config/                   # Arquivos de configuração
│   ├── .env.example            # Template de variáveis
│   ├── pyproject.toml          # Configuração Python
│   └── setup.py                 # Setup do pacote
│
├── 📁 docs/                     # Documentação
│   ├── README.md               # Documentação completa
│   ├── LICENSE                 # Licença MIT
│   └── STRUCTURE.md            # Este arquivo
│
├── 📁 data/                     # Diretórios de dados
│   ├── raw/                    # Arquivos de entrada
│   ├── temp/                   # Arquivos temporários
│   └── processed/              # Arquivos processados
│
├── 📁 logs/                     # Logs de execução
├── 📁 tests/                    # Testes automatizados
└── 📁 .github/                  # Configurações GitHub
```

## 📋 Arquivos na Raiz

### Essenciais
- **main.py**: Único arquivo executável na raiz
- **requirements.txt**: Dependências necessárias
- **README.md**: Guia rápido de início

### Configuração
- **.env**: Credenciais (criado a partir de config/.env.example)
- **.gitignore**: Arquivos ignorados pelo versionamento

## 🚀 Como Usar

### Execução Principal
```bash
python main.py                    # Executa o pipeline
python main.py --teams 200        # Equipe específica
python main.py --validate         # Modo validação
```

### Scripts de Automação
```bash
python scripts/schedule_pipeline.py           # Scheduler
python scripts/test_validation_only.py        # Teste validação
scripts/install_service.bat                   # Instalar serviço
scripts/test_team_200.bat                     # Teste equipe 200
```

## 🎯 Benefícios da Organização

### ✅ Clareza
- **Raiz limpa**: Apenas arquivos essenciais
- **Separação**: Scripts, configuração e docs em pastas próprias
- **Lógica**: Cada pasta tem propósito claro

### ✅ Manutenção
- **Scripts centralizados**: Todos em `scripts/`
- **Configuração agrupada**: Arquivos de config em `config/`
- **Documentação organizada**: Docs em `docs/`

### ✅ Segurança
- **.env protegido**: Não está na raiz
- **Credenciais isoladas**: Em pasta de configuração
- **Acesso controlado**: Scripts em pasta separada

## 🔄 Fluxo de Trabalho

1. **Desenvolvimento**: Trabalhar em `src/`
2. **Testes**: Usar scripts em `scripts/`
3. **Configuração**: Ajustar arquivos em `config/`
4. **Documentação**: Atualizar em `docs/`
5. **Execução**: Apenas `python main.py` na raiz

## 📝 Regras

- ✅ **Raiz**: Apenas `main.py`, `requirements.txt`, `README.md`
- ✅ **Scripts**: Todos em `scripts/`
- ✅ **Config**: Arquivos de configuração em `config/`
- ✅ **Docs**: Documentação em `docs/`
- ✅ **Código fonte**: Sempre em `src/`

Esta organização mantém o projeto limpo, profissional e fácil de manter!
