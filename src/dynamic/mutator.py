from types import ModuleType, MethodType


def unbind(f):
    """
    Function that unbinds a given function if it's actually binded to an object. If it's not binded to an object it'll
    raise a TypeError Exception
    :param f: function to unbind from an object
    :type f: function
    :raises: TypeError
    """
    self = getattr(f, '__self__', None)
    if self is not None and not isinstance(self, ModuleType) and not isinstance(self, type):
        if hasattr(f, '__func__'):
            return f.__func__
        return getattr(type(f.__self__), f.__name__)
    raise TypeError('not a bound method')


class Mutator(object):
    def create_function(self, instance, code):
        """
        Method to create a function/method given a code in python and set it to a given instance.
        :param instance: object to set the code given in the parameters of this method
        :type instance: <type 'instance'>
        :param code: String containing the code to set to the object
        :type code: str
        """
        method_dict = {}
        methodName = self.get_signature_string(code)
        exec (code.strip(), globals(), method_dict)
        setattr(instance, methodName, method_dict[methodName])
        return instance.__dict__[methodName]