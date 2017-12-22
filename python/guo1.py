import numpy
from math import log2, sqrt
from scipy.linalg import solve
from decimal import Decimal


def pi(k):
    a = Decimal(2) ** Decimal(0.5)
    for i in range(0, int(log2(k / 4))):
        a = ((a / 2) ** 2 + (1 - (1 - (a / 2) ** 2).sqrt()) ** 2).sqrt()
    return float(k * a / 2)


def pi1(k):
    b = 1
    for i in range(0, int(log2(k / 4))):
        b = numpy.sqrt(1 - 2 / (numpy.sqrt(b ** 2 + 1) + 1))
    return k * b


def test():
    ret = []
    for n in range(2, 10):
        k = 2 ** n
        A = numpy.array([[1, 1 / k, 1 / k**2, 1 / k**3],
                         [1, 1 / (2*k), 1 / (2*k)**2, 1 / (2*k)**3],
                         [1, 1 / (4 * k), 1 / (4*k)**2, 1 / (4*k)**3],
                         [1, 1 / (8*k), 1 / (8*k)**2, 1 / (8*k)**3]])
        B = numpy.array([pi(k), pi(2*k), pi(4*k), pi(8*k)])
        ret.append(solve(A, B))
    return ret

