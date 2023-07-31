'''
100个人中有10个罪犯. 已知10个罪犯中，有5个是穿红衣服，有8个穿白袜子。这一百个人中，有10个人穿红衣服，有45个穿白袜子，请问一个概率，遇到一个红衣服白袜子的人，多大的可能这人是个罪犯？
'''

import numpy as np
from scipy.special import comb


def exhaust(num_criminal, noncriminal, red1, white1, red2, white2):
    cws = range(1, red1 + 1)
    nws = range(0, red2 + 1)
    p0 = sum([comb(white1, i) * comb(num_criminal - white1, red1 - i) * comb(white2, j) * comb(noncriminal - white2, red2 - j) * i / (i + j) for i in cws for j in nws]) / comb(num_criminal, red1) / comb(noncriminal, red2)
    p1 = sum([comb(red1, i) * comb(num_criminal-red1, white1-i) * comb(red2, j) * comb(noncriminal-red2, white2-j) * i / (i+j) for i in cws for j in nws]) / comb(num_criminal, white1) / comb(noncriminal, white2)
    nws = range(1, red2 + 1)
    cws = range(red1 + 1)
    p2 = sum([comb(red2, i) * comb(noncriminal-red2, white2-i) * comb(red1, j) * comb(num_criminal-red1, white1-j) * i / (i+j) for i in nws for j in cws if i+j > 0]) / comb(num_criminal, white1) / comb(noncriminal, white2)
    p_rwc = sum([comb(red1, i) * comb(num_criminal-red1, white1-i) * i for i in cws]) / comb(num_criminal, white1) / (num_criminal + noncriminal)
    p_rwn = sum([comb(red2, i) * comb(noncriminal-red2, white2-i) * i for i in nws]) / comb(noncriminal, white2)/ (num_criminal + noncriminal)

    p_rwc1 = num_criminal * red1 * white1 / num_criminal ** 2 / (num_criminal + noncriminal)
    p_rwn1 = noncriminal * red2 * white2 / noncriminal ** 2 / (num_criminal + noncriminal)
    return p0, p1, p2, p_rwc / (p_rwc + p_rwn), p_rwc1 / (p_rwc1 + p_rwn1)


## monte carlo
def draw():
    # make a random distribution
    p = np.zeros((100, 3), dtype=bool)
    criminal = range(10)
    innocent = range(10, 100)
    cred = np.random.choice(criminal, 5, replace=False)
    cwhite = np.random.choice(criminal, 8, replace=False)
    pred = np.random.choice(innocent, 5, replace=False)
    pwhite = np.random.choice(innocent, 37, replace=False)
    # criminals
    p[criminal, 0] = True
    p[cred, 1] = True
    p[cwhite, 2] = True
    # regular people
    # innocent = np.array([i for i in range(100) if i not in criminal])
    p[pred, 1] = True
    p[pwhite, 2] = True
    return np.sum(p[:, 0] * p[:, 1] * p[:, 2]) / np.sum(p[:, 1] * p[:, 2])


# p = np.mean([draw() for i in range(100000)])
# print(p)

def draw3():
    # make a random distribution
    p = np.zeros((3, 100), dtype=bool)
    criminal = range(10)
    innocent = range(10, 100)
    cred = np.random.choice(criminal, 5, replace=False)
    cwhite = np.random.choice(criminal, 8, replace=False)
    pred = np.random.choice(innocent, 5, replace=False)
    pwhite = np.random.choice(innocent, 37, replace=False)
    # criminals
    p[0, criminal] = True
    p[1, cred] = True
    p[2, cwhite] = True
    # regular people
    # innocent = np.array([i for i in range(100) if i not in criminal])
    p[1, pred] = True
    p[2, pwhite] = True
    return np.sum(p[0] * p[1] * p[2]) / np.sum(p[1] * p[2])


def draw1(cshirts, csocks, pshirts, psocks):
    np.random.shuffle(cshirts)
    np.random.shuffle(csocks)
    np.random.shuffle(pshirts)
    np.random.shuffle(psocks)
    c = np.sum(cshirts * csocks)
    p = np.sum(pshirts * psocks)
    return c / (c + p) if c + p > 0 else None


def draw2(nc, nn, cr, cw, nr, nw, num):
    cshirts = np.array([0] * (nc - cr) + [1] * cr)
    csocks = np.array([0] * (nc - cw) + [1] * cw)
    pshirts = np.array([0] * (nn - nr) + [1] * nr)
    psocks = np.array([0] * (nn - nw) + [1] * nw)
    total = 0
    n = 0
    for i in range(num):
        p = draw1(cshirts, csocks, pshirts, psocks)
        if p is not None:
            total += p
            n += 1
    print(n)
    return total / n


if __name__ == '__main__':
    p = np.mean([draw3() for i in range(100000)])
    print(p)
    # draw3()
