import simpy
from src.all_exceptions import SelectorNotFoundException, EnviromentException

class EnviromentWrapper(object):
    def __init__(self):
        self.env = simpy.Environment()
        self.contexts = []

    def attach_context(self, context):
        self.contexts.append(context)

    def get_enviroment(self):
        return self.env

    def search_in_context(self, selector_name):
        for context in self.contexts:
            try:
                selector = context[selector_name]
                return selector
            except AttributeError, e:
                pass
        raise SelectorNotFoundException

    def attach_process_name(self, selector_name):
        try:
            selector = self.search_in_context(selector_name)
            return self.attach_process(selector)
        except EnviromentException, e:
            raise EnviromentException(e)

    def attach_process(self, selector):
        # selector should understand selector(env: Enviroment)
        self.env.process(selector(self.env))

    def execute(self, until=None):
        return self.env.run(until)