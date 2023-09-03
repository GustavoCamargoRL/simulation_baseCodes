import random
import math
import numpy as np # convenção. Outra alternativa: import numpy as np


def getExp(lbd):
    u = 0.0
    while u < 10**(-20) or u >= 1 : # 10**-20 is same than pow (10,-20)
       u = random.random()
       X = -math.log(1.0 - u) / lbd #Generate the inter-event time from the exponential distribution's CDF
    return X

N_A = int #it counts the arrival events
n = int
n_servers = 2
samples = 1000 #number of iterations
steps = 10 # number of time steps
T = 480 # mission time
h = T/steps # time step
lbd = 10/60 #arrival rate
mu = 5/60 # service rate
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

for i in range (samples):
    A_i = [] #list that records the arrival time
    D_i = [] #list that records the departure time
    t = 0
    N_A = n = 0
    N_D = np.zeros(n_servers, dtype = "int") #number of costumers for each server j
    customer_index = np.zeros(n_servers, dtype = "int")
    X = getExp(lbd)
    t_A = X
    t_D = np.ones(n_servers, dtype = "float")
    t_D = t_D*big_m
    n_total_before = 0
    aux_idle = np.zeros(n_servers, dtype = "float")
    servers = np.zeros(n_servers, dtype="int") #vetor de ocupacao, cada indice representa um servidor. 
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
                A_i.insert(N_A-1,t)
                D_i.insert(N_A-1, big_m)
                X = getExp(lbd)
                t_A = t + X
                n = n + 1
                if n <= n_servers and np.sum(servers) < n_servers:
                    for s in range(n_servers):
                        if(s_A[s]==True):   
                            s_A[s] = False
                            servers[s] = 1
                            Y = getExp(mu)
                            t_D[s] = t + Y
                            if t_idle[s] == 0 and s_idle[s] == True:
                                t_idle[s] = t
                                s_idle[s] = False
                            elif s_idle[s] == True:
                                t_idle[s] += t - aux_idle[s]
                                s_idle[s] = False
                            break     
                
            
            elif t_D_server == minimum and t_D_server <= T_step[j]: #second case
                t = t_D_server    
                server = np.argmin(t_D)
                N_D[server] = customer_index[server]
                D_i[N_D[server]-1] = t
                s_A[server] = True
                servers[server] = 0
                if n > n_servers and s_A[server] == True:
                    s_A[server] = False
                    servers[server] = 1
                    m = np.argmax(customer_index)
                    customer_index[server] = customer_index[m]+1
                    Y = getExp(mu)
                    t_D[server] = t + Y
    
                else:
                    s_idle[server] = True
                    aux_idle[server] = t
                    s_A[server] = True
                    servers[server] = 0
                    t_D[server] = big_m
                    customer_index[server] = 0
            
                n = n - 1

            else: 
                isOver = True
        
        n_mean[j] = n_mean[j] + n
        
        if (minimum > T and n > 0):
            for _ in range(n):
                server = np.argmin(t_D)
                t = t_D[server]
                n = n - 1 
                N_D[server] = customer_index[server]
                D_i[N_D[server]-1] = t
                s_A[server] = True
                servers[server] = 0
                if n >= n_servers and s_A[server] == True:
                    s_A[server] = False
                    servers[server] = 1
                    Y = getExp(mu)
                    t_D[server] = t + Y
                elif n > 0:
                    t_D[server] = big_m
                    s_A[server] = True
                    servers[server] = 0
                    customer_index[server] = 0
                else:
                    maximum = t - T
                    if maximum < 0 :
                        maximum = 0
                    T_p = T_p + maximum
        
        n_total_after = N_D[np.argmax(N_D)]#esse for tá calculando todos os tempos de todos os clientes repetidas vezes
        waiting_time = 0
        rng = range(n_total_before, n_total_after)
        for a in rng:
            if D_i[a] < big_m and A_i[a] < big_m:
                waiting_time = waiting_time + D_i[a] - A_i[a]
            #else:
                #print ("")
        
        if n_total_after - n_total_before > 0:
            time_spent[j] = time_spent[j] + waiting_time/(n_total_after - n_total_before)
            
        n_total_before = n_total_after

                   
    #print(i, n_mean[steps-1], time_spent[steps-1], T_p)
    
n_mean = n_mean/samples
time_spent = time_spent / samples
T_p = T_p/samples    
print (T_step, n_mean, time_spent, T_p)
print("tempo ocioso: ", t_idle/samples)

#Theoretical results - MMm

m = n_servers
roh = lbd/(m*mu)

sum0 = 0.0
rng = range (m)
for n in rng:
    fact_n = math.factorial(n)
    sum0 = sum0 + pow(roh*m,n)/fact_n

fact_m = math.factorial(m)
a = pow(roh*m,m)/fact_m
if (1.0-roh>0):
    sum0 = sum0 + a/(1.0-roh)

P0 = 1.0/sum0
if (fact_m*((1-roh)**2)>0):
    E_Lq = ((((roh*m)**m)*roh)/(fact_m*((1-roh)**2)))*P0
else:
    E_Lq = 0
E_S = roh*m/lbd
E_Ls = lbd*E_S
E_L = E_Lq + E_Ls

E_W = E_L/lbd

print ("P0=", P0)
print ("E(L)=", E_L)
print ("E(W)=", E_W)

import matplotlib.pyplot as plt

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
