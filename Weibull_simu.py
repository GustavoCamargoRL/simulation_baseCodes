#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 10

#geracao de variavel aleatoria por distribuicao weibull

import matplotlib.pyplot as plt
import math
import numpy as np
from random import *
from scipy import stats
#Vetor vazio para armazenar os valores gerados
data = []
data_teo = []
#Número de gerações
N = 100
alfa = 8
beta = 2
#iniciação do plot
fig = plt.figure()
# simulação em N eventos
for i in range(N):
    U = random()
    #distribuicao de weibull
    X = alfa*(-math.log(U))**(1/beta)
    data.append(X)
#convertendo os dados em numpy array

#weibull teorico
for i in range(20):
    Y = (beta/alfa)*((i/alfa)**(beta-1))*np.exp(-(i/alfa)**beta)
    data_teo.append(Y)

array = np.array(data)
ax1 = fig.add_subplot()
plt.plot(data_teo)
ax1.hist(array, bins=20, color='k', alpha=0.8, density=True)
plt.show()