-- ============================================
-- INSERT - Dados de Exemplo
-- ============================================

-- Inserir Categorias (primeiro as principais, depois as subcategorias)
INSERT INTO categorias (id, nome, descricao, categoria_pai_id) VALUES
(1, 'Eletrônicos', 'Produtos eletrônicos em geral', NULL),
(6, 'Moda', 'Roupas e acessórios', NULL),
(9, 'Livros', 'Livros físicos e digitais', NULL),
(10, 'Casa e Decoração', 'Itens para casa', NULL);

-- Subcategorias de Eletrônicos
INSERT INTO categorias (id, nome, descricao, categoria_pai_id) VALUES
(2, 'Computadores', 'Computadores e acessórios', 1),
(3, 'Smartphones', 'Telefones celulares e acessórios', 1);

-- Subcategorias de Computadores
INSERT INTO categorias (id, nome, descricao, categoria_pai_id) VALUES
(4, 'Notebooks', 'Notebooks e ultrabooks', 2),
(5, 'Periféricos', 'Teclados, mouses, monitores', 2);

-- Subcategorias de Moda
INSERT INTO categorias (id, nome, descricao, categoria_pai_id) VALUES
(7, 'Roupas Masculinas', 'Vestuário masculino', 6),
(8, 'Roupas Femininas', 'Vestuário feminino', 6);

-- Inserir Fornecedores
INSERT INTO fornecedores (id, nome, cnpj, email, telefone, cidade, estado) VALUES
(1, 'Tech Solutions Ltda', '12345678901234', 'contato@techsolutions.com.br', '11987654321', 'São Paulo', 'SP'),
(2, 'Mega Eletrônicos S.A.', '23456789012345', 'vendas@megaeletronicos.com.br', '21976543210', 'Rio de Janeiro', 'RJ'),
(3, 'Fashion Style Import', '34567890123456', 'importacao@fashionstyle.com.br', '11965432109', 'São Paulo', 'SP'),
(4, 'Livros & Cia', '45678901234567', 'pedidos@livroseciа.com.br', '31954321098', 'Belo Horizonte', 'MG'),
(5, 'Casa Bella Decorações', '56789012345678', 'contato@casabella.com.br', '41943210987', 'Curitiba', 'PR');

-- Inserir Produtos
INSERT INTO produtos (id, nome, descricao, categoria_id, fornecedor_id, preco, custo, estoque_atual, peso) VALUES
(1, 'Notebook Dell Inspiron 15', 'Notebook com Intel i5, 8GB RAM, 256GB SSD', 4, 1, 3299.90, 2500.00, 15, 2.100),
(2, 'Mouse Logitech MX Master 3', 'Mouse sem fio ergonômico', 5, 1, 499.90, 350.00, 45, 0.141),
(3, 'Teclado Mecânico Keychron K2', 'Teclado mecânico wireless', 5, 1, 699.90, 450.00, 30, 0.580),
(4, 'iPhone 13 128GB', 'Smartphone Apple última geração', 3, 2, 4999.00, 4000.00, 25, 0.173),
(5, 'Samsung Galaxy S21', 'Smartphone Android top de linha', 3, 2, 3499.00, 2800.00, 32, 0.169),
(6, 'Monitor LG 27" 4K', 'Monitor UHD com HDR', 5, 2, 1899.00, 1400.00, 20, 6.800),
(7, 'Camiseta Polo Masculina', 'Camiseta polo 100% algodão', 7, 3, 89.90, 45.00, 120, 0.250),
(8, 'Calça Jeans Feminina', 'Calça jeans skinny', 8, 3, 159.90, 80.00, 85, 0.450),
(9, 'Vestido Floral Feminino', 'Vestido longo estampado', 8, 3, 199.90, 95.00, 60, 0.350),
(10, 'Sapato Social Masculino', 'Sapato em couro legítimo', 7, 3, 249.90, 150.00, 40, 0.900),
(11, 'O Senhor dos Anéis - Box', 'Trilogia completa em capa dura', 9, 4, 189.90, 120.00, 50, 2.100),
(12, 'Clean Code', 'Livro sobre programação limpa', 9, 4, 89.90, 55.00, 75, 0.650),
(13, 'Luminária de Mesa LED', 'Luminária moderna com dimmer', 10, 5, 149.90, 85.00, 35, 1.200),
(14, 'Conjunto de Panelas 5 Peças', 'Panelas antiaderentes', 10, 5, 299.90, 180.00, 28, 4.500),
(15, 'Notebook Lenovo IdeaPad', 'Notebook Intel i7, 16GB RAM, 512GB SSD', 4, 1, 4599.00, 3500.00, 12, 2.200);

