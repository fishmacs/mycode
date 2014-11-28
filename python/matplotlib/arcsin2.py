import numpy as np
from scipy.misc import derivative as der
from matplotlib import pyplot as pp


def arcsin2(x):
    return np.arcsin(x) ** 2
    
x = np.linspace(-1, 1, 200)
pp.subplot(121)
pp.plot(x, arcsin2(x))
pp.plot(x, der(arcsin2, x, dx=0.01, n=2), 'black')
pp.plot(x, der(arcsin2, x, dx=0.01, n=4, order=5), 'y')
pp.plot(x, der(arcsin2, x, dx=0.01, n=6, order=7), 'g')
pp.plot(x, der(arcsin2, x, dx=0.01, n=8, order=9), 'r')
pp.ylim(-10, 20000)

pp.subplot(122)
pp.plot(x, der(arcsin2, x, dx=0.01))
pp.plot(x, der(arcsin2, x, dx=0.01, n=3, order=5), 'black')
pp.plot(x, der(arcsin2, x, dx=0.01, n=5, order=7), 'y')
pp.plot(x, der(arcsin2, x, dx=0.01, n=7, order=9), 'g')
pp.plot(x, der(arcsin2, x, dx=0.01, n=9, order=11), 'r')
pp.ylim(-20, 20)

pp.show()
