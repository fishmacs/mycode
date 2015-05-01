class B(object):
    def __init__(self):
        self.x = 0

        
class C(B):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.__dict__[k] = v
        super(C, self).__init__()
        
    def __getattr__(self, name):
        print 'name'
        return super(C, self).__getattr__(name)

    def __setattr__(self, k, v):
        if k in ['id', 'pk']:
            self.__dict__[k] = v
        else:
            print 'set', k, v
            super(C, self).__setattr__(k, v)


def func(self):
    print self
    

class Test(object):
    def __getattr__(self, key):
        if not key:
            print 'yes!'
        return super(Test, self).__getattr__(key)

    def f(self):
        func(self)
