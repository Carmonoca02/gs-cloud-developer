import os
import pymysql
import json
from flask import Flask, jsonify, render_template, request

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

def get_db_connection():
    """Cria conexão com o banco de dados MySQL"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"Erro ao conectar com o banco: {e}")
        return None

def init_db():
    """Inicializa tabelas específicas do serviço de pagamentos se não existirem"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Criar tabela de transações se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transacoes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tipo VARCHAR(50) NOT NULL,
                    detalhes JSON,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Verificar se a tabela pagamentos existe, se não, criar
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagamentos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    metodo VARCHAR(50) NOT NULL
                )
            """)
            
            print("Tabelas inicializadas com sucesso!")
            
        except Exception as e:
            print(f"Erro ao inicializar banco: {e}")
        finally:
            connection.close()

def adicionar_transacao(tipo, detalhes):
    """Adiciona uma nova transação ao banco"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO transacoes (tipo, detalhes) VALUES (%s, %s)",
                (tipo, json.dumps(detalhes))
            )
            return True
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")
            return False
        finally:
            connection.close()
    return False

def obter_historico_transacoes():
    """Obtém o histórico de transações do banco"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM transacoes ORDER BY data_criacao DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao obter histórico: {e}")
            return []
        finally:
            connection.close()
    return []

def adicionar_forma_pagamento(forma):
    """Adiciona uma forma de pagamento ao banco"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO pagamentos (metodo) VALUES (%s)",
                (forma,)
            )
            return True
        except Exception as e:
            print(f"Erro ao adicionar forma de pagamento: {e}")
            return False
        finally:
            connection.close()
    return False

def obter_formas_pagamento():
    """Obtém as formas de pagamento do banco"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM pagamentos")
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao obter formas de pagamento: {e}")
            return []
        finally:
            connection.close()
    return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cartao_credito = request.form.get('cartao')
        boleto = request.form.get('boleto')
        pix = request.form.get('pix')
        
        # Exemplo de integração fictícia com Stripe
        if cartao_credito:
            charge = {
                "id": "ch_1Example",
                "amount": 1000,
                "currency": "brl",
                "description": "Pagamento com cartão de crédito",
                "status": "succeeded"
            }
            adicionar_transacao("cartao_credito", charge)
            return jsonify({"data": {"cartao_credito": charge}})
        
        # Exemplo de integração fictícia com PagSeguro para boleto
        if boleto:
            response = {
                "payment_url": "https://pagseguro.uol.com.br/checkout/payment/boleto/1234567890"
            }
            adicionar_transacao("boleto", response)
            return jsonify({"data": {"boleto": response}})
        
        # Exemplo de integração fictícia com PagSeguro para PIX
        if pix:
            response = {
                "payment_url": "https://pagseguro.uol.com.br/checkout/payment/pix/0987654321"
            }
            adicionar_transacao("pix", response)
            return jsonify({"data": {"pix": response}})
        
        return jsonify({"data": {"cartao_credito": cartao_credito, "boleto": boleto, "pix": pix}})
    return render_template('index.html')

@app.route('/status')
def status():
    # Verificar conexão com o banco
    connection = get_db_connection()
    if connection:
        connection.close()
        return jsonify({"status": "ok", "database": "connected"})
    else:
        return jsonify({"status": "ok", "database": "disconnected"}), 503

@app.route('/formas_pagamento', methods=['GET', 'POST'])
def formas_pagamento_route():
    if request.method == 'POST':
        nova_forma = request.form.get('forma_pagamento')
        if adicionar_forma_pagamento(nova_forma):
            formas = obter_formas_pagamento()
            return jsonify({"message": "Forma de pagamento cadastrada com sucesso", "formas_pagamento": formas})
        else:
            return jsonify({"error": "Erro ao cadastrar forma de pagamento"}), 500
    
    formas = obter_formas_pagamento()
    return jsonify({"formas_pagamento": formas})

@app.route('/historico')
def historico():
    transacoes = obter_historico_transacoes()
    return jsonify({"historico": transacoes})

# Inicializar banco quando a aplicação iniciar
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8787, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')