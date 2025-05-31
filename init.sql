-- Criando o banco de dados (caso use um único banco)
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- Tabela Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Tabela Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Tabela Permissões
CREATE TABLE IF NOT EXISTS permissoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

-- Tabela Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabela Categorias
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

-- Tabela Estoque
CREATE TABLE IF NOT EXISTS estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Tabela Orçamentos
CREATE TABLE IF NOT EXISTS orcamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status ENUM('Pendente', 'Aprovado', 'Rejeitado') NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela Fornecedores
CREATE TABLE IF NOT EXISTS fornecedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    contato VARCHAR(100)
);

-- Tabela Lojas
CREATE TABLE IF NOT EXISTS lojas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

-- Tabela Formas de Pagamento
CREATE TABLE IF NOT EXISTS pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metodo VARCHAR(50) NOT NULL
);

-- Tabela Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pendente', 'Pago', 'Enviado', 'Entregue') NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela Itens do Pedido
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Tabela Avaliações
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    cliente_id INT NOT NULL,
    nota INT NOT NULL CHECK(nota BETWEEN 1 AND 5),
    comentario TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela Frete
CREATE TABLE IF NOT EXISTS frete (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    prazo INT NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

-- Inserir dados iniciais para permitir funcionamento do microserviço
INSERT IGNORE INTO categorias (id, nome) VALUES (1, 'Categoria Padrão');

INSERT IGNORE INTO clientes (id, nome, email) VALUES (1, 'Cliente Demo', 'demo@example.com');

INSERT IGNORE INTO pedidos (id, cliente_id, status) VALUES (1, 1, 'Pendente');

-- Índices para otimização
CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos(categoria_id);
CREATE INDEX IF NOT EXISTS idx_items_pedido ON items(pedido_id);
CREATE INDEX IF NOT EXISTS idx_items_produto ON items(produto_id);
CREATE INDEX IF NOT EXISTS idx_estoque_produto ON estoque(produto_id);