class Integer(int):
    __metaclass__ = partial

    def factorial(self):
        if not self:
            return 1
        return self * Integer(self-1).factorial()


class Integer(int):
    __metaclass__ = partial

    def iseven(self):
        return not (self % 2)
    