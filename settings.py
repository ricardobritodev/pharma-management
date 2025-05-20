# Importa o módulo necessário para conectar ao MySQL
import mysql.connector
from mysql.connector import Error

# Função que cria a conexão com o banco de dados
def conectar_banco():
    try:
        # Cria uma conexão com o banco usando as credenciais fornecidas
        conexao = mysql.connector.connect(
            host='localhost',          # Endereço do servidor do banco
            user='root',               # Nome do usuário do banco
            password='Alpine@187',     # Senha do usuário
            database='estoque_farmacia' # Nome do banco de dados a ser acessado
        )
        return conexao  # Retorna a conexão se for bem-sucedida

    except mysql.connector.Error as erro:
        # Caso ocorra um erro na conexão, mostra a mensagem
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None  # Retorna None em caso de falha
