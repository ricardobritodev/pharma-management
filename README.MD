# Pharma Management System

Este projeto é um sistema de gerenciamento farmacêutico desenvolvido em Python com integração a banco de dados MySQL.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
- Python 3.x
- MySQL Connector
- bcrypt
- MySQL Workbench ou outra ferramenta para gerenciamento de bancos MySQL

## Configuração do Ambiente

1. **Criar ambiente virtual Python**:
   No Windows:
   python -m venv pharmaEnv

   Ativar Enviroment

   No Windows:
   pharmaEnv\Scripts\activate

   No Linux/MacOS:
   source pharmaEnv/bin/activate


Configuração do Banco de Dados

    Criar o banco de dados executando script db.sql no seu MySQL Workbench ou cliente MySQL preferido.

    Configurar as credenciais de acesso ao banco de dados no arquivo settings.py:

DB_CONFIG = {
    'host': 'localhost',
    'user': 'seu_usuario',  # Alterar para seu usuário MySQL
    'password': 'sua_senha',  # Alterar para sua senha MySQL
    'database': 'nome_do_banco'  # Nome do banco criado
}

Executando a Aplicação

Após configurar o ambiente e o banco de dados, execute:
  python main.py


Estrutura do Projeto

    main.py: Arquivo principal da aplicação

    db.sql: Script SQL para criação do banco de dados

    settings.py: Configurações do sistema (incluindo conexão com o banco)