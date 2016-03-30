import numpy as np
from matplotlib import pyplot as pt


def singen(amps, freqs, phases):
    def func(x):
        sum = 3.0
        for amp, freq, phase in zip(amps, freqs, phases):
            sum += amp * np.sin(freq * x + phase)
        return sum
    return func


def cos7():
    x = np.linspace(0, 4 * np.pi, 1000)
    func = singen([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2.5], range(1, 8), [np.pi / 2] * 7)
    pt.plot(x, func(x))
    pt.show()


def cos8():
    x = np.linspace(0, 4 * np.pi, 1000)
    func = singen([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2.5], range(1, 9), [np.pi / 2] * 8)
    pt.plot(x, func(x))
    pt.show()
