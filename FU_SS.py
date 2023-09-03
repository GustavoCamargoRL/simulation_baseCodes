## Algoritmo para simulacao em logica puxada para fila unica servidor sequencial
## Tecnicas de Simulacao
## Prof: Marcio das Chagas Moura
## Autores: Gustavo Camargo; Gabriela Farias; Bruna Leal


import random
import math
import numpy as np # convenção. Outra alternativa: import numpy as np


def getExp(lbd):
    u = 0.0
    while u < 10**(-20) or u >= 1 : # 10**-20 is same than pow (10,-20)
       u = random.random()
       X = -math.log(1.0 - u) / lbd #Generate the inter-event time from the exponential distribution's CDF
    return X

n_servers = 3 # number of sequential servers
samples = 1000 #number of iterations
steps = 10 # number of time steps
T = 480 # mission time
h = T/steps # time step
lbd = 10/60 #arrival rate
mu = np.array([[5/60, 3/60, 3/60]])
big_m = 10**303 #defines a "big-m" (MAX = 1e+303 on C++)
T_p = 0
n_queue_mean = np.zeros(steps, dtype = "float")
n_mean = np.zeros(steps, dtype = "float")
time_spent = np.zeros(steps, dtype = "float")
T_step = np.zeros(steps, dtype = "float")
s_idle = []
for i in range (n_servers):
        s_idle.append(True)
t_idle = np.zeros(n_servers, dtype = "float")


roh = lbd/mu[0]
E_L = sum(roh/(1-roh))
E_W = E_L/lbd

print ("E(L)=", E_L)
print ("E(W)=", E_W)

for i in range (samples):
    A_i = [] #list that records the arrival time at system 1
    D_i = np.zeros(n_servers, dtype = "float") #list that records the departure time at each server
    N_A = 0 # number of arrivals at server 0
    N_D = np.zeros(n_servers, dtype = "int") #number of costumers for each server j
    n = np.zeros(n_servers, dtype = "int") #number of costumers for each server j
    t = 0
    X = getExp(lbd)
    t_A = X
    t_D = np.ones(n_servers, dtype = "float")
    t_D = t_D*big_m
    t_D_frozen = np.ones((1,n_servers), dtype = "float")
    t_D_frozen = t_D_frozen*big_m
    D_i = t_D_frozen
    aux_idle = np.zeros(n_servers, dtype = "float")
    s_A = [] # disponibilidade para chamada
    for i in range (n_servers):
        s_A.append(True)

    for j in range (steps):

        T_step[j] = (j + 1)*h

        isOver = False

        while isOver == False:
            t_D_server = np.amin(t_D)
            minimum = min(t_A, t_D_server)

            if t_A == minimum and t_A <= T_step[j]:#first case
                t = t_A
                N_A = N_A + 1
                n[0] = n[0] + 1
                X = getExp(lbd)
                t_A = t + X
                A_i.insert(N_A-1,t)
                if n[0] == 1 and s_A[0] == True:
                    s_A[0] = False
                    Y = getExp(mu[0][0])
                    t_D[0] = t + Y
                    if t_idle[0] == 0 and s_idle[0] == True:
                                t_idle[0] = t
                                s_idle[0] = False
                    elif s_idle[0] == True:
                        t_idle[0] += t - aux_idle[0]
                        s_idle[0] = False
                if N_A > 0:
                    D_i = np.vstack((D_i, t_D_frozen))

            elif t_D_server == minimum and t_D_server <= T_step[j]:#second case
                t = t_D_server
                server = np.argmin(t_D)
                s_A[server] = True
                t_D[server] = big_m
                if (server == 0):
                    if (s_A[1] == True and n[1] == 0): # Checa se o 2 servidor esta disponivel e o cliente do 1 servidor pode seguir adiante
                        n[server] = n[server] - 1
                        N_D[server] = N_D[server] + 1
                        D_i[N_D[server]-1,server] = t
                        s_A[1] = False
                        Y = getExp(mu[0][server+1])
                        t_D[server+1] = t + Y
                        n[server+1] = n[server+1] + 1
                        if t_idle[server] == 0 and s_idle[server] == True:
                                t_idle[server] = t
                                s_idle[server] = False
                        elif s_idle[server] == True:
                            t_idle[server] += t - aux_idle[0]
                            s_idle[server] = False
                        if (n[server] > 0):
                            s_A[server] = False
                            Y = getExp(mu[0][server])
                            t_D[server] = t + Y

                else: #checa se o ultimo servidor terminou o servico
                    n[server] = n[server] - 1
                    N_D[server] = N_D[server] + 1
                    D_i[N_D[server]-1,server] = t
                    for i in range(n_servers - (n_servers - server)):  #itera por todos os servidores puxando os clientes em espera ate o ultimo servidor
                        if i != 0:
                            if(n[server-i]>0 and s_A[server-i] == True):
                                n[server-i] = n[server-i] - 1
                                N_D[server-i] = N_D[server-i] + 1
                                D_i[N_D[server-i]-1,server-i] = t
                                s_A[server - i+1] = False
                                Y = getExp(mu[0][server- i+1])
                                t_D[server- i+1] = t + Y
                                n[server- i+1] = n[server- i+1] + 1
                                if(server-i) == 0:
                                    s_A[server - i] = False
                                    Y = getExp(mu[0][server- i])
                                    t_D[server- i] = t + Y
                            else:
                                break
