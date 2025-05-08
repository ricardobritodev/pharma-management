from settings import conectar_banco # Importa a função de conexão com o banco do arquivo settings.py
from delete import deletar_produto # Impora função de deletar produto.

from datetime import datetime  # Importa o módulo para trabalhar com datas e horários.
import bcrypt # Biblipteca que transforma a senha comum em HASH para motivos de segurança.

# Menu principal que exibe as opções para o usuário
def menu_produtos():
    while True:
        print("\n=== Sistema de Farmácia ===")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Registrar saída")
        print("4. Verificar validade")
        print("5. Deletar produto")  
        print("6. Sair")  

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            listar_produtos()
        elif opcao == '3':
            registrar_saida()
        elif opcao == '4':
            verificar_validade()
        elif opcao == '5':  
            deletar_produto()
        elif opcao == '6':  
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

# Função para login
def login_usuario():
    conexao = conectar_banco()  # Cria conexão com o banco
    cursor = conexao.cursor()   # Cria o cursor
    username = input("Nome de usuário: ")
    senha = input("Senha: ")

    cursor.execute("SELECT senha FROM usuarios WHERE username = %s", (username,))
    resultado = cursor.fetchone()

    if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[0].encode('utf-8')):
        print("Login bem-sucedido! Bem-vindo,", username)
        menu_produtos()
    else:
        print("Nome de usuário ou senha inválidos.")

    cursor.close()
    conexao.close()


# Função para cadastrar usuário
def cadastrar_usuario():
    nome = input("Nome completo: ")
    cpf = input("CPF (somente números): ")
    email = input("Email: ")
    username = input("Nome de usuário: ")
    senha = input("Senha: ")
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    conexao = conectar_banco()
    cursor = conexao.cursor() 

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, cpf, email, username, senha)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cpf, email, username, senha_hash))
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao cadastrar:", err)
    finally:
        cursor.close()
        conexao.close()

# Função para cadastrar um novo produto no banco de dados
def cadastrar_produto():
    print("\n--- Cadastro de Produto ---")
    
    # Coleta os dados do usuário
    nome = input("Nome do produto: ")
    principio_ativo = input("Princípio ativo: ")
    lote = input("Número do lote: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço unitário: "))
    data_validade = input("Data de validade (AAAA-MM-DD): ")
    fabricante = input("Fabricante: ")
    categoria = input("Categoria: ")

    # Conecta ao banco
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()

        # Insere o novo produto na tabela 'produtos'
        cursor.execute('''
            INSERT INTO produtos 
            (nome, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nome, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria))
        
        produto_id = cursor.lastrowid  # Recupera o ID do produto recém-inserido

        # Registra o movimento de entrada do produto
        cursor.execute('''
            INSERT INTO movimentacoes 
            (produto_id, tipo, quantidade, data, responsavel)
            VALUES (%s, %s, %s, %s, %s)
        ''', (produto_id, 'entrada', quantidade, datetime.now(), 'Sistema'))

        conexao.commit()  # Salva as alterações no banco
        conexao.close()   # Fecha a conexão com o banco

        print("Produto cadastrado com sucesso!")

# Lista todos os produtos cadastrados
def listar_produtos():
    print("\n--- Lista de Produtos ---")
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor(dictionary=True)  # Usa dicionário para acessar colunas por nome
        cursor.execute('SELECT * FROM produtos')  # Busca todos os produtos
        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto cadastrado.")
        else:
            for produto in produtos:
                print(f"ID: {produto['id']} | Nome: {produto['nome']} | Quantidade: {produto['quantidade']}")
        
        conexao.close()

# Registra a saída de um produto do estoque
def registrar_saida():
    listar_produtos()  # Mostra produtos disponíveis
    produto_id = int(input("\nID do produto para saída: "))
    quantidade = int(input("Quantidade a retirar: "))
    responsavel = input("Responsável pela retirada: ")

    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()

        # Verifica o estoque atual do produto
        cursor.execute('SELECT quantidade FROM produtos WHERE id = %s', (produto_id,))
        estoque = cursor.fetchone()

        if not estoque:
            print("Produto não encontrado!")
        elif quantidade > estoque[0]:
            print(f"Estoque insuficiente! Disponível: {estoque[0]}")
        else:
            novo_estoque = estoque[0] - quantidade

            # Atualiza o valor da quantidade
            cursor.execute('UPDATE produtos SET quantidade = %s WHERE id = %s', (novo_estoque, produto_id))

            # Registra a movimentação de saída
            cursor.execute('''
                INSERT INTO movimentacoes 
                (produto_id, tipo, quantidade, data, responsavel)
                VALUES (%s, %s, %s, %s, %s)
            ''', (produto_id, 'saida', quantidade, datetime.now(), responsavel))

            conexao.commit()
            print("Saída registrada com sucesso!")

        conexao.close()

# Verifica produtos com validade próxima (em até 30 dias)
def verificar_validade():
    print("\n--- Produtos Próximos da Validade ---")
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM produtos
            WHERE data_validade BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            ORDER BY data_validade
        ''')
        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto próximo da validade.")
        else:
            for produto in produtos:
                print(f"ID: {produto['id']} | Nome: {produto['nome']} | Validade: {produto['data_validade']}")
        
        conexao.close()

# Menu Cadastro/login
def menu():
    while True:
        print("\n1. Cadastrar usuário")
        print("2. Login")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login_usuario()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")


# Ponto de entrada principal do programa
if __name__ == "__main__":
    menu()