import math
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


# # exp(ix)
def expi():
    x = np.linspace(0, 30, 1000)
    fig = pyplot.figure()
    xi = np.asarray([(0 + 1j) * r for r in x])
    y = np.exp(xi)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(np.real(y), np.imag(y), x)
    fig.show()


def divid(m, n):
    ret = []
    d = 2 * m / n
    for i in range(n + 1):
        blue = 255 * i // n
        red = 255 - 255 * i // n
        y = m - i * d
        for j in range(n + 1):
            blue = 255 * i // n
            red = 255 - 255 * i // n
            red = max(0, red - 255 * j // n)
            green = 255 * j // n
            if red == 0 and green > 128 and blue > 128:
                red = green
                blue = 0
            x = -m + j * d
            ret.append((x, y, '#%02x%02x%02x' % (red, green, blue)))
    return ret


def draw(points, ax=None, xlim=None, ylim=None):
    n = int(math.sqrt(len(points)))
    if not xlim:
        xs = [p[0] for p in points]
        xlim = (min(xs), max(xs))
    if not ylim:
        ys = [p[1] for p in points]
        ylim = (min(ys), max(ys))
    if not ax:
        pyplot.xlim(xlim[0], xlim[1])
        pyplot.ylim(ylim[0], ylim[1])
        ax = pyplot
    else:
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xlim(xlim[0], xlim[1])
        ax.set_ylim(ylim[0], ylim[1])
    for i in range(n):
        for j in range(n - 1):
            p1 = points[i * n + j]
            p2 = points[i * n + j + 1]
            ax.plot((p1[0], p2[0]), (p1[1], p2[1]), color=p1[2])
    for i in range(n - 1):
        for j in range(n):
            p1 = points[i * n + j]
            p2 = points[i * n + j + n]
            ax.plot((p1[0], p2[0]), (p1[1], p2[1]), color=p1[2])
    if ax == pyplot:
        pyplot.show()


def calc(points, func):
    comps = np.asarray([np.complex(p[0], p[1]) for p in points])
    comps = [c for c in func(comps)]
    return [(np.real(c).tolist(), np.imag(c).tolist(), p[2]) for (c, p) in zip(comps, points)]


def f1(x):
    return x / (np.power(np.real(x), 2) + np.imag(x) * 2)


def all():
    ps1 = divid(1, 20)
    ps2 = divid(3, 60)
    #ps3 = divid(10, 100)

    output1 = calc(ps2, np.exp)
    output2 = calc(ps2, lambda x: np.power(x, 2))
    output3 = calc(ps2, lambda x: np.power(x, 3))
    output4 = calc(ps2, lambda x: np.power(x, 4))
    output5 = calc(ps2, np.cos)
    output6 = calc(ps1, f1)
    output7 = calc(ps2, lambda x: x / (1 + x))  # (y: -1:1, x: 0: 1)
    output8 = calc(ps1, lambda x: np.power(x, -1))

    f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = pyplot.subplots(3, 3)
    print('begin drawing...')
    draw(ps1, ax1)
    print('1 ok')
    draw(output1, ax2, (-24, 24), (-20, 20))
    print('2 ok')
    draw(output2, ax3, (-20, 20))
    print('3 ok')
    draw(output3, ax4)
    print('4 ok')
    draw(output4, ax5, ylim=(-200, 200))
    print('5 ok')
    draw(output5, ax6, (-12, 12))
    print('6 ok')
    draw(output6, ax7, (-5, 5), (-2, 3))
    print('7 ok')
    draw(output7, ax8, (0, 2), (-2, 2))
    print('8 ok')
    draw(output8, ax9, (-5, 5), (-5, 5))
    print('9 ok')
    pyplot.show()


if __name__ == '__main__':
    all()
    
