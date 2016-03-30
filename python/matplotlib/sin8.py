import numpy as np
import itertools as it
from random import randint
from matplotlib import pyplot as pp


def singen(equations):
    def func(x):
        sum = 0
        for amp, freq, phase in equations:
            sum += amp * np.sin(freq * x + phase)
        return sum
    return func

epsilon = 1e-6


def floats_eq(a1, a2):
    for x, y in zip(a1, a2):
        if abs(x - y) > epsilon:
            return False
    return True


def fit():
    x = np.linspace(0, 2 * np.pi, 300)
    freqs = xrange(1, 10)
    amps = [a / 2.0 for a in xrange(1, 11)]
    phases = [p / 2.0 for p in xrange(1, 11)]
    amps = list(it.permutations(amps, 8))
    freqs = list(it.combinations(freqs, 8))
    phases = list(it.permutations(phases, 8))
    for a in amps:
        for f in freqs:
            for p in phases:
                fn = singen(zip(a, f, p))
                try:
                    if judge(fn(x)):
                        print a
                        print f
                        print p
                except:
                    pass


def rand():
    for i in xrange(5):
        ret = randint(1, 11)
    return ret - 1


def fit1(total, count):
    x = np.linspace(0, 2 * np.pi, 300)
    #freqs = [f / 100.0 for f in xrange(1, 1001)]
    #freqs = list(it.permutations(xrange(1, 11), count))
    amps = [a / 10.0 + 0.5 for a in xrange(0, 11)]
    #phases = [p / 10.0 + 0.5 for p in xrange(0, 11)]
    #nf = len(freqs)
    for i in range(total):
        freq = range(1, 9) #freqs[randint(0, nf - 1)]
        amp = [amps[rand()] for j in range(count)]
        phase = [1.5] * 8 #[phases[rand()] for j in range(count)]
        fn = singen(zip(amp, freq, phase))
        try:
            if judge(fn(x)):
                print amp
                #print freq
                #print phase
        except:
            pass


def fit2():
    x = np.linspace(0, 2 * np.pi, 300)
    amps = [1.3, 1.1, 1.3, 1.1, 1.1, 0.7, 0.8, 1.5]
    for amp in it.permutations(amps):
        fn = singen(zip(amp, range(1, 9), [1.5] * 8))
        try:
            if judge(fn(x)):
                print amp
                #print freq
                #print phase
        except:
            pass


def judge(ys):
    maxs = []
    mins = []
    i = 1
    curr = ys[0]
    while True:
        if ys[i] > curr:
            curr = ys[i]
        else:
            break
        i += 1
    #maxs.append(curr)
    while i < len(ys):
        while True:
            if ys[i] < curr:
                curr = ys[i]
            else:
                break
            i += 1
        mins.append(curr)
        while i < len(ys):
            if ys[i] > curr:
                curr = ys[i]
            else:
                break
            i += 1
        maxs.append(curr)
    return len(mins) == 8 and len(maxs) == 8 and balance(mins, 0.4) and balance(maxs[:-1], 0.8)
    #return mins, maxs


def balance(xs, t):
    x0 = xs[0]
    xs1 = [abs(x - x0) < t for x in xs]
    return all(xs1)


def test(amps, freqs, phases):
    f = singen(zip(amps, freqs, phases))
    x = np.linspace(0, 4 * np.pi, 1000)
    pp.plot(x, f(x))
    pp.show()


def testm(amps, freqs, phases, color='b'):
    f = singen(zip(amps, freqs, phases))
    x = np.linspace(0, 4 * np.pi, 1000)
    pp.plot(x, f(x), color)


def test1(amps):
    freqs = range(1, 8)
    #phases = [1.5] * 8
    phases = [1.5, 1.25, 1.125, 1, 1.625, 1.75, 1.25, 1.75]
    f = singen(zip(amps, freqs, phases))
    x = np.linspace(0, 4 * np.pi, 1000)
    pp.plot(x, f(x))
    pp.show()


def test2(amps, phases):
    freqs = range(1, 9)
    f = singen(amps, freqs, phases)
    x = np.linspace(0, 4 * np.pi, 1000)
    pp.plot(x, f(x))
    pp.show()

#[0.31, 0.54, 0.21, 0.1, 0.07, 0.59, 0.27, 1.66]
#[1.8, 0.41, 1.75, 0.18, 0.84, 1.58, 1.09, 0.17]

#[0.8, 0.9, 1.0, 0.8, 0.7, 0.6, 0.6, 1.3]
#[1.3, 1.1, 1.3, 1.1, 1.1, 0.7, 0.8, 1.5]
#[1.0, 0.9, 0.8, 0.9, 0.7, 0.6, 0.6, 0.6] 上面齐下面不齐
