import numpy as np
from numpy import cos, pi
import matplotlib.pyplot as plt


def H(F):
    if -0.25 < F <= 0.25:
        return 1
    elif -0.5 < F <= -0.25:
        return 0
    elif 0.25 < F < 0.5:
        return 0


def r_n(r1):    # step 3
    k = (len(r1) - 1) // 2  # 8
    temp = [0.0 for i in range(len(r1))]
    for n in range(len(r1)):
        if n < k:  # 0 ~ 7
            temp[n] = r1[n + k + 1]
        elif n >= k:  # 8 ~ 16
            temp[n] = r1[n - k]
    return temp


def r_p(r1, n):  # r period step 4

    N = len(r1)
    k = (N - 1) // 2
    if n < (-k) or n > (k):  # N = 17
        n = n + N

    return r1[n + k]  # r[n] n = -8 ~ 8 mapping


def R(r, F):
    temp = 0.0
    k = (len(r) - 1) // 2
    for n in range(len(r)):
        temp += (float(r_p(r, n - k) * float(cos(2*pi*F*(n - k)))))

    return temp


if __name__ == "__main__":

    # set up
    interval_F = np.arange(0, 0.9999, 0.0001)
    F = []
    for i in interval_F:
        if i > 0.5:
            F.append(H(i - 1))
        else:
            F.append(H(i))

    # step 1
    a = [1, 1, 1, 1, 1, 1, 1, 1, 0.7,
         0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2,
         0.7, 1, 1, 1, 1, 1, 1, 1]
    print(len(a))
    # step 2
    r1 = np.fft.ifft(a)
    ri = r1.imag

    # step 3
    r = r_n(r1.real)

    # step 4
    h = [0 for i in range(len(r))]
    k = (len(r) - 1) // 2
    for i in range(len(r)):
        h[i] = r_p(r, i - k)  # n = -8 ~ 8 from step 3

    k = []
    for i in interval_F:
        k.append(R(r, i))

    for i in range(len(h)):
        print("h[{}] = {}".format(i, h[i]))
    print("------------")

    plt.plot(interval_F, k, c='r')
    plt.plot(interval_F, F, c='b')
    plt.savefig("signal.png")
    plt.show()
    plt.close()
    Interval_h = np.arange(0, len(r), 1)
    plt.scatter(Interval_h, h, c='b')
    plt.savefig("response.png")
    plt.show()
    plt.close()
