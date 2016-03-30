import numpy as np
from random import randint


def singen(amps, freqs, phases):
    def func(x):
        sum = 0
        for amp, freq, phase in zip(amps, freqs, phases):
            sum += amp * np.sin(freq * x + phase)
        return sum
    return func


def rand_offset(value):
    n = randint(0, 1000)
    if n < 350:
        return (n - 350) * value / 350
    elif n > 650:
        return (n - 650) * value / 350
    else:
        return 0


def fit(total):
    x = np.linspace(0, 2 * np.pi, 300)
    base_amp = [1.0] * 8
    freqs = range(1, 9)
    base_phase = [1.5] * 8
    ret = []
    for i in range(total):
        amps = [ba + rand_offset(0.5) for ba in base_amp]
        phases = [bp + rand_offset(0.75) for bp in base_phase]
        fn = singen(amps, freqs, phases)
        try:
            smin, smax = judge(fn(x))
            if smin and smin < 0.2:
                ret.append((smin, smax, amps, phases))
                #print amps, phases
        except:
            pass
    ret = sorted(ret, key=lambda x: x[0])[:20]
    print ret


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
    if len(mins) == 8 and len(maxs) == 8:
        return np.std(mins), np.std(maxs[:-1])
    else:
        return None, None
    #return mins, maxs


def balance(xs, t):
    x0 = xs[0]
    xs1 = [abs(x - x0) < t for x in xs]
    return all(xs1)


if __name__ == '__main__':
    import sys

    fit(int(sys.argv[1]))

# 0, 4, 6
# 2
