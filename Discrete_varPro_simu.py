#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 02

#geracao de variaveis discretas aleatorias proporcionais

from random import *

#criação dos dados iniciais de tempo de vida do rolamento em horas e sua respectiva probabilidade
prob_tempo = [[1,1/8],[2,1/8],[3,1/8],[4,1/8],[5,1/8],[6,1/8],[7,1/8],[8,1/8]]
#contagem dos eventos simulados
simulado = [[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0]]
#inicialização da lista de probabilidades simuladas
prob_simu = simulado
N = 1000
# simulação em N eventos
for i in range(N):
    #geração da semente aleatoria entre 0 <= U <= 1
    U = random()
    x = int(8*U) + 1
    simulado[x-1][1] = simulado[x-1][1] + 1

print(simulado)
#calculo das probabilidades simuladas
for i in range(8):
    prob_simu[i][1] = simulado[i][1]/N

#calculo da media simulada e teorica
media_simu = 0
media_teo = 0
for i in range(8):
    media_simu = media_simu + simulado[i][0]*simulado[i][1]
    media_teo = media_teo + prob_tempo[i][0]*prob_tempo[i][1]



print("Media teorica: ", media_teo)
print("Media simulada: ", media_simu)
