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
    if n < (-k) or n > (k):  # N = 17
        n = n + N

    return r1[n + k]  # r[n] n = -8 ~ 8 mapping


def R(r, F):
    temp = 0.0
    k = (len(r) - 1) // 2
    for n in range(len(r)):
        temp += (float(rn(r, n - k) * float(cos(2 * pi * F * (n - k)))))

    return temp


def R_i(ri, F):
    temp = 0.0
    k = (len(ri) - 1) // 2
    for n in range(len(r)):
        temp += (float(rn(ri, n - k) * float(-(np.sin(2 * pi * F * (n - k))))))

    return temp


def plot_(interval, value1, value2, mode, name):
    assert mode in ['scatter', 'plot']
    if not value2:
        if mode == 'scatter':
            plt.scatter(interval, value1)
            plt.savefig(name + ".png")
            plt.show()
            plt.close()
        elif mode == 'plot':
            plt.plot(interval, value1)
            plt.savefig(name + ".png")
            plt.show()
            plt.close()
    else:
        if mode == 'scatter':
            plt.scatter(interval, value1, c='r')
            plt.scatter(interval, value2, c='b')
            plt.savefig(name + ".png")
            plt.show()
            plt.close()
        elif mode == 'plot':
            plt.plot(interval, value1, c='r')
            plt.plot(interval, value2, c='b')
            plt.savefig(name + ".png")
            plt.show()
            plt.close()


if __name__ == "__main__":

    # set up
    Interval_F = np.arange(0, 0.9999, 0.0001)
    Hd = []
    #  the ideal filter
    for i in Interval_F:
        if i > 0.5:
            Hd.append(H(i - 1))
        else:
            Hd.append(H(i))

    # step 1
    s = []
    sn = 17  # the number of sampling number
    for i in range(sn):
        p = i / sn
        if p > 0.5:
            s.append(H(p - 1))
        else:
            s.append(H(p))
    print(s)
    print("The number of sampling points: {}".format(sn))
    print("---------------")

    k = (len(s) - 1) // 2
    Interval_s = np.arange(0, len(s), 1)  # interval of sampling
    Interval_r = [i - k for i in range(len(s))]

    # step 2
    r1 = np.fft.ifft(s)
    ri = r1.imag

    # step 3
    r = r1_to_rn(r1.real)
    for i in range(len(r)):
        print("r[{}] = {}".format(i - k, round(r[i], 3)))
    print("-------------")

    plot_(Interval_r, value1=r, value2=None, mode='scatter', name='r[n]')

    # step 4
    h = [0 for i in range(len(r))]
    for i in range(len(r)):
        h[i] = rn(r, i - k)  # n = -8 ~ 8 from step 3

    RF = []
    RI = []
    for i in Interval_F:
        RF.append(R(r, i))
        RI.append(R_i(r, i))

    for i in range(len(h)):
        print("h[{}] = {}".format(i, round(h[i], 3)))
    print("------------")

    plot_(Interval_F, value1=RI, value2=None, mode='plot', name='RI')
    plot_(Interval_F, value1=RF, value2=Hd, mode='plot', name='frequency response')
    plot_(Interval_s, value1=h, value2=None, mode='scatter', name='h[n]')
