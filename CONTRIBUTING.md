# Contribuindo com o Pipeline de Relatórios

Obrigado pelo seu interesse em contribuir! Este documento fornece diretrizes para contribuições.

## 🚀 Como Contribuir

### 1. Setup do Ambiente

```bash
# Clone o repositório
git clone <repository-url>
cd email-pedidos-faturados

# Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### 2. Configure as Variáveis de Ambiente

Crie um arquivo `.env` baseado em `.env.example`:
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

### 3. Desenvolvimento

```bash
# Execute testes
pytest tests/ -v

# Formate o código
black src/ tests/

# Verifique tipos
mypy src/

# Execute linting
flake8 src/ tests/
```

## 📋 Tipos de Contribuições

### 🐛 Reportando Bugs

- Use o template de issue para bugs
- Inclua logs relevantes
- Descreva os passos para reproduzir

### ✨ Novas Funcionalidades

- Abra uma issue para discussão antes de implementar
- Siga a arquitetura existente
- Adicione testes quando aplicável

### 📝 Documentação

- Correções de ortografia e gramática
- Melhorias na clareza
- Traduções

### 🧪 Testes

- Testes unitários para novas funcionalidades
- Testes de integração
- Testes de ponta a ponta

## 🎯 Padrões de Código

### Python

- Use type hints
- Siga PEP 8
- Comentários em português
- Nomes de variáveis em português quando apropriado

### Commits

- Use mensagens de commit claras
- Formato: `tipo: descrição`
  - `feat`: nova funcionalidade
  - `fix`: correção de bug
  - `docs`: documentação
  - `style`: formatação
  - `refactor`: refatoração
  - `test`: testes
  - `chore`: manutenção

### Exemplos

```
feat: adicionar validação de email
fix: corrigir erro de parsing de data
docs: atualizar README com instruções de instalação
```

## 🔄 Processo de Pull Request

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça suas alterações
4. Execute testes: `pytest`
5. Formate código: `black`
6. Commit suas alterações: `git commit -m 'feat: adicionar nova funcionalidade'`
7. Push para o fork: `git push origin feature/nova-funcionalidade`
8. Abra um Pull Request

## 📋 Checklist de PR

- [ ] Código segue os padrões do projeto
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Logs em português
- [ ] Sem segredos hardcoded
- [ ] Mensagens de commit claras

## 🤝 Código de Conduta

Seja respeitoso e profissional. Todas as contribuições são bem-vindas!

## 📞 Contato

Para dúvidas:
- Gustavo Barbosa: gustavo.barbosa@vilanova.com.br
- WhatsApp: (35) 99825-3791

---

Obrigado por contribuir! 🎉
