import time
import sys

def texto_piscando(texto, repeticoes=5, intervalo=0.5):
    for _ in range(repeticoes):
        # Mostra o texto
        sys.stdout.write("\r" + texto)
        sys.stdout.flush()
        time.sleep(intervalo)
        
        # "Apaga" o texto (substitui por espaços)
        sys.stdout.write("\r" + " " * len(texto))
        sys.stdout.flush()
        time.sleep(intervalo)
    
    sys.stdout.write("\r" + texto + "\n")  # Mantém o texto visível no final

# Exemplo de uso:
texto_piscando("ALERTA: ESTOQUE BAIXO!", repeticoes=3, intervalo=0.3)