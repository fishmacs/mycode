class Car(object):
    __slots__ = ['make', 'model', 'year', 'color']

    def __init__(self, make, model, year, color):
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    @property
    def description(self):
        """ Return a description of this car. """
        return "%s %s %s %s" % (self.color, self.year, self.make, self.model)


class AttributeInitType(type):
    def __call__(self, *args, **kwargs):
        """ Create a new instance. """

        # First, create the object in the normal default way.
        obj = type.__call__(self, *args)

        # Additionally, set attributes on the new object.
        for name, value in kwargs.items():
            setattr(obj, name, value)

        # Return the new object.
        return obj


class Car1(object):
    __metaclass__ = AttributeInitType
    __slots__ = ['make', 'model', 'year', 'color']
 
    @property
    def description(self):
        """ Return a description of this car. """
        return "%s %s %s %s" % (self.color, self.year, self.make, self.model)
