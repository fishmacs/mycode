import numpy as np
from matplotlib import pyplot as pp


f1 = lambda n: n * np.log(1 + 1 / n)

f2 = lambda n: n * (np.exp(1 / n) - 1)


def plot():
    x = np.linspace(1, 200, 1000)
    pp.plot(x, f1(x))
    pp.plot(x, f2(x), 'black')
    pp.ylim(0.5, 1.5)
    pp.show()
