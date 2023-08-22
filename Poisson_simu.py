#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 03

#geracao de variavel aleatoria atraves de Poisson

import matplotlib.pyplot as plt
import math
import numpy as np
from random import *
#Vetor vazio para armazenar os valores gerados
data = []
#Número de gerações
N = 100
#Poisson
parametro = math.exp(-2)
_lambda = 2
media_teo = _lambda
#iniciação do plot
fig = plt.figure()
# simulação em N eventos
for i in range(N):
    parada = False
    prodU = 1
    K = 1
    #distribuicao de poisson
    while parada == False:
        #geração da semente aleatoria entre 0 <= U <= 1
        U = random()
        #comparacao entre o produtorio de U com o parametro da poisson
        if(parametro < prodU*U):
            K += 1
            prodU = prodU*U
        else:
            X = K - 1
            parada = True
    data.append(X)
#convertendo os dados em numpy array
array = np.array(data)
print("Media Teorica: ", media_teo)
print("Media Simulada: ", np.average(array))
print("Desvio Padrão Teorico: ", math.sqrt(media_teo))
print("Desvio Padrão Simulado: ", np.std(array))
ax1 = fig.add_subplot()
ax1.hist(array, bins=20, color='k', alpha=0.8)
plt.show()
