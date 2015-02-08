expr, res = "28+32+++32++39", 0
for t in expr.split('+'):
    if t:
        res += int(t)
print res

from operator import add
expr = '28+32+++32++39'
print reduce(add, map(int, filter(bool, expr.split('+'))))


operator import methodcaller

methodcaller("__str__")([1,2,3,4,5])
#'[1, 2, 3, 4, 5]'

methodcaller("keys")(dict(name="Alexey", topic="FP"))
#['topic', 'name']

values_extractor = methodcaller("values")
values_extractor(dict(name="Alexey", topic="FP"))
#['FP', 'Alexey']

methodcaller("count", 1)([1,1,1,2,2]) 
# same as [1,1,1,2,2].count(1)

#BAD
ss = ["UA", "PyCon", "2012"]
reduce(lambda acc, s: acc + len(s), ss, 0)

#NOT BAD...
ss = ["UA", "PyCon", "2012"]
reduce(lambda l, r: l + r, map(lambda s: len(s), ss))

import operator
#GOOD
ss = ["UA", "PyCon", "2012"]
reduce(operator.add, map(len, ss))


###
def ask(self, question):
    print "{name}, {q}?".format(name=self["name"], q=question)


def talk(self):
    print "I'm starting {topic}".format(topic=self["topic"])


from functools import partial


def cls(**methods):
    def bind(self):
        return lambda (name, method): (name, partial(method, self))
    return lambda **attrs: dict(
        attrs.items() + map(bind(attrs.copy()), methods.items())
    )

Speaker = cls(ask=ask, talk=talk)


###
def cls(**methods):
    def bind(**attrs):
        attrs = attrs.copy()
        attrs.update(dict(map(lambda(n, m): (n, partial(m, attrs)),
                              methods.items())))
        return attrs
    return bind


###
def dct(*items):
    def pair((key, value)):
        return lambda k: value if k == key else None

    def merge(l, r):
        return lambda k: l(k) or r(k)

    return reduce(merge, map(pair, items), pair((None, None)))
    