#                else:  # faz as manipulacoes necessarias quando for um servidor intermediario que finalizou o atendimento(Apenas para n_servers > 2)
#                    if(s_A[server+1] == True and n[server+1] == 0):
#                        n[server] = n[server] - 1
#                        N_D[server] = N_D[server] + 1
#                        D_i[N_D[server]-1,server] = t
#                        s_A[server+1] = False
#                        Y = getExp(mu[0][server+1])
#                        t_D[server+1] = t + Y
#                        n[server+1] = n[server+1] + 1
#                    if(s_A[server-1] == True and n[server-1] > 0 and n[server] == 0):
#                        n[server-1] = n[server-1] - 1
#                        N_D[server-1] = N_D[server-1] + 1
#                        D_i[N_D[server-1]-1,server-1] = t
#                        s_A[server-1] = False
#                        s_A[server] = False
#                        Y = getExp(mu[0][server-1])
#                        t_D[server-1] = t + Y
#                        Y = getExp(mu[0][server])
#                        t_D[server] = t + Y
#                        n[server] = n[server] + 1

            else:
                isOver = True

        n_mean[j] = n_mean[j] + sum(n)

        if (minimum > T and sum(n) > 0):
            while sum(n) != 0:   # obriga o atendimento de todos os clientes ate zerar o sistema
                server = np.argmin(t_D)
                t = t_D[server]
                s_A[server] = True
                t_D[server] = big_m
                if (server == 0):
                    if (s_A[1] == True and n[1] == 0):
                        n[server] = n[server] - 1
                        N_D[server] = N_D[server] + 1
                        D_i[N_D[server]-1,server] = t
                        s_A[1] = False
                        Y = getExp(mu[0][server+1])
                        t_D[server+1] = t + Y
                        n[server+1] = n[server+1] + 1
                        if (n[server] > 0):
                            s_A[server] = False
                            Y = getExp(mu[0][server])
                            t_D[server] = t + Y

                elif (server == n_servers - 1):
                    n[server] = n[server] - 1
                    N_D[server] = N_D[server] + 1
                    D_i[N_D[server]-1,server] = t
                    for i in range(n_servers):
                        if i != 0:
                            if(n[server-i]>0 and s_A[server-i] == True):
                                n[server-i] = n[server-i] - 1
                                N_D[server-i] = N_D[server-i] + 1
                                D_i[N_D[server-i]-1,server-i] = t
                                s_A[server - i+1] = False
                                Y = getExp(mu[0][server- i+1])
                                t_D[server- i+1] = t + Y
                                n[server- i+1] = n[server- i+1] + 1
                                if(server-i) == 0:
                                    s_A[server - i] = False
                                    Y = getExp(mu[0][server- i])
                                    t_D[server- i] = t + Y
                            else:
                                break
                else:
                    if(s_A[server+1] == True and n[server+1] == 0):
                        n[server] = n[server] - 1
                        N_D[server] = N_D[server] + 1
                        D_i[N_D[server]-1,server] = t
                        s_A[server+1] = False
                        Y = getExp(mu[0][server+1])
                        t_D[server+1] = t + Y
                        n[server+1] = n[server+1] + 1
                    if(s_A[server-1] == True and n[server-1] > 0 and n[server] == 0):
                        n[server-1] = n[server-1] - 1
                        N_D[server-1] = N_D[server-1] + 1
                        D_i[N_D[server-1]-1,server-1] = t
                        s_A[server-1] = False
                        s_A[server] = False
                        Y = getExp(mu[0][server-1])
                        t_D[server-1] = t + Y
                        Y = getExp(mu[0][server])
                        t_D[server] = t + Y
                        n[server] = n[server] + 1

                if sum(n) == 0:
                    maximum = t - T
                    if maximum < 0 :
                        maximum = 0
                    T_p = T_p + maximum

        if N_D[n_servers-1] > 0:
            waiting_time = 0
            rng = range (N_D[n_servers-1])
            for a in rng:
                if (a != (N_D[n_servers-1] - 1)):
                    if D_i[a,n_servers-1] < big_m and A_i[a] < big_m:
                        waiting_time = waiting_time + D_i[a,n_servers-1] - A_i[a]

            time_spent[j] = time_spent[j] + waiting_time/N_D[n_servers-1]
        if(sum(n)==0):
            for y in range(n_servers):
                for x in range(len(D_i) - 1):
                    if y == 0:
                        if  x == 0:
                            t_idle[y] += A_i[x]
                        else:
                            t_idle[y] += D_i[x][y] - D_i[x-1][y]
                    else:
                        if x == 0:
                            t_idle[y] += D_i[x][y]
                        else:
                            t_idle[y] += D_i[x][y] - D_i[x-1][y]
            #print(i, n_mean[steps-1], time_spent[steps-1], T_p)

