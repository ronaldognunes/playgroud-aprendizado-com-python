import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, jsonify, request
app = Flask(__name__)
load_dotenv("../.env")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Configuração da conexão com o banco de dados
def get_db_connection():
    """Retorna uma conexão com o banco PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            port=POSTGRES_PORT,
            cursor_factory=RealDictCursor  # Retorna resultados como dicionário
        )
        return connection
    except psycopg2.Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None


class Material:
    def __init__(self, id, nome, descricao, data_criacao=None, data_atualizacao=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.data_criacao = data_criacao
        self.data_atualizacao = data_atualizacao
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "data_criacao": str(self.data_criacao) if self.data_criacao else None,
            "data_atualizacao": str(self.data_atualizacao) if self.data_atualizacao else None
        }

def get_materials():
    """Busca todos os materiais do banco de dados"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, nome, descricao, data_criacao, data_atualizacao FROM materiais ORDER BY id")
        rows = cursor.fetchall()
        
        materiais = []
        for row in rows:
            material = Material(
                id=row['id'],
                nome=row['nome'],
                descricao=row['descricao'],
                data_criacao=row['data_criacao'],
                data_atualizacao=row['data_atualizacao']
            )
            materiais.append(material)
        
        return materiais
    
    except psycopg2.Error as e:
        print(f"Erro ao buscar materiais: {e}")
        return []
    
    finally:
        cursor.close()
        connection.close()

@app.route("/materiais", methods=["GET"])
def retornar_materiais():
    """Retorna todos os materiais do banco de dados"""
    try:
        materiais = get_materials()
        materiais_json = [material.to_dict() for material in materiais]
        return jsonify(materiais_json), 200
    except Exception as e:
        return jsonify({"erro": f"Erro interno do servidor: {str(e)}"}), 500

@app.route("/cadastrar-material", methods=["POST"]) 
def cadastrar_material():
    """Cadastra um novo material no banco de dados"""
    data = request.get_json()
    if not data or 'nome' not in data or 'descricao' not in data:
        return jsonify({"erro": "Nome e descrição são obrigatórios"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"erro": "Erro de conexão com o banco de dados"}), 500

    try:
        cursor = connection.cursor()
        
        # INSERT com RETURNING para obter o ID gerado
        query = """
            INSERT INTO materiais (nome, descricao) 
            VALUES (%s, %s) 
            RETURNING id, nome, descricao, data_criacao, data_atualizacao
        """
        cursor.execute(query, (data['nome'], data['descricao']))
        row = cursor.fetchone()
        
        connection.commit()
        
        # Criar objeto Material com os dados retornados
        novo_material = Material(
            id=row['id'],
            nome=row['nome'],
            descricao=row['descricao'],
            data_criacao=row['data_criacao'],
            data_atualizacao=row['data_atualizacao']
        )
        
        return jsonify({
            "mensagem": "Material cadastrado com sucesso",
            "material": novo_material.to_dict()
        }), 201
        
    except psycopg2.Error as e:
        connection.rollback()
        return jsonify({"erro": f"Erro ao cadastrar material: {str(e)}"}), 500
    
    finally:
        cursor.close()
        connection.close()

@app.route("/atualizar-material/<int:id>", methods=["PUT"])
def atualizar_material(id):
    """Atualiza um material existente no banco de dados"""
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Dados JSON são obrigatórios"}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"erro": "Erro de conexão com o banco de dados"}), 500

    try:
        cursor = connection.cursor()
        
        # Verificar se o material existe
        cursor.execute("SELECT id FROM materiais WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"erro": "Material não encontrado"}), 404
        
        # Construir query de update dinamicamente
        campos_update = []
        valores = []
        
        if 'nome' in data:
            campos_update.append("nome = %s")
            valores.append(data['nome'])
            
        if 'descricao' in data:
            campos_update.append("descricao = %s")
            valores.append(data['descricao'])
        
        if not campos_update:
            return jsonify({"erro": "Nenhum campo para atualizar"}), 400
        
        # Adicionar data_atualizacao e id no final
        campos_update.append("data_atualizacao = CURRENT_TIMESTAMP")
        valores.append(id)
        
        query = f"""
            UPDATE materiais 
            SET {', '.join(campos_update)}
            WHERE id = %s
            RETURNING id, nome, descricao, data_criacao, data_atualizacao
        """
        
        cursor.execute(query, valores)
        row = cursor.fetchone()
        connection.commit()
        
        # Criar objeto Material atualizado
        material_atualizado = Material(
            id=row['id'],
            nome=row['nome'],
            descricao=row['descricao'],
            data_criacao=row['data_criacao'],
            data_atualizacao=row['data_atualizacao']
        )
        
        return jsonify({
            "mensagem": "Material atualizado com sucesso",
            "material": material_atualizado.to_dict()
        }), 200
        
    except psycopg2.Error as e:
        connection.rollback()
        return jsonify({"erro": f"Erro ao atualizar material: {str(e)}"}), 500
    
    finally:
        cursor.close()
        connection.close()

@app.route("/excluir-material/<int:id>", methods=["DELETE"])
def excluir_material(id):
    """Exclui um material do banco de dados"""
    connection = get_db_connection()
    if not connection:
        return jsonify({"erro": "Erro de conexão com o banco de dados"}), 500

    try:
        cursor = connection.cursor()
        
        # Verificar se o material existe antes de deletar
        cursor.execute("SELECT id FROM materiais WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"erro": "Material não encontrado"}), 404
        
        # Deletar o material
        cursor.execute("DELETE FROM materiais WHERE id = %s", (id,))
        connection.commit()
        
        return jsonify({"mensagem": "Material excluído com sucesso"}), 200
        
    except psycopg2.Error as e:
        connection.rollback()
        return jsonify({"erro": f"Erro ao excluir material: {str(e)}"}), 500
    
    finally:
        cursor.close()
        connection.close()

@app.route("/material/<int:id>", methods=["GET"])
def retornar_material_por_id(id):
    """Retorna um material específico por ID"""
    connection = get_db_connection()
    if not connection:
        return jsonify({"erro": "Erro de conexão com o banco de dados"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, nome, descricao, data_criacao, data_atualizacao FROM materiais WHERE id = %s", 
            (id,)
        )
        row = cursor.fetchone()
        
        if row:
            material = Material(
                id=row['id'],
                nome=row['nome'],
                descricao=row['descricao'],
                data_criacao=row['data_criacao'],
                data_atualizacao=row['data_atualizacao']
            )
            return jsonify(material.to_dict()), 200
        else:
            return jsonify({"erro": "Material não encontrado"}), 404
            
    except psycopg2.Error as e:
        return jsonify({"erro": f"Erro ao buscar material: {str(e)}"}), 500
    
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)







