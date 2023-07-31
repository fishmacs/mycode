import numpy as np
from matplotlib import pyplot as pt
from matplotlib.gridspec import GridSpec


def find_2npower(x):
    power2 = np.floor(np.log(x) / np.log(2))
    if (np.power(2, power2) == x):
        return (power2, power2)
    else:
        return (power2, power2 + 1)


def func1(x, base):
    p1, p2 = find_2npower(x)
    if (p1 == p2):
        return np.power(base, -p1)
    else:
        x1 = np.power(2, p1)
        x2 = np.power(2, p2)
        y1 = np.power(base, -p1)
        y2 = np.power(base, -p2)
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)


def display(funcs, xs):
    n = len(funcs)
    col = int(np.sqrt(n))
    row = int(np.ceil(n / col))
    grid = GridSpec(row, col)
    for i in range(row):
        for j in range(col):
            print('zwww', i, j)
            pt.subplot(grid[i, j])
            func, x = funcs[i * col + j], xs[i * col + j]
            pt.plot(x, func(x))
    pt.show()


def continuous():
    xs1 = np.linspace(-1, 1, 4000)
    xs2 = np.linspace(0, 1.5, 2000)
    display([
        lambda x: [func1(np.abs(y), -1) for y in x],
        lambda x: np.sin(1 / x),
        lambda x: [func1(np.abs(y), -0.5) for y in x],
        lambda x: x * np.sin(1 / x)
    ], [
        xs1,
        xs2,
        xs1,
        xs2
    ])


if __name__ == '__main__':
    continuous()
