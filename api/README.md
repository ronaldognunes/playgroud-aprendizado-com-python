# 🐍 API Flask - Gestão de Materiais

API REST desenvolvida em Flask para gerenciamento de materiais com PostgreSQL.

## 📋 **Características:**

- ✅ **CRUD Completo** de materiais
- ✅ **PostgreSQL** com queries SQL manuais
- ✅ **Docker** para banco de dados e pgAdmin
- ✅ **Variáveis de ambiente** para configuração
- ✅ **Timestamps automáticos** (data_criacao, data_atualizacao)

## 🚀 **Tecnologias:**

- **Python 3.13.5**
- **Flask 3.1.1** 
- **PostgreSQL 14.3**
- **psycopg2-binary** (sem ORM)
- **Docker & Docker Compose**

## 🗄️ **Estrutura do Banco:**

```sql
CREATE TABLE materiais (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📡 **Endpoints da API:**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/materiais` | Lista todos os materiais |
| GET | `/material/<id>` | Busca material por ID |
| POST | `/cadastrar-material` | Cria novo material |
| PUT | `/atualizar-material/<id>` | Atualiza material |
| DELETE | `/excluir-material/<id>` | Exclui material |

## 🛠️ **Configuração e Execução:**

### **1. Clonar e Configurar:**
```bash
# Clonar repositório
git clone <url-do-repo>
cd api

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais
```

### **2. Ambiente Python:**
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente (Windows)
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### **3. Banco de Dados (Docker):**
```bash
# Subir PostgreSQL e pgAdmin
docker-compose up -d

# Verificar se iniciou corretamente
docker-compose logs db
```

### **4. Executar API:**
```bash
# Navegar para o diretório app
cd app

# Executar aplicação
python main.py
```

### **5. Acessar:**
- **API:** http://localhost:5000
- **pgAdmin:** http://localhost:8080
  - Email: admin@admin.com
  - Senha: admin123

## 📝 **Exemplo de Uso:**

### **Criar Material:**
```bash
curl -X POST http://localhost:5000/cadastrar-material \
  -H "Content-Type: application/json" \
  -d '{"nome": "Material Teste", "descricao": "Descrição do teste"}'
```

### **Listar Materiais:**
```bash
curl -X GET http://localhost:5000/materiais
```

### **Resposta JSON:**
```json
{
  "id": 1,
  "nome": "Material Teste",
  "descricao": "Descrição do teste",
  "data_criacao": "2025-08-02T10:30:00",
  "data_atualizacao": "2025-08-02T10:30:00"
}
```

## 📂 **Estrutura do Projeto:**

```
api/
├── app/
│   └── main.py              # Aplicação Flask
├── init-db/
│   └── 01-init.sql          # Script de inicialização
├── pgadmin-config/
│   └── servers.json         # Configuração pgAdmin
├── .env                     # Variáveis de ambiente (não versionado)
├── .env.example             # Exemplo de configuração
├── .gitignore               # Arquivos ignorados pelo Git
├── docker-compose.yaml      # Configuração Docker
├── requirements.txt         # Dependências Python
└── README.md               # Esta documentação
```

## 🔧 **Desenvolvimento:**

### **Conectar ao Banco via pgAdmin:**
1. Acessar http://localhost:8080
2. Login com admin@admin.com / admin123
3. Configurar conexão:
   - Host: `db`
   - Port: `5432`
   - Database: `crud_db`
   - Username: (do .env)
   - Password: (do .env)

### **Comandos Úteis:**
```bash
# Ver logs do banco
docker-compose logs db

# Acessar PostgreSQL diretamente
docker-compose exec db psql -U ronaldo -d crud_db

# Parar containers
docker-compose down

# Limpar volumes (recria banco)
docker-compose down -v
```

## 📖 **Documentação Adicional:**

- [`DATABASE-SETUP.md`](DATABASE-SETUP.md) - Configuração do banco
- [`API-DATABASE.md`](API-DATABASE.md) - Documentação da API
- [`PGADMIN-CONNECTION.md`](PGADMIN-CONNECTION.md) - Configuração pgAdmin
- [`GITIGNORE-DOCS.md`](GITIGNORE-DOCS.md) - Documentação do .gitignore

## 🤝 **Contribuição:**

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 **Licença:**

Este projeto está sob a licença MIT.
