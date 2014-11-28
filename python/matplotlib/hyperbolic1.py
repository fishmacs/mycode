import numpy as np
from matplotlib import pyplot as pp


def arccoth(x):
    return np.log((x + 1) / (x - 1)) / 2
    
x = np.linspace(-20, 20, 200)
pp.subplot(221)
pp.plot(x, np.arcsinh(x))

pp.subplot(222)
x = np.linspace(1, 100, 200)
pp.plot(x, np.arccosh(x))

x = np.linspace(-1, 1, 200)
pp.subplot(223)
pp.plot(x, np.arctanh(x))
#pp.plot(x, np.tan(x), 'r')

pp.subplot(224)
x = np.linspace(-20, 1)
pp.plot(x, arccoth(x))
x = np.linspace(1, 20)
pp.plot(x, arccoth(x))

pp.show()
