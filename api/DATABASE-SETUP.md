# Instruções para Inicialização do Banco de Dados

## 📋 Script de Inicialização

O arquivo `init-db/01-init.sql` contém:

### 🗃️ **Estrutura da Tabela Materiais:**
```sql
CREATE TABLE materiais (
    id SERIAL PRIMARY KEY,           -- ID auto-incremento
    nome VARCHAR(255) NOT NULL,      -- Nome do material
    descricao TEXT,                  -- Descrição do material
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Data de criação
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data de atualização
);
```

### 🔧 **Funcionalidades Automáticas:**
- **Trigger de data_atualizacao:** Atualiza automaticamente quando um registro é modificado
- **Dados de exemplo:** Insere 3 materiais de teste

## 🚀 **Como Usar:**

### 1. **Primeira Execução (Criação):**
```bash
# Remove containers e volumes existentes (se houver)
docker-compose down -v

# Cria e executa os containers
docker-compose up -d
```

### 2. **Verificar se o Script foi Executado:**
```bash
# Ver logs do banco de dados
docker-compose logs db

# Conectar ao PostgreSQL para verificar
docker-compose exec db psql -U ronaldo -d crud_db -c "\dt"
```

### 3. **Acessar pgAdmin:**
- URL: http://localhost:8080
- Email: admin@admin.com
- Senha: admin123

### 4. **Configurar Conexão no pgAdmin:**
- Host: `db`
- Port: `5432`
- Username: `ronaldo`
- Password: `ronaldo123`
- Database: `crud_db`

## ⚠️ **Importante:**

- O script só executa na **primeira criação** do container
- Para re-executar, delete o volume: `docker-compose down -v`
- Os arquivos em `init-db/` são executados em ordem alfabética
- Use prefixos numerados (01-, 02-) para controlar a ordem de execução

## 🔍 **Verificar Funcionamento:**

```sql
-- No pgAdmin ou psql, execute:
SELECT * FROM material;

-- Deve retornar os 3 materiais de exemplo
```
