# 🚀 Guia Passo a Passo - Publicar no GitHub

## 📋 Pré-requisitos

### 1. Instalar Git
Se ainda não tiver Git instalado:

**Windows:**
1. Baixe Git em: https://git-scm.com/download/win
2. Execute o instalador
3. Aceite as configurações padrão
4. Reinicie o terminal

**Verificar instalação:**
```bash
git --version
```

### 2. Configurar Git
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

### 3. Criar Conta GitHub
- Acesse: https://github.com
- Crie uma conta gratuita
- Verifique seu email

---

## 🎯 Passo 1: Criar Repositório no GitHub

### 1.1 Acessar GitHub
1. Faça login em https://github.com
2. Clique no **+** no canto superior direito
3. Selecione **"New repository"**

### 1.2 Configurar Repositório
- **Repository name**: `email-pedidos-faturados`
- **Description**: `Pipeline de relatórios de pedidos faturados com integração Power BI`
- **Visibility**: Public (ou Private se preferir)
- **Add a README file**: ❌ (já temos um)
- **Add .gitignore**: ❌ (já temos um)
- **Choose a license**: ❌ (já temos um)

### 1.3 Criar Repositório
Clique em **"Create repository"**

### 1.4 Copiar URL
O GitHub mostrará a URL do repositório:
```
https://github.com/SEU_USERNAME/email-pedidos-faturados.git
```
Copie esta URL!

---

## 📁 Passo 2: Preparar Projeto Local

### 2.1 Abrir Terminal
1. Pressione `Win + R`
2. Digite `cmd` e pressione Enter
3. Navegue até a pasta do projeto:
```bash
cd "C:\Users\gustavo.barbosa\Documents\E-mail Pedidos Faturados"
```

### 2.2 Inicializar Git
```bash
git init
```

### 2.3 Adicionar Remote
```bash
git remote add origin https://github.com/SEU_USERNAME/email-pedidos-faturados.git
```
(Substitua SEU_USERNAME pelo seu username do GitHub)

---

## 📦 Passo 3: Fazer Primeiro Commit

### 3.1 Adicionar Arquivos
```bash
git add .
```

### 3.2 Verificar Status
```bash
git status
```

### 3.3 Fazer Commit
```bash
git commit -m "feat: implementação inicial do pipeline de relatórios"
```

### 3.4 Push para GitHub
```bash
git branch -M main
git push -u origin main
```

### 3.5 Autenticação (se necessário)
Se pedir usuário e senha:
- **Username**: Seu username do GitHub
- **Password**: Use um **Personal Access Token** (não sua senha!)

---

## 🔐 Passo 4: Criar Personal Access Token

### 4.1 Acessar Settings GitHub
1. No GitHub, clique sua foto > **Settings**
2. Vá para **Developer settings** > **Personal access tokens**
3. Clique **"Generate new token"**

### 4.2 Configurar Token
- **Token name**: `Pipeline Access`
- **Expiration**: 90 days
- **Scopes**: Marque:
  - ✅ **repo** (controle total de repositórios)
  - ✅ **workflow** (gerenciar GitHub Actions)

### 4.3 Gerar Token
1. Clique **"Generate token"**
2. **COPIE O TOKEN IMEDIATAMENTE** (ele não aparecerá novamente!)
3. Guarde em lugar seguro

---

## 🚀 Passo 5: Configurar Repositório

### 5.1 Verificar no GitHub
1. Atualize a página do repositório
2. Você deve ver todos os arquivos
3. Verifique se o README.md apareceu corretamente

### 5.2 Configurar Branch Protection
1. Vá para **Settings** > **Branches**
2. Clique **"Add rule"**
3. **Branch name pattern**: `main`
4. Marque:
   - ✅ **Require pull request reviews before merging**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
5. Clique **"Create"**

### 5.3 Configurar Secrets
1. Vá para **Settings** > **Secrets and variables** > **Actions**
2. Clique **"New repository secret"**
3. Adicione (se tiver):
   - `PYPI_API_TOKEN`: Token para publicação no PyPI
   - `CODECOV_TOKEN`: Token para Codecov

---

## 🔄 Passo 6: Ativar GitHub Actions

### 6.1 Verificar Workflows
1. Vá para **Actions** tab
2. Você deve ver os workflows executando
3. Aguarde a conclusão

### 6.2 Verificar Status
Os workflows devem mostrar:
- ✅ **CI/CD Pipeline**: Testes e qualidade
- ✅ **Security**: Scans de segurança
- ⚠️ **Release**: Pode falhar sem secrets configurados

---

## 🎉 Passo 7: Primeira Release

### 7.1 Criar Release
1. Vá para **Releases** > **"Create a new release"**
2. **Tag**: `v1.0.0`
3. **Title**: `Versão 1.0.0 - Produção`
4. **Description**:
```
## 🎉 Versão 1.0.0 - Produção

### ✨ Funcionalidades
- Pipeline completo de relatórios
- Integração com Power BI
- Envio automático de emails
- Scheduler para execução diária
- Validação de modelo semântico

### 🛠️ Instalação
```bash
pip install email-pedidos-faturados
```

### 📋 Documentação
- README completo em português
- Guia de instalação
- Troubleshooting

### 🚀 Em Produção
- Sistema rodando diariamente às 09:00
- Emails automáticos para gerentes
- Logs estruturados
- Monitoramento ativo
```

### 7.2 Publicar Release
Clique **"Publish release"**

---

## 📊 Passo 8: Verificar Configurações

### 8.1 Checklist Visual
- [ ] Arquivos aparecem no repositório
- [ ] README.md renderiza corretamente
- [ ] Badges funcionam
- [ ] CI/CD executou com sucesso
- [ ] Release criada
- [ ] Branch protection ativa
- [ ] Issues templates disponíveis

### 8.2 Testar Funcionalidades
1. Tente abrir uma **Issue**
2. Verifique os **Pull Request templates**
3. Teste o **GitHub Pages** (se configurado)

---

## 🆘 Problemas Comuns

### ❌ "Authentication failed"
**Solução**: Use Personal Access Token, não senha

### ❌ "Permission denied"
**Solução**: Verifique se o token tem scope `repo`

### ❌ "Push rejected"
**Solução**: Faça pull primeiro:
```bash
git pull origin main --allow-unrelated-histories
```

### ❌ "CI/CD failed"
**Solução**: Verifique logs em Actions > workflow

---

## 📞 Suporte

Se tiver dificuldades:
- **Gustavo Barbosa**: gustavo.barbosa@vilanova.com.br
- **WhatsApp**: (35) 99825-3791
- **GitHub Issues**: Crie issue no repositório

---

## 🎯 Resultado Final

Ao final deste processo você terá:
- ✅ Repositório profissional no GitHub
- ✅ CI/CD automatizado
- ✅ Documentação completa
- ✅ Sistema pronto para colaboração
- ✅ Releases automatizadas

**Parabéns! Seu projeto está no GitHub!** 🎉
