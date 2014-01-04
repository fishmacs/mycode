from sets import Set
from collections import MutableSet

# the key would be rehashed if update dict: update() or d[k] = v


class HashCountingInt(int):
    def __init__(self, *args):
        self.count = 0

    def __hash__(self):
        self.count += 1
        return int.__hash__(self)


class MySet(MutableSet):
    def __init__(self, iterable=()):
        self.dictset = dict((item, i) for i, item in enumerate(iterable))

    def __bomb(s, *a, **k):
        raise NotImplementedError

    add = discard = __contains__ = __iter__ = __len__ = __bomb


def test_do_not_rehash_dict_keys(thetype, n=1):
    d = dict.fromkeys(HashCountingInt(k) for k in xrange(n))
    before = sum(elem.count for elem in d)
    thetype(d)
    after = sum(elem.count for elem in d)
    return before, after


def test_rehash_set():
    for t in set, frozenset, Set, MySet:
        before, after = test_do_not_rehash_dict_keys(t, 10)
        print '%s: %d %d' % (t.__name__, before, after)


def test_rehash():
    keys = [HashCountingInt(x) for x in xrange(100)]
    d = dict.fromkeys(keys)
    before = keys[0].count
    before1 = sum(i.count for i in d)
    d[keys[0]] = 0
    after = keys[0].count
    after1 = sum(i.count for i in d)
    print before, before1, after, after1


if __name__ == '__main':
    test_rehash()
