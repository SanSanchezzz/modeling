from math import *
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

table_I = [0.5, 1, 5, 10, 50, 200, 400, 800, 1200]
table_T0 = [6700, 6790, 7150, 7270, 8010, 9185, 10010, 11140, 12010]
table_M = [0.5, 0.55, 1.7, 3.0, 11.0, 32.0, 40.0, 41.0, 39.0]

table_T = [4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000]
table_Sigma = [0.031, 0.27, 2.05, 6.06, 12.0, 19.9, 29.6, 41.1, 54.1, 67.7, 81.5]

tw = 2000
grp = 0
gt0 = 0

Igraph = []
Ugraph = []
Tgraph = []
RPgraph = []
T0graph = []

# Интерполяция
def interpolation(val, tableVal, table):
    min_i = 0
    max_i = 0

    for i in range(len(tableVal)):
        if (val > tableVal[i]):
            max_i = i
        else:
            max_i = i
            break

    if (0 == max_i):
        max_i = 1

    min_i = max_i - 1

    return table[min_i] + (table[max_i] - table[min_i]) / (tableVal[max_i] - tableVal[min_i]) * (val - tableVal[min_i])

# функция под интегралом
def funcInt(I, z):
    # Нахождение T(z)
    t0 = interpolation(I, table_I, table_T0)
    global gt0
    gt0 = t0
    m = interpolation(I, table_I, table_M)
    t = t0 + (tw - t0) * (z ** m)

    # Нахождение коэф. sigma
    sigma = interpolation(t, table_T, table_Sigma)

    return sigma * z

# Интегрирование методом трапеций
def trapezoidInt(I):
    a = 0
    b = 1
    n = 100
    h = (b - a) / n

    s = (funcInt(I, a) + funcInt(I, b)) / 2

    x = 0
    for i in range(n - 1):
        x = x + h
        s = s + funcInt(I, x)

    s = s * h

    return s

# Сопротивление
def Rp(le, R, I):
    return le / (2 * pi * R ** 2 * trapezoidInt(I))

# Производная для U
def f(I, U, le, R, Lk, Rk):
    global grp
    grp = Rp(le, R, fabs(I))

    return (U - (Rk + grp) * I) / Lk

# Производная для I
def g(I, Ck):
    return -I / Ck

# Нахождение I +1 и  U +1
def step(I, U, le, R, Lk, hn, Rk, Ck):
    k1 = f(I, U, le, R, Lk, Rk)
    q1 = g(I, Ck)

    k2 = f(I + hn * k1 / 2, U + hn * q1 / 2, le, R, Lk, Rk)
    q2 = g(I + hn * k1 / 2, Ck)

    k3 = f(I + hn * k2 / 2, U + hn * q2 / 2, le, R, Lk, Rk)
    q3 = g(I + hn * k2 / 2, Ck)

    k4 = f(I + hn * k3, U + hn * q3, le, R, Lk, Rk)
    q4 = g(I + hn * k3, Ck)

    return I + hn * (k1 + 2 * k2 + 2 * k3 + k4) / 6, U + hn * (q1 + 2 * q2 + 2 * q3 + q4) / 6

def stepOrder2(I, U, le, R, Lk, hn, Rk, Ck):
    k1 = f(I, U, le, R, Lk, Rk)
    q1 = g(I, Ck)

    k2 = f(I + hn * k1 / 2, U + hn * q1 / 2, le, R, Lk, Rk)
    q2 = g(I + hn * k1 / 2, Ck)

    return I + hn * ((1 - alpha) * k1 + alpha * k2), U + hn * ((1 - alpha) * q1 + alpha * q2)


def graf():
    gridsize = (3, 2)
    fig = plt.figure(figsize=(12, 8))
    ax1 = plt.subplot2grid(gridsize, (0, 0))
    ax1.set_xlabel('$t$')
    ax1.set_ylabel('$I$')

    ax2 = plt.subplot2grid(gridsize, (0, 1))
    ax2.set_xlabel('$t$')
    ax2.set_ylabel('$U$')

    ax3 = plt.subplot2grid(gridsize, (1, 0))
    ax3.set_xlabel('$t$')
    ax3.set_ylabel('$Rp$')

    ax4 = plt.subplot2grid(gridsize, (1, 1))
    ax4.set_xlabel('$t$')
    ax4.set_ylabel('$To$')

    ax5 = plt.subplot2grid(gridsize, (2, 0))
    ax5.set_xlabel('$t$')
    ax5.set_ylabel('$I*Rp$')

    ax1.plot(Tgraph, Igraph, color ='orange')
    ax2.plot(Tgraph, Ugraph, color ='green')
    ax3.plot(Tgraph, RPgraph, color ='red')
    ax4.plot(Tgraph, T0graph, color = 'blue')

    IRPgraph = [x * y for x, y in zip(Igraph, RPgraph)]
    ax5.plot(Tgraph, IRPgraph)

    plt.show()



def main():
    R = 0.35
    le = 12
    Lk = 0.000187
    Ck = 0.000268
    Rk = 0.25
    Uc = 1400
    I = 0
    hn = 0.000001
    t = 0

    for i in range(1200):
        I, U = step(I, Uc, le, R, Lk, hn, Rk, Ck)
        t += hn

        Igraph.append(I)
        Ugraph.append(Uc)
        Tgraph.append(t)
        RPgraph.append(grp)
        T0graph.append(gt0)

    graf()

if __name__ == "__main__":
    main()


