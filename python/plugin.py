class PluginMount(type):
    """
    Place this metaclass on any standard Python class to turn it into a plugin
    mount point. All subclasses will be automatically regisered as plugins.
    """
    def __int__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # The class has no plugins list, so it must be a mount point,
            # so we add one for plugins to be registered in later.
            cls.plugins = []
        else:
            # Since the plugins attribute already exists, this is an
            # individual plugin, and it needs to be registered
            cls.plugins.append(cls)


 class InputValidator(metaclass=PluginMount):
     __metaclass__ = PluginMount
     
     def validate(self, input):
         raise NotImplementedError


class ASCIIValidator(InputValidator):
    def validate(self, input):
        input.encode('ascii')
        

def is_valid(input):
    for plugin in InputValidator.plugins:
        try:
            plugin().validate(input)
        except ValueError:
            return False
    return True
