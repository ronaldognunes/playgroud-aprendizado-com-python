# 🗃️ API Flask com PostgreSQL - Queries Manuais

## 📋 **Resumo das Implementações**

### 🔧 **Pacotes Instalados:**
- **psycopg2-binary**: Driver PostgreSQL para Python (sem ORM)

### 🛠️ **Funcionalidades Implementadas:**

#### **1. Conexão com Banco:**
```python
def get_db_connection():
    """Retorna uma conexão com o banco PostgreSQL"""
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        cursor_factory=RealDictCursor  # Retorna como dicionário
    )
```

#### **2. CRUD Completo com Queries Manuais:**

| Endpoint | Método | Função | Query SQL |
|----------|--------|--------|-----------|
| `/materiais` | GET | Listar todos | `SELECT * FROM materiais ORDER BY id` |
| `/material/<id>` | GET | Buscar por ID | `SELECT * FROM materiais WHERE id = %s` |
| `/cadastrar-material` | POST | Criar | `INSERT INTO materiais (nome, descricao) VALUES (%s, %s)` |
| `/atualizar-material/<id>` | PUT | Atualizar | `UPDATE materiais SET ... WHERE id = %s` |
| `/excluir-material/<id>` | DELETE | Deletar | `DELETE FROM materiais WHERE id = %s` |

## 🚀 **Como Executar:**

### **1. Subir o Banco de Dados:**
```bash
# Navegar para o diretório do projeto
cd c:\projetos_python\api

# Subir PostgreSQL e pgAdmin
docker-compose up -d

# Aguardar inicialização (verifica logs)
docker-compose logs db
```

### **2. Configurar Variáveis de Ambiente:**

**Para usar com Docker (recomendado):**
```bash
# Editar .env
POSTGRES_HOST=db  # Nome do serviço no Docker
```

**Para usar localmente:**
```bash
# Editar .env  
POSTGRES_HOST=localhost  # Se PostgreSQL estiver local
```

### **3. Executar a API:**
```bash
# Ativar ambiente virtual e executar
.venv\Scripts\python.exe app\main.py
```

## 📝 **Exemplos de Uso da API:**

### **1. Listar Materiais:**
```bash
curl -X GET http://localhost:5000/materiais
```

### **2. Criar Material:**
```bash
curl -X POST http://localhost:5000/cadastrar-material \
  -H "Content-Type: application/json" \
  -d '{"nome": "Material Teste", "descricao": "Descrição do teste"}'
```

### **3. Buscar Material por ID:**
```bash
curl -X GET http://localhost:5000/material/1
```

### **4. Atualizar Material:**
```bash
curl -X PUT http://localhost:5000/atualizar-material/1 \
  -H "Content-Type: application/json" \
  -d '{"nome": "Material Atualizado"}'
```

### **5. Deletar Material:**
```bash
curl -X DELETE http://localhost:5000/excluir-material/1
```

## 🔍 **Exemplo de Resposta JSON:**

```json
{
  "id": 1,
  "nome": "Material 1",
  "descricao": "Description 1",
  "data_criacao": "2025-08-02T10:30:00",
  "data_atualizacao": "2025-08-02T10:30:00"
}
```

## ⚠️ **Tratamento de Erros:**

### **Erros de Conexão:**
```json
{
  "erro": "Erro de conexão com o banco de dados"
}
```

### **Erros de Validação:**
```json
{
  "erro": "Nome e descrição são obrigatórios"
}
```

### **Erros SQL:**
```json
{
  "erro": "Erro ao cadastrar material: [detalhes do erro]"
}
```

## 🏗️ **Arquitetura:**

### **Vantagens da Implementação:**
✅ **Queries Manuais**: Controle total sobre SQL
✅ **Performance**: Sem overhead de ORM
✅ **Flexibilidade**: Queries customizadas
✅ **Segurança**: Parâmetros preparados (evita SQL Injection)
✅ **Transações**: Controle manual de commit/rollback
✅ **Logs**: Tratamento de erros detalhado

### **Estrutura do Código:**
- **Conexão**: Função reutilizável `get_db_connection()`
- **Cursor**: `RealDictCursor` para resultados como dicionário
- **Validação**: Verificação de dados de entrada
- **Segurança**: Uso de parâmetros preparados (%s)
- **Cleanup**: Fechamento adequado de conexões

## 🔧 **Configurações de Ambiente:**

### **Desenvolvimento:**
- Use `POSTGRES_HOST=localhost` para desenvolvimento local
- PostgreSQL deve estar rodando na porta 5432

### **Docker:**
- Use `POSTGRES_HOST=db` para containers Docker
- A API e banco estarão na mesma rede Docker

### **Produção:**
- Configure `POSTGRES_HOST` com o endereço do servidor
- Use variáveis de ambiente seguras para credenciais
