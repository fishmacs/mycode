class AttrDict(dict):
    DEFAULT_VALUE = '__default_value__'
    __slots__ = [DEFAULT_VALUE]

    # consider remove _source param, because **kwargs can replace it in some degree,
    # but json.load need it, so must keep this param
    def __init__(self, _source, _defval=AttributeError(), *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        if _source and isinstance(_source, dict):
            self.update(_source)
        setattr(self, self.DEFAULT_VALUE, _defval)
        
    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
        try:
            return self[name]
        except KeyError:
            defval = getattr(self, self.DEFAULT_VALUE)
            if type(defval) is AttributeError:
                raise AttributeError("AttrDict object has no attribute '{0}'".format(name))
            return defval

    def __setattr__(self, name, value):
        if name != self.DEFAULT_VALUE:
            self[name] = value
        else:
            super(AttrDict, self).__setattr__(name, value)
            
    def __delattr__(self, name):
        del self[name]
