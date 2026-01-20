# 🐙 Guia de Configuração do GitHub

## 🚀 Passos para Publicar no GitHub

### 1. Preparar o Repositório

```bash
# Inicializar Git (se ainda não estiver)
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "feat: implementação inicial do pipeline de relatórios"

# Adicionar remote
git remote add origin https://github.com/SEU_USERNAME/email-pedidos-faturados.git
```

### 2. Configurar Branch Principal

```bash
# Renomear para main (se necessário)
git branch -M main

# Push inicial
git push -u origin main
```

### 3. Configurar Proteção de Branch

No GitHub:
1. Vá para Settings > Branches
2. Adicione regra para `main`
3. Exija:
   - Pull requests antes de merge
   - Status checks passando
   - Revisões de código

### 4. Configurar Secrets

Em Settings > Secrets and variables > Actions:
- `PYPI_API_TOKEN`: Token para publicação no PyPI
- `CODECOV_TOKEN`: Token para Codecov

### 5. Configurar Issues

1. Vá para Issues > Templates
2. Configure os templates criados:
   - Bug Report
   - Feature Request

### 6. Configurar Pull Requests

1. Vá para Pull requests > Templates
2. Configure o template de PR

### 7. Configurar Wiki

Crie páginas na Wiki:
- Instalação
- Configuração
- Troubleshooting
- FAQ

### 8. Configurar Projects

Crie um board para:
- Backlog
- Em Progresso
- Code Review
- Done

### 9. Configurar Releases

1. Vá para Releases
2. Crie primeira release:
   - Tag: `v1.0.0`
   - Title: `Versão 1.0.0 - Produção`
   - Description: Descreva as funcionalidades

### 10. Configurar GitHub Pages

1. Vá para Settings > Pages
2. Configure para mostrar documentação
3. Use branch `main` com pasta `/docs`

## 📋 Checklist Final

- [ ] Repositório criado e configurado
- [ ] Arquivos de configuração adicionados
- [ ] CI/CD funcionando
- [ ] Secrets configurados
- [ ] Templates configurados
- [ ] Proteção de branch ativada
- [ ] Primeira release criada
- [ ] Wiki configurada
- [ ] Issues e PRs templates ativos

## 🏷️ Tags e Releases

### Criar Nova Versão

```bash
# Criar tag
git tag -a v1.1.0 -m "Versão 1.1.0 - Nova funcionalidade"

# Push da tag
git push origin v1.1.0
```

### Publicar no PyPI

O GitHub Actions irá automaticamente:
1. Buildar o pacote
2. Fazer upload para o PyPI
3. Criar release no GitHub

## 📊 Monitoramento

### GitHub Insights

- Acompanhe:
  - Traffic (visitas, clones)
  - Contributors
  - Commits
  - Issues e PRs

### Code Quality

- SonarCloud (integrado com GitHub)
- CodeClimate
- Dependabot (para dependências)

## 🔄 Manutenção Contínua

### Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Security

- GitHub Dependabot alerts
- Security advisories
- Code scanning

## 📞 Suporte

Para dúvidas sobre configuração:
- Gustavo Barbosa: gustavo.barbosa@vilanova.com.br
- WhatsApp: (35) 99825-3791

---

**Seu projeto está pronto para o GitHub!** 🎉
