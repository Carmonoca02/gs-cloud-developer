from flask import Flask, jsonify, request, render_template
import pymysql
import os
from contextlib import contextmanager

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql-db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'ecommerce_db'),
    'charset': 'utf8mb4',
    'autocommit': True
}

@contextmanager
def get_db_connection():
    """Context manager para conexão com banco de dados"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection:
            connection.close()

def init_db():
    """Inicializa as tabelas se não existirem"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Verificar se a tabela items existe
            cursor.execute("SHOW TABLES LIKE 'items'")
            if not cursor.fetchone():
                print("Tabela items não encontrada, banco será inicializado pelo init.sql")
        print("✅ Conexão com banco de dados estabelecida")
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")

# Inicializar banco na inicialização da app
init_db()

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/itens', methods=['GET', 'POST'])
def itens_route():
    if request.method == 'POST':
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Inserir produto diretamente
                cursor.execute("""
                    INSERT INTO produtos (nome, descricao, preco, categoria_id) 
                    VALUES (%s, %s, %s, %s)
                """, (
                    request.form.get('nome'),
                    request.form.get('descricao'),
                    float(request.form.get('preco')),
                    1  # categoria padrão
                ))
                
                produto_id = cursor.lastrowid
                
                # Criar entrada no estoque com quantidade padrão
                cursor.execute("""
                    INSERT INTO estoque (produto_id, quantidade) 
                    VALUES (%s, %s)
                """, (produto_id, 1))
                
                return jsonify({
                    "message": "Produto cadastrado com sucesso", 
                    "produto_id": produto_id
                })
                
        except Exception as e:
            return jsonify({"error": f"Erro ao cadastrar produto: {str(e)}"}), 500
    
    # GET - Listar itens (produtos)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT 
                    p.id as produto_id,
                    p.id as item_id,
                    p.nome,
                    p.descricao,
                    p.preco,
                    COALESCE(e.quantidade, 1) as quantidade,
                    p.categoria_id
                FROM produtos p
                LEFT JOIN estoque e ON p.id = e.produto_id
                ORDER BY p.id DESC
            """)
            itens = cursor.fetchall()
            return jsonify({"itens": itens})
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar itens: {str(e)}"}), 500

@app.route('/itens/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def item_route(item_id):
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("""
                    SELECT 
                        i.id as item_id,
                        p.id as produto_id,
                        p.nome,
                        p.descricao,
                        i.preco,
                        i.quantidade
                    FROM items i
                    JOIN produtos p ON i.produto_id = p.id
                    WHERE i.id = %s
                """, (item_id,))
                item = cursor.fetchone()
                
                if not item:
                    return jsonify({"message": "Item não encontrado"}), 404
                    
                return jsonify({"item": item})
        except Exception as e:
            return jsonify({"error": f"Erro ao buscar item: {str(e)}"}), 500

    if request.method == 'PUT':
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Atualizar produto
                cursor.execute("""
                    UPDATE produtos p
                    JOIN items i ON p.id = i.produto_id
                    SET p.nome = %s, p.descricao = %s, p.preco = %s
                    WHERE i.id = %s
                """, (
                    request.form.get('nome'),
                    request.form.get('descricao'),
                    float(request.form.get('preco')),
                    item_id
                ))
                
                # Atualizar item
                cursor.execute("""
                    UPDATE items 
                    SET preco = %s
                    WHERE id = %s
                """, (float(request.form.get('preco')), item_id))
                
                if cursor.rowcount == 0:
                    return jsonify({"message": "Item não encontrado"}), 404
                    
                return jsonify({"message": "Item atualizado com sucesso"})
        except Exception as e:
            return jsonify({"error": f"Erro ao atualizar item: {str(e)}"}), 500

    if request.method == 'DELETE':
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Deletar estoque relacionado primeiro (se existir)
                cursor.execute("DELETE FROM estoque WHERE produto_id = %s", (item_id,))
                
                # Deletar produto
                cursor.execute("DELETE FROM produtos WHERE id = %s", (item_id,))
                
                if cursor.rowcount == 0:
                    return jsonify({"message": "Produto não encontrado"}), 404
                
                return jsonify({"message": "Produto removido com sucesso"})
        except Exception as e:
            return jsonify({"error": f"Erro ao remover produto: {str(e)}"}), 500

@app.route('/status')
def status():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return jsonify({
                "status": "ok", 
                "database": "connected",
                "service": "itens-service"
            })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "database": "disconnected",
            "error": str(e),
            "service": "itens-service"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8383, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')