import numpy as np
from numpy import cos, pi
import matplotlib.pyplot as plt


def arrayA(F, k):
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

    A = np.mat([m0, m1, m2, m3, m4, m5])
    A = np.linalg.inv(A)
    return A


def W(F):
    if 0 <= F <= 0.22:
        return 5
    elif 0.22 < F < 0.28:
        return 0
    elif 0.28 <= F <= 0.5:
        return 5


def H(F):
    if 0 <= F < 0.25:
        return 0
    elif 0.25 <= F <= 0.5:
        return 1


def R(s, F):
    y = s[0] + (s[1] * cos(2 * pi * F)) + (s[2] * cos(4 * pi * F)) + (s[3] * cos(6 * pi * F)) \
           + (s[4] * cos(8 * pi * F))
    y = float(y)
    return y


def find_err(S, Interval):

    temp = []
    for i in Interval:
        error_temp = (R(S, i) - H(i)) * W(i)
        temp.append(error_temp)

    return temp


def fine_extre(err, Interval):

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
    max = np.max(err_temp)
    return temp, max


def find_h(s, k):
    temp = [0.0 for i in range((2 * k) + 1)]
    temp[k] = float(s[0])
    for n in range(k):
        temp[k + (n + 1)] = float(s[n] / 2)
        temp[k - (n + 1)] = float(s[n] / 2)

    return temp


if __name__ == '__main__':

    # step 1 for set up
    #  N = 9, k = 4, k + 2 = 6
    k = 4; N = 9
    Interval = np.arange(0, 0.5001, 0.0001)
    F = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    E0 = 5; E1 = 50
    # step 2
    i = 0

    while not (0 <= (E1 - E0) <= 0.001):
        E1 = E0
        A = arrayA(F, k + 1)
        Hd = np.mat([0, 0, 0, 1, 1, 1]).T
        s = np.array(A.dot(Hd))

        # step 3
        err = find_err(s, Interval)

        # step 4 and step 5
        F, E0 = fine_extre(err, Interval)

        i += 1

    # step 6
    h = find_h(s, k)
    print("Take {} times iteration".format(i))
    print(s.tolist())
    print(F)
    print(h)





