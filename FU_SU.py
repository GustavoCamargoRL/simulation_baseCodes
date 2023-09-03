
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
N_D = int #it counts the departure events
n = int #number of costumers in the system
samples = 1000 #number of iterations
steps = 10 # number of time steps
T = 480 # mission time
h = T/steps # time step
lbd = 10/60 #arrival rate
mu = 5/60 # service rate
big_m = 10**303 #defines a "big-m" (MAX = 1e+303 on C++)
n_queue_mean = np.zeros(steps, dtype = "float")
n_mean = np.zeros(steps, dtype = "float")
time_spent = np.zeros(steps, dtype = "float")
T_p = 0
T_step = np.zeros(steps, dtype = "float")
t_idle = 0
t_idle_simu = np.zeros(samples, dtype="float")

for i in range (samples):
    A_i = [] #list that records the arrival time
    D_i = [] #list that records the departure time
    t = 0
    N_A = N_D = n = 0
    X = getExp(lbd)
    t_A = X
    s_A = False # disponibilidade para chamada
    t_D = big_m
        
    for j in range (steps):    
        
        T_step[j] = (j + 1)*h
        
        isOver = False
        
        while isOver == False:
            minimum = min(t_A,t_D)

            if (t_D == big_m):
                s_A = True

            if t_A <= t_D and t_A <= T_step[j]:#first case
                t = t_A
                N_A = N_A + 1
                n = n + 1
                X = getExp(lbd)
                t_A = t + X
                if n == 1 and s_A == True:
                    s_A = False
                    Y = getExp(mu)
                    t_D = t + Y
                A_i.insert(N_A-1,t)
                
            elif t_D <= t_A and t_D <= T_step[j]: #second case
                t = t_D
                n = n - 1
                N_D = N_D + 1
                s_A = True
                if n == 0 :
                    t_D = big_m
                elif s_A == True:
                    Y = getExp(mu)
                    t_D = t + Y
                    s_A = False
                D_i.insert(N_D-1, t)
                
            else: 
                isOver = True
        
        n_mean[j] = n_mean[j] + n
        if N_D > 0:
            for a in range (N_D):
               if a < len(D_i) - 1:
                    waiting_time = D_i[a] - A_i[a]
                    time_spent[j] = time_spent[j] + waiting_time
            time_spent[j] = time_spent[j]/N_D
        
        if (minimum > T and n > 0):
            for k in range(n):
                t = t_D
                n = n - 1 
                N_D = N_D + 1
                D_i.insert(N_D-1, t)
                s_A = True
                if n > 0 and s_A == True:
                    s_A = False
                    Y = getExp(mu)
                    t_D = t + Y
                else:
                    maximum = t - T
                    if maximum < 0 :
                        maximum = 0
                    T_p = T_p + maximum
    if (len(A_i) == len(D_i)):
        for count in range(len(A_i)):
            if (count == 0):
                t_idle = A_i[0]
            elif (A_i[count] > D_i[count-1]):
                t_idle += A_i[count] - D_i[count-1]
        t_idle_simu[i] = t_idle
print(t_idle_simu)

t_idle_med = np.sum(t_idle_simu)/np.size(t_idle_simu)
n_mean = n_mean/samples
time_spent = time_spent / samples
T_p = T_p/samples    
n_mean_simu = sum(n_mean)
print("n_mean: ", n_mean_simu)
#print (T_step, n_mean, time_spent, T_p)
print("tempo ocioso: ", t_idle_med)

roh = lbd/mu
E_L = roh/(1-roh)
E_W = roh/(lbd*(1-roh))

print ("E(L)=", E_L)
print ("E(W)=", E_W)
