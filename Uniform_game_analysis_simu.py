#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 05

#Analise jogo de sorte por distribuicao uniforme

from random import *

#funcao para o metodo inclusivo dos limites
def included(a,b):
    U = random()
    gerador = int(a +(b-a)*U)
    return gerador
#funcao para selecao de 3 cartas em sequencia + análise de sequencia
def selecao(cartas_):
    mao = []
    car1 = included(a,b)
    mao.append(cartas_[car1])
    del cartas_[car1]
    car2 = included(a,b-1)
    mao.append(cartas_[car2])
    del cartas_[car2]
    car3 = included(a,b-2)
    mao.append(cartas_[car3])
    del cartas_[car3]

    mao.sort()

    if (mao[1] + 1 == mao[2]) and (mao[1] - 1 == mao[0]):
        return 1
    else:
        return 0
#contagem de derrotas da mesa, ou seja, vitorias do apostador
vitorias = 0

for i in range(110):
    a = 0
    b = 51
    cartas = [1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,
             1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13]
    vitorias = vitorias + selecao(cartas)

    
    #convertendo os dados em numpy array

print("Derrotas da mesa: ", vitorias)