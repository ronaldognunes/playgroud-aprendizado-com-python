-- Script de inicialização do banco de dados
-- Este script é executado automaticamente quando o container PostgreSQL é criado

-- Conectar ao banco de dados especificado
\c crud_db;

-- Criar a tabela materiais
CREATE TABLE IF NOT EXISTS materiais (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados de exemplo
INSERT INTO materiais (nome, descricao) VALUES 
    ('Material 1', 'Description 1'),
    ('Material 2', 'Description 2'),
    ('Material 3', 'Description 3')
ON CONFLICT DO NOTHING;

-- Criar função para atualizar data_atualizacao automaticamente
CREATE OR REPLACE FUNCTION update_data_atualizacao_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Criar trigger para atualizar data_atualizacao automaticamente
DROP TRIGGER IF EXISTS update_materiais_data_atualizacao ON materiais;
CREATE TRIGGER update_materiais_data_atualizacao 
    BEFORE UPDATE ON materiais 
    FOR EACH ROW 
    EXECUTE FUNCTION update_data_atualizacao_column();

-- Confirmar criação
\dt;
SELECT 'Tabela materiais criada com sucesso!' as status;