-- Inserir Clientes
INSERT INTO clientes (id, nome, email, cpf, telefone, data_nascimento, cidade, estado, cep, tipo_cliente) VALUES
(1, 'João Silva Santos', 'joao.silva@email.com', '12345678901', '11987654321', '1990-05-15', 'São Paulo', 'SP', '01310100', 'premium'),
(2, 'Maria Oliveira Costa', 'maria.oliveira@email.com', '23456789012', '21976543210', '1985-08-22', 'Rio de Janeiro', 'RJ', '20040020', 'premium'),
(3, 'Pedro Alves Ferreira', 'pedro.alves@email.com', '34567890123', '11965432109', '1992-11-30', 'São Paulo', 'SP', '04571020', 'regular'),
(4, 'Ana Paula Souza', 'ana.souza@email.com', '45678901234', '31954321098', '1988-03-10', 'Belo Horizonte', 'MG', '30130100', 'regular'),
(5, 'Carlos Eduardo Lima', 'carlos.lima@email.com', '56789012345', '41943210987', '1995-07-18', 'Curitiba', 'PR', '80010000', 'regular'),
(6, 'Juliana Mendes Rocha', 'juliana.rocha@email.com', '67890123456', '85932109876', '1991-12-05', 'Fortaleza', 'CE', '60010000', 'vip'),
(7, 'Roberto Carlos Dias', 'roberto.dias@email.com', '78901234567', '61921098765', '1987-09-25', 'Brasília', 'DF', '70040000', 'regular'),
(8, 'Fernanda Lima Santos', 'fernanda.lima@email.com', '89012345678', '71910987654', '1993-04-14', 'Salvador', 'BA', '40010000', 'regular');

-- Inserir Pedidos
INSERT INTO pedidos (id, cliente_id, data_pedido, status, subtotal, desconto, frete, total, forma_pagamento) VALUES
(1, 1, '2024-11-15 10:30:00', 'entregue', 3799.80, 100.00, 50.00, 3749.80, 'cartao_credito'),
(2, 2, '2024-11-20 14:45:00', 'entregue', 4999.00, 0.00, 0.00, 4999.00, 'pix'),
(3, 3, '2024-11-25 09:15:00', 'enviado', 1199.80, 50.00, 30.00, 1179.80, 'cartao_credito'),
(4, 4, '2024-12-01 16:20:00', 'processando', 449.80, 0.00, 25.00, 474.80, 'boleto'),
(5, 5, '2024-12-03 11:00:00', 'pendente', 299.90, 0.00, 15.00, 314.90, 'cartao_debito'),
(6, 1, '2024-12-05 13:30:00', 'entregue', 899.80, 50.00, 0.00, 849.80, 'cartao_credito'),
(7, 6, '2024-12-06 15:45:00', 'enviado', 5798.90, 200.00, 0.00, 5598.90, 'pix'),
(8, 7, '2024-12-07 10:10:00', 'processando', 339.80, 0.00, 20.00, 359.80, 'cartao_credito');

-- Inserir Itens dos Pedidos
INSERT INTO itens_pedido (id, pedido_id, produto_id, quantidade, preco_unitario, desconto, subtotal) VALUES
(1, 1, 1, 1, 3299.90, 50.00, 3249.90),
(2, 1, 2, 1, 499.90, 0.00, 499.90),
(3, 2, 4, 1, 4999.00, 0.00, 4999.00),
(4, 3, 2, 1, 499.90, 25.00, 474.90),
(5, 3, 3, 1, 699.90, 25.00, 674.90),
(6, 4, 7, 5, 89.90, 0.00, 449.50),
(7, 5, 14, 1, 299.90, 0.00, 299.90),
(8, 6, 12, 10, 89.90, 50.00, 849.00),
(9, 7, 1, 1, 3299.90, 100.00, 3199.90),
(10, 7, 4, 1, 4999.00, 100.00, 4899.00),
(11, 8, 8, 2, 159.90, 0.00, 319.80),
(12, 8, 10, 1, 249.90, 0.00, 249.90);

