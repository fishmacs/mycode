from __future__ import division
import math
import random


def buffon():
    n = 0
    intersected = 0
    while True:
        alpha = random.random() * math.pi
        center = random.random() * 0.5
        if math.sin(alpha) / 2 > center:
            intersected += 1
        n += 1
        if intersected > 0:
            pi = 2 * n / intersected
            if abs(pi - math.pi) < 0.000001:
                print(n, pi)
                break
