import numpy as np
from numpy import cos, pi
import matplotlib.pyplot as plt


# define the array A at page 57
def MatrixA(F, k):
    m0 = [cos(2 * i * pi * F[0]) for i in range(k)]
    m0.append(1 / W(F[0]))
    m1 = [cos(2 * i * pi * F[1]) for i in range(k)]
    m1.append(-1 / W(F[1]))
    m2 = [cos(2 * i * pi * F[2]) for i in range(k)]
    m2.append(1 / W(F[2]))
    m3 = [cos(2 * i * pi * F[3]) for i in range(k)]
    m3.append(-1 / W(F[3]))
    m4 = [cos(2 * i * pi * F[4]) for i in range(k)]
    m4.append(1 / W(F[4]))
    m5 = [cos(2 * i * pi * F[5]) for i in range(k)]
    m5.append(-1 / W(F[5]))
    m6 = [cos(2 * i * pi * F[6]) for i in range(k)]
    m6.append(1 / W(F[6]))
    m7 = [cos(2 * i * pi * F[7]) for i in range(k)]
    m7.append(-1 / W(F[7]))
    m8 = [cos(2 * i * pi * F[8]) for i in range(k)]
    m8.append(1 / W(F[8]))
    m9 = [cos(2 * i * pi * F[9]) for i in range(k)]
    m9.append(-1 / W(F[9]))

    A = np.mat([m0, m1, m2, m3, m4, m5, m6, m7, m8, m9])
    A = np.linalg.inv(A)

    return A


# weight function
def W(F):
    if 0 <= F <= 0.2:
        return 1
    elif 0.2 < F < 0.25:
        return 0
    elif 0.25 <= F <= 0.5:
        return 0.6


# ideal filter
def H(F):
    if 0 <= F < 0.225:
        return 1
    elif 0.225 <= F <= 0.5:
        return 0


# R
def R(s, F):
    y = s[0] + (s[1] * cos(2 * pi * F)) + (s[2] * cos(4 * pi * F)) + (s[3] * cos(6 * pi * F)) \
           + (s[4] * cos(8 * pi * F)) + (s[5] * cos(10 * pi * F)) + (s[6] * cos(12 * pi * F)) \
           + (s[7] * cos(14 * pi * F)) + (s[8] * cos(16 * pi * F))
    y = float(y)
    return y


# error function
def find_err(S, Interval):

    temp = []
    temp_R = []
    temp_H = []
    for i in Interval:
        error_temp = (R(S, i) - H(i)) * W(i)
        temp_H.append(H(i))
        temp_R.append(R(S, i))
        temp.append(error_temp)

    return temp, temp_R, temp_H


# find extrem point and consider the boundaries
def find_extre(err, Interval):

    temp = []
    err_temp = []
    for i in range(len(err)):
        # conider the B.C.
        if i == 0:
            if err[i] - 0 < 0 and err[i] - err[i + 1] < 0:
                temp.append(Interval[i])
                err_temp.append(abs(err[i]))
            if err[i] - 0 > 0 and err[i] - err[i + 1] > 0:
                temp.append(Interval[i])
                err_temp.append(abs(err[i]))
        if i != 0 and i != len(err) - 1:
            if err[i] - err[i - 1] < 0 and err[i] - err[i + 1] < 0:
                temp.append(Interval[i])
                err_temp.append(abs(err[i]))
            if err[i] - err[i - 1] > 0 and err[i] - err[i + 1] > 0:
                temp.append(Interval[i])
                err_temp.append(abs(err[i]))
        if i == len(err) - 1:
            if err[i] - err[i - 1] < 0 and err[i] - 0 < 0:
                temp.append(Interval[i])
                err_temp.append(abs(err[i]))
            if err[i] - err[i - 1] > 0 and err[i] - 0 > 0:
                temp.append(Interval[i])
                err_temp.append(abs(err[i]))
    max_temp = np.max(err_temp)
    return temp, max_temp


# return the h
def find_h(s, k):
    temp = [0.0 for i in range((2 * k) + 1)]
    temp[k] = float(s[0])
    for n in range(k):
        temp[k + (n + 1)] = float(s[n + 1] / 2)
        temp[k - (n + 1)] = float(s[n + 1] / 2)

    return temp


if __name__ == '__main__':

    # step 1 for set up
    # pass band 0 ~ 0.2  transition band 0.2 ~ 0.25 stop band 0.25 ~ 0.5
    #  N = 17, k = 8, k + 2 = 10
    k = 8; N = 17
    Interval = np.arange(0, 0.5001, 0.0001)
    # initial condition
    F = [0, 0.1, 0.15, 0.18, 0.20, 0.25, 0.35, 0.4, 0.45, 0.5]
    E0 = 5; E1 = 50
    # step 2
    i = 0
    E = []
    while not (0 <= (E1 - E0) <= 0.0001):  # delta = 0.001
        E1 = E0
        A = MatrixA(F, k + 1)
        Hd = np.mat([H(F[0]), H(F[1]), H(F[2]), H(F[3]), H(F[4]), H(F[5]), H(F[6]), H(F[7]), H(F[8]), H(F[9])]).T
        # Hd = np.mat([H(F[0]), H(F[1]), H(F[2]), H(F[2]), 1, 0, 0, 0, 0, 0]).T
        s = np.array(A.dot(Hd))
        # print(s.tolist())

        # step 3
        err, rr, hh = find_err(s, Interval)

        # step 4 and step 5
        F, E0 = find_extre(err, Interval)
        E.append(E0)
        i += 1
    # step 6
    h = find_h(s, k)

    plt.plot(Interval, rr)
    plt.savefig("filter.png")
    plt.close()
    plt.plot(Interval, hh)
    plt.xlim(0, 0.5)
    # plt.show()
    plt.close()

    Interval_h = np.arange(0, 17, 1)
    plt.scatter(Interval_h, h)
    plt.axhline(y=0, c='k')
    plt.savefig("response.png")
    # plt.show()
    plt.close()

    print("Take {} times iteration".format(i))
    print("------------")

    for i in range(len(E)):
        print("E of step {} = {}".format(i + 1, E[i]))
    print("------------")

    for i in range(len(s)):
        print("s{} = {}".format(i, s[i]))
    print("------------")

    for i in range(len(F)):
        print("F{} = {}".format(i, F[i]))
    print("------------")

    for i in range(len(h)):
        print("h{} = {}".format(i, h[i]))





