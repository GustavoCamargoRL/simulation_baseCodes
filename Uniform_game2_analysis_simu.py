#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 06

#jogo de sorte, analise por distribuicao uniforme

from random import *


#funcao para o metodo inclusivo dos limites
def included(a,b):
    U = random()
    gerador = int(a +(b-a)*U)
    return gerador
#funcao para selecao de 6 números em sequencia
def selecao(cartela):
    select = []
    for i in range(6):
        num = included(a,b-i)
        select.append(cartela[num])
        del cartela[num]
    return select
#jogos gerados
jogos = []
for i in range(30):
    a = 0
    b = 59
    cartela = []
    for j in range(60):
        cartela.append(j+1)
    
    jogos.append(selecao(cartela))

    #convertendo os dados em numpy array

print("Jogos: ", jogos)