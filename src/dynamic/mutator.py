from types import ModuleType, MethodType
from src.all_exceptions import MutatorException

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


class Context(dict):
    def get_selector(self, selector_name):
        return self.get(selector_name)


class Mutator(object):
    def __init__(self):
        self.context = Context()

    def get_context(self, new_context=False):
        if new_context:
            self.context = Context()
        return self.context

    def _build_arg_list(self, arg_list, instance_bound=False):
        preffix = ''
        if instance_bound:
            preffix = 'self,'

        if arg_list:
            print preffix
            return preffix + ''.join(str(i) for i in arg_list)
        return preffix

    def _build_var_args(self, arg_list, variable_args):
        preffix = ','
        if not arg_list:
            preffix = ''
        if variable_args:
            return preffix + '*args, **kwargs'
        return ''

    def define_new_method(self, method_name, args_list, block_code, variable_args=False, instance_bound=False):
        method_code = '''def {0}({1}{2}):
            {3}
        '''.format(method_name, self._build_arg_list(args_list, instance_bound),
                   self._build_var_args(args_list, variable_args),
                   block_code)
        return self.compile_code(method_code)

    def compile_code(self, code, new_context=False):
        if not isinstance(code, str):
            raise MutatorException(
                'Invalid type for code: {0}. Type should be str. Found: {1}.'.format(code, type(code)))
        context = self.get_context(new_context)

        try:
            exec (code.strip(), globals(), context)
        except SyntaxError, e:
            raise MutatorException('Failed compiling code: {0}'.format(code))

        return context

    def get_signature_string(self, code_function):
        """
        """
        return code_function[code_function.find("def") + 3:code_function.find("(")].strip()

    def create_class(self, class_name, bases=(object,), bound_context=False):
        context = self.get_context() if bound_context else Context()

        new_class = type(class_name, bases, context)
        return new_class

    def define_instance_method(self, instance, method_name, args_list, block_code, variable_args=False,
                               instance_bound=False):
        self.define_new_method(method_name, args_list, block_code, variable_args, instance_bound)

        setattr(instance, method_name, self.context[method_name])
        return instance.__dict__[method_name]