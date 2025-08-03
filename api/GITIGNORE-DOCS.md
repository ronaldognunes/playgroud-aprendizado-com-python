# 📋 Documentação do .gitignore

Este arquivo `.gitignore` foi criado especificamente para o projeto Flask com PostgreSQL, seguindo as melhores práticas para projetos Python.

## 🗂️ **Principais Seções Ignoradas:**

### 🐍 **Python Específico:**
- **`__pycache__/`** - Cache de bytecode compilado
- **`*.py[cod]`** - Arquivos compilados Python
- **`.venv/`, `venv/`** - Ambientes virtuais Python
- **`*.egg-info/`** - Metadados de pacotes Python
- **`dist/`, `build/`** - Diretórios de build/distribuição

### 🌍 **Variáveis de Ambiente:**
- **`.env`** - ⚠️ **CRÍTICO** - Contém credenciais do banco
- **`.env.local`, `.env.production`** - Ambientes específicos
- **`instance/`** - Configurações Flask sensíveis

### 🗄️ **Banco de Dados:**
- **`*.sql.backup`** - Backups de banco
- **`*.dump`, `*.pg_dump`** - Dumps PostgreSQL
- **`postgres_data/`** - Dados locais PostgreSQL

### 🐳 **Docker:**
- **`docker-compose.override.yml`** - Overrides locais do Docker
- **`.docker/`** - Dados específicos do Docker

### 💻 **IDEs e Editores:**
- **`.vscode/`** - Configurações VS Code (mantém algumas úteis)
- **`.idea/`** - Configurações PyCharm/IntelliJ
- **`.DS_Store`** - Arquivos sistema macOS

### 📊 **Testes e Coverage:**
- **`.pytest_cache/`** - Cache do pytest
- **`htmlcov/`** - Relatórios de cobertura
- **`.coverage`** - Dados de cobertura

### 📁 **Logs e Temporários:**
- **`*.log`** - Arquivos de log
- **`logs/`** - Diretório de logs
- **`*.tmp`, `*.temp`** - Arquivos temporários

## ⚠️ **Arquivos Críticos Ignorados:**

### 🔐 **Segurança:**
```bash
.env                    # ❌ NUNCA versionar - contém senhas!
instance/               # ❌ Configurações Flask sensíveis
*.log                   # ❌ Podem conter dados sensíveis
```

### 🗄️ **Dados:**
```bash
postgres_data/          # ❌ Dados do banco PostgreSQL
*.sql.backup           # ❌ Backups podem ter dados sensíveis
*.dump                 # ❌ Dumps do banco
```

## ✅ **Arquivos que DEVEM ser versionados:**

### 📋 **Configuração:**
```bash
docker-compose.yaml     # ✅ Configuração dos containers
requirements.txt        # ✅ Dependências Python (se houver)
pyproject.toml         # ✅ Configuração do projeto
```

### 🗄️ **Scripts de Banco:**
```bash
init-db/               # ✅ Scripts de inicialização
*.sql                  # ✅ Scripts SQL (exceto backups)
```

### 📖 **Documentação:**
```bash
README.md              # ✅ Documentação do projeto
*.md                   # ✅ Documentação em geral
```

### 🐍 **Código:**
```bash
app/                   # ✅ Código da aplicação
*.py                   # ✅ Arquivos Python
```

## 🔧 **Configurações Especiais:**

### 📝 **VS Code (Parcialmente Incluído):**
```bash
.vscode/settings.json   # ✅ Configurações úteis do projeto
.vscode/tasks.json      # ✅ Tasks de build/run
.vscode/launch.json     # ✅ Configurações de debug
```

### 🐳 **Docker:**
```bash
docker-compose.yaml         # ✅ Configuração base
docker-compose.override.yml # ❌ Overrides locais
```

## 📝 **Como Usar:**

### **Verificar arquivos ignorados:**
```bash
git status --ignored
```

### **Forçar adicionar arquivo ignorado (cuidado!):**
```bash
git add -f arquivo.txt
```

### **Ver o que seria ignorado:**
```bash
git check-ignore -v .env
```

## 🚨 **Avisos Importantes:**

1. **Nunca commite o arquivo `.env`** - contém credenciais!
2. **Cuidado com logs** - podem conter informações sensíveis
3. **Ambientes virtuais** - sempre use `.venv/` ou `venv/`
4. **Dados de banco** - nunca versione dados reais

## 💡 **Dicas:**

1. **Sempre revise** o que está sendo commitado: `git status`
2. **Use `.env.example`** para mostrar estrutura sem dados sensíveis
3. **Documente dependências** em `requirements.txt` ou `pyproject.toml`
4. **Mantenha logs separados** do código versionado
