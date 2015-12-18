import numpy
from matplotlib import pyplot as pp


def func1(x):
    return numpy.sin(x) / x

xs1 = numpy.linspace(-1.57, 1.57, 200)


def plot(xs, func):
    pp.plot(xs, func(xs))
    pp.show()