# 🔗 Configuração de Conexão: pgAdmin ↔ PostgreSQL

## 🚀 **Configuração Automática (Implementada)**

O pgAdmin foi configurado para se conectar automaticamente ao PostgreSQL através de:

### 📁 **Arquivo de Configuração:**
- **Localização:** `pgadmin-config/servers.json`
- **Montagem:** Mapeado para `/pgladmin4/servers.json` no container

### 🔧 **Parâmetros de Conexão Automática:**
```json
{
  "Name": "PostgreSQL Local",
  "Host": "db",                    # Nome do serviço no Docker
  "Port": 5432,                   # Porta padrão do PostgreSQL
  "MaintenanceDB": "crud_db",     # Banco principal
  "Username": "ronaldo"           # Usuário do .env
}
```

## 🖱️ **Conexão Manual (Backup)**

Se a configuração automática não funcionar, conecte manualmente:

### **1. Acessar pgAdmin:**
- URL: http://localhost:8080
- Email: `admin@admin.com`
- Senha: `admin123`

### **2. Criar Nova Conexão:**
1. Clique com botão direito em "Servers" → "Register" → "Server"
2. **Aba General:**
   - Name: `PostgreSQL Local`
   
3. **Aba Connection:**
   - Host name/address: `db` ⚠️ **IMPORTANTE: Use "db", não "localhost"**
   - Port: `5432`
   - Maintenance database: `crud_db`
   - Username: `ronaldo`
   - Password: `ronaldo123`
   - Save password: ✅ Marcar

### **3. Testar Conexão:**
- Clique em "Test Connection"
- Se bem-sucedida, clique "Save"

## 🌐 **Rede Docker**

### **Por que usar "db" como host?**
```yaml
# No docker-compose.yaml, ambos estão na mesma rede:
networks:
  - network_bd
```

- ✅ **"db"** → Nome do serviço PostgreSQL (correto)
- ❌ **"localhost"** → Refere-se ao próprio container pgAdmin
- ❌ **"127.0.0.1"** → Refere-se ao próprio container pgAdmin

## 🔍 **Verificação de Conectividade**

### **Testar conexão de rede:**
```bash
# Executar dentro do container pgAdmin
docker-compose exec pgadmin ping db

# Verificar se PostgreSQL está rodando
docker-compose exec db pg_isready -U ronaldo -d crud_db
```

### **Ver logs em caso de erro:**
```bash
# Logs do pgAdmin
docker-compose logs pgadmin

# Logs do PostgreSQL
docker-compose logs db
```

## 📋 **Resumo das Configurações**

| Parâmetro | Valor | Observação |
|-----------|-------|------------|
| **Host** | `db` | Nome do serviço no Docker |
| **Port** | `5432` | Porta padrão PostgreSQL |
| **Database** | `crud_db` | Do arquivo .env |
| **Username** | `ronaldo` | Do arquivo .env |
| **Password** | `ronaldo123` | Do arquivo .env |
| **pgAdmin URL** | http://localhost:8080 | Interface web |
| **pgAdmin Email** | admin@admin.com | Login pgAdmin |
| **pgAdmin Password** | admin123 | Login pgAdmin |

## 🎯 **Próximos Passos**

1. Execute: `docker-compose up -d`
2. Aguarde os containers iniciarem
3. Acesse: http://localhost:8080
4. A conexão deve aparecer automaticamente
5. Se não aparecer, use a conexão manual
