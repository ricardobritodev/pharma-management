from datetime import datetime  # Importa o módulo para trabalhar com datas e horários.
from settings import conectar_banco # Importa a função de conexão com o banco do arquivo settings.py
import re #Regex
import bcrypt # Biblipteca que transforma a senha comum em HASH para motivos de segurança.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                           Menu principal que exibe as opções para o usuário                                       #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def menu_produtos():
    while True:
        print("\n=== Sistema de Farmácia ===")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Registrar saída")
        print("4. Verificar validade")
        print("5. Deletar produto")  
        print("6. Editar produto") 
        print("7. Sair")  

        opcao = input("Escolha uma opção: >> ")

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
            editar_produto()
        elif opcao == '7':  
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                         Função Para Login do Usuário                                              #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def login_usuario():
    print("\n--- Login de Usuário ---")
    conexao = conectar_banco()  # Cria conexão com o banco
    cursor = conexao.cursor()   # Cria o cursor
    username = input("Nome de usuário: >> ").strip().lower()
    senha = input("Senha: >> ").strip()

    cursor.execute("SELECT senha FROM usuarios WHERE username = %s", (username,))
    resultado = cursor.fetchone()

    if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[0].encode('utf-8')):
        print("Login bem-sucedido! Bem-vindo,", username)
        menu_produtos()
    else:
        print("Nome de usuário ou senha inválidos.")

    cursor.close()
    conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                         Função Para Validar Email                                           #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' 
    return re.match(padrao, email) is not None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                         Função para cadastrar usuário                                             #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")

    while True:
        nome = input("Nome completo: >> ").strip().upper()
        if nome:
            break
        print("Nome não pode ser vazio. Tente novamente.")

    cpf = input("CPF (somente números): >> ")

    while True:
        email = input("Email: >> ").strip().lower()
        if validar_email(email):
            break
        print("Email Invalido. Tente novamente.")

    while True:
        username = input("Nome de usuário: >> ").strip().lower()
        if len(username) >= 4:
            break
        print("Username deve ter pelo menos 4 caracteres.")

    while True:
        senha = input("Senha: >> ").strip()
        if len(senha) >= 6:
            break
        print("Senha deve ter pelo menos 6 caracteres.")

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    conexao = conectar_banco()
    cursor = conexao.cursor() 

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome_usuario, cpf, email, username, senha)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cpf, email, username, senha_hash))
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao cadastrar:", err)
    finally:
        cursor.close()
        conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                         Validador de input de Data                                                #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def validar_data(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        if data < datetime.now().date():
            print("Erro: Data não pode ser anterior à data atual!")
            return False
        return True
    except ValueError:
        print("Erro: Formato inválido! Use AAAA-MM-DD")
        return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                Função para cadastrar um novo produto no banco de dados                            #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def cadastrar_produto():
    print("\n--- Cadastro de Produto ---")
    
    # Coleta os dados do usuário
    nome = input("Nome do produto: >> ").upper()
    principio_ativo = input("Princípio ativo: >> ").upper()
    lote = input("Número do lote: >> ").upper()
    
    # Validação numérica segura
    while True:
        try:
            quantidade = int(input("Quantidade: >> "))
            if quantidade > 0:
                break
            print("Valor negativo. Digite novamente.")
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
    
    while True:
        try:
            preco = float(input("Preço unitário: >> "))
            if preco > 0:
                break
            print("Valor negativo. Digite novamente.")
        except ValueError:
            print("Erro: Digite um valor numérico válido!")
     
    fabricante = input("Fabricante: >> ").upper()
    categoria = input("Categoria: >> ").upper()

     # Validação de data com loop
    while True:
        data_validade = input("Data de validade (AAAA-MM-DD): >> ").strip()
        if validar_data(data_validade):
            break

    # Conecta ao banco
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()

        try:
            cursor.execute('''
                INSERT INTO produtos 
                (nome_produto, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (nome, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria))
            
            produto_id = cursor.lastrowid

            cursor.execute('''
                INSERT INTO movimentacoes 
                (produto_fk, tipo, quantidade, data, responsavel)
                VALUES (%s, %s, %s, %s, %s)
            ''', (produto_id, 'entrada', quantidade, datetime.now(), 'Sistema'))

            conexao.commit()
            print("Produto cadastrado com sucesso!")

        except mysql.connector.Error as err:
            print(f"Erro no banco: {err}")
            conexao.rollback()
            
        finally:
            conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                Função para Listar todos os produtos cadastrados                                   #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
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
                print(f"ID: {produto['produto_id']} | Nome: {produto['nome_produto']} | Quantidade: {produto['quantidade']}")
        
        conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                               Função para Registrar a saída de um produto do estoque                              #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def registrar_saida():
    print("\n--- Registro de Saída de Produto ---")
    listar_produtos()  

    while True:
        try:
            produto_id = int(input("\nID do produto para saída: >> "))
            if produto_id > 0:
                break
            print("Valor negativo. Digite novamente.")
        except ValueError:
            print("Erro: Digite um valor numérico válido!")

    while True:
        try:
            quantidade = int(input("Quantidade a retirar: >> "))
            if quantidade > 0:
                break
            print("Valor negativo. Digite novamente.")
        except ValueError:
            print("Erro: Digite um valor numérico válido!")


    responsavel = input('Responsável pela retirada: >> ').upper()

    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()

        # Verifica o estoque atual do produto
        cursor.execute('SELECT quantidade FROM produtos WHERE produto_id = %s', (produto_id,))
        estoque = cursor.fetchone()

        if not estoque:
            print("Produto não encontrado!")
        elif quantidade > estoque[0]:
            print(f"Estoque insuficiente! Disponível: {estoque[0]}")
        else:
            novo_estoque = estoque[0] - quantidade

            # Atualiza o valor da quantidade
            cursor.execute('UPDATE produtos SET quantidade = %s WHERE produto_id = %s', (novo_estoque, produto_id))

            # Registra a movimentação de saída
            cursor.execute('''
                INSERT INTO movimentacoes 
                (produto_fk, tipo, quantidade, data, responsavel)
                VALUES (%s, %s, %s, %s, %s)
            ''', (produto_id, 'saida', quantidade, datetime.now(), responsavel))

            conexao.commit()
            print("Saída registrada com sucesso!")

        conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                 Função para Verificar validade dos produtos                                       #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def verificar_validade():
    print("\n--- Produtos Próximos da Validade ---")
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM produtos
            WHERE data_validade BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 45 DAY)
            ORDER BY data_validade
        ''')
        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto próximo da validade.")
        else:
            for produto in produtos:
                print(f"ID: {produto['produto_id']} | Nome: {produto['nome_produto']} | Validade: {produto['data_validade']}")
        
        conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                               Função para editar as propriedades de um produto do estoque                         #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def editar_produto():
    print("\n--- Edição de Produto ---")
    listar_produtos()  # Mostra a lista de produtos disponíveis
    
    produto_id = input("Digite o ID do produto que deseja editar (ou 0 para cancelar): >> ")
    
    if produto_id == '0':
        return
    
    try:
        produto_id = int(produto_id)
    except ValueError:
        print("ID inválido! Deve ser um número.")
        return
    
    conexao = conectar_banco()
    if not conexao:
        print("Erro ao conectar ao banco de dados")
        return
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        # Primeiro busca o produto atual
        cursor.execute('SELECT * FROM produtos WHERE produto_id = %s', (produto_id,))
        produto = cursor.fetchone()
        
        if not produto:
            print("Produto não encontrado!")
            return
        
        print("\nDeixe em branco para manter o valor atual")
        print(f"Valor atual: {produto['nome_produto']}")
        novo_nome = input("Novo nome do produto: >> ") or produto['nome_produto']
        
        print(f"\nValor atual: {produto['principio_ativo']}")
        novo_principio = input("Novo princípio ativo: >> ") or produto['principio_ativo']
        
        print(f"\nValor atual: {produto['lote']}")
        novo_lote = input("Novo número do lote: >> ") or produto['lote']
        
        print(f"\nValor atual: {produto['quantidade']}")
        try:
            nova_quantidade = int(input("Nova quantidade: >> ") or produto['quantidade'])
        except ValueError:
            print("Quantidade deve ser um número! Mantendo valor atual.")
            nova_quantidade = produto['quantidade']
        
        print(f"\nValor atual: {produto['preco']}")
        try:
            novo_preco = float(input("Novo preço unitário: >> ") or produto['preco'])
        except ValueError:
            print("Preço deve ser um número! Mantendo valor atual.")
            novo_preco = produto['preco']
        
        print(f"\nValor atual: {produto['data_validade']}")
        nova_validade = input("Nova data de validade (AAAA-MM-DD): >> ") or produto['data_validade']
        
        print(f"\nValor atual: {produto['fabricante']}")
        novo_fabricante = input("Novo fabricante: >> ") or produto['fabricante']
        
        print(f"\nValor atual: {produto['categoria']}")
        nova_categoria = input("Nova categoria: >> ") or produto['categoria']
        
        # Atualiza o produto no banco de dados
        cursor.execute('''
            UPDATE produtos SET
                nome_produto = %s,
                principio_ativo = %s,
                lote = %s,
                quantidade = %s,
                preco = %s,
                data_validade = %s,
                fabricante = %s,
                categoria = %s
            WHERE produto_id = %s
        ''', (
            novo_nome, novo_principio, novo_lote, nova_quantidade,
            novo_preco, nova_validade, novo_fabricante, nova_categoria,
            produto_id
        ))
        
        # Registra a movimentação de edição
        cursor.execute('''
            INSERT INTO movimentacoes 
            (produto_fk, tipo, quantidade, data, responsavel, observacao)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            produto_id, 'edicao', nova_quantidade, 
            datetime.now(), 'Sistema', 'Edição de produto'
        ))
        
        conexao.commit()
        print("\nProduto atualizado com sucesso!")
        
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar produto: {err}")
        conexao.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                       Função para menu de cadastro e login                                        #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def menu():
    while True:
        print("\n1. Login")
        print("2. Cadastrar usuário")
        print("3. Sair")
        opcao = input("Escolha uma opção: >> ")

        if opcao == "1":
            login_usuario()
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            print("Finalizando Programa")
            break
        else:
            print("Opção inválida.")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                           Função para deletar um produto                                          #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def deletar_produto():
    """Deleta um produto do banco de dados"""
    print("\n--- Deletar Produto ---")
    
    conexao = None
    try:
        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor(dictionary=True)
            
            # Listagem básica de produtos
            cursor.execute('SELECT produto_id, nome_produto FROM produtos')
            produtos = cursor.fetchall()
            
            if not produtos:
                print("Nenhum produto cadastrado.")
                return
                
            print("\nProdutos disponíveis:")
            for produto in produtos:
                print(f"ID: {produto['produto_id']} | Nome: {produto['nome_produto']}")
            
            while True:
                try:
                    produto_id = int(input("\nID do produto a ser deletado: >> "))
                    if produto_id > 0:
                        break
                    print("Valor negativo. Digite novamente.")
                except ValueError:
                    print("Erro: Digite um valor numérico válido!")

            while True:
                try:
                    confirmacao = input(f"Tem certeza que deseja deletar o produto ID {produto_id}? (s/n): >> ").lower()
                    if confirmacao == 's':
                        # 1. Primeiro deleta as movimentações
                        cursor.execute('DELETE FROM movimentacoes WHERE produto_fk = %s', (produto_id,))
                        # 2. Depois deleta o produto
                        cursor.execute('DELETE FROM produtos WHERE produto_id = %s', (produto_id,))
                        conexao.commit()
                        
                        if cursor.rowcount > 0:
                            print(f"Produto ID {produto_id} deletado com sucesso!")
                            break

                    if confirmacao == 'n':
                        print("Nenhum produto foi deletado.")
                        break
                        
                    else:
                        print(f"Operação Invalida. Tem certeza que deseja deletar o produto ID {produto_id}? (s/n): ")

                except Error as e:
                    print(f"Erro ao deletar: {e}")
                    conexao.rollback()
                     
    except ValueError:
        print("Por favor, digite um ID válido (número inteiro).")
    except Exception as e:
        print(f"Erro ao deletar produto: {e}")
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                       Ponto de entrada principal do programa                                      #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == "__main__":
    menu()


"""
Tasks:
02 - Validador de inputs na função de editar produto
03 - Melhorar interface com Rich
04 - melhora conexao b db com aula mentoria 
"""