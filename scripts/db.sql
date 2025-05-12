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

CREATE TABLE IF NOT EXISTS movimentacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    produto_id INT NOT NULL,
    tipo VARCHAR (100) NOT NULL,
    quantidade INT NOT NULL,
    data DATE NOT NULL,
    responsavel VARCHAR (100),
    observacao VARCHAR (500),
    FOREIGN KEY (produto_id) REFERENCES produtos (produto_id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);