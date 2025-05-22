"""2) Em uma eleição presidencial existem 3 candidatos. 
Os votos são informados através de códigos. Os dados utilizados 
para a contagem dos votos obedecem à seguinte codificação:
1 - Eymael
2 - Levy Fidelix
3 - Cabo Daciolo
4 – Voto nulo
5 – Voto em branco
Elabore um programa que leia o código de cada voto, calcule e escreva:
total e o % de votos para cada candidato;
total e o % de votos nulos;
total e o % de votos em branco;
Como finalizador da votação, tem-se o valor 0."""

# Inicia contadores dos votos
eymael = 0
levy_fidelix = 0
cabo_daciolo = 0
voto_nulo = 0
voto_em_branco = 0 

# Loop para a recebe input dos votos, se digitar 0 finaliza a votação e mostra o resultado.
while True:
  print("\n++++++++++    ELEIÇÃO PRESIDENCIAL 2026 - FAZ O L     ++++++++++\n")
  print("+++++++++++++++++      ELEITORES 2025      ++++++++++++++++")
  print("[1]Eymael - [2]Levy Fidelix - [3]Cabo Daciolo")
  print("[4]Voto Nulo - [5]Voto em Branco")
  print("Digite [0] para finalizar a votação.\n")
  voto = int(input("Digite o codigo do voto: ")) # Variavelque recebe input dos votos

  # Condicinal que verifica o codigo dos votos e atribui a cada eleitor. Vale para votos brancos e nulos.
  if voto == 0:
    break # Finaliza a votação
  elif voto == 1:
    eymael += 1
  elif voto == 2:
    levy_fidelix += 1
  elif voto == 3:
    cabo_daciolo += 1
  elif voto == 4:
    voto_nulo += 1
  elif voto == 5:
    voto_em_branco += 1
  else:
    print("Código invalido. Use números de [1 a 5] ou 0 Para Finalizar.\n")

total = (eymael + levy_fidelix + cabo_daciolo + voto_nulo + voto_em_branco) # Computa o total de votos

# Condicional que calcula o percentual de votos e atribui a cada eleitor, votos brancos e nulo.
if total == 0:
  perc_eymael = perc_levy = perc_cabo = perc_nulo = perc_branco = 0.0
else:
  perc_eymael = (eymael / total) * 100
  perc_levy = (levy_fidelix / total) * 100
  perc_cabo = (cabo_daciolo / total) * 100
  perc_nulo = (voto_nulo / total) * 100
  perc_branco = (voto_em_branco / total) * 100

# Resultado da votação
print("\n---  RESULTADOS   ---\n")
print(f"Eymael: {eymael} votos ({perc_eymael:.2f}%)")
print(f"Levy Fidelix: {levy_fidelix} votos ({perc_levy:.2f}%)")
print(f"Cabo Daciolo: {cabo_daciolo} votos ({perc_cabo:.2f}%)")
print(f"Votos nulos: {voto_nulo} votos ({perc_nulo:.2f}%)")
print(f"Votos em branco: {voto_em_branco} votos ({perc_branco:.2f}%)")





