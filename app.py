import mysql.connector
from datetime import datetime
from mysql.connector import Error

class SistemaEstoqueFarmacia:
    def __init__(self):
        try:
            # Configuração da conexão com o MySQL
            self.conexao = mysql.connector.connect(
                host='localhost',
                user='root',  # Substitua pelo seu usuário MySQL
                password='Alpine@187',  # Substitua pela sua senha MySQL
                database='estoque_farmacia'  # O banco deve existir previamente
            )
            
            # Verifica se a conexão foi estabelecida
            if self.conexao.is_connected():
                print("Conexão ao MySQL estabelecida com sucesso!")
                self.criar_tabelas()
                
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise

    def criar_tabelas(self):
        cursor = self.conexao.cursor()
        
        try:
            # Tabela de produtos (MySQL usa AUTO_INCREMENT em vez de AUTOINCREMENT)
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                principio_ativo VARCHAR(100) NOT NULL,
                lote VARCHAR(50) NOT NULL,
                quantidade INT NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                data_validade DATE NOT NULL,
                fabricante VARCHAR(100) NOT NULL,
                categoria VARCHAR(50) NOT NULL
            )
            ''')
            
            # Tabela de movimentações
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INT PRIMARY KEY AUTO_INCREMENT,
                produto_id INT NOT NULL,
                tipo ENUM('entrada', 'saida') NOT NULL,
                quantidade INT NOT NULL,
                data DATETIME NOT NULL,
                responsavel VARCHAR(100),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
            ''')
            
            self.conexao.commit()
            print("Tabelas criadas/verificadas com sucesso!")
            
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
            raise
    
    def cadastrar_produto(self):
        print("\n--- Cadastro de Produto ---")
        nome = input("Nome do produto: ")
        principio_ativo = input("Princípio ativo: ")
        lote = input("Número do lote: ")
        quantidade = int(input("Quantidade: "))
        preco = float(input("Preço unitário: "))
        data_validade = input("Data de validade (AAAA-MM-DD): ")
        fabricante = input("Fabricante: ")
        categoria = input("Categoria (ex: analgésico, antibiótico): ")
        
        cursor = self.conexao.cursor()
        
        try:
            # Inserir produto
            cursor.execute('''
            INSERT INTO produtos (nome, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (nome, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria))
            
            # Obter o ID do último registro inserido
            produto_id = cursor.lastrowid
            
            # Registrar a entrada no estoque
            cursor.execute('''
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, responsavel)
            VALUES (%s, %s, %s, %s, %s)
            ''', (produto_id, 'entrada', quantidade, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Sistema'))
            
            self.conexao.commit()
            print("Produto cadastrado com sucesso!")
            
        except Error as e:
            self.conexao.rollback()
            print(f"Erro ao cadastrar produto: {e}")
    
    def listar_produtos(self):
        print("\n--- Lista de Produtos ---")
        cursor = self.conexao.cursor(dictionary=True)  # Retorna resultados como dicionários
        
        try:
            cursor.execute('''
            SELECT id, nome, principio_ativo, quantidade, preco, data_validade 
            FROM produtos
            ''')
            
            produtos = cursor.fetchall()
            
            if not produtos:
                print("Nenhum produto cadastrado.")
                return
            
            for produto in produtos:
                print(f"ID: {produto['id']} | Nome: {produto['nome']} | Princípio Ativo: {produto['principio_ativo']} | "
                      f"Quantidade: {produto['quantidade']} | Preço: R${produto['preco']:.2f} | "
                      f"Validade: {produto['data_validade']}")
                
        except Error as e:
            print(f"Erro ao listar produtos: {e}")
    
    def registrar_saida(self):
        self.listar_produtos()
        produto_id = int(input("\nID do produto para saída: "))
        quantidade = int(input("Quantidade a retirar: "))
        responsavel = input("Responsável pela retirada: ")
        
        cursor = self.conexao.cursor()
        
        try:
            # Verificar estoque (usando FOR UPDATE para lockar o registro)
            cursor.execute('''
            SELECT quantidade FROM produtos WHERE id = %s FOR UPDATE
            ''', (produto_id,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                print("Produto não encontrado!")
                return
            
            estoque_atual = resultado[0]
            
            if quantidade > estoque_atual:
                print(f"Estoque insuficiente! Disponível: {estoque_atual}")
                return
            
            # Atualizar estoque
            novo_estoque = estoque_atual - quantidade
            cursor.execute('''
            UPDATE produtos SET quantidade = %s WHERE id = %s
            ''', (novo_estoque, produto_id))
            
            # Registrar saída
            cursor.execute('''
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, responsavel)
            VALUES (%s, %s, %s, %s, %s)
            ''', (produto_id, 'saida', quantidade, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), responsavel))
            
            self.conexao.commit()
            print("Saída registrada com sucesso!")
            
        except Error as e:
            self.conexao.rollback()
            print(f"Erro ao registrar saída: {e}")
    
    def verificar_validade(self):
        print("\n--- Produtos Próximos da Validade ---")
        data_atual = datetime.now().strftime('%Y-%m-%d')
        
        cursor = self.conexao.cursor(dictionary=True)
        
        try:
            # MySQL usa DATE_ADD em vez da função date do SQLite
            cursor.execute('''
            SELECT id, nome, data_validade, quantidade 
            FROM produtos 
            WHERE data_validade BETWEEN %s AND DATE_ADD(%s, INTERVAL 30 DAY)
            ORDER BY data_validade
            ''', (data_atual, data_atual))
            
            produtos = cursor.fetchall()
            
            if not produtos:
                print("Nenhum produto próximo da validade (próximos 30 dias).")
                return
            
            for produto in produtos:
                print(f"ID: {produto['id']} | Nome: {produto['nome']} | "
                      f"Validade: {produto['data_validade']} | Quantidade: {produto['quantidade']}")
                
        except Error as e:
            print(f"Erro ao verificar validade: {e}")
    
    def menu(self):
        while True:
            print("\n=== Sistema de Gerenciamento de Estoque - Farmácia ===")
            print("1. Cadastrar novo produto")
            print("2. Listar produtos")
            print("3. Registrar saída de produto")
            print("4. Verificar produtos próximos da validade")
            print("5. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.cadastrar_produto()
            elif opcao == '2':
                self.listar_produtos()
            elif opcao == '3':
                self.registrar_saida()
            elif opcao == '4':
                self.verificar_validade()
            elif opcao == '5':
                print("Saindo do sistema...")
                if self.conexao.is_connected():
                    self.conexao.close()
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    sistema = SistemaEstoqueFarmacia()
    sistema.menu()