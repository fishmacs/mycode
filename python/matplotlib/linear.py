import numpy as np
from matplotlib import pyplot as pt


def perspect(x, abcd):
    a, b, c, d = abcd
    return (a * x + b) / (c * x + d)


def plotPerspect(xs, abcd):
    pt.plot(xs, perspect(xs, abcd))


def display():
    x = np.linspace(-20, 20, 1000)
    pt.subplot(331)
    plotPerspect(x, (1, 2, 3, 4))
    pt.ylim(-5, 5)

    pt.subplot(332)
    plotPerspect(x, (4, 3, 2, 1))
    pt.ylim(-5, 5)

    pt.subplot(333)
    plotPerspect(x, (3, 2, 4, 1))
    pt.ylim(-5, 5)

    pt.subplot(334)
    plotPerspect(x, (-1, 2, 3, 4))
    pt.ylim(-10, 10)

    pt.subplot(335)
    plotPerspect(x, (4, -3, 2, 1))
    pt.ylim(-10, 10)

    pt.subplot(336)
    plotPerspect(x, (3, 2, -4, 1))
    pt.ylim(-10, 10)

    pt.subplot(337)
    plotPerspect(x, (1, -2, 3, 4))
    pt.ylim(-10, 10)

    pt.subplot(338)
    plotPerspect(x, (4, 3, -2, 1))
    pt.ylim(-10, 10)

    pt.subplot(339)
    plotPerspect(x, (3, 2, 4, -1))
    pt.ylim(-10, 10)

    pt.show()


if __name__ == '__main__':
    display()
