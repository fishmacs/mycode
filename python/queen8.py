# original:
def f(ok):
    if len(ok) == 8:
        return [ok]
    else:
        boards = []
        for i in range(8):
            p = (len(ok), i)
            # print ok, p
            if pos_ok(ok, p):
                boards += f(ok + [p])
        return boards

def pos_ok(ok_points, pt):
    for p in ok_points:
        if p[1] == pt[1] or abs(pt[0] - p[0]) == abs(pt[1] - p[1]):
            return False
    return True
#=============

def queen(num=8, boards=[]):
    if len(boards) == num:
        return [boards]
    else:
        new_boards = []
        for i in xrange(num):
            if not conflict(boards, i):
                new_boards += queen(num, boards + [i])
        return new_boards

def conflict(boards, new_y):
    new_x = len(boards)
    for x, y in enumerate(boards):
        if y == new_y or new_x - x == abs(new_y - y):
            return True
    return False

# generator, from zhihu
def queens(num=8, state=()):
    for i in range(num):
        if not conflict(state, i):
            if len(state) == num - 1:
                yield (i,)
            else:
               for result in queens(num, state + (i,)):
                   yield (i,) + result

# inspired by generator solution
def queen1(num=8, boards=[]):
    new_boards = []
    for i in range(num):
        if not conflict(boards, i):
            if len(boards) == num - 1:
                return [[i]]
            else:
                for result in queen1(num, boards + [i]):
                    new_boards.append([i] + result)
    return new_boards

# itertools
from itertools import permutations

def queen2(num=8):
    for queens in permutations(xrange(num)):
        if num == len(set(queens[i] + i for i in xrange(num))) == len(set(queens[i] - i for i in xrange(num))):
            yield queens

# not successful, return in recursive calling discard rewinding
def f1(queens, new_pt):
    if pos_ok(queens, new_pt):
        print queens, new_pt
        queens.append(new_pt)
        if len(queens) == 8:
            return [queens]
        else:
            return reduce(list.__add__, [f1(queens, (len(queens), i)) for i in xrange(8)])
        #[x for x in [f1(queens, (len(queens), i)) for i in xrange(8)] if x]
    return []

def f2():
    return [x for x in [f1([], (0, i)) for i in range(8)] if x]

if __name__ == '__main__':
    boards = f([])
    print boards
