#Verificação Parcial - Variáveis Aleatórias
#Prof Márcio das Chagas Moura
#Alunos: Gabriela Farias e Gustavo Camargo

#Questão 04

#geracao de variavel aleatória inteira uniformemente distribuida entre dois limites

from random import *

#funcao para o metodo inclusivo dos limites
def included(a,b):
    U = random()
    gerador = int(a +(b-a)*U)
    return gerador
#funcao para o metodo exclusivo dos limites
def excluded(a,b):
    U = random()
    gerador = int(a +(b-a)*U)
    if(gerador == a or gerador == b):
        print("Recalculando...")
        return excluded(a,b)
    else:
        return gerador

a = 2
b = 8

for i in range(1):
    var1 = included(a,b)
    var2 = excluded(a,b)
    
    #convertendo os dados em numpy array

    print("var inclusivo: ", var1)
    print("var exclusivo: ", var2)