n_mean_total = np.sum(n_mean)/n_mean.size
n_mean_simu = n_mean_total/samples
time_spent = time_spent / samples
T_p = T_p/samples
t_idle_med = np.sum(t_idle)/np.size(t_idle)

print (t_idle)
print (T_step)
print (n_mean_simu)
print (time_spent)
print (T_p)

t_idle_med = np.sum(t_idle) / np.size(t_idle)

print("Tempo ocioso dos servidores:", t_idle/samples)
print("Tempo ocioso médio:", t_idle_med/samples)

import matplotlib.pyplot as plt
import numpy as np

# As plotagens na matplotlib ficam em um objeto Figure

fig = plt.figure()

ax1 = fig.add_subplot(2,1,1)
ax1.set_xlabel('Time')
ax1.set_ylabel('Expected number of customers')

ax2 = fig.add_subplot(2,1,2)
ax2.set_xlabel('Time')
ax2.set_ylabel('Total waiting time')

ax1.plot(T_step, n_mean, 'k', label='simulated')
EL = np.ones(steps, dtype = "float")*E_L
ax1.plot(T_step, EL, 'k--', label='theoretical')
ax2.plot(T_step, time_spent, 'k', label='simulated')
EW = np.ones(steps, dtype = "float")*E_W
ax2.plot(T_step, EW, 'k--', label='theoretical')
ax1.legend(loc='best')
ax2.legend(loc='best')
