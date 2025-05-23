CREATE DATABASE estoque_farmacia;

USE estoque_farmacia;

CREATE TABLE IF NOT EXISTS produtos (
produto_id INT PRIMARY KEY AUTO_INCREMENT,
nome_produto VARCHAR (150) NOT NULL,
principio_ativo VARCHAR (100) NOT NULL,
lote VARCHAR (50) NOT NULL,
quantidade INT NOT NULL,
preco DECIMAL (10,2) NOT NULL,
data_validade DATE NOT NULL,
fabricante VARCHAR (100) NOT NULL,
categoria VARCHAR (100) NOT NULL
);

/* Insere produtos farmacêuticos  */
INSERT INTO produtos (nome_produto, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria) VALUES
('Dipirona 500mg', 'Dipirona Sódica', 'LOT20230101', 150, 8.90, '2025-05-30', 'EMS', 'Analgésico'),
('Tylenol 750mg', 'Paracetamol', 'LOT20230215', 200, 15.50, '2025-12-11', 'Johnson & Johnson', 'Analgésico'),
('Amoxicilina 500mg', 'Amoxicilina Triidratada', 'LOT20230410', 90, 28.90, '2025-11-30', 'Novartis', 'Antibiótico'),
('Azitromicina 500mg', 'Azitromicina Diidratada', 'LOT20230505', 75, 45.00, '2025-06-20', 'Pfizer', 'Antibiótico'),
('Losartana 50mg', 'Losartana Potássica', 'LOT20230618', 120, 22.30, '2026-05-15', 'Aché', 'Anti-hipertensivo'),
('Atenolol 25mg', 'Atenolol', 'LOT20230722', 110, 18.75, '2025-09-30', 'Sanofi', 'Anti-hipertensivo'),
('Metformina 850mg', 'Cloridrato de Metformina', 'LOT20230830', 95, 14.90, '2025-07-12', 'Medley', 'Diabetes'),
('Sabonete Líquido Antibacteriano', 'Triclosan', 'LOT20231120', 45, 9.80, '2025-08-15', 'Johnson & Johnson', 'Higiene'),
('Vacina Influenza 2023', 'Vírus Influenza Inativado', 'LOT20231201', 30, 89.90, '2025-06-20', 'Butantan', 'Vacina'),
('Insulina NPH 100UI/ml', 'Insulina Humana', 'LOT20240115', 25, 120.00, '2026-06-15', 'Novo Nordisk', 'Diabetes');


CREATE TABLE IF NOT EXISTS movimentacoes (
movimentacoes_id INT PRIMARY KEY AUTO_INCREMENT,
produto_fk INT,
tipo VARCHAR (100) NOT NULL,
quantidade INT NOT NULL,
data DATE NOT NULL,
responsavel VARCHAR (100),
observacao VARCHAR (200)
);

/* Insere movimentações produtos   */
INSERT INTO movimentacoes (produto_fk, tipo, quantidade, data, responsavel) VALUES
(1, 'Entrada', 100, '2024-03-15', 'João Silva Pereira'),
(2, 'Saída', 50, '2024-03-16', 'Maria Oliveira Santos'),
(3, 'Ajuste de Estoque', 30, '2024-03-17', 'Carlos Eduardo Souza'),
(5, 'Entrada', 200, '2024-03-18', 'Ana Clara Fernandes'),
(7, 'Saída', 75, '2024-03-19', 'Pedro Henrique Alves'),
(4, 'Devolução', 25, '2024-03-20', 'Juliana Costa Lima'),
(9, 'Entrada', 150, '2024-03-21', 'Lucas Martins Rocha'),
(6, 'Saída', 90, '2024-03-22', 'Fernanda Gomes Castro'),
(8, 'Transferência', 60, '2024-03-23', 'Rafael Pereira Nunes'),
(10, 'Ajuste de Estoque', 10, '2024-03-24', 'Amanda Ribeiro Teixeira');

CREATE TABLE IF NOT EXISTS usuarios (
usuario_id INT PRIMARY KEY AUTO_INCREMENT,
nome_usuario VARCHAR(150) NOT NULL,
cpf VARCHAR(14) NOT NULL UNIQUE,
email VARCHAR(50) NOT NULL UNIQUE,
username VARCHAR(20) NOT NULL UNIQUE,
senha VARCHAR(100) NOT NULL
);

/* Insere Usuários  */
INSERT INTO usuarios (nome_usuario, cpf, email, username, senha) VALUES
('João Silva Pereira', '123.456.789-09', 'joao.silva@gmail.com', 'joaosilva', '123456'),
('Maria Oliveira Santos', '987.654.321-00', 'maria.oliveira@bol.com.br', 'maria_oliveira', '123456'),
('Carlos Eduardo Souza', '456.789.123-45', 'carlos.souza@uol.com.br', 'carlosedu', '123456'),
('Ana Clara Fernandes', '321.654.987-32', 'ana.fernandes@uol.com.br', 'anafernandes', '123456'),
('Pedro Henrique Alves', '159.753.486-25', 'pedro.alves@live.com', 'pedroalves', '123456'),
('Juliana Costa Lima', '753.951.852-96', 'juliana.lima@uol.com.br', 'julianacosta', '123456'),
('Lucas Martins Rocha', '258.369.147-36', 'lucas.rocha@live.com', 'lucasmartins', '123456'),
('Fernanda Gomes Castro', '654.321.987-01', 'fernanda.castro@hotmail.com', 'fgcastro', '123456'),
('Rafael Pereira Nunes', '951.623.487-12', 'rafael.nunes@hotmail.com', 'rafanunes', '123456'),
('Amanda Ribeiro Teixeira', '357.159.486-73', 'amanda.teixeira@gmail.com', 'amandaribeiro', '123456');

ALTER TABLE movimentacoes ADD CONSTRAINT fk_movimentacoes_prod
FOREIGN KEY (produto_fk)
REFERENCES produtos (produto_id)
ON DELETE RESTRICT;

ALTER TABLE movimentacoes ADD CONSTRAINT fk_movimentacoes_usu
FOREIGN KEY (produto_fk)
REFERENCES usuarios (usuario_id)
ON DELETE RESTRICT;



