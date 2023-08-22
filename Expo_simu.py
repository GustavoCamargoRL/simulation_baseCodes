#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 07

#geracao de variavel aleatoria por distribuicao exponencial com teste de aderencia 

import math
import numpy as np
from scipy import stats
from random import *


#Distribuicao exponencial
lambda_ = 2
N = 1000
data = []

for i in range(N):
    U = random()
    parametro = -np.log(1-U)/lambda_
    data.append(parametro)


resultado = stats.kstest(data, stats.expon.cdf)

print(resultado)