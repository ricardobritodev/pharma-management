from settings import conectar_banco
from mysql.connector import Error  # Importe isso se ainda não estiver importado

def deletar_produto():
    """Deleta um produto do banco de dados"""
    print("\n--- Deletar Produto ---")
    
    conexao = None
    try:
        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor(dictionary=True)
            
            # Listagem básica de produtos
            cursor.execute('SELECT id, nome FROM produtos')
            produtos = cursor.fetchall()
            
            if not produtos:
                print("Nenhum produto cadastrado.")
                return
                
            print("\nProdutos disponíveis:")
            for produto in produtos:
                print(f"ID: {produto['id']} | Nome: {produto['nome']}")
            
            produto_id = int(input("\nID do produto a ser deletado: "))
            confirmacao = input(f"Tem certeza que deseja deletar o produto ID {produto_id}? (s/n): ").lower()

            if confirmacao != 's':
                print("Operação cancelada.")
                return
                
            # Só executa as deleções SE o usuário confirmar
            try:
                # 1. Primeiro deleta as movimentações
                cursor.execute('DELETE FROM movimentacoes WHERE produto_id = %s', (produto_id,))
                # 2. Depois deleta o produto
                cursor.execute('DELETE FROM produtos WHERE id = %s', (produto_id,))
                conexao.commit()
                
                if cursor.rowcount > 0:
                    print(f"Produto ID {produto_id} deletado com sucesso!")
                else:
                    print("Nenhum produto foi deletado.")
                    
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