-- ============================================
-- DDL - Schema do E-commerce
-- ============================================

-- Tabela de Categorias
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    categoria_pai_id INTEGER,
    ativa BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_pai_id) REFERENCES categorias(id)
);

-- Tabela de Fornecedores
CREATE TABLE fornecedores (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco TEXT,
    cidade VARCHAR(100),
    estado VARCHAR(2),
    pais VARCHAR(50) DEFAULT 'Brasil',
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Produtos
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    categoria_id INTEGER NOT NULL,
    fornecedor_id INTEGER NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    custo DECIMAL(10, 2),
    estoque_atual INTEGER DEFAULT 0,
    estoque_minimo INTEGER DEFAULT 10,
    peso DECIMAL(8, 3),
    dimensoes VARCHAR(50),
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
    CHECK (preco >= 0),
    CHECK (estoque_atual >= 0)
);

-- Tabela de Clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cpf VARCHAR(11) UNIQUE,
    telefone VARCHAR(20),
    data_nascimento DATE,
    endereco TEXT,
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(8),
    tipo_cliente VARCHAR(20) DEFAULT 'regular',
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_compra TIMESTAMP
);

-- Tabela de Pedidos
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pendente',
    subtotal DECIMAL(12, 2) NOT NULL,
    desconto DECIMAL(12, 2) DEFAULT 0,
    frete DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(12, 2) NOT NULL,
    forma_pagamento VARCHAR(50),
    observacoes TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    CHECK (subtotal >= 0),
    CHECK (total >= 0),
    CHECK (status IN ('pendente', 'processando', 'enviado', 'entregue', 'cancelado'))
);

-- Tabela de Itens do Pedido
CREATE TABLE itens_pedido (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    desconto DECIMAL(10, 2) DEFAULT 0,
    subtotal DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    CHECK (quantidade > 0),
    CHECK (preco_unitario >= 0)
);

-- Tabela de Avaliações
CREATE TABLE avaliacoes (
    id INTEGER PRIMARY KEY,
    produto_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    nota INTEGER NOT NULL,
    titulo VARCHAR(200),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verificada BOOLEAN DEFAULT false,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    CHECK (nota >= 1 AND nota <= 5)
);

-- Tabela de Movimentações de Estoque
CREATE TABLE movimentacoes_estoque (
    id INTEGER PRIMARY KEY,
    produto_id INTEGER NOT NULL,
    tipo_movimentacao VARCHAR(20) NOT NULL,
    quantidade INTEGER NOT NULL,
    estoque_anterior INTEGER NOT NULL,
    estoque_novo INTEGER NOT NULL,
    referencia VARCHAR(100),
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100),
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    CHECK (tipo_movimentacao IN ('entrada', 'saida', 'ajuste', 'devolucao'))
);

-- Tabela de Promoções
CREATE TABLE promocoes (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    tipo_desconto VARCHAR(20) NOT NULL,
    valor_desconto DECIMAL(10, 2) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    ativa BOOLEAN DEFAULT true,
    codigo_cupom VARCHAR(50) UNIQUE,
    CHECK (tipo_desconto IN ('percentual', 'valor_fixo')),
    CHECK (valor_desconto > 0)
);

-- Tabela de Produtos em Promoção
CREATE TABLE produtos_promocao (
    id INTEGER PRIMARY KEY,
    promocao_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    FOREIGN KEY (promocao_id) REFERENCES promocoes(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    UNIQUE(promocao_id, produto_id)
);

-- Índices para melhorar performance
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
CREATE INDEX idx_produtos_fornecedor ON produtos(fornecedor_id);
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_data ON pedidos(data_pedido);
CREATE INDEX idx_itens_pedido ON itens_pedido(pedido_id);
CREATE INDEX idx_avaliacoes_produto ON avaliacoes(produto_id);
CREATE INDEX idx_movimentacoes_produto ON movimentacoes_estoque(produto_id);
CREATE INDEX idx_clientes_email ON clientes(email);