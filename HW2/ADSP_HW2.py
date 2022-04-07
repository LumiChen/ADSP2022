import numpy as np
from numpy import cos, pi
import matplotlib.pyplot as plt
from scipy.fftpack import *
import os


def H(F, transition=False):
    if not transition:
        if -0.5 < F < 0:
            return 1j
        elif 0 < F < 0.5:
            return -1j
        elif F == 0 or F == 0.5 or F == -0.5:
            return 0
    else:
        # 0.75
        if F == -0.5:
            return 0
        elif -0.5 < F <= -0.1:
            return 1j
        elif -0.1 < F < 0:
            return 0.7j
        elif F == 0:
            return 0
        elif 0 < F < 0.1:
            return -0.7j
        elif 0.1 <= F < 0.5:
            return -1j
        elif F == 0.5:
            return 0


def r1_to_rn(r1):    # step 3
    k = (len(r1) - 1) // 2  # 8
    temp = [0.0 for i in range(len(r1))]
    for n in range(len(r1)):
        if n < k:  # 0 ~ 7
            temp[n] = r1[n + k + 1]
        elif n >= k:  # 8 ~ 16
            temp[n] = r1[n - k]
    return temp


def rn(r1, n):  # r period step 4

    N = len(r1)
    k = (N - 1) // 2
    if n < (-k) or n > k:  # N = 17
        n = n + N
    return r1[n + k]  # r[n] n = -8 ~ 8 mapping


def R(r, F):
    temp_imag = 0.0
    k = (len(r) - 1) // 2
    for n in range(len(r)):
        temp_imag += (rn(r, n - k) * (np.exp(-1j * 2 * pi * F * (n-k)))).imag

    return temp_imag


def plot_(interval, value1, value2, mode, name):
    assert mode in ['scatter', 'plot']
    if not value2:
        if mode == 'scatter':
            plt.scatter(interval, value1)
            plt.savefig(name + ".png")
            plt.title(name)
            plt.show()
            plt.close()
        elif mode == 'plot':
            plt.plot(interval, value1)
            plt.savefig(name + ".png")
            plt.title(name)
            plt.show()
            plt.close()
    else:
        if mode == 'scatter':
            plt.scatter(interval, value1, c='r')
            plt.scatter(interval, value2, c='b')
            plt.savefig(name + ".png")
            plt.title(name)
            plt.show()
            plt.close()
        elif mode == 'plot':
            plt.plot(interval, value1, c='r')
            plt.plot(interval, value2, c='b')
            plt.savefig(name + ".png")
            plt.title(name)
            plt.show()
            plt.close()


if __name__ == "__main__":

    # set up
    Interval_F = np.arange(0, 0.9999, 0.0001)
    Hd = []
    #  the ideal filter
    for i in Interval_F:
        if i > 0.5:
            Hd.append(H(i - 1).imag)
        else:
            Hd.append(H(i).imag)

    # step 1
    s = []
    sn = 55  # the number of sampling number
    trans = True
    for i in range(sn):
        p = i / sn
        if p > 0.5:
            s.append(H(p - 1, transition=trans))
        else:
            s.append(H(p, transition=trans))
    print(s)
    print("The number of sampling points: {}".format(sn))
    print("---------------")

    k = (len(s) - 1) // 2
    Interval_s = np.arange(0, len(s), 1)  # interval of sampling
    Interval_r = [i - k for i in range(len(s))]

    # step 2
    r1 = np.fft.ifft(s)

    # step 3
    r = r1_to_rn(r1)
    for i in range(len(r)):
        print("r[{}] = {}".format(i - k, r[i]))
    print("-------------")

    # step 4
    h = [0 for i in range(len(r))]
    for i in range(len(r)):
        h[i] = rn(r, i - k)  # n = -8 ~ 8 from step 3

    RF = []
    for i in Interval_F:
        RF.append(R(r, i))

    for i in range(len(h)):
        print("h[{}] = {}".format(i, h[i]))
    print("------------")

    plot_(Interval_F, value1=RF, value2=Hd, mode='plot', name='frequency response')
    plot_(Interval_s, value1=h, value2=None, mode='scatter', name='h[n]')
