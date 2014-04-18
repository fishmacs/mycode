from collections import MutableMapping
#from UserDict import DictMixin


class RevealAccess(object):
    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        #print 'get', self.name
        return self.val

    def __set__(self, obj, val):
        #print 'set', self.name
        self.val = val

        
class Myclass(object):
    x = RevealAccess(10, 'var x')
    y = 5

    def __init__(self):
        super(Myclass, self).__init__()

    # this __setattr__ shadow descriptor's __set__!
    def __setattr__(self, name, val):
        pass
        #print 'setattr!'

        
class DefaultProperties(object):
    def __init__(self):
        self.value_map = {}

    def __get__(self, obj, objtype):
        #print 'get', obj, ',', objtype
        if not obj:
            return self
        return self.value_map[id(obj)]

    def __set__(self, obj, value):
        #print 'set', obj, ',', value
        self.value_map[id(obj)] = value


# move defval/attrerr from instance to class's __dict__, otherwise there are 2 extra keys
class AttrDict2(dict):
    extra_prop = DefaultProperties()

    def __init__(self, d=None, defval=None, attrerr=True, *args, **kwargs):
        super(AttrDict2, self).__init__(*args, **kwargs)
        if d and type(d) == dict:
            self.update(d)
        # can not just use self.properties, otherwise properties is just a dict key
        #self.extra_prop = (defval, attrerr)

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
        try:
            return self[name]
        except KeyError:
            defval, attrerr = self.extra_prop
            if attrerr:
                raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
            return defval

    def __setattr__(self, name, value):
        #print '__setattr__', name, value
        self[name] = value

    def __delattr__(self, name):
        del self[name]


class AttrDict(dict):
    # descriptor is not necessary, just use a dict in __class__.__dict__
    default_val_map = {}
    
    def __init__(self, d=None, defval=AttributeError(), *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        if d and type(d) == dict:
            self.update(d)
        self.default_val_map[id(self)] = defval
        
    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
        try:
            return self[name]
        except KeyError:
            defval = self.default_val_map[id(self)]
            if isinstance(defval, AttributeError):
                raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
            return defval

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


# keep default values in class's __dict__ has a problem, the useless item never cleaned! so consider mixin MutableMapping, make AttrDict has it's own __dict__
class AttrDict3(dict, MutableMapping):
    def __init__(self, d=None, defval=AttributeError(), *args, **kwargs):
        self._default_value_ = defval
        super(AttrDict3, self).__init__(*args, **kwargs)
        if d and type(d) == dict:
            self.update(d)

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
        try:
            return self[name]
        except KeyError:
            defval = self._default_value_
            if isinstance(defval, AttributeError):
                raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
            return defval

    def __setattr__(self, name, value):
        if name != '_default_value_':
            self[name] = value
        else:
            super(AttrDict3, self).__setattr__(name, value)
            
    def __delattr__(self, name):
        del self[name]

    def __setitem(self, key, value):
        super(AttrDict3, self).__setitem__(key, value)


# use __slot__ to replace __dict__, do not need mixin now!
class AttrDict4(dict):
    __slots__ = ['_default_value_']
    
    def __init__(self, d=None, defval=AttributeError(), *args, **kwargs):
        super(AttrDict4, self).__init__(*args, **kwargs)
        if d and type(d) == dict:
            self.update(d)
        self._default_value_ = defval

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
        try:
            return self[name]
        except KeyError:
            defval = self._default_value_
            if isinstance(defval, AttributeError):
                raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
            return defval

    def __setattr__(self, name, value):
        if name != '_default_value_':
            self[name] = value
        else:
            super(AttrDict4, self).__setattr__(name, value)
            
    def __delattr__(self, name):
        del self[name]

        
# first version of above implementation, no default value
class AttributeDict1(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


#an failed implementation: too many other functions to implement: update, ittems, iteritems
#you can see ruby's good
class AttrDict0(tuple):
    def __new__(cls, d, defval=None, attrerr=True):
        if isinstance(d, dict):
            if defval is not None:
                attrerr = False
            return super(AttrDict, cls).__new__(cls, (d, defval, attrerr))
        return super(AttrDict, cls).__new__(cls, d)

    def __init__(self, d, defval=None, attrerr=True):
        # if defval is not None:
        #     attrerr = False
        super(AttrDict, self).__init__()  # (d, defval, attrerr))

    def __getattr__(self, name):
        try:
            return self[0][name]
        except KeyError:
            if self[2]:
                raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
            return self[1]

    def __setattr__(self, name, value):
        self[0][name] = value

    def __delattr__(self, name):
        del self[0][name]

    def __getitem__(self, name):
        if name not in [0, 1, 2]:
            return self[0].__getitem__(name)
        return super(AttrDict, self).__getitem__(name)
        
    def __setitem__(self, name, value):
        return self[0].__setitem__(name, value)
        
    def __delitem__(self, name):
        return self[0].__delitem__(name)
        
    def __len__(self):
        return len(self[0])

    def __contains__(self, item):
        return self[0].__contains__(item)
