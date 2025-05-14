from rich.console import Console
from rich.table import Table
from backend import *
from settings import conectar_banco

console = Console()

def listar_produtos():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produtos')
    
    table = Table(title="Estoque de Medicamentos")
    table.add_column("ID", style="cyan")
    table.add_column("Nome", style="magenta")
    table.add_column("Quantidade", justify="right")
    
    for produto in cursor.fetchall():
        table.add_row(
            str(produto['produto_id']),
            produto['nome_produto'],
            str(produto['quantidade'])
        )
    
    console.print(table)

listar_produtos()
