CREATE DATABASE estoque_farmacia;

USE estoque_farmacia;

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome TEXT NOT NULL,
    principio_ativo TEXT NOT NULL,
    lote TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    data_validade TEXT NOT NULL,
    fabricante TEXT NOT NULL,
    categoria TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    produto_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,  -- 'entrada' ou 'saida'
    quantidade INTEGER NOT NULL,
    data TEXT NOT NULL,
    responsavel TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);