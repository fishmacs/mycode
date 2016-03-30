from __future__ import division
# import numpy as np
# from numpy import random
import math
import random


def buffon(n):
    intersected = 0
    for i in xrange(n):
        alpha = random.random() * math.pi
        center = random.random() * 0.5
        if math.sin(alpha) / 2 >= center:
            intersected += 1
    print(2 * n / intersected)


# def buffon(n):
#     intersected = 0
#     m = 1000
#     i = 0
#     n = np.floor(n / m) * m
#     while i < n:
#         alpha = np.asarray([random.random() * np.pi for j in xrange(m)])
#         center = [random.random() * 0.5 for j in xrange(m)]
#         for x, y in zip(np.sin(alpha), center):
#             if x / 2 >= y:
#                 intersected += 1
#         i += m
#     print(2 * n / intersected)
