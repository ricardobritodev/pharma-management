from datetime import datetime
from settings import conectar_banco
import re
import bcrypt

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt

console = Console()

# ----------------------------
# Menu Principal com Rich
# ----------------------------
def menu_produtos():
    while True:
        console.print(Panel.fit(
            "[bold cyan]Sistema de Farmácia[/]\n"
            "[green]1[/]. Cadastrar produto    [green]2[/]. Listar produtos\n"
            "[green]3[/]. Registrar saída     [green]4[/]. Verificar validade\n"
            "[green]5[/]. Deletar produto      [green]6[/]. Editar produto\n"
            "[green]7[/]. Sair",
            title="[bold yellow]Menu[/]", title_align="left"
        ))

        opcao = Prompt.ask("[bold]Escolha uma opção[/]", choices=[str(n) for n in range(1,8)])
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
        else:
            console.print("[red]Saindo do sistema...[/]")
            break

# ----------------------------
# Exemplo de Listagem com Table
# ----------------------------
def listar_produtos():
    console.print("\n[bold underline]Lista de Produtos[/]\n")
    conexao = conectar_banco()
    if not conexao:
        console.print("[red]Falha ao conectar ao banco![/]")
        return

    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()

    if not produtos:
        console.print("[yellow]Nenhum produto cadastrado.[/]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", justify="right")
    table.add_column("Nome", style="cyan")
    table.add_column("Quantidade", justify="right")
    table.add_column("Validade", style="green")
    table.add_column("Preço (R$)", justify="right")

    for p in produtos:
        table.add_row(
            str(p["produto_id"]),
            p["nome_produto"],
            str(p["quantidade"]),
            p["data_validade"].strftime("%Y-%m-%d"),
            f"{p['preco']:.2f}".replace(".", ",")
        )

    console.print(table)

# ----------------------------
# Exemplo de Cadastro com Prompt
# ----------------------------
def cadastrar_produto():
    console.print(Panel("[bold]Cadastro de Produto[/]", style="blue"))
    nome = Prompt.ask("Nome do produto").upper()
    principio = Prompt.ask("Princípio ativo").upper()
    lote = Prompt.ask("Lote").upper()

    quantidade = IntPrompt.ask("Quantidade", default=1, show_default=True)
    preco = FloatPrompt.ask("Preço unitário (R$)", default=0.0, show_default=True)

    # validação de data
    while True:
        data_str = Prompt.ask("Data de validade (AAAA-MM-DD)")
        try:
            data_val = datetime.strptime(data_str, "%Y-%m-%d").date()
            if data_val < datetime.now().date():
                console.print("[red]Data anterior à de hoje![/]")
                continue
            break
        except ValueError:
            console.print("[red]Formato inválido! Use AAAA-MM-DD[/]")

    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO produtos 
            (nome_produto, principio_ativo, lote, quantidade, preco, data_validade)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (nome, principio, lote, quantidade, preco, data_str))
        conexao.commit()
        console.print("[green]✔ Produto cadastrado com sucesso![/]")
    except Exception as e:
        console.print(f"[red]Erro ao cadastrar: {e}[/]")
    finally:
        conexao.close()

# Você pode replicar o uso de Console.print, Panel, Table, Prompt, IntPrompt e FloatPrompt
# para as funções registrar_saida(), verificar_validade(), editar_produto() e deletar_produto()!

if __name__ == "__main__":
    menu_produtos()
