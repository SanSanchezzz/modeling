import matplotlib.pyplot as plt
import numpy as np

# Исходные данные:
K0 = 0.4
KN = 0.1
alpha0 = 0.05
alphaN = 0.01
l = 10
T0 = 300
R = 0.5
F0 = 50
h = 0.1

# Параметры для краевых условий
b = (KN * l) / (KN - K0)
a = - K0 * b
d = (alphaN * l) / (alphaN - alpha0)
c = - alpha0 * d

# Коэффициенты теплопроводности и теплоотдачи
def k(x):
    return a / (x - b)

def alpha(x):
    return c / (x - d)

# Выполнение замены
def p(x):
    return 2 * alpha(x) / R

def f(x):
    return 2 * alpha(x) * T0 / R

# Простая аппроксимация
def x_plus_half(x):
    return (k(x) + k(x + h)) / 2

def x_minus_half(x):
    return (k(x) + k(x - h)) / 2

# Разностная схема
def A(x):
    return x_plus_half(x) / h

def C(x):
    return x_minus_half(x) / h

def B(x):
    return A(x) + C(x) + p(x) * h

def D(x):
    return f(x) * h

# Краевые условия
# при x = 0
K0 = x_plus_half(0) + h * h * (p(0) + p(h)) / 16 + h * h * p(0) / 4
M0 = -(x_plus_half(0) - h * h * (p(0) + p(h)) / 16)
P0 = h * F0 + h * h / 4 * ((f(0) + f(h)) / 2 + f(0))
# при x = N
KN = -x_minus_half(l) / h - alphaN - p(l) * h / 4 - (p(l) + p(l - h)) * h / 16
MN = x_minus_half(l) / h - (p(l) + p(l - h)) * h / 16
PN = -(alphaN * T0 + ((f(l) + f(l - h)) / 2 + f(l)) * h / 4)

# Метод прогонки
def run():
    # Прямой ход
    eps = [0, -M0 / K0]
    eta = [0, P0 / K0]

    x = h
    n = 1
    while (x + h < l):
        eps.append(C(x) / (B(x) - A(x) * eps[n]))
        eta.append((D(x) + A(x) * eta[n]) / (B(x) - A(x) * eps[n]))
        n += 1
        x += h

    # Обратный ход
    t = [0] * (n + 1)
    # Значение функции в конечной точке
    t[n] = (PN - MN * eta[n]) / (KN + MN * eps[n])

    for i in range(n - 1, -1, -1):
        t[i] = eps[i + 1] * t[i + 1] + eta[i + 1]

    return t

# def graf():
    # f1 = open('x.txt', 'r')
    # while (

def main():
    t = run()
    x = [i for i in np.arange(0, l, h)]

    # f1 = open('x.txt', 'w')
    for i in range (0, len(x), 2):
        print(str(x[i]), end=' ')
        print(str(300) + ' ')
    # print(t[:-1])
    # f1.close()
    print('\n')
    # f1 = open('y.txt', 'w')
    # for i in range (0, len(t[:-1]), 100):
        # print(str(300) + ' ', end=' ')
    # print(t[:-1])
    # f1.close()

    plt.plot(x, t[:-1])
    plt.xlabel("Длина, см")
    plt.ylabel("Температура, K")
    plt.show()

if __name__ == "__main__":
    main()
