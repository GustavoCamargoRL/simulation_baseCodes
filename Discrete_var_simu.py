#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 01

#geracao de variaveis aleatorias discretas com diferentes probabilidades

from random import *

#criação dos dados iniciais de tempo de vida do rolamento em horas e sua respectiva probabilidade
prob_vida = [[1000,0.1],[1100,0.13],[1200,0.25],[1300,0.13],[1400,0.09],[1500,0.12],[1600,0.02],[1700,0.06],[1800,0.05],[1900,0.05]]
#contagem dos eventos simulados
simulado = [[1000,0],[1100,0],[1200,0],[1300,0],[1400,0],[1500,0],[1600,0],[1700,0],[1800,0],[1900,0]]
#inicialização da lista de probabilidades simuladas
prob_simu = simulado
N = 1000000
# simulação em N eventos
for i in range(N):
    #geração da semente aleatoria entre 0 <= U <= 1
    U = random()
    if(U < 0.25):
        simulado[2][1] = simulado[2][1] + 1
    elif(U < 0.38):
        simulado[1][1] = simulado[1][1] + 1
    elif(U < 0.51):
        simulado[3][1] = simulado[3][1] + 1
    elif(U < 0.63):
        simulado[5][1] = simulado[5][1] + 1
    elif(U < 0.73):
        simulado[0][1] = simulado[0][1] + 1
    elif(U < 0.82):
        simulado[4][1] = simulado[4][1] + 1
    elif(U < 0.88):
        simulado[7][1] = simulado[7][1] + 1
    elif(U < 0.93):
        simulado[8][1] = simulado[8][1] + 1
    elif(U < 0.98):
        simulado[9][1] = simulado[9][1] + 1
    else:
        simulado[6][1] = simulado[6][1] + 1

#calculo das probabilidades simuladas
for i in range(10):
    prob_simu[i][1] = simulado[i][1]/N

#calculo da media simulada e teorica
media_simu = 0
media_teo = 0
for i in range(10):
    media_simu = media_simu + simulado[i][0]*simulado[i][1]
    media_teo = media_teo + prob_vida[i][0]*prob_vida[i][1]



print("Media teorica: ", media_teo)
print("Media simulada: ", media_simu)




