import numpy as np
from matplotlib import pyplot as pp


def coth(x):
    return 1 / np.tanh(x)

    
def ctg(x):
    return 1 / np.tan(x)
    
    
x = np.linspace(-1.57, 1.57, 200)
pp.subplot(221)
pp.plot(x, np.sinh(x))
pp.plot(x, np.sin(x), 'r')

x1 = np.linspace(-3.142, 3.142, 200)
pp.subplot(222)
pp.plot(x1, np.cosh(x1))
pp.plot(x1, np.cos(x1), 'r')

pp.subplot(223)
x = np.linspace(-2, 2, 200)
pp.ylim(-1, 1)
pp.plot(x, np.tanh(x))
#pp.plot(x, np.tan(x), 'r')

pp.subplot(224)
pp.ylim(-5, 5)
pp.plot(x, coth(x))
#pp.plot(x, ctg(x), 'r')

pp.show()