-- Inserir Avaliações
INSERT INTO avaliacoes (id, produto_id, cliente_id, nota, titulo, comentario, verificada) VALUES
(1, 1, 1, 5, 'Excelente notebook!', 'Produto de ótima qualidade, super rápido e silencioso. Recomendo!', true),
(2, 2, 1, 5, 'Melhor mouse que já usei', 'Ergonomia perfeita, bateria dura muito. Vale cada centavo.', true),
(3, 4, 2, 4, 'iPhone top', 'Ótimo celular, mas o preço poderia ser melhor.', true),
(4, 12, 6, 5, 'Leitura obrigatória', 'Todo programador deveria ler este livro. Mudou minha forma de escrever código.', true),
(5, 7, 4, 4, 'Boa qualidade', 'Camiseta confortável e bem acabada. Tamanho conforme esperado.', true),
(6, 14, 5, 5, 'Panelas excelentes', 'Antiaderente de verdade, fácil de limpar. Ótima compra!', true),
(7, 1, 7, 5, 'Superou expectativas', 'Notebook potente e com bom custo-benefício.', true);

-- Inserir Movimentações de Estoque
INSERT INTO movimentacoes_estoque (id, produto_id, tipo_movimentacao, quantidade, estoque_anterior, estoque_novo, referencia, usuario) VALUES
(1, 1, 'entrada', 20, 0, 20, 'Compra inicial', 'admin'),
(2, 1, 'saida', 1, 20, 19, 'Pedido #1', 'sistema'),
(3, 1, 'saida', 1, 19, 18, 'Pedido #7', 'sistema'),
(4, 1, 'ajuste', -3, 18, 15, 'Inventário mensal', 'admin'),
(5, 2, 'entrada', 50, 0, 50, 'Compra inicial', 'admin'),
(6, 2, 'saida', 2, 50, 48, 'Vendas diversas', 'sistema'),
(7, 2, 'ajuste', -3, 48, 45, 'Ajuste de inventário', 'admin'),
(8, 4, 'entrada', 30, 0, 30, 'Compra inicial', 'admin'),
(9, 4, 'saida', 5, 30, 25, 'Vendas período', 'sistema'),
(10, 12, 'entrada', 100, 0, 100, 'Compra inicial', 'admin'),
(11, 12, 'saida', 10, 100, 90, 'Pedido #6', 'sistema'),
(12, 12, 'devolucao', 2, 90, 92, 'Devolução cliente', 'atendimento'),
(13, 12, 'saida', 17, 92, 75, 'Vendas diversas', 'sistema');

-- Inserir Promoções
INSERT INTO promocoes (id, nome, descricao, tipo_desconto, valor_desconto, data_inicio, data_fim, codigo_cupom) VALUES
(1, 'Black Friday 2024', 'Descontos especiais para Black Friday', 'percentual', 20.00, '2024-11-25', '2024-11-30', 'BLACKFRIDAY'),
(2, 'Cyber Monday', 'Promoção relâmpago eletrônicos', 'percentual', 15.00, '2024-12-02', '2024-12-02', 'CYBERMONDAY'),
(3, 'Natal 2024', 'Promoção de Natal', 'percentual', 10.00, '2024-12-15', '2024-12-25', 'NATAL2024'),
(4, 'Frete Grátis Premium', 'Frete grátis para clientes premium', 'valor_fixo', 50.00, '2024-11-01', '2024-12-31', 'FRETEGRATIS');

-- Inserir Produtos em Promoção
INSERT INTO produtos_promocao (id, promocao_id, produto_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 2, 1),
(6, 2, 15),
(7, 2, 6),
(8, 3, 7),
(9, 3, 8),
(10, 3, 9),
(11, 3, 10);